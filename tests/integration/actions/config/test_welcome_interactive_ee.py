"""Tests for ``config`` from welcome, interactive, with an EE.
"""
import pytest

from ..._interactions import Command
from ..._interactions import TestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import BaseClass
from .base import base_steps


CLI = Command(execution_environment=True).join()

initial_steps = (
    TestStep(user_input=CLI, comment="welcome screen"),
    TestStep(user_input=":config", comment="enter config from welcome screen"),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``config`` from welcome, interactive, with an EE."""

    UPDATE_FIXTURES = False
