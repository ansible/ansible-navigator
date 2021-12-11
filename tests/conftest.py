"""fixtures for all tests"""
import os
import shutil
import subprocess

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
    """directory without rw for throwing errors"""
    os.chmod(tmpdir, 0o000)
    yield tmpdir
    os.chmod(tmpdir, 0o777)


@pytest.fixture(scope="session")
def pullable_image(valid_container_engine):
    """pullable container"""
    yield PULLABLE_IMAGE
    subprocess.run([valid_container_engine, "image", "rm", PULLABLE_IMAGE], check=True)
