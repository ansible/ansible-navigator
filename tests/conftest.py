"""fixtures for all tests"""
import os
import shutil
import subprocess

from pathlib import Path

import pytest

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
