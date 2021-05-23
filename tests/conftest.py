""" fixtures for all tests """
import os
import pytest
import subprocess

from ._common import container_runtime_or_fail
from .defaults import PULLABLE_IMAGE


@pytest.fixture(scope="session", name="container_runtime_or_fail")
def fixture_container_runtime_or_fail():
    """check if container runtime is available"""
    yield container_runtime_or_fail


@pytest.fixture(scope="function")
def locked_directory(tmpdir):
    """diretory without rw for throwing errors"""
    os.chmod(tmpdir, 0o000)
    yield tmpdir
    os.chmod(tmpdir, 0o777)


@pytest.fixture(scope="session")
def pullable_image(container_runtime_or_fail):
    yield PULLABLE_IMAGE
    subprocess.run([container_runtime_or_fail(), "image", "rm", PULLABLE_IMAGE], check=True)
