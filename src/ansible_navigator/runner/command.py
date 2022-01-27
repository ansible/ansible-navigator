"""Herewithin lies the ability to have ansible-runner
run a command in a synchronous manner
"""
from typing import Tuple

from ansible_runner import run_command  # type: ignore[import]

from .command_base import CommandBase


class Command(CommandBase):
    """a runner wrapper"""

    def run(self) -> Tuple[str, str, int]:
        """run"""

        self.generate_run_command_args()
        out, err, ret_code = run_command(**self._runner_args)
        return out, err, ret_code
