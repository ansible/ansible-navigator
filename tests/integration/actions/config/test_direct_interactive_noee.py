""" config direct from cli interactive w/o ee
"""
import pytest

from .base import add_indicies
from .base import base_steps
from .base import step_id
from .base import BaseClass
from .base import Command
from .base import Step


CLI = Command(subcommand="config", execution_environment=False).join()

initial_steps = (Step(user_input=CLI, comment="ansible-navigator config command top window"),)

steps = add_indicies(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
