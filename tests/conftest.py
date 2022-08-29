"""fixtures for all tests"""
from __future__ import annotations

import os
import shutil
import subprocess

from copy import deepcopy
from pathlib import Path

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
from .defaults import PULLABLE_IMAGE


@pytest.fixture(scope="session", name="valid_container_engine")
def fixture_valid_container_image():
    """returns an available container engine"""
    for engine in ("podman", "docker"):
        if shutil.which(engine):
            return engine
    raise Exception("container engine required")


@pytest.fixture(scope="function")
def locked_directory(tmpdir):
    """directory without read-write for throwing errors"""
    os.chmod(tmpdir, 0o000)
    yield tmpdir
    os.chmod(tmpdir, 0o777)


@pytest.fixture(scope="session")
def pullable_image(valid_container_engine):
    """A container that can be pulled."""
    yield PULLABLE_IMAGE
    subprocess.run([valid_container_engine, "image", "rm", PULLABLE_IMAGE], check=True)


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
