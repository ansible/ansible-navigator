# cspell:ignore sessionstart,unconfigure,workerinput
"""Fixtures for all tests."""
from __future__ import annotations

import errno
import os
import pty
import select
import shutil
import subprocess
import sys

from collections.abc import Generator
from copy import deepcopy
from pathlib import Path
from typing import Protocol

import pytest

from ansible_navigator.configuration_subsystem import to_sample
from ansible_navigator.configuration_subsystem.definitions import SettingsFileType
from ansible_navigator.configuration_subsystem.navigator_configuration import APP_NAME
from ansible_navigator.configuration_subsystem.navigator_configuration import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.utils import parse_ansible_verison
from ansible_navigator.content_defs import ContentView
from ansible_navigator.content_defs import SerializationFormat
from ansible_navigator.image_manager.puller import ImagePuller
from ansible_navigator.utils.functions import find_settings_file
from ansible_navigator.utils.packaged_data import ImageEntry
from ansible_navigator.utils.serialize import Loader
from ansible_navigator.utils.serialize import serialize_write_file
from ansible_navigator.utils.serialize import yaml

from .defaults import FIXTURES_DIR


def valid_ce() -> str:
    """Return an available container engine.

    :returns: The container engine or exits
    """
    for engine in ("podman", "docker"):
        if shutil.which(engine):
            return engine
    pytest.exit(reason="Container engine required", returncode=1)
    return False


@pytest.fixture(scope="session", name="valid_container_engine")
def fixture_valid_container_engine() -> str:
    """Return an available container engine.

    :returns: The container engine or exits
    """
    return valid_ce()


def default_ee_image_name() -> str:
    """Return the default ee image name.

    :returns: The default ee image name
    """
    return ImageEntry.DEFAULT_EE.get(app_name=APP_NAME)


@pytest.fixture(scope="session", name="default_ee_image_name")
def fixture_default_image_name() -> str:
    """Return the default ee image name.

    :returns: The default ee image name
    """
    return default_ee_image_name()


def small_image_name() -> str:
    """Return the small image name.

    :returns: The small image name
    """
    return ImageEntry.SMALL_IMAGE.get(app_name=APP_NAME)


@pytest.fixture(scope="session", name="small_image_name")
def fixture_small_image_name() -> str:
    """Return the small image name.

    :returns: The small image name
    """
    return small_image_name()


@pytest.fixture(scope="function")
def locked_directory(tmpdir) -> Generator[str, None, None]:
    """Directory without read-write for throwing errors.

    :param tmpdir: Fixture for temporary directory
    :yields: The temporary directory
    """
    os.chmod(tmpdir, 0o000)
    yield tmpdir
    os.chmod(tmpdir, 0o777)


@pytest.fixture(scope="session")
def pullable_image(valid_container_engine) -> Generator[str, None, None]:
    """Return a container that can be pulled.

    :param valid_container_engine: Fixture for a valid container engine
    :yields: The image name
    """
    image = ImageEntry.PULLABLE_IMAGE.get(app_name=APP_NAME)
    yield image
    subprocess.run([valid_container_engine, "image", "rm", image], check=True)


@pytest.fixture
def patch_curses(monkeypatch) -> None:
    """Patch curses so it doesn't traceback during tests.

    :param monkeypatch: Fixture for patching
    """
    monkeypatch.setattr("curses.cbreak", lambda: None)
    monkeypatch.setattr("curses.nocbreak", lambda: None)
    monkeypatch.setattr("curses.endwin", lambda: None)


