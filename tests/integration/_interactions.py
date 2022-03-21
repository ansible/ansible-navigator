"""common classes to handle user interactions
"""
import shlex

from enum import Enum
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Union


class SearchFor(Enum):
    """set the test mode"""

    HELP = "search for help"
    PROMPT = "search for the shell prompt"
    WARNING = "search for a blocking warning notification"


class Command(NamedTuple):
    """command details"""

    execution_environment: bool
    cmdline: Optional[str] = None
    command: str = "ansible-navigator"
    log_level: str = "debug"
    mode: str = "interactive"
    pass_environment_variables: List = []
    preclear: bool = False
    precommand: str = ""
    raw_append: str = ""
    """Anything raw that should be appended, and not shlex quoted"""
    subcommand: Optional[str] = None

    def join(self):
        """create CLI command"""
        args = [self.command]
        if isinstance(self.subcommand, str):
            args.append(self.subcommand)
        if isinstance(self.cmdline, str):
            args.extend(shlex.split(self.cmdline))
        args.extend(["--ee", self.execution_environment])
        args.extend(["--ll", self.log_level])
        args.extend(["--mode", self.mode])
        if self.pass_environment_variables:
            for env_var in self.pass_environment_variables:
                args.extend(["--penv", env_var])
        cmd = " ".join(shlex.quote(str(arg)) for arg in args)
        if self.precommand:
            cmd = f"{self.precommand} {cmd}"
        if self.preclear:
            cmd = f"clear && {cmd}"
        if self.raw_append:
            cmd = f"{cmd} {self.raw_append}"
        return cmd


class UiTestStep(NamedTuple):
    """A simulated user interaction with the user interface."""

    #: The string to send to the tmux session
    user_input: str
    #: Explanation of what is being sent or done
    comment: str
    #: Search for in the response
    present: List[str] = []
    #: Ensure not in the response
    absent: List[str] = []
    #: Should the output be masked prior to writing a fixture
    mask: bool = True
    #: The index of the step with the list of all steps
    step_index: int = 0
    #: Find this before returning from the tmux session to the test
    search_within_response: Union[SearchFor, str, List] = SearchFor.HELP

    def __str__(self):
        """Produce a test id for this step."""
        return f"{self.comment}  {self.user_input}"


def add_indices(steps):
    """update the index of each"""
    return (step._replace(step_index=idx) for idx, step in enumerate(steps))


def step_id(value):
    """return the test id from the test step object"""
    return f"{value.step_index}-{value.user_input}-{value.comment}"


def step_id_padded(value):
    """Return the test id from the test step object, index padded to 2.

    :param value: The test value
    """
    return f"{value.step_index:02d}-{value.user_input}-{value.comment}"
