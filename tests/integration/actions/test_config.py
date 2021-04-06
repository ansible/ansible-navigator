""" config integration tests
"""
import os
from .._common import ActionRunTest
from tests import defaults


def test_run_config_interactive() -> None:
    """test config in interactive mode"""
    at = ActionRunTest("config")
    action_obj = at.run_action_interactive()
    assert action_obj._config[0]["option"] == "ACTION_WARNINGS"


def test_run_config_stdout_list() -> None:
    """test config list to stdout"""
    at = ActionRunTest("config")
    out, err = at.run_action_stdout(["list"])
    assert "ACTION_WARNING" in out
    # TODO: handle DEPRECATION WARNINGS
    # assert err == ""


def test_run_stdout_dump() -> None:
    """test config dump to stdout"""
    at = ActionRunTest("config")
    out, err = at.run_action_stdout(["dump"])
    assert "ACTION_WARNING" in out
    # TODO: handle DECRECATION WARNINGS
    # assert err == ""


def test_run_stdout_dump_custom_config(test_fixtures_dir) -> None:
    """test config dump to stdout"""
    at = ActionRunTest("config")
    out, err = at.run_action_stdout(
        ["dump", "-c", os.path.join(test_fixtures_dir, "ansible.cfg"), "--only-changed"]
    )
    assert "DEFAULT_TIMEOUT" in out
    assert "350" in out
    # TODO: handle DEPRECATION WARNINGS
    # assert err == ""


def test_run_config_interactive_container(container_runtime_installed) -> None:
    """test config in interactive mode within execution environment"""
    kwargs = {
        "container_engine": container_runtime_installed,
        "execution_environment": True,
        "ee_image": defaults.default_container_image,
    }
    at = ActionRunTest("config", **kwargs)
    action_obj = at.run_action_interactive()
    assert action_obj._config[0]["option"] == "ACTION_WARNINGS"


def test_run_stdout_dump_container(container_runtime_installed) -> None:
    """test config dump to stdout within execution environment"""
    kwargs = {
        "container_engine": container_runtime_installed,
        "execution_environment": True,
        "ee_image": defaults.default_container_image,
    }
    at = ActionRunTest("config", **kwargs)
    out, err = at.run_action_stdout(["dump"])
    assert "ACTION_WARNING" in out
    # TODO: handle DEPRECATION WARNINGS
    # assert err == ""
