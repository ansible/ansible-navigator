"""Some simple tests for exec command and param generation."""

from typing import List
from typing import NamedTuple

import pytest

from ansible_navigator.actions.exec import Action as ExecAction


class CommandTestData(NamedTuple):
    """The artifact files test data object."""

    name: str
    command: str
    shell: bool
    result_command: str
    result_params: list


def id_from_data(value):
    """Return the name from the test data object.

    :param value: The value from which the test id will be extracted
    :returns: The test id
    """
    return f" {value.name} "


command_test_data = [
    CommandTestData(
        name="With shell simple",
        command="echo foo",
        shell=True,
        result_command="/bin/bash",
        result_params=["-c", "echo foo"],
    ),
    CommandTestData(
        name="Without shell simple",
        command="echo foo",
        shell=False,
        result_command="echo",
        result_params=["foo"],
    ),
    CommandTestData(
        name="With shell complex",
        command=(
            "ansible-vault encrypt_string --vault-password-file"
            " a_password_file 'foobar' --name 'the_secret'"
        ),
        shell=True,
        result_command="/bin/bash",
        result_params=[
            "-c",
            "ansible-vault encrypt_string --vault-password-file"
            " a_password_file 'foobar' --name 'the_secret'",
        ],
    ),
    CommandTestData(
        name="Without shell complex",
        command=(
            "ansible-vault encrypt_string --vault-password-file"
            " a_password_file 'foobar' --name 'the secret'"
        ),
        shell=False,
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
]


@pytest.mark.parametrize("data", command_test_data, ids=id_from_data)
def test_artifact_path(data: CommandTestData):
    """Test the generation of the command and params.

    :param data: The test data
    """
    # pylint: disable=protected-access
    command, params = ExecAction._generate_command(exec_command=data.command, exec_shell=data.shell)
    comment = data, command, params
    assert command == data.result_command, comment
    assert params == data.result_params, comment
