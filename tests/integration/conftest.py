import os
import pytest

from ._common import TmuxSession

EXECUTION_MODES = ["interactive", "stdout"]


@pytest.fixture(scope="session")
def test_fixtures_dir():
    return os.path.join(os.path.dirname(__file__), "..", "fixtures")


@pytest.fixture(scope="session")
def tmux_session():
    with TmuxSession("interactive_inventory_list") as ts:
        yield ts


@pytest.fixture(scope="session", autouse=True)
def container_runtime_available():
    """check if a container runtime is available"""
    # pylint: disable=import-outside-toplevel
    import subprocess
    import warnings

    runtimes_available = True
    for runtime in ("docker", "podman"):
        try:
            subprocess.run([runtime, "-v"], check=False)
        except FileNotFoundError:
            warnings.warn(UserWarning(f"{runtime} not available"))
            runtimes_available = False
    return runtimes_available


@pytest.fixture(scope="session")
def container_runtime_installed():
    """check if container runtime is available"""
    # pylint: disable=import-outside-toplevel
    import subprocess

    for runtime in ("podman", "docker"):
        try:
            subprocess.run([runtime, "-v"], check=False)
            return runtime
        except FileNotFoundError:
            pass
    pytest.skip("No container runtime is available.")
