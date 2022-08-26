"""Herein lies the ability to have ansible-runner run a command in a synchronous manner."""
from __future__ import annotations

from ansible_runner import run_command

from .command_base import CommandBase


class Command(CommandBase):
    """A runner wrapper."""

    def run(self) -> tuple[str, str, int]:
        """Run command.

        :returns: Output, error, and error code
        """
        self.generate_run_command_args()
        out, err, ret_code = run_command(**self._runner_args)
        return out, err, ret_code
