"""Tests for exec, mode stdout, parameters set using the CLI.

A variety of formats are tested here, each with a different
placement of the vault command. Although none result in a vaulted
file, the intent is to ensure the entire vault command is passed
to ansible vault within the execution environment.
"""

import pytest

from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from .base import BaseClass


class ShellCommand(UiTestStep):
    """A shell command."""

    search_within_response = SearchFor.PROMPT


VAULT_COMMAND = (
    "ansible-vault encrypt_string --vault-password-file a_password_file 'foobar'"
    " --name 'the_secret'"
)

BASE_COMMAND = "ansible-navigator --ll debug --la false"

variations = (
    f"{BASE_COMMAND} --mode stdout exec {VAULT_COMMAND}",
    f"{BASE_COMMAND} --mode stdout exec --exec-shell false {VAULT_COMMAND}",
    f"{BASE_COMMAND} --mode stdout exec -- {VAULT_COMMAND}",
    f"{BASE_COMMAND} --mode stdout exec --exec-shell false -- {VAULT_COMMAND}",
    f'{BASE_COMMAND} exec "{VAULT_COMMAND}" --mode stdout',
    f'{BASE_COMMAND} exec "{VAULT_COMMAND}" --mode stdout --exec-shell false',
)

stdout_tests = (
    ShellCommand(
        comment="Vault variation",
        user_input=f"clear && {variation}",
        present=["a_password_file was not found"],
    )
    for idx, variation in enumerate(variations)
)

steps = add_indices(stdout_tests)


def step_id(test_value: ShellCommand) -> str:
    """Return the test id from the test step object.

    :param test_value: The data from the test iteration
    :returns: An id for the test
    """
    return f"{test_value.comment}  {test_value.user_input}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for exec, mode stdout, parameters set using the CLI."""

    update_fixtures = False
