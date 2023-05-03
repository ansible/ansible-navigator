"""Run the :exec subcommand."""
from __future__ import annotations

import logging
import os
import shlex

from typing import Optional

from ansible_navigator.action_base import ActionBase
from ansible_navigator.action_defs import RunStdoutReturn
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.configuration_subsystem.definitions import Constants
from ansible_navigator.runner import Command

from . import _actions as actions


GeneratedCommand = tuple[str, Optional[list[str]]]

logger = logging.getLogger(__name__)


def _generate_command(
    exec_command: str,
    exec_shell: bool,
    extra_args: Constants | list[str],
    exec_command_is_default: bool,
) -> GeneratedCommand:
    """Generate the command and args.

    :param exec_command: The command to run
    :param exec_shell: Should the command be wrapped in a shell
    :param extra_args: Any unknown or extra arguments passed on the command line
    :param exec_command_is_default: If the exec_command is set to its default value
    :returns: The command and any pass through arguments
    """
    logger.debug("exec_command: %s", exec_command)
    logger.debug("exec_shell: %s", exec_shell)
    logger.debug("extra_args: %s", extra_args)
    if exec_shell:
        command = "/bin/bash"
        # Determine if any extra args were picked up
        _extra_args = []
        if not exec_command_is_default:
            _extra_args.append(exec_command)
        if isinstance(extra_args, list):
            _extra_args.extend(extra_args)
        if _extra_args:
            pass_command = " ".join(_extra_args)
            pass_through_args = ["-c", pass_command]
        else:
            pass_through_args = []

    else:
        if exec_command_is_default and isinstance(extra_args, list):
            command, pass_through_args = extra_args[0], extra_args[1:]
        else:
            parts = shlex.split(exec_command)
            command = parts[0]
            if len(parts) == 1 and isinstance(extra_args, list):
                # Use the extra arguments
                pass_through_args = extra_args
            else:
                # Use the leftovers or an empty list
                pass_through_args = parts[1:]
    logger.debug("runner command: %s", command)
    logger.debug("runner passthrough: %s", pass_through_args)
    return (command, pass_through_args)


@actions.register
class Action(ActionBase):
    """Run the :exec subcommand."""

    KEGEX = "^e(?:xec)?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:exec`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="exec")

    def run_stdout(self) -> RunStdoutReturn:
        """Execute the ``exec`` request for mode stdout.

        :returns: The return code or 1. If the response from the runner invocation is None,
            indicates there is no console output to display, so assume an issue and return 1
            along with a message to review the logs.
        """
        self._logger.debug("exec requested in stdout mode")
        response = self._run_runner()
        if response is None:
            self._logger.error("Unexpected response: %s", response)
            return RunStdoutReturn(message="Please review the log for errors.", return_code=1)
        _out, error, return_code = response
        return RunStdoutReturn(message=error, return_code=return_code)

    def _run_runner(self) -> tuple | None:
        """Spin up runner.

        :returns: The stdout, stderr and return code from runner
        """
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

        kwargs = {
            "container_engine": self._args.container_engine,
            "host_cwd": os.getcwd(),
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "navigator_mode": self._args.mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": env_vars_to_set,
            "timeout": self._args.ansible_runner_timeout,
        }

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs["container_volume_mounts"] = self._args.execution_environment_volume_mounts

        if isinstance(self._args.container_options, list):
            kwargs["container_options"] = self._args.container_options

        command, pass_through_args = _generate_command(
            exec_command=self._args.exec_command,
            exec_shell=self._args.exec_shell,
            extra_args=self._args.cmdline,
            exec_command_is_default=self._args.entry("exec_command").value.source
            is Constants.DEFAULT_CFG,
        )
        if isinstance(pass_through_args, list):
            kwargs["cmdline"] = pass_through_args

        runner = Command(executable_cmd=command, **kwargs)
        return runner.run()
