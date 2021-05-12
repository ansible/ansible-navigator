""" from welcome interactive w/ ee
"""
import pytest

from .base import base_steps
from .base import BaseClass
from .base import Command
from .base import Step
from .base import Steps

CLI = Command(execution_environment=True).join()

initial_steps = [
    Step(user_input=CLI, comment="Welcome screen"),
    Step(user_input=":ee-details", comment="Initial play list", playbook_status="SUCCESSFUL"),
]

steps = Steps(initial_steps + base_steps).add_indicies()


@pytest.mark.parametrize("step", steps, ids=steps.step_id)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
