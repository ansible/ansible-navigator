"""Tests for the execution environment volume mount post processor."""
from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass
from itertools import repeat
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pytest

from ansible_navigator.configuration_subsystem import Constants as C
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.navigator_post_processor import (
    NavigatorPostProcessor,
)


@dataclass
class Scenario:
    """Data structure for EEV post processor tests."""

    current: Union[bool, str, List, Dict]
    source: C
    expected: Optional[List[str]] = None
    exit_message_substr: str = ""
    index: int = 0

    def __post_init__(self):
        """Set the expected if errors are expected."""
        if self.expected is None and self.exit_message_substr:
            self.expected = self.current

    def __str__(self):
        """Provide a test id.

        :returns: The test id
        """
        return f"{self.source}-{self.current}"


test_data = (
    Scenario(
        current="",
        exit_message_substr="Source not provided. Destination not provided",
        source=C.USER_CLI,
    ),
    Scenario(
        current="abcdef",
        exit_message_substr="Source: 'abcdef' does not exist. Destination not provided.",
        source=C.USER_CLI,
    ),
    Scenario(
        current=[["/tmp:/tmp"]],
        expected=["/tmp:/tmp"],
        source=C.USER_CLI,
    ),
    Scenario(
        current=[["/tmp:/tmp:Z"]],
        expected=["/tmp:/tmp:Z"],
        source=C.USER_CLI,
    ),
    Scenario(
        current=[["/tmp:/tmp:Y"]],
        exit_message_substr="Unrecognized option: 'Y'",
        source=C.USER_CLI,
    ),
    Scenario(
        current=[["/tmp:/tmp:Z,z"]],
        expected=["/tmp:/tmp:Z,z"],
        source=C.USER_CLI,
    ),
    Scenario(
        current=[["/tmp:/tmp:Z,Y"]],
        exit_message_substr="Unrecognized option: 'Y'",
        source=C.USER_CLI,
    ),
    Scenario(
        current=["/tmp:/tmp"],
        expected=["/tmp:/tmp"],
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        current=["/tmp:/tmp", "/tmp:/tmp"],
        expected=["/tmp:/tmp"],
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        current=["/tmp:/tmp:Z", "/tmp:/tmp"],
        expected=["/tmp:/tmp:Z", "/tmp:/tmp"],
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        current=["/tmp:/tmp:Z,z", "/tmp:/tmp"],
        expected=["/tmp:/tmp:Z,z", "/tmp:/tmp"],
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        current=["/tmp:/tmp:Z,y", "/tmp:/tmp"],
        exit_message_substr="Unrecognized option: 'y'",
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        current=True,
        exit_message_substr="could not be parsed",
        source=C.USER_CFG,
    ),
    Scenario(
        current=[True],
        exit_message_substr="could not be parsed",
        source=C.USER_CFG,
    ),
    Scenario(
        current=[[True]],
        exit_message_substr="could not be parsed",
        source=C.USER_CFG,
    ),
    Scenario(
        current={"src": "/tmp", "dest": "/tmp", "options": "Z"},
        exit_message_substr="could not be parsed",
        source=C.USER_CFG,
    ),
    Scenario(
        current=[{"my_src": "/tmp", "my_dest": "/tmp", "my_options": "Z"}],
        exit_message_substr="could not be parsed",
        source=C.USER_CFG,
    ),
    Scenario(
        current=[{"src": "/tmp", "dest": "/tmp", "options": "Z"}],
        expected=["/tmp:/tmp:Z"],
        source=C.USER_CFG,
    ),
    Scenario(
        current=[{"src": True, "dest": False, "options": 42}],
        exit_message_substr=(
            "Source: 'True' is not a string."
            " Destination: 'False' is not a string."
            " Options: '42' is not a string."
        ),
        source=C.USER_CFG,
    ),
    Scenario(
        current=list(repeat({"src": "/tmp", "dest": "/tmp", "options": "Z"}, 4)),
        expected=["/tmp:/tmp:Z"],
        source=C.USER_CFG,
    ),
    Scenario(
        current=[{"src": "/tmp", "dest": "/tmp", "options": "Z,z"}],
        expected=["/tmp:/tmp:Z,z"],
        source=C.USER_CFG,
    ),
    Scenario(
        current=[{"src": "/tmp", "dest": "/tmp", "options": "Z,y"}],
        exit_message_substr="Unrecognized option: 'y'",
        source=C.USER_CFG,
    ),
    Scenario(
        current=[[r"C:\WINNT\System32:/tmp"]],
        exit_message_substr="Unrecognized option: '/tmp'",
        source=C.USER_CLI,
    ),
    Scenario(
        current=[[r"/WINNT/System32:/tmp"]],
        exit_message_substr="does not exist",
        source=C.USER_CLI,
    ),
)


@pytest.mark.parametrize(argnames="data", argvalues=test_data, ids=str)
def test(data: Scenario):
    """Test the eev post processor.

    :param data: The test data
    """
    settings = deepcopy(NavigatorConfiguration)
    entry = settings.entry("execution_environment_volume_mounts")

    entry.value.current = data.current
    entry.value.source = data.source

    _messages, exit_messages = NavigatorPostProcessor().execution_environment_volume_mounts(
        entry=entry,
        config=settings,
    )
    if isinstance(data.expected, Iterable) and isinstance(entry.value.current, Iterable):
        assert sorted(data.expected) == sorted(entry.value.current)
    else:
        # A bool can't be sorted
        assert data.expected == entry.value.current

    if data.exit_message_substr:
        assert data.exit_message_substr in exit_messages[0].message
