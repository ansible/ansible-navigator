"""Herein lies the base class for running commands using ansible-runner.

All attributes common to a subprocess or async command are defined here.
"""

from __future__ import annotations

import sys

from .base import Base


class CommandBase(Base):
    """Base class for runner command interaction."""

    def __init__(
        self,
        executable_cmd: str,
        cmdline: list | None = None,
        playbook: str | None = None,
        inventory: list | None = None,
        **kwargs,
    ):
        """Handle common arguments of ``run_command`` interface for ``ansible-runner``.

        :param executable_cmd: The command to be invoked
        :param cmdline: A list of arguments to be passed to the executable command
        :param playbook: The playbook file name to run
        :param inventory: List of path to the inventory files
        :param kwargs: The arguments for the runner call
        """
        self._executable_cmd = executable_cmd
        self._cmdline: list[str] = cmdline if isinstance(cmdline, list) else []
        self._playbook = playbook
        self._inventory: list[str] = inventory if isinstance(inventory, list) else []
        super().__init__(**kwargs)

    def generate_run_command_args(self) -> None:
        """Generate arguments required to be passed to ansible-runner."""
        if self._playbook:
            self._cmdline.insert(0, self._playbook)

        for inv in self._inventory:
            self._cmdline.extend(["-i", inv])

        self._runner_args["executable_cmd"] = self._executable_cmd
        self._runner_args["cmdline_args"] = self._cmdline

        if self._navigator_mode == "stdout":
            self._runner_args.update(
                {"input_fd": sys.stdin, "output_fd": sys.stdout, "error_fd": sys.stderr},
            )

        for key, value in self._runner_args.items():
            self._logger.debug("Runner arg: %s:%s", key, value)
