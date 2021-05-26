""" run stdout tests using tmux """
import pytest

from .base import BaseClass
from .base import inventory_path
from .base import playbook_path
from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import Step
from ..._interactions import add_indicies


class StdoutCommand(Command):
    """stdout command"""

    subcommand = "run"
    preclear = True


class ShellCommand(Step):
    """a shell command"""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="run playbook with ee",
        user_input=StdoutCommand(
            cmdline=f"{playbook_path} -i {inventory_path} --pae false",
            mode="stdout",
            execution_environment=True,
        ).join(),
    ),
    ShellCommand(
        comment="run playbook without ee",
        user_input=StdoutCommand(
            cmdline=f"{playbook_path} -i {inventory_path} --pae false",
            mode="stdout",
            execution_environment=False,
        ).join(),
    ),
    ShellCommand(
        comment="playbook help with ee",
        user_input=StdoutCommand(
            cmdline="--help-playbook",
            mode="stdout",
            execution_environment=True,
        ).join(),
        look_fors=["usage: ansible-playbook [-h]"],
    ),
    ShellCommand(
        comment="playbook help without ee",
        user_input=StdoutCommand(
            cmdline="--help-playbook",
            mode="stdout",
            execution_environment=False,
        ).join(),
        look_fors=["usage: ansible-playbook [-h]"],
    ),
    ShellCommand(
        comment="run help-playbook fail with interactive with ee",
        user_input=StdoutCommand(
            cmdline="--help-playbook",
            mode="interactive",
            execution_environment=True,
        ).join(),
        look_fors=["--hp or --help-playbook is valid only when 'mode' argument is set to 'stdout'"],
    ),
    ShellCommand(
        comment="run help-playbook fail with interactive without ee",
        user_input=StdoutCommand(
            cmdline="--help-playbook",
            mode="interactive",
            execution_environment=False,
        ).join(),
        look_fors=["--hp or --help-playbook is valid only when 'mode' argument is set to 'stdout'"],
    ),
)

steps = add_indicies(stdout_tests)


def step_id(value):
    """return the test id from the test step object"""
    return f"{value.comment}  {value.user_input}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
