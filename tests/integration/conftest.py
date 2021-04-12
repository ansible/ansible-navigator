import pytest
import os
import libtmux
import time

from .. import defaults


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

@pytest.fixture
def run_command_tmux_session():
    def _method(window_name, user_interactions, config_path=None, session_name="ansible-navigator-test"):
        out = ''
        cwd=os.path.join(os.path.dirname(__file__), "..", "..")

        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), "..", "fixtures", "ansible-navigator.yaml"
            )
        os.environ.update({"ANSIBLE_NAVIGATOR_CONFIG": config_path})

        try:
            server = libtmux.Server()
            session = server.new_session(session_name, kill_session=True)
            window = session.new_window(window_name)
            pane = window.panes[0]
            # ensure cwd is library top level folder
            pane.send_keys(f"cd {cwd}")
            for user_interaction in user_interactions:
                pane.send_keys(user_interaction)
                time.sleep(defaults.tumx_read_delay_after_user_interaction)
                out += '\n'.join(window.cmd('capture-pane', '-p').stdout)
        finally:
            if server.has_session(session_name):
                session.kill_session()
            server.kill_server()

        return out

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
