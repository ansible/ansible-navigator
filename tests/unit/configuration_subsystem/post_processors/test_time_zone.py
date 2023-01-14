"""Tests for the time zone post processor."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

import pytest

from ansible_navigator.configuration_subsystem import Constants as C
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.configurator import Configurator
from ansible_navigator.configuration_subsystem.navigator_post_processor import (
    NavigatorPostProcessor,
)
from tests.defaults import id_func
from ....defaults import BaseScenario


@dataclass
class Scenario(BaseScenario):
    """Data structure for the time zone post processor tests."""

    name: str
    current: bool | str | dict
    source: C
    exit_message_substr: str = ""
    expected: str | None = None
    index: int = 0

    def __post_init__(self):
        """Set the expected if errors are expected."""
        if self.expected is None:
            object.__setattr__(self, "expected", self.current)

    def __str__(self):
        """Provide a test id.

        :returns: The test id
        """
        return f"{self.source}-{self.current}"


test_data = (
    Scenario(
        name="0",
        current="foo",
        exit_message_substr=(
            "The specified time zone 'foo', set by environment variable, could not be found."
        ),
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        name="1",
        current="Japan",
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        name="2",
        current="local",
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        name="3",
        current={},
        exit_message_substr=(
            "The specified time zone '{}', set by settings file,"
            " must be a string but was found to be a 'dict'."
        ),
        source=C.USER_CFG,
    ),
    Scenario(
        name="4",
        current=True,
        exit_message_substr=(
            "The specified time zone 'True', set by settings file,"
            " must be a string but was found to be a 'bool'."
        ),
        source=C.USER_CFG,
    ),
    Scenario(
        name="5",
        current="foo",
        source=C.USER_CFG,
        exit_message_substr=(
            "The specified time zone 'foo', set by settings file, could not be found."
        ),
    ),
    Scenario(
        name="6",
        current="Japan",
        source=C.USER_CFG,
    ),
    Scenario(
        name="7",
        current="local",
        source=C.USER_CFG,
    ),
    Scenario(
        name="8",
        current="foo",
        exit_message_substr=(
            "The specified time zone 'foo', set by command line, could not be found."
        ),
        source=C.USER_CLI,
    ),
    Scenario(
        name="9",
        current="Japan",
        source=C.USER_CLI,
    ),
    Scenario(
        name="10",
        current="local",
        source=C.USER_CLI,
    ),
)


@pytest.mark.parametrize(argnames="data", argvalues=test_data, ids=id_func)
def test_pp_direct(data: Scenario):
    """Test the time zone post processor.

    :param data: The test data
    """
    settings = deepcopy(NavigatorConfiguration)
    entry = settings.entry("time_zone")

    entry.value.current = data.current
    entry.value.source = data.source

    _messages, exit_messages = NavigatorPostProcessor().time_zone(
        entry=entry,
        config=settings,
    )

    if data.exit_message_substr:
        assert data.exit_message_substr in exit_messages[0].message
    else:
        assert entry.value.current == data.expected


env_var_test_data = [s for s in test_data if s.source is C.ENVIRONMENT_VARIABLE]


@pytest.mark.parametrize(argnames="data", argvalues=env_var_test_data, ids=id_func)
def test_env_var(monkeypatch: pytest.MonkeyPatch, data: Scenario):
    """Test the time zone post processor using the environment variable.

    :param monkeypatch: The monkey patch fixture
    :param data: The test data
    """
    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = True
    configurator = Configurator(application_configuration=application_configuration, params=[])

    monkeypatch.setenv("TZ", str(data.current))

    _messages, exit_messages = configurator.configure()

    if data.exit_message_substr:
        assert data.exit_message_substr in exit_messages[2].message
    else:
        assert application_configuration.entry("time_zone").value.current == data.expected
