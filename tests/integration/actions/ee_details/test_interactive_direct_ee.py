"""direct from cli interactive w/ ee
"""
import pytest

from .base import add_indicies
from .base import base_steps
from .base import step_id
from .base import BaseClass
from .base import Command
from .base import Step

CLI = Command(subcommand="ee-details", execution_environment=True).join()

initial_steps = (
    Step(user_input=CLI, comment="Initial play list", search_within_response="SUCCESSFUL"),
)

steps = add_indicies(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
