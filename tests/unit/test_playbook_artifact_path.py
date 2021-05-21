"""Some simple test to confirm the artifact path is correctly set
"""
import logging
import os

from copy import deepcopy
from typing import NamedTuple
from typing import Union
from unittest.mock import patch
from unittest.mock import mock_open

import pytest

from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.actions.run import Action as action


class TstData(NamedTuple):
    """the test data object"""

    name: str
    filename: Union[None, str]
    playbook: str
    expected: str
    help_playbook: bool = False


def id_from_data(value):
    """return the name from the test data object"""
    return value.name


test_data = [
    TstData("Filename absolute", "/tmp/artifact.json", "site.yml", "/tmp/artifact.json"),
    TstData(
        "Filename with .", "./artifact.json", "site.yml", f"{os.path.abspath('.')}/artifact.json"
    ),
    TstData(
        "Filename with ..", "../artifact.json", "site.yml", f"{os.path.abspath('..')}/artifact.json"
    ),
    TstData(
        "Filename with ~", "~/artifact.json", "/tmp/site.yaml", "/home/test_user/artifact.json"
    ),
    TstData("Playbook absolute", None, "/tmp/site.yaml", "/tmp/site-artifact"),
    TstData("Playbook with .", None, "./site.yaml", f"{os.path.abspath('.')}/site-artifact"),
    TstData("Playbook with ..", None, "../site.yaml", f"{os.path.abspath('..')}/site-artifact"),
    TstData("Playbook with ~", None, "~/site.yaml", "/home/test_user/site-artifact"),
    TstData("help_plabook enabled", None, "~/site.yaml", "/home/test_user/site-artifact", True),
]


@patch.dict("os.environ", {"HOME": "/home/test_user"})
@patch("os.makedirs", return_value=True)
@patch("builtins.open", new_callable=mock_open)
@patch("ansible_navigator.actions.run.Action._get_status", return_value=(0, 0))
@pytest.mark.parametrize("data", test_data, ids=id_from_data)
def test_artifact_path(_mocked_get_status, mocked_open, _mocked_makedirs, caplog, data):
    """Test the building of the artifact filename given a filename or playbook"""
    caplog.set_level(logging.DEBUG)

    args = deepcopy(NavigatorConfiguration)
    args.entry("playbook").value.current = data.playbook
    args.entry("help_playbook").value.current = data.help_playbook
    args.post_processor.playbook(entry=args.entry("playbook"), config=args)
    playbook_artifact_save_as = args.entry("playbook_artifact_save_as")
    if data.filename:
        args.entry("playbook_artifact_save_as").value.current = data.filename
    else:
        args.entry(
            "playbook_artifact_save_as"
        ).value.current = playbook_artifact_save_as.value.default
    args.entry("playbook_artifact_enable").value.current = True

    run = action(args=args)
    run.write_artifact(filename=data.filename)

    if data.help_playbook is not True:
        open_filename = mocked_open.call_args[0][0]
        assert open_filename.startswith(data.expected), caplog.text
    else:
        mocked_open.assert_not_called()
