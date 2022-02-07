"""tests for runner.api
"""

import pytest

from ansible_navigator.runner import Command


@pytest.mark.parametrize(
    "orig_exec, orig_args, sh_c_arg",
    (
        (
            "ansible-lint",
            [],
            "exec 2>/dev/null; ansible-lint",
        ),
        (
            "ansible-lint",
            ["/tmp/my_roles/supercool/tasks/main.yml"],
            "exec 2>/dev/null; ansible-lint /tmp/my_roles/supercool/tasks/main.yml",
        ),
        (
            "ansible-lint",
            ["lintable1", "lintable2", "lintable3"],
            "exec 2>/dev/null; ansible-lint lintable1 lintable2 lintable3",
        ),
        (
            "ansible-lint",
            ["lintable1", "lint\"able'2", "lint able3"],
            "exec 2>/dev/null; ansible-lint lintable1 'lint\"able'\"'\"'2' 'lint able3'",
        ),
    ),
    ids=[
        "only executable command",
        "executable command with one argument",
        "executable command with several arguments",
        "executable command with arguments containing quotes and spaces",
    ],
)
def test_command_base_runner_wrap_sh(orig_exec, orig_args, sh_c_arg):
    # pylint: disable=protected-access
    """test CommandBaseRunner properly wraps commands with sh -c when asked."""

    # default (no sh wrap)
    runner_cmd = Command(orig_exec, cmdline=orig_args)
    runner_cmd.generate_run_command_args()
    assert runner_cmd._runner_args.get("executable_cmd") == orig_exec
    assert runner_cmd._runner_args.get("cmdline_args") == orig_args

    # explicit sh wrap
    runner_cmd = Command(orig_exec, cmdline=orig_args, wrap_sh=True)
    runner_cmd.generate_run_command_args()
    assert runner_cmd._runner_args.get("executable_cmd") == "/bin/sh"
    assert runner_cmd._runner_args.get("cmdline_args") == ["-c", sh_c_arg]
