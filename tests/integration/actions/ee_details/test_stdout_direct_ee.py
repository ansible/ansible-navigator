"""direct from cli interactive w/ ee
"""
import pytest

from .base import add_indicies
from .base import step_id
from .base import BaseClass
from .base import Command
from .base import Step

CLI = Command(subcommand="ee-details", execution_environment=True, mode="stdout").join()

only_step = (
    Step(
        user_input=CLI,
        comment="Playbook output",
        look_fors=["python_version", "failed=0"],
        wait_on_cli_prompt=True,
    ),
)

steps = add_indicies(only_step)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
