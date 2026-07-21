"""Tests for stdout-mode run cancellation behavior."""

from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace

from ansible_navigator.actions.run import Action
from ansible_navigator.configuration_subsystem import NavigatorConfiguration


def test_run_stdout_requests_runner_cancellation_on_keyboard_interrupt(mocker) -> None:
    args = deepcopy(NavigatorConfiguration)
    args.entry("app").value.current = "run"
    args.entry("mode").value.current = "stdout"
    args.entry("playbook_artifact_enable").value.current = False

    run = Action(args=args)

    fake_runner = SimpleNamespace(
        finished=False,
        cancelled=False,
        ansible_runner_instance=SimpleNamespace(rc=None),
    )

    def fake_run_runner() -> None:
        run.runner = fake_runner

    def fake_sleep(_seconds: float) -> None:
        if fake_runner.cancelled:
            fake_runner.finished = True

    run._run_runner = fake_run_runner  # type: ignore[method-assign]
    run._dequeue = mocker.Mock(side_effect=[KeyboardInterrupt, None])
    mocker.patch("ansible_navigator.actions.run.time.sleep", side_effect=fake_sleep)

    result = run.run_stdout()

    assert fake_runner.cancelled is True
    assert fake_runner.finished is True
    assert result.return_code == 1
