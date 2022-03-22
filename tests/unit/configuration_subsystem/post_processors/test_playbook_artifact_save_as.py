"""Tests for the playbook artifact save as post processor."""
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional

import pytest

from ansible_navigator.configuration_subsystem import Constants as C
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.navigator_post_processor import (
    NavigatorPostProcessor,
)


@dataclass
class Scenario:
    """Data structure for PAS post processor tests."""

    current: Optional[str] = None
    expected: Optional[str] = None
    exit_message_substr: str = ""

    def __post_init__(self):
        """Set the expected if errors are expected."""
        if self.expected is None:
            self.expected = self.current

    def __str__(self):
        """Provide a test id.

        :returns: The test id
        """
        return f"{self.current}"


test_data = (
    Scenario(
        expected="{playbook_dir}/{playbook_name}-artifact-{time_stamp}.json",
    ),
    Scenario(
        current="/tmp/artifact.json",
    ),
    Scenario(
        current="{playbook_dir}/{playbook_name}-artifact-{ts_utc}.json",
        exit_message_substr=(
            "The playbook artifact file name"
            " '{playbook_dir}/{playbook_name}-artifact-{ts_utc}.json', set by command line,"
            " has unrecognized variables: 'ts_utc'"
        ),
    ),
    Scenario(
        current="{name}.json",
        exit_message_substr=(
            "The playbook artifact file name"
            " '{name}.json', set by command line,"
            " has unrecognized variables: 'name'"
        ),
    ),
)


@pytest.mark.parametrize(argnames="data", argvalues=test_data, ids=str)
def test(data: Scenario):
    """Test the PAS post processor.

    :param data: The test data
    """
    settings = deepcopy(NavigatorConfiguration)
    entry = settings.entry("playbook_artifact_save_as")

    if data.current is None:
        entry.value.current = entry.value.default
    else:
        entry.value.current = data.current
    entry.value.source = C.USER_CLI

    _messages, exit_messages = NavigatorPostProcessor().playbook_artifact_save_as(
        entry=entry,
        config=settings,
    )
    assert entry.value.current == data.expected

    if data.exit_message_substr:
        assert data.exit_message_substr in exit_messages[0].message
