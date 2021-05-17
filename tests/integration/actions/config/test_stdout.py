""" config integration tests
"""
import os
import pytest

from tests import defaults
from typing import List

from .base import BaseClass

from ..._action_run_test import ActionRunTest

from ...._common import container_runtime_or_fail


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


def test_run_stdout_dump_container() -> None:
    """test config dump to stdout within execution environment"""
    kwargs = {
        "set_environment_variable": {"PAGER": "cat"},
        "container_engine": container_runtime_or_fail(),
        "execution_environment": True,
        "execution_environment_image": defaults.DEFAULT_CONTAINER_IMAGE,
    }
    actionruntest = ActionRunTest("config", **kwargs)
    out, _err = actionruntest.run_action_stdout(["dump"])
    assert "ACTION_WARNING" in out
    # TODO: handle DEPRECATION WARNINGS
    # assert err == ""


# ansible-config list without EE
CLI_CONFIG_LIST_WITHOUT_EE = (
    "ansible-navigator config list -m stdout" " --execution-environment false"
)


# ansible-config help with EE
CLI_CONFIG_HELP_WITH_EE = (
    "ansible-navigator config --help-config -m stdout"
    " --execution-environment true --ce " + container_runtime_or_fail()
)

testdata_2: List = [
    (
        0,
        CLI_CONFIG_HELP_WITH_EE,
        "ansible-navigator config help with ee",
        "config_help_with_ee",
        ["usage: ansible-config [-h]"],
    ),
]


@pytest.mark.parametrize("index, user_input, comment, testname, expected_in_output", testdata_2)
class TestConfigHelpWithEE(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "stdout"


# ansible-config help without EE
CLI_CONFIG_HELP_WITH_EE = (
    "ansible-navigator config --help-config -m stdout --execution-environment false"
)

testdata_3: List = [
    (
        0,
        CLI_CONFIG_HELP_WITH_EE,
        "ansible-navigator config help without ee",
        "config_help_without_ee",
        ["usage: ansible-config [-h]"],
    ),
]


@pytest.mark.parametrize("index, user_input, comment, testname, expected_in_output", testdata_3)
class TestConfigHelpWithoutEE(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "stdout"


# ansible-config help failed check in interactive mode
CLI_CONFIG_HELP_WITH_EE_WRONG_MODE = (
    "ansible-navigator config --help-config -m interactive"
    " --execution-environment true --ce " + container_runtime_or_fail()
)

testdata_4: List = [
    (
        0,
        CLI_CONFIG_HELP_WITH_EE_WRONG_MODE,
        "ansible-navigator config help with ee in wrong mode",
        "config_help_with_ee_wrong_mode",
        ["--help-config or --hc is valid only when 'mode' argument is set to 'stdout'"],
    ),
]


@pytest.mark.parametrize("index, user_input, comment, testname, expected_in_output", testdata_4)
class TestConfigHelpWithEEWrongMode(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "stdout"


# ansible-config help failed check in interactive mode
CLI_CONFIG_HELP_WITHOUT_EE_WRONG_MODE = (
    "ansible-navigator config --help-config -m interactive" " --execution-environment false"
)

testdata_5: List = [
    (
        0,
        CLI_CONFIG_HELP_WITHOUT_EE_WRONG_MODE,
        "ansible-navigator config help without ee in wrong mode",
        "config_help_with_ee_wrong_mode",
        ["--help-config or --hc is valid only when 'mode' argument is set to 'stdout'"],
    ),
]


@pytest.mark.parametrize("index, user_input, comment, testname, expected_in_output", testdata_5)
class TestConfigHelpWithoutEEWrongMode(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "stdout"
