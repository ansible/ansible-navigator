""" :doc """
import logging
import json
import os
import subprocess

from argparse import Namespace
from distutils.spawn import find_executable
from typing import Tuple
from typing import Union
from . import _actions as actions
from ..player import App
from ..ui import Interaction


@actions.register
class Action:
    """:doc"""

    # pylint:disable=too-few-public-methods

    KEGEX = r"^d(?:oc)?(\s(?P<plugin>.*))?$"

    def __init__(self):
        self._logger = logging.getLogger()
        self._app = None

    def run(self, interaction: Interaction, app: App) -> Union[Interaction, bool]:
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
                return False
        else:
            self._logger.info("no plugin provided, not showing content")
            return False

        if app.args.execution_environment:
            self._logger.debug("trying execution environment")
            plugin_doc, xform = self._try_ee(app.args, interaction.ui.xform(), plugin)
            if not plugin_doc:
                self._logger.debug("ee ansible-doc failed, trying local")
                plugin_doc, xform = self._try_local(interaction, plugin)
        else:
            self._logger.debug("trying local")
            plugin_doc, xform = self._try_local(interaction, plugin)

        if not plugin_doc:
            return False

        previous_scroll = interaction.ui.scroll()
        interaction.ui.scroll(0)
        while True:
            result = interaction.ui.show(obj=plugin_doc, xform=xform)
            app.update()
            if result.action.name != "refresh":
                break
        interaction.ui.scroll(previous_scroll)
        return result

    def _try_ee(
        self, args: Namespace, xform: str, plugin: str
    ) -> Tuple[Union[str, dict, None], Union[str, None]]:

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
                plugin_doc = json.loads(stdout)
                if plugin_doc:
                    plugin_doc = plugin_doc[list(plugin_doc.keys())[0]]
                    if stderr:
                        plugin_doc["WARNINGS"] = stderr.splitlines()
                    self._logger.debug("ee ansible-doc output %s", proc_out)
                    return plugin_doc, xform
                self._logger.debug("ee command failed, json was empty.")
                return None, None
            self._logger.debug("ee command failed, no json in response: '%s'", proc_out.stdout)
            return None, None

        except subprocess.CalledProcessError as exc:
            self._logger.debug("ee command execution failed: '%s'", str(exc))
            self._logger.debug("ee command execution failed: '%s'", exc.output)
            return None, None
        except json.JSONDecodeError as exc:
            self._logger.debug("ee command json decode failed: '%s'", str(exc))
            return None, None

    def _try_local(
        self, interaction: Interaction, plugin: str
    ) -> Tuple[Union[str, dict, None], Union[str, None]]:
        adoc_path = find_executable("ansible-doc")
        if adoc_path:
            self._logger.debug("local ansible-doc path is: %s", adoc_path)
            try:
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

                plugin_doc = json.loads(proc_out.stdout)
                if plugin_doc:
                    plugin_doc = plugin_doc[list(plugin_doc.keys())[0]]

                if proc_out.stderr:
                    plugin_doc["WARNINGS"] = proc_out.stderr.splitlines()

                xform = interaction.ui.xform()

            except subprocess.CalledProcessError as exc:
                self._logger.info(
                    "Command failed 'ansible-doc %s --json'", interaction.action.value
                )
                self._logger.debug(
                    "ansible-doc command failure for '%s' %s", interaction.action.value, str(exc)
                )
                plugin_doc = exc.output
                xform = None

            except json.JSONDecodeError as exc:
                self._logger.info(
                    "Parsing of ansible-doc output failed for '%s'", interaction.action.value
                )
                self._logger.debug("json decode error: %s", str(exc))
                self._logger.debug("tried: %s", plugin_doc.stdout)
                plugin_doc = plugin_doc.stdout
                xform = None
            return plugin_doc, xform
        self._logger.error("no ansible-doc command found in path")
        return None, None
