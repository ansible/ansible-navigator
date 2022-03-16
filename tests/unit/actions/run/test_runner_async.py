"""Test settings through to runner."""

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from queue import Queue
from typing import Dict
from typing import List
from typing import Optional

import pytest

from pytest_mock import MockerFixture

from ansible_navigator.actions.run import Action as action
from ansible_navigator.configuration_subsystem import NavigatorConfiguration


@dataclass
class Scenario:
    """The runner test data object."""

    # pylint: disable=too-many-instance-attributes
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

    def __str__(self):
        """Provide the test id.

        :returns: The test id
        """
        return self.name


TEST_QUEUE: Queue = Queue()

test_data = [
    Scenario(
        name="Validate args passed to runner API",
        container_engine="docker",
        container_options=["--net=host"],
        execution_environment_image="quay.io/ansible/network-ee:latest",
        execution_environment=True,
        inventory=["/test1/inv1", "/test2/inv2"],
        playbook_artifact_enable=False,
        mode="stdout",
        pass_environment_variable=["pass_env1", "pass_env2"],
        set_environment_variable={"setvar1": "env1", "setvar2": "env2"},
        playbook="~/site.yaml",
        container_volume_mounts=[
            "/home/on_host/vol1:/home/in_container/vol1:Z",
            "~/vol2:/home/user/vol2",
        ],
        help_playbook=True,
        cmdline=["--tags", "test"],
        private_data_dir="/tmp/test1",
        rotate_artifacts=10,
        timeout=200,
        expected={
            "executable_cmd": "ansible-playbook",
            "queue": TEST_QUEUE,
            "container_engine": "docker",
            "container_options": ["--net=host"],
            "execution_environment_image": "quay.io/ansible/network-ee:latest",
            "execution_environment": True,
            "inventory": ["/test1/inv1", "/test2/inv2"],
            "navigator_mode": "stdout",
            "pass_environment_variable": ["pass_env1", "pass_env2"],
            "set_environment_variable": {"setvar1": "env1", "setvar2": "env2"},
            "playbook": "~/site.yaml",
            "container_volume_mounts": [
                "/home/on_host/vol1:/home/in_container/vol1:Z",
                "~/vol2:/home/user/vol2",
            ],
            "cmdline": ["--help", "--tags", "test"],
            "host_cwd": str(Path.cwd()),
            "private_data_dir": "/tmp/test1",
            "rotate_artifacts": 10,
            "timeout": 200,
        },
    ),
]


@pytest.mark.parametrize("data", test_data, ids=str)
def test_runner_args(mocker: MockerFixture, data: Scenario):
    """Test the arguments passed to runner API.

    :param mocker: The mocker fixture
    :param data: The test data
    """
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

    TestRunnerException = Exception
    command_async = mocker.patch(
        "ansible_navigator.actions.run.CommandAsync",
        side_effect=TestRunnerException,
    )

    run = action(args=args)
    run._queue = TEST_QUEUE  # pylint: disable=protected-access
    with pytest.raises(TestRunnerException):
        run._run_runner()  # pylint: disable=protected-access

    command_async.assert_called_once_with(**data.expected)
