import pytest
import os


EXECUTION_MODES = ["interactive", "stdout"]


@pytest.fixture(scope="session")
def test_fixtures_dir():
    return os.path.join(os.path.dirname(__file__), "..", "fixtures")


@pytest.fixture
def output_fixture():
    def _method(mode, test_name):
        if mode not in EXECUTION_MODES:
            raise ValueError(
                "Value of {0} can be either one of {1}".format(mode, ", ".join(EXECUTION_MODES))
            )
        fixture_dir = os.path.join(os.path.dirname(__file__), "..", "fixtures")
        fixture_file_path = os.path.join(fixture_dir, "output", mode, f"{test_name}.txt")
        if not os.path.exists(fixture_file_path):
            raise ValueError(
                f"fixture for {test_name} with file path {fixture_file_path} does not exit"
            )

        with open(fixture_file_path) as fp:
            return fp.read()

    return _method


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
