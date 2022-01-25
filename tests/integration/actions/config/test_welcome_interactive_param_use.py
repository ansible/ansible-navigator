"""Tests for ``config`` from welcome, interactive, with parameters.
"""
import pytest

from ..._interactions import Command
from ..._interactions import Step
from ..._interactions import add_indicies
from ..._interactions import step_id
from .base import BaseClass


CLI = Command(execution_environment=False).join()

steps = (
    Step(user_input=CLI, comment="welcome screen"),
    Step(
        user_input=":config",
        comment="enter config from welcome screen",
        mask=False,
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
    """Run the tests for ``config`` from welcome, interactive, with parameters."""

    UPDATE_FIXTURES = False
