""" check return codes from mode stdout
"""
import os
from typing import NamedTuple
from typing import Tuple


import pytest

from ..defaults import DEFAULT_CONTAINER_IMAGE
from ..defaults import FIXTURES_DIR

PLAYBOOK = os.path.join(FIXTURES_DIR, "integration", "stdout_exit_codes", "site.yml")


@pytest.fixture(name="params")
def fixture_params(container_runtime_or_fail, request):
    """generate params"""
    return {
        "execution_environment": request.param,
        "container_engine": container_runtime_or_fail(),
        "execution_environment_image": DEFAULT_CONTAINER_IMAGE,
    }


def id_ee(value):
    """generate id"""
    return f"execution_environment={value}"


def id_test_data(value):
    """generate id"""
    return f"action={value.action_name} return={value.return_code}"


class StdoutTest(NamedTuple):
    """define the stdout test"""

    action_name: str
    action_params: Tuple[Tuple]
    message: str
    return_code: int


test_datas = (
    StdoutTest(
        action_name="config",
        action_params=(("cmdline", ["--help"]),),
        message="usage: ansible-config",
        return_code=0,
    ),
    StdoutTest(
        action_name="config",
        action_params=(("cmdline", ["foo"]),),
        message="invalid choice: 'foo'",
        return_code=1,
    ),
    StdoutTest(
        action_name="doc",
        action_params=(("cmdline", ["--help"]),),
        message="usage: ansible-doc",
        return_code=0,
    ),
    StdoutTest(
        action_name="doc",
        action_params=(("cmdline", ["--json"]),),
        message="Incorrect options passed",
        return_code=1,
    ),
    StdoutTest(
        action_name="inventory",
        action_params=(("cmdline", ["--help"]),),
        message="usage: ansible-inventory",
        return_code=0,
    ),
    StdoutTest(
        action_name="inventory",
        action_params=(("cmdline", ["foo"]),),
        message="No action selected",
        return_code=1,
    ),
    StdoutTest(
        action_name="run", action_params=(("playbook", PLAYBOOK),), message="success", return_code=0
    ),
    StdoutTest(
        action_name="run",
        action_params=(("playbook", "foo"),),
        message="foo could not be found",
        return_code=1,
    ),
)


@pytest.mark.parametrize("params", [True, False], indirect=["params"], ids=id_ee)
@pytest.mark.parametrize("test_data", test_datas, ids=id_test_data)
def test(action_run_stdout, params, test_data):
    """test for a return code"""
    actionruntest = action_run_stdout(action_name=test_data.action_name, **params)
    ret, out, err = actionruntest.run_action_stdout(**dict(test_data.action_params))
    assert ret == test_data.return_code
    if test_data.return_code == 0:
        assert test_data.message in out, (test_data.message, out, err)
    else:
        std_stream = out if params["execution_environment"] else err
        assert test_data.message in std_stream, (test_data.message, out, err)
