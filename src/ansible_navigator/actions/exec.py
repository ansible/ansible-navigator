""" :exec """
import os

from typing import Optional
from typing import Tuple
from typing import Union

from . import _actions as actions
from ..app import App
from ..app_public import AppPublic
from ..runner.api import CommandRunner
from ..ui_framework import warning_notification
from ..ui_framework import Interaction


@actions.register
class Action(App):
    """:exec"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^e(?:xec)?$"

    def __init__(self, args):
        super().__init__(args=args, logger_name=__name__, name="exec")

    @staticmethod
    def no_interactive_mode(interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        # pylint: disable=unused-argument
        """Warm the user interactive mode is not supported"""
        warning = warning_notification(
            messages=[
                "The 'exec' subcommand is not available while using interactive mode.",
                "[HINT] Start an additional instance of ansible-navigator"
                " in a new terminal with mode 'stdout'.",
                "       e.g. 'ansible-navigator exec --mode stdout",
            ]
        )
        interaction.ui.show(warning)

    def run_stdout(self) -> Union[None, int]:
        """Run in mode stdout"""
        self._logger.debug("exec requested in stdout mode")
        response = self._run_runner()
        if response:
            _, _, ret_code = response
            return ret_code
        return None

    def _run_runner(self) -> Optional[Tuple]:
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        """spin up runner"""

        if isinstance(self._args.set_environment_variable, dict):
            set_envvars = {**self._args.set_environment_variable}
        else:
            set_envvars = {}

        if self._args.display_color is False:
            set_envvars["ANSIBLE_NOCOLOR"] = "1"

        kwargs = {
            "container_engine": self._args.container_engine,
            "host_cwd": os.getcwd(),
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "navigator_mode": self._args.mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": set_envvars,
            "timeout": self._args.ansible_runner_timeout,
        }

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs["container_volume_mounts"] = self._args.execution_environment_volume_mounts

        if isinstance(self._args.container_options, list):
            kwargs["container_options"] = self._args.container_options

        if self._args.exec_shell and self._args.exec_command:
            command = "/bin/bash"
            pass_through_args = ["-c", self._args.exec_command]
            kwargs.update({"cmdline": pass_through_args})
        else:
            command = self._args.exec_command

        runner = CommandRunner(executable_cmd=command, **kwargs)
        runner_return = runner.run()
        return runner_return
