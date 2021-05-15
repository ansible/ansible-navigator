""" direct from cli interactive w/o ee
"""
import pytest

from .base import add_indicies
from .base import base_steps
from .base import step_id
from .base import BaseClass
from .base import Command
from .base import Step

# Note: even thought we are specifing ee=false here, the action should enable it
CLI = Command(subcommand="ee-details", execution_environment=False).join()

initial_steps = (
    Step(user_input=CLI, comment="Initial play list", search_within_response="SUCCESSFUL"),
)

steps = add_indicies(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
