""" config integration tests
"""
import os

from tests import defaults

from ..._common import ActionRunTest


def test_run_config_stdout_list() -> None:
    """test config list to stdout"""
    actionruntest = ActionRunTest("config")
    out, _err = actionruntest.run_action_stdout(["list"])
    assert "ACTION_WARNING" in out
    # TODO: handle DEPRECATION WARNINGS
    # assert err == ""


def test_run_stdout_dump() -> None:
    """test config dump to stdout"""
    actionruntest = ActionRunTest("config")
    out, _err = actionruntest.run_action_stdout(["dump"])
    assert "ACTION_WARNING" in out
    # TODO: handle DECRECATION WARNINGS
    # assert err == ""


def test_run_stdout_dump_custom_config(test_fixtures_dir) -> None:
    """test config dump to stdout"""
    actionruntest = ActionRunTest("config")
    out, _err = actionruntest.run_action_stdout(
        ["dump", "-c", os.path.join(test_fixtures_dir, "ansible.cfg"), "--only-changed"]
    )
    assert "DEFAULT_TIMEOUT" in out
    assert "350" in out
    # TODO: handle DEPRECATION WARNINGS
    # assert err == ""


def test_run_stdout_dump_container(container_runtime_installed) -> None:
    """test config dump to stdout within execution environment"""
    kwargs = {
        "set_environment_variable": {"PAGER": "cat"},
        "container_engine": container_runtime_installed,
        "execution_environment": True,
        "execution_environment_image": defaults.DEFAULT_CONTAINER_IMAGE,
    }
    actionruntest = ActionRunTest("config", **kwargs)
    out, _err = actionruntest.run_action_stdout(["dump"])
    assert "ACTION_WARNING" in out
    # TODO: handle DEPRECATION WARNINGS
    # assert err == ""
