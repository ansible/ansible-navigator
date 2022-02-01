"""Run the builder subcommand."""
import os
import shlex
import shutil

from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from ..app import App
from ..configuration_subsystem import ApplicationConfiguration
from ..configuration_subsystem.definitions import Constants
from ..runner import Command
from . import _actions as actions


@actions.register
class Action(App):
    """Run the :exec subcommand."""

    # pylint: disable=too-few-public-methods

    KEGEX = "^e(?:xec)?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the action.

        :param args: The current application configuration.
        """
        super().__init__(args=args, logger_name=__name__, name="exec")
        self._runner: Command

    def run_stdout(self) -> Union[None, int]:
        """Run in mode stdout.

        :returns: The return code or None
        """
        self._logger.debug("builder requested in stdout mode")
        response = self._run_runner()
        if response:
            _, _, ret_code = response
            return ret_code
        return None

    def _run_runner(self) -> Optional[Tuple]:
        """Spin up runner.

        :return: The stdout, stderr and return code from runner
        """
        if isinstance(self._args.set_environment_variable, dict):
            envvars_to_set = self._args.set_environment_variable.copy()
        elif isinstance(self._args.set_environment_variable, Constants):
            envvars_to_set = {}
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
        envvars_to_set = {}

        if self._args.display_color is False:
            envvars_to_set["ANSIBLE_NOCOLOR"] = "1"

        if self._args.execution_environment:
            self._logger.info("For builder subcommand execution-environment is disabled")

        kwargs = {
            "execution_environment": False,
            "host_cwd": os.path.abspath(os.path.expanduser(self._args.workdir)),
            "navigator_mode": self._args.mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": envvars_to_set,
            "timeout": self._args.ansible_runner_timeout,
        }

        ansible_builder_path = shutil.which("ansible-builder")
        if ansible_builder_path is None:
            msg = "'ansible-builder' executable not found"
            self._logger.error(msg)
            raise RuntimeError(msg)

        pass_through_arg = []

        if self._args.help_builder is True:
            pass_through_arg.append("--help")

        if isinstance(self._args.cmdline, list):
            pass_through_arg.extend(self._args.cmdline)

        kwargs.update({"cmdline": pass_through_arg})

        self._runner = Command(executable_cmd=ansible_builder_path, **kwargs)
        return self._runner.run()
