"""Unit tests for the run action.
"""
import logging
import os

from copy import deepcopy
from queue import Queue
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Union
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

from ansible_navigator.actions.run import Action as action
from ansible_navigator.configuration_subsystem import NavigatorConfiguration

TEST_QUEUE: Queue = Queue()


class ArtifactTstData(NamedTuple):
    """The artifact files test data object."""

    name: str
    filename: Union[None, str]
    playbook: str
    expected: str
    help_playbook: bool = False


def id_from_data(value):
    """Return the name from the test data object."""
    return f" {value.name} "


artifact_test_data = [
    ArtifactTstData("Filename absolute", "/tmp/artifact.json", "site.yml", "/tmp/artifact.json"),
    ArtifactTstData(
        "Filename with .", "./artifact.json", "site.yml", f"{os.path.abspath('.')}/artifact.json"
    ),
    ArtifactTstData(
        "Filename with ..", "../artifact.json", "site.yml", f"{os.path.abspath('..')}/artifact.json"
    ),
    ArtifactTstData(
        "Filename with ~", "~/artifact.json", "/tmp/site.yaml", "/home/test_user/artifact.json"
    ),
    ArtifactTstData("Playbook absolute", None, "/tmp/site.yaml", "/tmp/site-artifact"),
    ArtifactTstData(
        "Playbook with .", None, "./site.yaml", f"{os.path.abspath('.')}/site-artifact"
    ),
    ArtifactTstData(
        "Playbook with ..", None, "../site.yaml", f"{os.path.abspath('..')}/site-artifact"
    ),
    ArtifactTstData("Playbook with ~", None, "~/site.yaml", "/home/test_user/site-artifact"),
    ArtifactTstData(
        "help_plabook enabled", None, "~/site.yaml", "/home/test_user/site-artifact", True
    ),
]


@patch.dict("os.environ", {"HOME": "/home/test_user"})
@patch("os.makedirs", return_value=True)
@patch("builtins.open", new_callable=mock_open)
@patch("ansible_navigator.actions.run.Action._get_status", return_value=(0, 0))
@pytest.mark.parametrize("data", artifact_test_data, ids=id_from_data)
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


class RunRunnerTstData(NamedTuple):
    """the run runner test data object"""

    name: str
    container_engine: Optional[str]
    container_options: Optional[List]
    execution_environment_image: Optional[str]
    execution_environment: Optional[bool]
    inventory: Optional[List]
    playbook_artifact_enable: bool
    mode: Optional[str]
    pass_environment_variable: Optional[List]
    set_environment_variable: Optional[Dict]
    playbook: Optional[str]
    container_volume_mounts: Optional[List]
    help_playbook: bool
    cmdline: Optional[List]
    private_data_dir: Optional[str]
    rotate_artifacts: Optional[int]
    timeout: Optional[int]
    expected: Dict


runner_test_data = [
    RunRunnerTstData(
        "Validate args passed to runner API",
        "docker",
        ["--net=host"],
        "quay.io/ansible/network-ee:latest",
        True,
        ["/test1/inv1", "/test2/inv2"],
        False,
        "stdout",
        ["passenv1", "passenv2"],
        {"setvar1": "env1", "setvar2": "env2"},
        "~/site.yaml",
        ["/home/onhost/vol1:/home/oncontainer/vol1:Z", "~/vol2:/home/user/vol2"],
        True,
        ["--tags", "test"],
        "/tmp/test1",
        10,
        200,
        {
            "executable_cmd": "ansible-playbook",
            "queue": TEST_QUEUE,
            "container_engine": "docker",
            "container_options": ["--net=host"],
            "execution_environment_image": "quay.io/ansible/network-ee:latest",
            "execution_environment": True,
            "inventory": ["/test1/inv1", "/test2/inv2"],
            "navigator_mode": "stdout",
            "pass_environment_variable": ["passenv1", "passenv2"],
            "set_environment_variable": {"setvar1": "env1", "setvar2": "env2"},
            "playbook": "~/site.yaml",
            "container_volume_mounts": [
                "/home/onhost/vol1:/home/oncontainer/vol1:Z",
                "~/vol2:/home/user/vol2",
            ],
            "cmdline": ["--help", "--tags", "test"],
            "host_cwd": os.getcwd(),
            "private_data_dir": "/tmp/test1",
            "rotate_artifacts": 10,
            "timeout": 200,
        },
    ),
]


@patch("ansible_navigator.actions.run.CommandAsync")
@pytest.mark.parametrize("data", runner_test_data, ids=id_from_data)
def test_runner_args(_mocked_command_runner, caplog, data):
    """Test the arguments passed to runner API"""
    caplog.set_level(logging.DEBUG)

    args = deepcopy(NavigatorConfiguration)
    args.entry("container_engine").value.current = data.container_engine
    args.entry("container_options").value.current = data.container_options
    args.entry("execution_environment_image").value.current = data.execution_environment_image
    args.entry("execution_environment").value.current = data.execution_environment
    args.entry("inventory").value.current = data.inventory
    args.entry("playbook_artifact_enable").value.current = data.playbook_artifact_enable
    args.entry("mode").value.current = data.mode
    args.entry("pass_environment_variable").value.current = data.pass_environment_variable
    args.entry("set_environment_variable").value.current = data.set_environment_variable
    args.entry("playbook").value.current = data.playbook
    args.entry("execution_environment_volume_mounts").value.current = data.container_volume_mounts
    args.entry("help_playbook").value.current = data.help_playbook
    args.entry("cmdline").value.current = data.cmdline
    args.entry("ansible_runner_artifact_dir").value.current = data.private_data_dir
    args.entry("ansible_runner_rotate_artifacts_count").value.current = data.rotate_artifacts
    args.entry("ansible_runner_timeout").value.current = data.timeout

    run = action(args=args)
    run._queue = TEST_QUEUE  # pylint: disable=protected-access
    run._run_runner()  # pylint: disable=protected-access

    _runner_args_passed = _mocked_command_runner.call_args[1]
    assert _runner_args_passed == data.expected
    _mocked_command_runner.assert_called_once()
