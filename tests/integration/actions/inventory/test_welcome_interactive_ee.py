""" inventory from welcome interactive w/ ee
"""
import pytest

from .base import ANSIBLE_INVENTORY_FIXTURE_DIR
from .base import base_steps
from .base import BaseClass


from ..._interactions import add_indicies
from ..._interactions import Command
from ..._interactions import Step
from ..._interactions import step_id


CLI = Command(execution_environment=True).join()
cmdline = f":inventory -i {ANSIBLE_INVENTORY_FIXTURE_DIR}"

initial_steps = (
    Step(user_input=CLI, comment="welcome screen"),
    Step(user_input=cmdline, comment="ansible-navigator inventory command top window"),
)

steps = add_indicies(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
