"""Unit tests for artifact creation. in the run action."""
import logging
import os
import re

from copy import deepcopy
from dataclasses import dataclass
from typing import Optional
from typing import Pattern

import pytest

from pytest_mock import MockerFixture

from ansible_navigator.actions.run import Action as action
from ansible_navigator.configuration_subsystem import NavigatorConfiguration


@dataclass
class Scenario:
    """The artifact files test data object."""

    name: str
    filename: Optional[str]
    playbook: str
    starts_with: Optional[str] = None
    re_match: Optional[Pattern] = None
    help_playbook: bool = False
    time_zone: str = "UTC"

    def __post_init__(self):
        """Ensure one match is set.

        :raises ValueError: When neither is set
        """
        if not (self.re_match or self.starts_with):
            raise ValueError("re_match or starts_with required")

    def __str__(self):
        """Provide the test id.

        :returns: The test id
        """
        return self.name


test_data = [
    Scenario(
        name="Filename absolute",
        filename="/tmp/artifact.json",
        playbook="site.yml",
        starts_with="/tmp/artifact.json",
    ),
    Scenario(
        name="Filename with .",
        filename="./artifact.json",
        playbook="site.yml",
        starts_with=f"{os.path.abspath('.')}/artifact.json",
    ),
    Scenario(
        name="Filename with ..",
        filename="../artifact.json",
        playbook="site.yml",
        starts_with=f"{os.path.abspath('..')}/artifact.json",
    ),
    Scenario(
        name="Filename with ~",
        filename="~/artifact.json",
        playbook="/tmp/site.yaml",
        starts_with="/home/test_user/artifact.json",
    ),
    Scenario(
        name="Playbook absolute",
        filename=None,
        playbook="/tmp/site.yaml",
        starts_with="/tmp/site-artifact",
    ),
    Scenario(
        name="Playbook with .",
        filename=None,
        playbook="./site.yaml",
        starts_with=f"{os.path.abspath('.')}/site-artifact",
    ),
    Scenario(
        name="Playbook with ..",
        filename=None,
        playbook="../site.yaml",
        starts_with=f"{os.path.abspath('..')}/site-artifact",
    ),
    Scenario(
        name="Playbook with ~",
        filename=None,
        playbook="~/site.yaml",
        starts_with="/home/test_user/site-artifact",
    ),
    Scenario(
        name="help_playbook enabled",
        filename=None,
        playbook="~/site.yaml",
        starts_with="/home/test_user/site-artifact",
        help_playbook=True,
    ),
    Scenario(
        name="Filename timezone",
        filename="/tmp/{time_stamp}.json",
        playbook="site.yml",
        time_zone="America/Los_Angeles",
        re_match=re.compile("^/tmp/.*-0[7,8]:00"),
    ),
]


@pytest.mark.parametrize("data", test_data, ids=str)
def test_artifact_path(
    monkeypatch: pytest.MonkeyPatch,
    mocker: MockerFixture,
    caplog: pytest.LogCaptureFixture,
    data: Scenario,
):
    """Test the building of the artifact filename given a filename or playbook.

    :param monkeypatch: The monkeypatch fixture
    :param mocker: The mocker fixture
    :param caplog: The log capture fixture
    :param data: The test data
    """
    caplog.set_level(logging.DEBUG)
    monkeypatch.setenv("HOME", "/home/test_user")

    def make_dirs(*_args, **_kwargs):
        return True

    monkeypatch.setattr(os, "makedirs", make_dirs)

    def get_status(*_args, **_kwargs):
        return (0, 0)

    monkeypatch.setattr(action, "_get_status", get_status)

    mocked_write = mocker.patch(
        "ansible_navigator.actions.run.serialize_write_file",
        return_value=None,
    )

    args = deepcopy(NavigatorConfiguration)
    args.entry("playbook").value.current = data.playbook
    args.entry("help_playbook").value.current = data.help_playbook
    args.entry("time_zone").value.current = data.time_zone
    args.entry("playbook_artifact_enable").value.current = True

    save_as = args.entry("playbook_artifact_save_as")

    if data.filename:
        save_as.value.current = data.filename
    else:
        save_as.value.current = save_as.value.default

    args.post_processor.playbook(
        entry=args.entry("playbook"),
        config=args,
    )
    args.post_processor.playbook_artifact_save_as(
        entry=save_as,
        config=args,
    )

    run_action = action(args=args)
    run_action.write_artifact(filename=data.filename)

    if data.help_playbook is not True:
        opened_filename = str(mocked_write.call_args[1]["file"])
        if data.starts_with is not None:
            assert opened_filename.startswith(data.starts_with), caplog.text
        if data.re_match is not None:
            assert data.re_match.match(opened_filename), caplog.text
    else:
        mocked_write.assert_not_called()
