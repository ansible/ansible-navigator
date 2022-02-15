"""Run the :exec subcommand."""
import os
import shlex

from typing import List
from typing import Optional
from typing import Tuple

from ..action_base import ActionBase
from ..action_defs import RunStdoutReturn
from ..configuration_subsystem import ApplicationConfiguration
from ..configuration_subsystem.definitions import Constants
from ..runner import Command
from . import _actions as actions


GeneratedCommand = Tuple[str, Optional[List[str]]]


def _generate_command(exec_command: str, exec_shell: bool) -> GeneratedCommand:
    """Generate the command and args.

    :param exec_command: The command to run
    :param exec_shell: Should the command be wrapped in a shell
    :returns: The command and any pass through arguments
    """
    pass_through_args = None
    if exec_shell and exec_command:
        command = "/bin/bash"
        pass_through_args = ["-c", exec_command]
    else:
        parts = shlex.split(exec_command)
        command = parts[0]
        if len(parts) > 1:
            pass_through_args = parts[1:]
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

    def _run_runner(self) -> Optional[Tuple]:
        """Spin up runner.

        :return: The stdout, stderr and return code from runner
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
        )
        if isinstance(pass_through_args, list):
            kwargs["cmdline"] = pass_through_args

        runner = Command(executable_cmd=command, **kwargs)
        return runner.run()
