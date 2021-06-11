""" :doc """

import curses
import json
import os
import shlex
import shutil

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

from ..ui_framework import CursesLinePart
from ..ui_framework import CursesLines
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

    def generate_content_heading(self, _obj: Dict, screen_w: int) -> CursesLines:
        """Generate a heading string for the doc"""
        plugin_str = f"{self._plugin_name} ({self._plugin_type})"
        empty_str = " " * (screen_w - len(plugin_str) + 1)
        heading_str = (plugin_str + empty_str).upper()

        heading = (
            (
                CursesLinePart(
                    column=0,
                    string=heading_str,
                    color=0,
                    decoration=curses.A_UNDERLINE | curses.A_BOLD,
                ),
            ),
        )

        return heading

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
            [self._name] + shlex.split(self._interaction.action.match.groupdict()["params"] or "")
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
            else:
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
            next_interaction: Interaction = interaction.ui.show(
                content_heading=self.generate_content_heading, obj=plugin_doc
            )
            if next_interaction.name != "refresh":
                break

        self._prepare_to_exit(interaction)
        return next_interaction

    def run_stdout(self) -> int:
        """Run in oldschool mode, just stdout"""
        self._plugin_name = self._args.plugin_name
        self._plugin_type = self._args.plugin_type
        self._logger.debug("doc requested in stdout mode")
        self._run_runner()
        return 1 if self._runner.status == "failed" else 0

    def _run_runner(self) -> Union[dict, None]:
        # pylint: disable=too-many-branches
        """spin up runner"""

        plugin_doc_response: Optional[Dict[Any, Any]] = None

        if isinstance(self._args.set_environment_variable, dict):
            set_envvars = {**self._args.set_environment_variable}
        else:
            set_envvars = {}

        if self._args.display_color is False or self._args.mode == "interactive":
            set_envvars["ANSIBLE_NOCOLOR"] = "1"

        kwargs = {
            "container_engine": self._args.container_engine,
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "navigator_mode": self._args.mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": set_envvars,
        }

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs.update(
                {"container_volume_mounts": self._args.execution_environment_volume_mounts}
            )

        if self._args.mode == "interactive":
            if isinstance(self._args.playbook, str):
                playbook_dir = os.path.dirname(self._args.playbook)
            else:
                playbook_dir = os.getcwd()
            kwargs.update({"host_cwd": playbook_dir})

            self._runner = DocRunner(**kwargs)

            # set the playbook directory so playbook
            # adjacent collection docs can be found
            self._logger.debug("doc playbook dir set to: %s", playbook_dir)

            plugin_doc, plugin_doc_err = self._runner.fetch_plugin_doc(
                [self._plugin_name], plugin_type=self._plugin_type, playbook_dir=playbook_dir
            )
            if plugin_doc_err:
                msg = "Error occurred while fetching doc for" " plugin {0}: '{1}'".format(
                    self._plugin_name, plugin_doc_err
                )
                self._logger.error(msg)

            plugin_doc_response = self._extract_plugin_doc(plugin_doc, plugin_doc_err)
        else:
            kwargs.update({"host_cwd": os.getcwd()})
            if self._args.execution_environment:
                ansible_doc_path = "ansible-doc"
            else:
                exec_path = shutil.which("ansible-doc")
                if exec_path is None:
                    self._logger.error("no ansible-doc command found in path")
                    return None
                ansible_doc_path = exec_path

            pass_through_arg = []
            if self._plugin_name is not C.NOT_SET:
                pass_through_arg.append(self._plugin_name)

            if self._plugin_type is not C.NOT_SET:
                pass_through_arg.extend(["-t", self._plugin_type])

            if self._args.help_doc is True:
                pass_through_arg.append("--help")

            if isinstance(self._args.cmdline, list):
                pass_through_arg.extend(self._args.cmdline)

            kwargs.update({"cmdline": pass_through_arg})

            self._runner = CommandRunner(executable_cmd=ansible_doc_path, **kwargs)
            self._runner.run()

        return plugin_doc_response

    def _extract_plugin_doc(
        self, out: Union[Dict[Any, Any], str], err: Union[Dict[Any, Any], str]
    ) -> Optional[Dict[Any, Any]]:
        # pylint: disable=too-many-branches
        plugin_doc = {}
        if self._args.execution_environment:
            error_key_name = "execution_environment_errors"
        else:
            error_key_name = "local_errors"

        if out:
            if isinstance(out, dict):
                plugin_doc = out[self._plugin_name]
            else:
                try:
                    json_loaded = json.loads(out)
                except json.JSONDecodeError as exc:
                    if self._args.mode == "interactive":
                        self._logger.info(
                            "Parsing of ansible-doc output failed for '%s'", self._plugin_name
                        )
                    self._logger.debug("json decode error: %s", str(exc))
                    self._logger.debug("tried: %s", out)
                    plugin_doc[error_key_name] = out
                else:
                    plugin_doc = json_loaded[self._plugin_name]

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
