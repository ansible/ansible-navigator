""" fixtures for all tests """
import os
import pytest

from ._common import container_runtime_or_fail


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
