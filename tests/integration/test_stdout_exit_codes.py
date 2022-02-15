"""check return codes from mode ``stdout``
"""
import os

from typing import NamedTuple
from typing import Tuple

import pytest

from ..defaults import DEFAULT_CONTAINER_IMAGE
from ..defaults import FIXTURES_DIR


PLAYBOOK = os.path.join(FIXTURES_DIR, "integration", "stdout_exit_codes", "site.yml")


@pytest.fixture(name="params")
def fixture_params(request):
    """generate parameters"""
    return {
        "execution_environment": request.param,
        "execution_environment_image": DEFAULT_CONTAINER_IMAGE,
    }


def id_ee(value):
    """generate id"""
    return f"execution_environment={value}"


def id_test_data(value):
    """generate id"""
    return f"action={value.action_name} return={value.return_code}"


class StdoutTest(NamedTuple):
    """Definition of a stdout test."""

    #: The name of the action
    action_name: str
    #: Parameters for the action
    action_params: Tuple[Tuple, ...]
    #: Text to search for
    present: str
    #: Expected return code
    return_code: int
    #: Expected return message
    message: str = ""


fixture_test_data = (
    StdoutTest(
        action_name="config",
        action_params=(("cmdline", ["--help"]),),
        present="usage: ansible-config",
        return_code=0,
    ),
    StdoutTest(
        action_name="config",
        action_params=(("cmdline", ["foo"]),),
        present="invalid choice: 'foo'",
        return_code=2,
    ),
    StdoutTest(
        action_name="doc",
        action_params=(("cmdline", ["--help"]),),
        present="usage: ansible-doc",
        return_code=0,
    ),
    StdoutTest(
        action_name="doc",
        action_params=(("cmdline", ["--json"]),),
        present="Incorrect options passed",
        return_code=5,
    ),
    StdoutTest(
        action_name="inventory",
        action_params=(("cmdline", ["--help"]),),
        present="usage: ansible-inventory",
        return_code=0,
    ),
    StdoutTest(
        action_name="inventory",
        action_params=(("cmdline", ["foo"]),),
        present="No action selected",
        return_code=1,
    ),
    StdoutTest(
        action_name="run",
        action_params=(("playbook", PLAYBOOK), ("playbook_artifact_enable", False)),
        present="success",
        return_code=0,
    ),
    StdoutTest(
        action_name="run",
        action_params=(("playbook", "foo"), ("playbook_artifact_enable", False)),
        present="foo could not be found",
        return_code=1,
    ),
)


@pytest.mark.parametrize("params", (True, False), indirect=["params"], ids=id_ee)
@pytest.mark.parametrize("test_data", fixture_test_data, ids=id_test_data)
def test(action_run_stdout, params, test_data):
    """test for a return code"""
    action_runner = action_run_stdout(action_name=test_data.action_name, **params)
    run_stdout_return, stdout, stderr = action_runner.run_action_stdout(
        **dict(test_data.action_params),
    )
    assert run_stdout_return.return_code == test_data.return_code
    if test_data.return_code == 0:
        assert test_data.present in stdout
        assert test_data.message in run_stdout_return.message
    else:
        std_stream = stdout if params["execution_environment"] else stderr
        assert test_data.present in std_stream
        assert test_data.message in run_stdout_return.message
