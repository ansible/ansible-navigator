""" exec stdout tests using tmux """
import pytest


from .base import BaseClass

from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import Step
from ..._interactions import add_indicies


class StdoutCommand(Command):
    """stdout command"""

    mode = "stdout"
    subcommand = "exec"
    preclear = True


class ShellCommand(Step):
    """a shell command"""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="exec echo with ee",
        user_input=StdoutCommand(
            cmdline="--excmd 'echo test_data_from_cli'",
            execution_environment=True,
        ).join(),
        look_fors=["bash", "test_data_from_cli"],
        look_nots=["ERROR"],
    ),
    ShellCommand(
        comment="exec echo without ee",
        user_input=StdoutCommand(
            cmdline="--excmd 'echo test_data_from_cli'",
            execution_environment=False,
        ).join(),
        look_fors=["bash", "test_data_from_cli", "ERROR", "requires execution environment support"],
    ),
    ShellCommand(
        comment="exec echo check path via shell",
        user_input=StdoutCommand(
            cmdline="--excmd 'echo $PATH'",
            execution_environment=True,
        ).join(),
        look_fors=["/sbin"],
    ),
    ShellCommand(
        comment="exec echo check no path via shell",
        user_input=StdoutCommand(
            cmdline="--excmd 'echo $PATH' --exshell false",
            execution_environment=True,
        ).join(),
        look_fors=["$PATH"],
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
