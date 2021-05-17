""" config from welcome interactive w ee
"""
import pytest

from .base import add_indicies
from .base import step_id
from .base import BaseClass
from .base import Command
from .base import Step


CLI = Command(execution_environment=False).join()

steps = (
    Step(user_input=CLI, comment="welcome screen"),
    Step(
        user_input=":config",
        comment="enter config from welcome screen",
        mask=False,
        look_nots=["/home/runner"],
        look_fors=["ANSIBLE_CACHE_PLUGIN_TIMEOUT", "42"],
    ),
    Step(user_input=":back", comment="return to welcome screen"),
    Step(
        user_input=":config --ee True",
        comment="enter config from welcome screen",
        mask=False,
        look_fors=["/home/runner"],
    ),
)

steps = add_indicies(steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
