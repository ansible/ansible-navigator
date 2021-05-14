""" from welcome interactive w/ ee
"""
import pytest

from .base import add_indicies
from .base import base_steps
from .base import step_id
from .base import BaseClass
from .base import Command
from .base import Mode
from .base import Step

CLI = Command(execution_environment=True).join()

initial_steps = (
    Step(user_input=CLI, comment="Welcome screen"),
    Step(user_input=":ee-details", comment="Initial play list", playbook_status="SUCCESSFUL"),
)

steps = add_indicies(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """run the tests"""

    TEST_MODE = Mode.INTERACTIVE
    UPDATE_FIXTURES = False
