"""Test settings through to runner."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from queue import Queue
from typing import TYPE_CHECKING
from typing import Any

import pytest


if TYPE_CHECKING:
    from pytest_mock import MockerFixture

from ansible_navigator.actions.run import Action as action
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from tests.defaults import BaseScenario
from tests.defaults import id_func


@dataclass
class Scenario(BaseScenario):
    """The runner test data object."""

    # pylint: disable=too-many-instance-attributes
    name: str
    container_engine: str | None
    container_options: list[str] | None
    execution_environment_image: str | None
    execution_environment: bool | None
    inventory: list[str] | None
    playbook_artifact_enable: bool
    mode: str | None
    pass_environment_variable: list[str] | None
    set_environment_variable: dict[str, str] | None
    playbook: str | None
    container_volume_mounts: list[str] | None
    help_playbook: bool
    cmdline: list[str] | None
    private_data_dir: str | None
    rotate_artifacts: int | None
    timeout: int | None
    write_job_events: bool
    expected: dict[str, Any]

    def __str__(self) -> str:
        """Provide the test id.

        Returns:
            The test id
        """
        return self.name


TEST_QUEUE: Queue[dict[str, str]] = Queue()

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
        write_job_events=False,
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
            "write_job_events": False,
        },
    ),
]


@pytest.mark.parametrize("data", test_data, ids=id_func)
def test_runner_args(mocker: MockerFixture, data: Scenario) -> None:
    """Test the arguments passed to runner API.

    Args:
        mocker: The mocker fixture
        data: The test data
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
    args.entry("ansible_runner_write_job_events").value.current = data.write_job_events

    class TestRunnerError(Exception):
        """Test runner exception."""

    command_async = mocker.patch(
        "ansible_navigator.actions.run.CommandAsync",
        side_effect=TestRunnerError,
    )

    run = action(args=args)
    run._queue = TEST_QUEUE
    with pytest.raises(TestRunnerError):
        run._run_runner()

    command_async.assert_called_once_with(**data.expected)
