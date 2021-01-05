""" :doc """
import logging
import json
import os
import subprocess

from argparse import Namespace
from distutils.spawn import find_executable
from typing import Union
from . import _actions as actions
from ..app_public import AppPublic
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

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        # pylint: disable=too-many-branches
        """Handle :doc

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("doc requested")
        self._app = app

        if plugin := interaction.action.match.groupdict()["plugin"]:
            self._logger.debug("plugin set by user: %s", plugin)
        elif interaction.content:
            try:
                plugin = interaction.content.showing["task action"]
                self._logger.debug("plugin derived from 'task action': %s", plugin)
            except (KeyError, AttributeError):
                self._logger.info("no plugin provided or found in content")
                return None
        else:
            self._logger.info("no plugin provided, not showing content")
            return None

        if app.args.execution_environment:
            self._logger.debug("trying execution environment")
            plugin_doc = self._try_ee(app.args, interaction, plugin)
            if isinstance(plugin_doc, str):
                plugin_doc = {"execution_environment_errors": plugin_doc.splitlines()}
                self._logger.debug("ee ansible-doc failed, trying local")
                local_plugin_doc = self._try_local(interaction, plugin)
                if isinstance(local_plugin_doc, str):
                    plugin_doc["local_errors"] = local_plugin_doc.splitlines()
                else:
                    plugin_doc = local_plugin_doc
        else:
            self._logger.debug("trying local")
            plugin_doc = self._try_local(interaction, plugin)
            if isinstance(plugin_doc, str):
                plugin_doc = {"local_errors": plugin_doc.splitlines()}

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

    def _try_ee(
        self, args: Namespace, interaction: Interaction, plugin: str
    ) -> Union[str, dict, None]:

        if "playbook" in self._app.args:
            playbook_dir = os.path.dirname(args.playbook)
        else:
            playbook_dir = os.getcwd()
        cmd = [args.container_engine, "run", "-i", "-t"]
        cmd.extend(["--env", "ANSIBLE_NOCOLOR=True"])
        cmd.extend(["-v", "{pdir}:{pdir}".format(pdir=playbook_dir)])
        cmd.extend([args.ee_image])
        cmd.extend(["ansible-doc", "--playbook-dir", playbook_dir, plugin, "--json"])

        if self._app.args.app == "doc" and self._app.args.type:
            cmd.extend(["-t", self._app.args.type])
            self._app.args.type = None

        self._logger.debug("ee command: %s", " ".join(cmd))
        try:
            proc_out = subprocess.run(
                " ".join(cmd), capture_output=True, check=True, text=True, shell=True
            )
            parts = proc_out.stdout.split("{", 1)
            stderr = parts[0]

            if len(parts) == 2:
                stdout = "{" + parts[1]
            else:
                stdout = ""

            plugin_doc = self._extract_plugin_doc(interaction, stdout, stderr)
            return plugin_doc

        except subprocess.CalledProcessError as exc:
            self._logger.debug("ee command execution failed: '%s'", str(exc))
            self._logger.debug("ee command execution failed: '%s'", exc.output)
            return None

    def _try_local(self, interaction: Interaction, plugin: str) -> Union[str, dict, None]:
        adoc_path = find_executable("ansible-doc")
        if adoc_path:
            self._logger.debug("local ansible-doc path is: %s", adoc_path)
            cmd = [adoc_path, plugin, "--json"]
            if "playbook" in self._app.args:
                cmd.extend(["--playbook-dir", os.path.dirname(self._app.args.playbook)])
            else:
                cmd.extend(["--playbook-dir", os.getcwd()])

            if self._app.args.app == "doc" and self._app.args.type:
                cmd.extend(["-t", self._app.args.type])
                self._app.args.type = None

            proc_out = subprocess.run(
                " ".join(cmd), capture_output=True, check=True, text=True, shell=True
            )
            self._logger.debug("ansible-doc output %s", proc_out)

            plugin_doc = self._extract_plugin_doc(interaction, proc_out.stdout, proc_out.stderr)
            return plugin_doc

        msg = "no ansible-doc command found in path"
        self._logger.error(msg)
        return msg

    def _extract_plugin_doc(self, interaction: Interaction, stdout: str, stderr: str):
        try:
            plugin_doc = json.loads(stdout)
            if plugin_doc:
                plugin_doc = plugin_doc[list(plugin_doc.keys())[0]]
                if stderr:
                    plugin_doc["WARNINGS"] = stderr.splitlines()
            else:
                plugin_doc = stderr

        except subprocess.CalledProcessError as exc:
            self._logger.info("Command failed 'ansible-doc %s --json'", interaction.action.value)
            self._logger.debug(
                "ansible-doc command failure for '%s' %s", interaction.action.value, str(exc)
            )
            plugin_doc = exc.output

        except json.JSONDecodeError as exc:
            self._logger.info(
                "Parsing of ansible-doc output failed for '%s'", interaction.action.value
            )
            self._logger.debug("json decode error: %s", str(exc))
            self._logger.debug("tried: %s", plugin_doc.stdout)
            plugin_doc = stdout

        return plugin_doc
