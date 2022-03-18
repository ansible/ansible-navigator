"""Tests for ``config`` from welcome, interactive, specify configuration.
"""
import pytest

from ..._interactions import Command
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import CONFIG_FIXTURE
from .base import BaseClass


CLI = Command(execution_environment=False).join()

steps = (
    UiTestStep(user_input=CLI, comment="welcome screen"),
    UiTestStep(
        user_input=":config",
        comment="enter config from welcome screen (no ee)",
        present=["Yaml filename extensions", "['.yml', '.yaml', '.json']"],
    ),
    UiTestStep(user_input=":back", comment="return to welcome screen"),
    UiTestStep(
        user_input=":config -c " + CONFIG_FIXTURE,
        comment="enter config from welcome screen, custom config, (no ee)",
        present=["Yaml filename extensions", "['.os2']"],
    ),
)

steps = add_indices(steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``config`` from welcome, interactive, specify configuration."""

    PANE_HEIGHT = 300
    UPDATE_FIXTURES = False
