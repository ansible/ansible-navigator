"""Check return codes from mode ``stdout``."""

from __future__ import annotations

import os

from collections.abc import Iterable
from pathlib import Path
from typing import Any
from typing import NamedTuple

import pytest

from ansible_navigator.utils.functions import shlex_join
from tests.conftest import TCmdInTty
from tests.defaults import FIXTURES_DIR
from tests.defaults import id_func

from .conftest import ActionRunTest


PLAYBOOK = os.path.join(FIXTURES_DIR, "integration", "stdout_exit_codes", "site.yml")


@pytest.fixture(name="params")
def fixture_params(
    default_ee_image_name: str,
    valid_container_engine: str,
    request: pytest.FixtureRequest,
) -> dict[str, str]:
    """Generate parameters.

    :param default_ee_image_name: The default execution environment image name
    :param valid_container_engine: The valid container engine
    :param request: The pytest request object
    :returns: The parameters
    """
    return {
        "container_engine": valid_container_engine,
        "execution_environment": request.param,
        "execution_environment_image": default_ee_image_name,
    }


def id_ee(value: bool):
    """Generate the test id.

    :param value: The value of the parameter
    :returns: The test id
    """
    return "-ee" if value else "-no_ee"


def id_test_data(value: StdoutTest):
    """Generate the test id.

    :param value: The value of the parameter
    :returns: The test id
    """
    return f"{value.action_name}-r{value.return_code}"


class StdoutTest(NamedTuple):
    """Definition of a stdout test."""

    #: The name of the action
    action_name: str
    #: Parameters for the action
    action_params: Iterable[tuple[str, str | bool | list[str]]]
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
        # cspell:disable-next-line
        present="ncorrect options passed",
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
def test_stdout(
    action_run_stdout: type[ActionRunTest],
    params: dict[str, Any],
    test_data: StdoutTest,
):
    """Test for a return code.

    :param action_run_stdout: The action runner
    :param params: The parameters
    :param test_data: The test data

    """
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


class StdoutCliTest(NamedTuple):
    """Definition of a stdout cli test."""

    name: str
    comment: str
    """Description of the test"""
    params: list[str]
    """Parameters for the subcommand"""
    return_code: int
    """Expected return code"""
    navigator_stderr: str
    """Navigator produced stderr"""
    navigator_stdout: str
    """Navigator produced stdout"""
    ansible_stdout: str
    """Ansible produced stdout"""
    ansible_stderr: str
    """Ansible produced stderr"""
    subcommand: str
    """The name of the subcommand"""
    mode: str = "stdout"
    """The mode to run in"""

    def __str__(self) -> str:
        """Provide a test id.

        :returns: The test id
        """
        return self.comment

    @property
    def command(self) -> list[str]:
        """Provide the constructed command.

        :returns: The command
        """
        return ["ansible-navigator", self.subcommand] + self.params + ["--mode", self.mode]


# Intentionally not using parametrize so the behavior can be documented
StdoutCliTests = (
    StdoutCliTest(
        name="0",
        comment="run pass",
        subcommand="run",
        params=[PLAYBOOK],
        return_code=0,
        ansible_stdout="ok=1",
        ansible_stderr="",
        navigator_stdout="",
        navigator_stderr="",
    ),
    StdoutCliTest(
        name="1",
        comment="run fail",
        subcommand="run",
        params=["no_such_playbook.yaml"],
        return_code=1,
        ansible_stdout="",
        ansible_stderr="could not be found",
        navigator_stdout="",
        navigator_stderr="review the log",
    ),
)


@pytest.mark.usefixtures("use_venv")
@pytest.mark.parametrize(argnames="pae", argvalues=(True, False), ids=("pae_true", "pae_false"))
@pytest.mark.parametrize(argnames="exec_env", argvalues=(True, False), ids=("ee_true", "ee_false"))
@pytest.mark.parametrize(argnames="data", argvalues=StdoutCliTests, ids=id_func)
def test_run_through_cli(
    tmp_path: Path,
    data: StdoutCliTest,
    exec_env: bool,
    pae: bool,
    cmd_in_tty: TCmdInTty,
) -> None:
    """Test for a return code from run through a shell.

    :param tmp_path: A tmp location
    :param data: The test data
    :param exec_env: Enable/disable execution environment support
    :param pae: Enable/disable playbook artifact creation
    :param cmd_in_tty: The tty command runner
    :raises AssertionError: When no virtual environment found
    """
    log_file = str(Path(tmp_path, "log.txt"))
    artifact_file = str(Path(tmp_path, "artifact.json"))

    common = ["--lf", log_file, "--pae", str(pae), "--pas", artifact_file, "--ee", str(exec_env)]
    command = shlex_join(data.command + common)
    stdout, stderr, exit_code = cmd_in_tty(command)

    assert data.ansible_stdout in stdout
    if not exec_env and not pae:
        # Without an EE and PAE, ansible writes to ``stderr``
        assert data.ansible_stderr in stderr
    else:
        # Everything is routed through ``stdout``
        assert data.ansible_stderr in stdout
    assert data.navigator_stdout in stdout
    assert data.navigator_stderr in stderr
    assert data.return_code == exit_code
