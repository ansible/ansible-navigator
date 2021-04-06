import pytest
import os

from ._common import ActionRunTest


@pytest.fixture(scope="session")
def test_fixtures_dir():
    return os.path.join(os.path.dirname(__file__), "..", "fixtures")


@pytest.fixture(scope="session", autouse=True)
def container_runtime_available():
    import subprocess
    import warnings

    runtimes_available = True
    for runtime in ("docker", "podman"):
        try:
            subprocess.run([runtime, "-v"])
        except FileNotFoundError:
            warnings.warn(UserWarning(f"{runtime} not available"))
            runtimes_available = False
    return runtimes_available


@pytest.fixture(scope="session")
def container_runtime_installed():
    import subprocess

    for runtime in ("podman", "docker"):
        try:
            subprocess.run([runtime, "-v"])
            return runtime
        except FileNotFoundError:
            pass
    pytest.skip("No container runtime is available.")
