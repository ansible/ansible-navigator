"""Tests for the execution environment volume mount post processor."""
from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass
from itertools import repeat
from pathlib import Path

import pytest

from ansible_navigator.configuration_subsystem import Constants as C
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.navigator_post_processor import (
    NavigatorPostProcessor,
)
from ....defaults import BaseScenario
from ....defaults import id_func


@dataclass
class Scenario(BaseScenario):
    """Data structure for EEV post processor tests."""

    name: str
    current: bool | str | list | dict
    source: C
    expected: list[str] | None = None
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
        name="0",
        current="",
        exit_message_substr="Source not provided. Destination not provided",
        source=C.USER_CLI,
    ),
    Scenario(
        name="1",
        current="abcdef",
        exit_message_substr="Destination not provided.",
        source=C.USER_CLI,
    ),
    Scenario(
        name="2",
        current=[["/tmp:/tmp"]],
        expected=["/tmp:/tmp"],
        source=C.USER_CLI,
    ),
    Scenario(
        name="3",
        current=[["/tmp:/tmp:Z"]],
        expected=["/tmp:/tmp:Z"],
        source=C.USER_CLI,
    ),
    Scenario(
        name="4",
        current=[["/tmp:/tmp:O"]],
        expected=["/tmp:/tmp:O"],
        source=C.USER_CLI,
    ),
    Scenario(
        name="5",
        current=[["/tmp:/tmp:ro"]],
        expected=["/tmp:/tmp:ro"],
        source=C.USER_CLI,
    ),
    Scenario(
        name="6",
        current=[["/tmp:/tmp:rw"]],
        expected=["/tmp:/tmp:rw"],
        source=C.USER_CLI,
    ),
    Scenario(
        name="7",
        current=[["/tmp:/tmp:Y"]],
        exit_message_substr="Unrecognized option: 'Y'",
        source=C.USER_CLI,
    ),
    Scenario(
        name="8",
        current=[["/tmp:/tmp:Z,z"]],
        expected=["/tmp:/tmp:Z,z"],
        source=C.USER_CLI,
    ),
    Scenario(
        name="9",
        current=[["/tmp:/tmp:Z,Y"]],
        exit_message_substr="Unrecognized option: 'Y'",
        source=C.USER_CLI,
    ),
    Scenario(
        name="10",
        current=["/tmp:/tmp"],
        expected=["/tmp:/tmp"],
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        name="11",
        current=["/tmp:/tmp", "/tmp:/tmp"],
        expected=["/tmp:/tmp"],
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        name="12",
        current=["/tmp:/tmp:Z", "/tmp:/tmp"],
        expected=["/tmp:/tmp:Z", "/tmp:/tmp"],
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        name="13",
        current=["/tmp:/tmp:Z,z", "/tmp:/tmp"],
        expected=["/tmp:/tmp:Z,z", "/tmp:/tmp"],
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        name="14",
        current=["/tmp:/tmp:Z,y", "/tmp:/tmp"],
        exit_message_substr="Unrecognized option: 'y'",
        source=C.ENVIRONMENT_VARIABLE,
    ),
    Scenario(
        name="15",
        current=True,
        exit_message_substr="could not be parsed",
        source=C.USER_CFG,
    ),
    Scenario(
        name="16",
        current=[True],
        exit_message_substr="could not be parsed",
        source=C.USER_CFG,
    ),
    Scenario(
        name="17",
        current=[[True]],
        exit_message_substr="could not be parsed",
        source=C.USER_CFG,
    ),
    Scenario(
        name="18",
        current={"src": "/tmp", "dest": "/tmp", "options": "Z"},
        exit_message_substr="could not be parsed",
        source=C.USER_CFG,
    ),
    Scenario(
        name="19",
        current=[{"my_src": "/tmp", "my_dest": "/tmp", "my_options": "Z"}],
        exit_message_substr="could not be parsed",
        source=C.USER_CFG,
    ),
    Scenario(
        name="20",
        current=[{"src": "/tmp", "dest": "/tmp", "options": "Z"}],
        expected=["/tmp:/tmp:Z"],
        source=C.USER_CFG,
    ),
    Scenario(
        name="21",
        current=[{"src": "/tmp", "dest": "/tmp", "options": "O"}],
        expected=["/tmp:/tmp:O"],
        source=C.USER_CFG,
    ),
    Scenario(
        name="22",
        current=[{"src": "~", "dest": "/tmp", "options": "Z"}],
        expected=[f"{Path.home()}:/tmp:Z"],
        source=C.USER_CFG,
    ),
    Scenario(
        name="23",
        current=[{"src": "/tmp", "dest": "~", "options": "Z"}],
        expected=[f"/tmp:{Path.home()}:Z"],
        source=C.USER_CFG,
    ),
    Scenario(
        name="24",
        current=[{"src": True, "dest": False, "options": 42}],
        exit_message_substr=(
            "Source: 'True' is not a string."
            " Destination: 'False' is not a string."
            " Options: '42' is not a string."
        ),
        source=C.USER_CFG,
    ),
    Scenario(
        name="25",
        current=list(repeat({"src": "/tmp", "dest": "/tmp", "options": "Z"}, 4)),
        expected=["/tmp:/tmp:Z"],
        source=C.USER_CFG,
    ),
    Scenario(
        name="26",
        current=[{"src": "/tmp", "dest": "/tmp", "options": "Z,z"}],
        expected=["/tmp:/tmp:Z,z"],
        source=C.USER_CFG,
    ),
    Scenario(
        name="27",
        current=[{"src": "/tmp", "dest": "/tmp", "options": "O,z"}],
        expected=["/tmp:/tmp:O,z"],
        source=C.USER_CFG,
    ),
    Scenario(
        name="28",
        current=[{"src": "/tmp", "dest": "/tmp", "options": "0,z"}],
        exit_message_substr="Unrecognized option: '0'",
        source=C.USER_CFG,
    ),
    Scenario(
        name="29",
        current=[{"src": "/tmp", "dest": "/tmp", "options": "Z,y"}],
        exit_message_substr="Unrecognized option: 'y'",
        source=C.USER_CFG,
    ),
    Scenario(
        name="30",
        current=[["/tmp:/tmp:/tmp"]],
        exit_message_substr="Unrecognized option: '/tmp'",
        source=C.USER_CLI,
    ),
    Scenario(
        name="31",
        current=[[r"C:\WINNT\System32:/tmp"]],
        exit_message_substr="does not exist",
        source=C.USER_CLI,
    ),
    Scenario(
        name="32",
        current=[[r"/WINNT/System32:/tmp"]],
        exit_message_substr="does not exist",
        source=C.USER_CLI,
    ),
)


@pytest.mark.parametrize(argnames="data", argvalues=test_data, ids=id_func)
def test_ee_volume_mount(data: Scenario):
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
