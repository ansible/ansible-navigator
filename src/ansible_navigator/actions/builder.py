"""Builder subcommand implementation.

Importing this module registers this subcommand in the external
global subcommand registry.
"""
from __future__ import annotations

import os
import shutil

from ansible_navigator.action_base import ActionBase
from ansible_navigator.action_defs import RunStdoutReturn
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.configuration_subsystem.definitions import Constants
from ansible_navigator.runner import Command

from . import _actions as actions


@actions.register
class Action(ActionBase):
    """Run the builder subcommand."""

    KEGEX = "^b(?:uilder)?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the action.

        :param args: The current application configuration
        """
        super().__init__(args=args, logger_name=__name__, name="builder")

    def run_stdout(self) -> RunStdoutReturn:
        """Execute the ``builder`` request for mode stdout.

        :returns: The return code or 1. If the response from the runner invocation is None,
            indicates there is no console output to display, so assume an issue and return 1
            along with a message to review the logs.
        """
        self._logger.debug("builder requested in stdout mode")
        response = self._run_runner()
        if response is None:
            self._logger.error("Unexpected response: %s", response)
            return RunStdoutReturn(message="Please review the log for errors.", return_code=1)
        _out, error, return_code = response
        return RunStdoutReturn(message=error, return_code=return_code)

    def _run_runner(self) -> tuple | None:
        """Spin up runner.

        :raises RuntimeError: When ansible-builder can not be found
        :returns: The stdout, stderr and return code from runner
        """
        ansible_builder_path = shutil.which("ansible-builder")
        if ansible_builder_path is None:
            msg = "'ansible-builder' executable not found"
            self._logger.error(msg)
            raise RuntimeError(msg)

        if isinstance(self._args.set_environment_variable, dict):
            env_vars_to_set = self._args.set_environment_variable.copy()
        elif isinstance(self._args.set_environment_variable, Constants):
            env_vars_to_set = {}
        else:
            log_message = (
                "The setting 'set_environment_variable' was neither a dictionary"
                " or Constants, please raise an issue. No environment variables will be set."
            )
            self._logger.error(
                "%s The current value was found to be '%s'",
                log_message,
                self._args.set_environment_variable,
            )
        env_vars_to_set = {}

        if self._args.display_color is False:
            env_vars_to_set["ANSIBLE_NOCOLOR"] = "1"

        if self._args.execution_environment:
            self._logger.info("For builder subcommand execution-environment is disabled")

        kwargs = {
            "execution_environment": False,
            "host_cwd": os.path.abspath(os.path.expanduser(self._args.workdir)),
            "navigator_mode": self._args.mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": env_vars_to_set,
            "timeout": self._args.ansible_runner_timeout,
        }

        pass_through_arg = []

        if isinstance(self._args.cmdline, list):
            pass_through_arg.extend(self._args.cmdline)

        if self._args.help_builder is True:
            pass_through_arg.append("--help")

        kwargs.update({"cmdline": pass_through_arg})

        command_runner = Command(executable_cmd=ansible_builder_path, **kwargs)
        return command_runner.run()
