# cspell:ignore sessionstart,unconfigure,workerinput
"""fixtures for all tests"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

from copy import deepcopy
from pathlib import Path

import pytest

from ansible_navigator.configuration_subsystem import to_sample
from ansible_navigator.configuration_subsystem.definitions import SettingsFileType
from ansible_navigator.configuration_subsystem.navigator_configuration import APP_NAME
from ansible_navigator.configuration_subsystem.navigator_configuration import (
    NavigatorConfiguration,
)
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


def _valid_container_engine():
    """Returns an available container engine."""
    for engine in ("podman", "docker"):
        if shutil.which(engine):
            return engine
    pytest.exit(reason="Container engine required", returncode=1)
    return False


@pytest.fixture(scope="session", name="valid_container_engine")
def fixture_valid_container_engine():
    """Returns an available container engine."""
    return _valid_container_engine()


def default_ee_image_name():
    """Returns the default ee image name."""
    return ImageEntry.DEFAULT_EE.get(app_name=APP_NAME)


@pytest.fixture(scope="session", name="default_ee_image_name")
def fixture_default_image_name():
    """Returns the default ee image name."""
    return default_ee_image_name()


def small_image_name():
    """Returns the small image name"""
    return ImageEntry.SMALL_IMAGE.get(app_name=APP_NAME)


@pytest.fixture(scope="session", name="small_image_name")
def fixture_small_image_name():
    """Returns the small image name"""
    return small_image_name()


@pytest.fixture(scope="function")
def locked_directory(tmpdir):
    """directory without read-write for throwing errors"""
    os.chmod(tmpdir, 0o000)
    yield tmpdir
    os.chmod(tmpdir, 0o777)


@pytest.fixture(scope="session")
def pullable_image(valid_container_engine):
    """A container that can be pulled."""
    image = ImageEntry.PULLABLE_IMAGE.get(app_name=APP_NAME)
    yield image
    subprocess.run([valid_container_engine, "image", "rm", image], check=True)


@pytest.fixture
def patch_curses(monkeypatch):
    """Patch curses so it doesn't traceback during tests.

    :param monkeypatch: Fixture for patching
    """
    monkeypatch.setattr("curses.cbreak", lambda: None)
    monkeypatch.setattr("curses.nocbreak", lambda: None)
    monkeypatch.setattr("curses.endwin", lambda: None)


@pytest.fixture
def use_venv(monkeypatch: pytest.MonkeyPatch):
    """Set the path such that it includes the virtual environment

    :param monkeypatch: Fixture for patching
    """
    venv_path = os.environ.get("VIRTUAL_ENV")
    if venv_path is None:
        raise AssertionError(
            "VIRTUAL_ENV environment variable was not set but tox should have set it.",
        )
    path_prepend = Path.cwd() / venv_path / "bin"
    monkeypatch.setenv("PATH", str(path_prepend), prepend=os.pathsep)


@pytest.fixture(name="settings_samples")
def _settings_samples() -> tuple[str, str]:
    """Provide the full settings samples

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
def test_dir_fixture_dir(request):
    """Provide the fixture directory for a given test directory.

    :param request: The pytest request object
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
    container_engine = _valid_container_engine()
    pull_image(
        valid_container_engine=container_engine,
        image_name=default_ee_image_name(),
    )
    pull_image(
        valid_container_engine=container_engine,
        image_name=small_image_name(),
    )


USER_ENVIRONMENT = {}


def pytest_configure(config: pytest.Config):  # pylint: disable=unused-argument
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

    # ensure a virtual environment is active
    if not os.environ.get("VIRTUAL_ENV"):
        pytest.exit("Please activate a virtual environment before testing.")

    # ensure tmux is installed
    tmux_location = shutil.which("tmux")
    if not tmux_location:
        pytest.exit("Please install tmux before testing.")


def pytest_unconfigure(config: pytest.Config):  # pylint: disable=unused-argument
    """Restore the environment variables that start with ANSIBLE_.

    :param config: The pytest config object
    """
    for key, value in USER_ENVIRONMENT.items():
        os.environ[key] = value
