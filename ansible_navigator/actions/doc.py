""" :doc """

import json
import os

from copy import deepcopy
from distutils.spawn import find_executable
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union
from . import _actions as actions

from ..app import App
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..configuration_subsystem import Constants as C
from ..runner.api import CommandRunner
from ..runner.api import DocRunner
from ..ui_framework import Interaction


@actions.register
class Action(App):
    """:doc"""

    # pylint:disable=too-few-public-methods

    KEGEX = r"^d(?:oc)?(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        super().__init__(args=args, logger_name=__name__, name="doc")

        self._plugin_name: Optional[str]
        self._plugin_type: Optional[str]
        self._runner: Union[CommandRunner, DocRunner]

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        # pylint: disable=too-many-branches
        """Handle :doc

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("doc requested in interactive")
        self._prepare_to_run(app, interaction)

        self._update_args(
            [self._name] + (self._interaction.action.match.groupdict()["params"] or "").split()
        )

        plugin_name_source = self._args.entry("plugin_name").value.source

        if plugin_name_source is C.USER_CLI:
            self._plugin_name = self._args.plugin_name
            self._plugin_type = self._args.plugin_type
            source = plugin_name_source.value
        elif plugin_name_source is C.NOT_SET:
            if interaction.content:
                try:
                    self._plugin_name = interaction.content.showing["task_action"]
                    self._plugin_type = self._args.entry("plugin_type").value.default
                    source = "task action"
                except (KeyError, AttributeError, TypeError):
                    self._logger.info("No plugin name found in current content")
                    return None
        elif plugin_name_source is not C.NOT_SET:
            self._plugin_name = self._args.plugin_name
            self._plugin_type = self._args.plugin_type
            source = plugin_name_source.value
        else:
            self._logger.info("No plugin provided or found, not showing content")
            self._prepare_to_exit(interaction)
            return None

        self._logger.debug("Plugin name used from %s: %s", source, self._plugin_name)
        self._logger.debug("Plugin type used from %s: %s", source, self._plugin_type)

        plugin_doc = self._run_runner()

        if not plugin_doc:
            self._prepare_to_exit(interaction)
            return None

        while True:
            app.update()
            next_interaction: Interaction = interaction.ui.show(obj=plugin_doc)
            if next_interaction.name != "refresh":
                break

        self._prepare_to_exit(interaction)
        return next_interaction

    def run_stdout(self) -> None:
        """Run in oldschool mode, just stdout"""
        self._plugin_name = self._args.plugin_name
        self._plugin_type = self._args.plugin_type
        self._logger.debug("doc requested in stdout mode")
        self._run_runner()

    def _run_runner(self) -> Union[dict, None]:
        """spin up runner"""

        plugin_doc_response: Optional[Dict[Any, Any]] = None

        if isinstance(self._args.set_environment_variable, dict):
            set_environment_variable = deepcopy(self._args.set_environment_variable)
        else:
            set_environment_variable = {}
        set_environment_variable.update({"ANSIBLE_NOCOLOR": "True"})

        kwargs = {
            "container_engine": self._args.container_engine,
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "navigator_mode": self._args.mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": set_environment_variable,
        }
        if self._args.mode == "interactive":
            if isinstance(self._args.playbook, str):
                playbook_dir = os.path.dirname(self._args.playbook)
            else:
                playbook_dir = os.getcwd()
            kwargs.update({"cwd": playbook_dir})

            self._runner = DocRunner(**kwargs)
            plugin_doc, plugin_doc_err = self._runner.fetch_plugin_doc(
                [self._plugin_name], plugin_type=self._plugin_type
            )
            if plugin_doc_err:
                msg = "Error occurred while fetching doc for" " plugin {0}: '{1}'".format(
                    self._plugin_name, plugin_doc_err
                )
                self._logger.error(msg)

            plugin_doc_response = self._extract_plugin_doc(plugin_doc, plugin_doc_err)
        else:
            kwargs.update({"cwd": os.getcwd()})
            if self._args.execution_environment:
                ansible_doc_path = "ansible-doc"
            else:
                exec_path = find_executable("ansible-doc")
                if exec_path is None:
                    self._logger.error("no ansible-doc command found in path")
                    return None
                ansible_doc_path = exec_path

            pass_through_arg = [self._plugin_name, "-t", self._plugin_type]
            if isinstance(self._args.cmdline, list):
                pass_through_arg.extend(self._args.cmdline)

            kwargs.update({"cmdline": pass_through_arg})

            self._runner = CommandRunner(executable_cmd=ansible_doc_path, **kwargs)
            self._runner.run()

        return plugin_doc_response

    def _extract_plugin_doc(
        self, out: Union[Dict[Any, Any], str], err: Union[Dict[Any, Any], str]
    ) -> Optional[Dict[Any, Any]]:
        plugin_doc = {}
        if self._args.execution_environment:
            error_key_name = "execution_environment_errors"
        else:
            error_key_name = "local_errors"

        if out:
            if isinstance(out, dict):
                plugin_doc = out
            else:
                try:
                    plugin_doc = json.loads(out)
                except json.JSONDecodeError as exc:
                    if self._args.mode == "interactive":
                        self._logger.info(
                            "Parsing of ansible-doc output failed for '%s'", self._plugin_name
                        )
                    self._logger.debug("json decode error: %s", str(exc))
                    self._logger.debug("tried: %s", out)
                    plugin_doc[error_key_name] = out

            if isinstance(err, dict):
                plugin_doc["warnings"] = err
            else:
                plugin_doc["warnings"] = err.splitlines()

        elif err:
            if isinstance(err, dict):
                plugin_doc[error_key_name] = err
            else:
                plugin_doc[error_key_name] = err.splitlines()

        return plugin_doc
