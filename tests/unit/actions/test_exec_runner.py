"""Unit tests for exec action runner invocation."""

from copy import deepcopy

from ansible_navigator.actions.exec import Action
from ansible_navigator.configuration_subsystem import NavigatorConfiguration


def test_exec_runner_uses_container_engine_container(mocker) -> None:
    args = deepcopy(NavigatorConfiguration)
    args.entry("container_engine").value.current = "container"
    args.entry("execution_environment").value.current = True
    args.entry("execution_environment_image").value.current = "ghcr.io/example/demo:latest"
    args.entry("mode").value.current = "stdout"
    args.entry("exec_command").value.current = "echo hello"
    args.entry("exec_shell").value.current = False
    args.entry("cmdline").value.current = None

    command = mocker.patch("ansible_navigator.actions.exec.Command")
    command.return_value.run.return_value = ("hello\n", "", 0)

    action = Action(args=args)
    result = action._run_runner()

    assert result == ("hello\n", "", 0)
    command.assert_called_once()
    assert command.call_args.kwargs["container_engine"] == "container"
    assert command.call_args.kwargs["execution_environment"] is True
    assert command.call_args.kwargs["execution_environment_image"] == "ghcr.io/example/demo:latest"
