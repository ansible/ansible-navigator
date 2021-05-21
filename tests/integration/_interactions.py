""" common classes to handle user interactions
"""
import shlex

from enum import Enum
from typing import List
from typing import NamedTuple
from typing import Union

from .._common import container_runtime_or_fail


class SearchFor(Enum):
    """set the test mode"""

    HELP = "search for help"
    PROMPT = "search for the shell prompt"


class Command(NamedTuple):
    """command details"""

    execution_environment: bool
    config_file: Union[None, str] = None
    container_engine: str = container_runtime_or_fail()
    command: str = "ansible-navigator"
    cmdline: Union[None, str] = None
    log_level: str = "debug"
    mode: str = "interactive"
    pass_environment_variables: List = []
    preclear: bool = False
    subcommand: Union[None, str] = None

    def join(self):
        """create cli command"""
        args = [self.command]
        if isinstance(self.subcommand, str):
            args.append(self.subcommand)
        if isinstance(self.cmdline, str):
            args.extend(shlex.split(self.cmdline))
        if isinstance(self.config_file, str):
            args.extend(["-c", self.config_file])
        args.extend(["--ee", self.execution_environment])
        args.extend(["--ce", self.container_engine])
        args.extend(["--ll", self.log_level])
        args.extend(["--mode", self.mode])
        if self.pass_environment_variables:
            for envvar in self.pass_environment_variables:
                args.extend(["--penv", envvar])
        cmd = " ".join(shlex.quote(str(arg)) for arg in args)
        if self.preclear:
            return "clear && " + cmd
        else:
            return cmd


class Step(NamedTuple):
    # pylint: disable=too-few-public-methods
    """test data object"""
    user_input: str
    comment: str

    look_fors: List[str] = []
    look_nots: List[str] = []
    mask: bool = True
    playbook_status: Union[None, str] = None
    step_index: int = 0
    search_within_response: Union[SearchFor, str, List] = SearchFor.HELP


def add_indicies(steps):
    """update the index of each"""
    return (step._replace(step_index=idx) for idx, step in enumerate(steps))


def step_id(value):
    """return the test id from the test step object"""
    return f"{value.step_index}-{value.user_input}-{value.comment}"
