"""fixtures for all tests"""
from __future__ import annotations

import os
import re
import shutil
import subprocess

from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Literal

import pytest

from ansible_navigator.configuration_subsystem import to_sample
from ansible_navigator.configuration_subsystem.definitions import SettingsFileType
from ansible_navigator.configuration_subsystem.navigator_configuration import (
    NavigatorConfiguration,
)
from ansible_navigator.content_defs import ContentView
from ansible_navigator.content_defs import SerializationFormat
from ansible_navigator.utils.serialize import Loader
from ansible_navigator.utils.serialize import serialize_write_file
from ansible_navigator.utils.serialize import yaml
from .defaults import FIXTURES_DIR


@pytest.fixture(scope="session", autouse=True)
def auto_pull_images(request):
    """Pulls test images."""
    print("\nPulling images...")
    # Basically during testing we always override the default ee image with
    # the one that we have stored inside our Dockerfile, so testing is not
    # affected by the upload of a newer image.
    os.environ["ANSIBLE_NAVIGATOR_EXECUTION_ENVIRONMENT_IMAGE"] = container_image("default")
    container_image("small")
    print("\nDone")


@pytest.fixture(scope="session", name="valid_container_engine")
def fixture_valid_container_image():
    """returns an available container engine"""
    return container_engine()


@lru_cache
def container_engine() -> str:
    """Return which container engine should be used."""
    for engine in ("podman", "docker"):
        if shutil.which(engine):
            return engine
    raise Exception("container engine required")


@lru_cache
def container_image(name: Literal["default", "hello", "small"] = "default") -> str:
    """Teturn default container image, the one that was used during testing."""
    # these are not to be pre-pulled, as we aim to test our own pulling
    if name == "hello":
        return "ghcr.io/ansible/hello-world:linux"
    if name == "small":
        # might not be the smallest but is likely already pre-loaded as being
        # the parent image used by creator-ee, so much faster and less disk space.
        image = "ghcr.io/ansible/creator-ee:latest"
    else:
        containers_map = {"default": ".config/Dockerfile"}
        if name not in containers_map:
            raise NotImplementedError(f"Unknown image alias {name}")
        with open(file=containers_map[name], encoding="utf-8") as f:
            line = f.read()

            from_re = re.compile("^FROM (.*)$")
            match = from_re.match(line)
            if not match:
                raise RuntimeError("Unable to read test container image.")
            image = match.groups()[0]
            if not image:
                raise RuntimeError("Unable to read test container image.")

    result = subprocess.run(
        [container_engine(), "pull", "-q", image], capture_output=False, check=False
    )
    if result.returncode != 0:
        pytest.fail(f"Failed to pull container image {image}.")
    return image


@pytest.fixture(scope="function")
def locked_directory(tmpdir):
    """directory without read-write for throwing errors"""
    os.chmod(tmpdir, 0o000)
    yield tmpdir
    os.chmod(tmpdir, 0o777)


@pytest.fixture(scope="session")
def pullable_image(valid_container_engine):
    """A container that can be pulled."""
    yield container_image("hello")
    subprocess.run([valid_container_engine, "image", "rm", container_image("hello")], check=True)


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
    """Set the settings environment variable to a full sample settings file in a tmp path."""
    _commented, uncommented = settings_samples
    settings_contents = yaml.load(uncommented, Loader=Loader)
    settings_path = tmp_path / "ansible-navigator.yml"
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
