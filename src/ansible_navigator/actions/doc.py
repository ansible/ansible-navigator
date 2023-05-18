"""Doc subcommand implementation."""

from __future__ import annotations

import curses
import json
import os
import shlex
import shutil

from typing import Any

from ansible_navigator.action_base import ActionBase
from ansible_navigator.action_defs import RunStdoutReturn
from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem import Constants as C
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.runner import AnsibleDoc
from ansible_navigator.runner import Command
from ansible_navigator.ui_framework import CursesLine
from ansible_navigator.ui_framework import CursesLinePart
from ansible_navigator.ui_framework import CursesLines
from ansible_navigator.ui_framework import Interaction

from . import _actions as actions


@actions.register
class Action(ActionBase):
    """Doc subcommand implementation."""

    KEGEX = r"^d(?:oc)?(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``doc`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="doc")

        self._plugin_name: str | None = None
        self._plugin_type: str | None = None
        self._runner: Command | AnsibleDoc

    def generate_content_heading(self, _obj: dict, screen_w: int) -> CursesLines:
        """Create a heading for doc content.

        :param _obj: The content going to be shown
        :param screen_w: The current screen width
        :returns: The heading
        """
        plugin_str = f"Name: {self._plugin_name} ({self._plugin_type})"
        empty_str = " " * (screen_w - len(plugin_str) + 1)
        heading_str = (plugin_str + empty_str).capitalize()

        line_part = CursesLinePart(
            column=0,
            string=heading_str,
            color=0,
            decoration=curses.A_UNDERLINE,
        )

        return CursesLines((CursesLine((line_part,)),))

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction | None:
        """Execute the ``doc`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction` or
            :data:`None`
        """
        self._logger.debug("doc requested in interactive")
        self._prepare_to_run(app, interaction)

        colon_prompt = self._interaction.action.match.groupdict()["params"]

        # Nothing provided at colon prompt and content is showing, get the task action
        if interaction.content and not colon_prompt:
            try:
                self._plugin_name = interaction.content.showing["task_action"]
                self._plugin_type = self._args.entry("plugin_type").value.default
                source = "task action"

            except (KeyError, AttributeError, TypeError):
                self._logger.info("No plugin name found in current content")

        # Process the colon prompt and allow update args to identify missing entries
        if self._plugin_name is None:
            args_updated = self._update_args([self._name] + shlex.split(colon_prompt or ""))
            if not args_updated:
                self._prepare_to_exit(interaction)
                return None
            source = self._args.entry("plugin_name").value.source.value
            self._plugin_name = self._args.plugin_name
            self._plugin_type = self._args.plugin_type

        self._logger.debug("Plugin name used from %s: %s", source, self._plugin_name)
        self._logger.debug("Plugin type used from %s: %s", source, self._plugin_type)

        plugin_doc = self._run_runner()

        if not isinstance(plugin_doc, dict):
            self._prepare_to_exit(interaction)
            return None

        while True:
            app.update()
            next_interaction: Interaction = interaction.ui.show(
                content_heading=self.generate_content_heading,
                obj=plugin_doc,
            )
            if next_interaction.name != "refresh":
                break

        self._prepare_to_exit(interaction)
        return next_interaction

    def run_stdout(self) -> RunStdoutReturn:
        """Execute the ``doc`` request for mode stdout.

        :returns: The return code or 1. If the response from the runner invocation is None,
            indicates there is no console output to display, so assume an issue and return 1
            along with a message to review the logs.
        """
        self._plugin_name = self._args.plugin_name
        self._plugin_type = self._args.plugin_type
        self._logger.debug("doc requested in stdout mode")
        response = self._run_runner()
        if response is None:
            self._logger.error("Unexpected response: %s", response)
            return RunStdoutReturn(message="Please review the log for errors.", return_code=1)
        _out, error, return_code = response
        return RunStdoutReturn(message=error, return_code=return_code)

    def _run_runner(self) -> dict | tuple[str, str, int] | None:
        # pylint: disable=no-else-return
        """Use the runner subsystem to retrieve the configuration.

        :raises RuntimeError: When the ansible-doc command cannot be found with execution
            environment support disabled.
        :returns: For mode interactive nothing or the plugin's doc. For mode stdout the
            output, errors and return code from runner.
        """
        if isinstance(self._args.set_environment_variable, dict):
            set_env_vars = {**self._args.set_environment_variable}
        else:
            set_env_vars = {}

        if self._args.display_color is False or self._args.mode == "interactive":
            set_env_vars["ANSIBLE_NOCOLOR"] = "1"

        kwargs = {
            "container_engine": self._args.container_engine,
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "navigator_mode": self._args.mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": set_env_vars,
            "private_data_dir": self._args.ansible_runner_artifact_dir,
            "rotate_artifacts": self._args.ansible_runner_rotate_artifacts_count,
            "timeout": self._args.ansible_runner_timeout,
        }

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs.update(
                {"container_volume_mounts": self._args.execution_environment_volume_mounts},
            )

        if isinstance(self._args.container_options, list):
            kwargs.update({"container_options": self._args.container_options})

        if self._args.mode == "interactive":
            if isinstance(self._args.playbook, str):
                playbook_dir = os.path.dirname(self._args.playbook)
            else:
                playbook_dir = os.getcwd()
            kwargs.update({"host_cwd": playbook_dir})

            self._runner = AnsibleDoc(**kwargs)

            # set the playbook directory so playbook
            # adjacent collection docs can be found
            self._logger.debug("doc playbook dir set to: %s", playbook_dir)

            plugin_doc, plugin_doc_err = self._runner.fetch_plugin_doc(
                [self._plugin_name],
                plugin_type=self._plugin_type,
                playbook_dir=playbook_dir,
            )
            if plugin_doc_err:
                self._logger.error(
                    "Error occurred while fetching doc for plugin %s: '%s'",
                    self._plugin_name,
                    plugin_doc_err,
                )
            plugin_doc_response = self._extract_plugin_doc(plugin_doc, plugin_doc_err)
            return plugin_doc_response
        else:
            kwargs.update({"host_cwd": os.getcwd()})
            if self._args.execution_environment:
                ansible_doc_path = "ansible-doc"
            else:
                exec_path = shutil.which("ansible-doc")
                if exec_path is None:
                    msg = "'ansible-doc' executable not found"
                    self._logger.error(msg)
                    raise RuntimeError(msg)
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

            self._runner = Command(executable_cmd=ansible_doc_path, **kwargs)
            stdout_return = self._runner.run()
            return stdout_return

    def _extract_plugin_doc(
        self,
        out: dict[Any, Any] | str,
        err: dict[Any, Any] | str,
    ) -> dict[Any, Any] | None:
        """Extract the plugin's documentation from the runner output.

        :param out: The output from runner
        :param err: Any runner errors
        :returns: The plugin's doc or errors
        """
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
                            "Parsing of ansible-doc output failed for '%s'",
                            self._plugin_name,
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
