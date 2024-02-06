"""Tests for ``config`` from welcome, interactive, with an EE."""

import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id

from .base import BaseClass
from .base import base_steps


CLI = Command(execution_environment=True).join()

initial_steps = (
    UiTestStep(user_input=CLI, comment="welcome screen"),
    UiTestStep(user_input=":config", comment="enter config from welcome screen"),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``config`` from welcome, interactive, with an EE."""

    UPDATE_FIXTURES = False
