"""Some simple tests for exec command and param generation."""

from __future__ import annotations

from typing import NamedTuple

import pytest

from ansible_navigator.actions.exec import _generate_command
from ansible_navigator.configuration_subsystem.definitions import Constants


class CommandTestData(NamedTuple):
    """The artifact files test data object."""

    name: str
    command: str
    use_shell: bool
    default_exec_command: bool
    result_command: str
    result_params: list[str]


command_test_data = [
    pytest.param(
        CommandTestData(
            name="With shell simple",
            command="echo foo",
            use_shell=True,
            default_exec_command=False,
            result_command="/bin/bash",
            result_params=["-c", "echo foo"],
        ),
        id="0",
    ),
    pytest.param(
        CommandTestData(
            name="Without shell simple",
            command="echo foo",
            use_shell=False,
            default_exec_command=False,
            result_command="echo",
            result_params=["foo"],
        ),
        id="1",
    ),
    pytest.param(
        CommandTestData(
            name="With shell complex",
            command="ansible-vault encrypt_string --vault-password-file"
            " a_password_file 'foobar' --name 'the_secret'",
            use_shell=True,
            default_exec_command=False,
            result_command="/bin/bash",
            result_params=[
                "-c",
                "ansible-vault encrypt_string --vault-password-file"
                " a_password_file 'foobar' --name 'the_secret'",
            ],
        ),
        id="2",
    ),
    pytest.param(
        CommandTestData(
            name="Without shell complex",
            command="ansible-vault encrypt_string --vault-password-file"
            " a_password_file 'foobar' --name 'the secret'",
            use_shell=False,
            default_exec_command=False,
            result_command="ansible-vault",
            result_params=[
                "encrypt_string",
                "--vault-password-file",
                "a_password_file",
                "foobar",
                "--name",
                "the secret",
            ],
        ),
        id="3",
    ),
]


@pytest.mark.parametrize("cmd_test_data", command_test_data)
def test_command_generation(cmd_test_data: CommandTestData) -> None:
    """Test the generation of the command and params.

    :param cmd_test_data: The test data
    """
    command, additional_params = _generate_command(
        exec_command=cmd_test_data.command,
        exec_shell=cmd_test_data.use_shell,
        extra_args=Constants.NOT_SET,
        exec_command_is_default=cmd_test_data.default_exec_command,
    )
    comment = command_test_data, command, additional_params
    assert command == cmd_test_data.result_command, comment
    assert additional_params == cmd_test_data.result_params, comment
