"""action for ee-details
"""
import os
import re
import shlex

from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

from ansible_navigator.actions import get as get_action

from . import _actions as actions

from ..app import App
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction


PLAY_COLUMNS = [
    "__play_name",
    "__% completed",
]

TASK_LIST_COLUMNS = [
    "__task",
]


def filter_content_keys(obj: Dict[Any, Any]) -> Dict[Any, Any]:
    """when showing content, filter out some keys"""
    result = obj.get("res") or obj
    result = {
        k: v
        for k, v in result.items()
        if not any((k.startswith("_"), k.endswith("uuid"), k == "changed"))
    }
    return result


@actions.register
class Action(App):

    """:ee-details"""

    KEGEX = r"^(?:eed|ee\-details)?(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        super().__init__(args=args, logger_name=__name__, name="ee-details")
        self._share_directory = self._args.internals.share_directory
        self._run_action = get_action("run")

    def _generate_command(self) -> Tuple[str, List[str]]:
        playbook_path = os.path.join(self._share_directory, self._name, "site.yml")
        inventory_path = os.path.join(self._share_directory, self._name, "inventory.yml")

        args = ["run", playbook_path]
        args.extend(["--inventory", inventory_path])
        args.extend(["--container-engine", self._args.container_engine])
        args.extend(["--execution-environment", "true"])
        args.extend(["--execution-environment-image", self._args.execution_environment_image])
        args.extend(["--playbook-artifact-enable", "false"])
        args.extend(["-e", f"ee_image={self._args.execution_environment_image}"])
        shlex_joined = " ".join(shlex.quote(str(arg)) for arg in args)
        self._logger.debug(shlex_joined)
        return args, shlex_joined

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        """Handle :ee-details interactive

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("ee-details requested")
        self._prepare_to_run(app, interaction)

        colon_command = [self._name] + shlex.split(
            self._interaction.action.match.groupdict()["params"] or ""
        )
        self._update_args(colon_command)

        _args, command = self._generate_command()

        match = re.match(self._run_action.KEGEX, command)
        if not match:
            self._logger.error("Run action KEGEX failure, match was: %s", match)
            return None

        action = self._interaction.action._replace(match=match, value=command)
        interaction = self._interaction._replace(action=action)

        run_result = self._run_action(
            args=self._args,
            content_key_filter=filter_content_keys,
            play_columns=PLAY_COLUMNS,
            task_list_columns=TASK_LIST_COLUMNS,
        ).run(interaction=interaction, app=self.app)
        self._prepare_to_exit(interaction=self._interaction)
        return run_result

    def run_stdout(self):
        """Handle :ee-details stdout"""
        self._logger.debug("ee-details requested")
        args, _command = self._generate_command()
        self._update_args(args)
        self._run_action(args=self._args).run_stdout()
