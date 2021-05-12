""" direct from cli interactive w/o ee
"""
import pytest

from .base import base_steps
from .base import BaseClass
from .base import Command
from .base import Step
from .base import Steps

# Note: even thought we are specifing ee=false here, the action should enable it
CLI = Command(subcommand="ee-details", execution_environment=False).join()

initial_steps = [
    Step(user_input=CLI, comment="Initial play list", playbook_status="SUCCESSFUL"),
]

steps = Steps(initial_steps + base_steps).add_indicies()


@pytest.mark.parametrize("step", steps, ids=steps.step_id)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
