""" fixtures for all tests """

import pytest

from ._common import container_runtime_or_fail


@pytest.fixture(scope="session", name="container_runtime_or_fail")
def fixture_container_runtime_or_fail():
    """check if container runtime is available"""
    yield container_runtime_or_fail
