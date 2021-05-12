"""action for ee-details
"""
import os
import re
import shlex

from distutils.spawn import find_executable
from typing import Any
from typing import Dict
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

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        """Handle :ee-details

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("ee-details requested")
        self._prepare_to_run(app, interaction)

        playbook_path = os.path.join(self._share_directory, self._name, "site.yml")

        command = [self._name] + shlex.split(
            self._interaction.action.match.groupdict()["params"] or ""
        )
        self._update_args(command)

        errors = []
        if not isinstance(self._args.container_engine, str):
            errors.append("A container-engine is required for execution environment details")

        if not isinstance(self._args.execution_environment_image, str):
            errors.append(
                "An execution-environment-image is required for execution environment details"
            )

        if not find_executable(self._args.container_engine):
            errors.append(
                f"The specified container engine '{self._args.container_engine}' could not be found"
            )

        if errors:
            for error in errors:
                self._logger.error(error)
                return None

        run_action = get_action("run")

        new_command = f"run {playbook_path}"
        new_command += f" --container-engine {self._args.container_engine}"
        new_command += " --execution-environment True"
        new_command += f" --execution-environment-image {self._args.execution_environment_image}"
        new_command += " --playbook-artifact-enable False"
        new_command += f" -e ee_image={self._args.execution_environment_image}"

        action = self._interaction.action._replace(
            match=re.match(run_action.KEGEX, new_command), value=new_command
        )
        interaction = self._interaction._replace(action=action)

        run_result = run_action(
            args=self._args,
            content_key_filter=filter_content_keys,
            play_columns=PLAY_COLUMNS,
            task_list_columns=TASK_LIST_COLUMNS,
        ).run(interaction=interaction, app=self.app)
        self._prepare_to_exit(interaction=self._interaction)
        return run_result
