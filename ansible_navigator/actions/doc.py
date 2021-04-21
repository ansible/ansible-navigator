""" :doc """
import logging
import json
import os

from distutils.spawn import find_executable
from typing import Union
from . import _actions as actions
from ..app_public import AppPublic
from ..runner.api import CommandRunner
from ..runner.api import DocRunner
from ..ui_framework import Interaction


@actions.register
class Action:
    """:doc"""

    # pylint:disable=too-few-public-methods

    KEGEX = r"^d(?:oc)?(\s(?P<plugin>.*))?$"

    def __init__(self, args):
        self._args = args
        self._logger = logging.getLogger(__name__)
        self._app = None
        self._plugin_name = None
        self._interaction_value = None

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        # pylint: disable=too-many-branches
        """Handle :doc

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("doc requested in interactive")
        self._app = app

        self._plugin_name = interaction.action.match.groupdict()["plugin"]
        if self._plugin_name:
            self._logger.debug("plugin set by user: %s", self._plugin_name)
        elif interaction.content:
            try:
                plugin = interaction.content.showing["task_action"]
                self._logger.debug("plugin derived from 'task_action': %s", plugin)
            except (KeyError, AttributeError, TypeError):
                self._logger.info("no plugin provided or found in content")
                return None
        else:
            self._logger.info("no plugin provided, not showing content")
            return None

        self._interaction_value = interaction.action.value
        plugin_doc = self._run_runner()

        if not plugin_doc:
            return None

        previous_scroll = interaction.ui.scroll()
        interaction.ui.scroll(0)
        while True:
            app.update()
            next_interaction: Interaction = interaction.ui.show(obj=plugin_doc)
            if next_interaction.name != "refresh":
                break
        interaction.ui.scroll(previous_scroll)
        return next_interaction

    def run_stdout(self) -> None:
        """Run in oldschool mode, just stdout"""
        self._logger.debug("doc requested in stdout mode")
        self._run_runner()

    def _run_runner(self) -> Union[dict, None]:
        """ spin up runner """

        plugin_type = None
        plugin_doc = None
        set_environment_variable = self._args.set_environment_variable.copy()
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
            if "playbook" in self._app.args:
                playbook_dir = os.path.dirname(self._args.playbook)
            else:
                playbook_dir = os.getcwd()
            kwargs.update({"cwd": playbook_dir})

            if self._app.args.app == "doc" and self._app.args.type:
                plugin_type = self._app.args.type

            _runner = DocRunner(**kwargs)
            plugin_doc, plugin_doc_err = _runner.fetch_plugin_doc(
                [self._plugin_name], plugin_type=plugin_type
            )
            if plugin_doc_err:
                msg = "Error occurred while fetching doc for" " plugin {0}: '{1}'".format(
                    self._plugin_name, plugin_doc_err
                )
                self._logger.error(msg)

            plugin_doc = self._extract_plugin_doc(plugin_doc, plugin_doc_err)
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

            pass_through_arg = self._args.cmdline.copy()
            pass_through_arg.append(self._args.value)

            if "type" in self._args and self._args.type:
                plugin_type = self._args.type

            if plugin_type:
                pass_through_arg.extend(["-t", plugin_type])

            kwargs.update({"cmdline": pass_through_arg})

            _runner = CommandRunner(executable_cmd=ansible_doc_path, **kwargs)
            _runner.run()

        return plugin_doc

    def _extract_plugin_doc(self, out: str, err: str):
        plugin_doc = {}
        if self._app.args.execution_environment:
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
                            "Parsing of ansible-doc output failed for '%s'", self._interaction_value
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