@pytest.fixture
def use_venv(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set the path such that it includes the virtual environment.

    :param monkeypatch: Fixture for patching
    :raises AssertionError: If the virtual environment is not set
    """
    venv_path = os.environ.get("VIRTUAL_ENV")
    if venv_path is None:
        msg = "VIRTUAL_ENV environment variable was not set but tox should have set it."
        raise AssertionError(msg)
    path_prepend = Path.cwd() / venv_path / "bin"
    monkeypatch.setenv("PATH", str(path_prepend), prepend=os.pathsep)


@pytest.fixture(name="settings_samples")
def _settings_samples() -> tuple[str, str]:
    """Provide the full settings samples.

    :returns: The commented and uncommented samples
    """
    settings = deepcopy(NavigatorConfiguration)
    commented, uncommented = to_sample(settings=settings)
    return commented, uncommented


@pytest.fixture()
def settings_env_var_to_full(
    settings_samples: tuple[str, str],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[Path, SettingsFileType]:
    """Set the settings environment variable to a full sample settings file in a tmp path.

    :param settings_samples: The commented and uncommented samples
    :param tmp_path: The tmp path
    :param monkeypatch: Fixture for patching
    :returns: The settings path and the settings contents
    """
    _commented, uncommented = settings_samples
    settings_contents = yaml.load(uncommented, Loader=Loader)
    settings_path = tmp_path / "ansible-navigator.yml"

    # Update the sample with the actual default execution environment image to avoid a pull attempt
    image = default_ee_image_name()
    settings_contents["ansible-navigator"]["execution-environment"]["image"] = image

    serialize_write_file(
        content=settings_contents,
        content_view=ContentView.NORMAL,
        file_mode="w",
        file=settings_path,
        serialization_format=SerializationFormat.YAML,
    )
    # The sample has volume mounts, so let's not exit because they doesn't exit
    root = settings_contents["ansible-navigator"]
    ee_root = root["execution-environment"]
    for volume_mount in ee_root["volume-mounts"]:
        Path(volume_mount["src"]).mkdir(exist_ok=True)

    monkeypatch.setenv("ANSIBLE_NAVIGATOR_CONFIG", str(settings_path))
    return settings_path, settings_contents


@pytest.fixture
def test_dir_fixture_dir(request) -> Path:
    """Provide the fixture directory for a given test directory.

    :param request: The pytest request object
    :returns: The fixture directory
    """
    test_dir = Path(FIXTURES_DIR) / request.path.parent.relative_to(Path(__file__).parent)
    return test_dir


def pull_image(valid_container_engine: str, image_name: str):
    """Pull an image.

    :param valid_container_engine: The container engine to use
    :param image_name: The default EE image name
    """
    image_puller = ImagePuller(
        container_engine=valid_container_engine,
        image=image_name,
        arguments=["--quiet"],
        pull_policy="missing",
    )
    image_puller.assess()
    image_puller.prologue_stdout()
    if image_puller.assessment.exit_messages:
        print(msg.to_lines() for msg in image_puller.assessment.exit_messages)
        pytest.exit("Image assessment failed", 1)
    if image_puller.assessment.pull_required:
        # ensure the output is flushed prior to the pull
        # cleans up GH action output
        sys.stdout.flush()
        image_puller.pull_stdout()
    if image_puller.assessment.pull_required:
        pytest.exit("Image pull failed", 1)


def _cmd_in_tty(
    cmd: str,
    bytes_input: bytes | None = None,
    cwd: Path | None = None,
) -> tuple[str, str, int]:
    """Capture the output of cmd using a tty.

    Based on Andy Hayden's gist:
    https://gist.github.com/hayd/4f46a68fc697ba8888a7b517a414583e

    :param cmd: The command to run
    :param bytes_input: Some bytes to input
    :param cwd: The working directory
    :raises OSError: Error if the command fails
    :returns: stdout, stderr, and the exit code
    """
    # pylint: disable=too-many-locals
    m_stdout, s_stdout = pty.openpty()  # provide tty to enable line-buffering
    m_stderr, s_stderr = pty.openpty()
    m_stdin, s_stdin = pty.openpty()

    with subprocess.Popen(
        cmd,
        bufsize=1,
        cwd=cwd,
        shell=True,
        stdin=s_stdin,
        stdout=s_stdout,
        stderr=s_stderr,
        close_fds=True,
    ) as proc:
        for file_d in [s_stdout, s_stderr, s_stdin]:
            os.close(file_d)
        if bytes_input:
            os.write(m_stdin, bytes_input)

        timeout = 0.04
        readable = [m_stdout, m_stderr]
        result = {m_stdout: b"", m_stderr: b""}
        try:
            while readable:
                ready, _, _ = select.select(readable, [], [], timeout)
                for file_d in ready:
                    try:
                        data = os.read(file_d, 512)
                    except OSError as exc:
                        if exc.errno != errno.EIO:
                            raise
                        # EIO means EOF on some systems
                        readable.remove(file_d)
                    else:
                        if not data:  # EOF
                            readable.remove(file_d)
                        result[file_d] += data

        finally:
            for file_d in [m_stdout, m_stderr, m_stdin]:
                os.close(file_d)
            if proc.poll() is None:
                proc.kill()
            proc.wait()

    return result[m_stdout].decode("utf-8"), result[m_stderr].decode("utf-8"), proc.returncode


@pytest.fixture
def cmd_in_tty():
    """Provide the cmd in tty function as a fixture.

    :yields: The cmd_in_tty function
    """
    yield _cmd_in_tty


class TCmdInTty(Protocol):
    """Type hint for the cmd_in_tty fixture."""

    def __call__(self, cmd: str, bytes_input: bytes | None = None) -> tuple[str, str, int]:
        """Provide the callable type hint for the cmd_in_tty fixture.

        :param cmd: The command to run
        :param bytes_input: Some bytes to input
        """


def pytest_sessionstart(session: pytest.Session):
    """Pull the default EE image before the tests start.

    Only in the main process, not the workers.
    https://github.com/pytest-dev/pytest-xdist/issues/271#issuecomment-826396320
    although the images will be downloaded by the time the workers
    run their session start, there is no reason from each to perform the image assessments

    :param session: The pytest session object
    """
    if getattr(session.config, "workerinput", None) is not None:
        return
    container_engine = valid_ce()
    pull_image(
        valid_container_engine=container_engine,
        image_name=default_ee_image_name(),
    )
    pull_image(
        valid_container_engine=container_engine,
        image_name=small_image_name(),
    )


USER_ENVIRONMENT = {}


def pytest_configure(config: pytest.Config):
    """Attempt to save a contributor some troubleshooting.

    :param config: The pytest config object
    """
    # limit an environment variables that may conflict with tests
    allow = ("ANSIBLE_NAVIGATOR_UPDATE_TEST_FIXTURES",)
    for k in os.environ:
        if k in allow:
            continue
        if k.startswith("ANSIBLE_"):
            USER_ENVIRONMENT[k] = os.environ.pop(k)
        if k == "EDITOR":
            USER_ENVIRONMENT[k] = os.environ.pop(k)
    if USER_ENVIRONMENT:
        env_vars = ",".join(USER_ENVIRONMENT.keys())
        print(f"[NOTE] The environment variable(s) {env_vars} will be restored after the test run")

    # look for ansible.cfg
    _log, errors, details = parse_ansible_verison()
    if details is None:
        err = "\n".join(error.message for error in errors)
        pytest.exit(f"Error parsing ansible version:\n{err}")
    config_file = details["config file"]
    if config_file != "None":
        pytest.exit(f"Please remove the ansible config file '{config_file}' before testing.")

    # look for ansible-navigator settings file
    _log, _errors, file_path = find_settings_file()
    if file_path:
        pytest.exit(f"Please remove the settings file '{file_path}' before testing.")

    # ensure tmux is installed
    tmux_location = shutil.which("tmux")
    if not tmux_location:
        pytest.exit("Please install tmux before testing.")


def pytest_unconfigure(config: pytest.Config):
    """Restore the environment variables that start with ANSIBLE_.

    :param config: The pytest config object
    """
    for key, value in USER_ENVIRONMENT.items():
        os.environ[key] = value
