"""Unit tests for diagnostics collectors."""

from copy import deepcopy

from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.diagnostics import DiagnosticsCollector


def test_container_engines_includes_apple_container(mocker) -> None:
    args = deepcopy(NavigatorConfiguration)
    args.entry("container_engine").value.current = "container"

    def fake_run_single_process(commands):
        for command in commands:
            command.return_code = 0
            command.stdout = f"{command.identity} version"
            command.stderr = ""
        return commands

    mocker.patch(
        "ansible_navigator.diagnostics.CommandRunner.run_single_process",
        side_effect=fake_run_single_process,
    )

    collector = DiagnosticsCollector(args=args, messages=[], exit_messages=[])
    result = collector._container_engines()

    assert "container" in result
    assert result["container"]["selected"] is True
    assert result["container"]["return_code"] == 0
