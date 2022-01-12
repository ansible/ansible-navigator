"""
This action provides ansible-lint results through ansible-navigator.
Internally, it works by using ansible-runner to execute ansible-lint (optionally
in an execution environment). When running ansible-lint, it passes
'-f codeclimate' which requests JSON output on stdout. The JSON output contains
a list of issues which we then report in the ansible-navigator UI.

We allow users to dig into an individual issue using the standard :<lineno>
commands, to learn more about the issue.

The full specification for ansible-lint's use of JSON (for the codeclimate
formatter) can be found in src/ansiblelint/formatters/__init__.py in the
ansible-lint codebase.
"""

import collections
import curses
from dataclasses import asdict, dataclass
from enum import IntEnum
from functools import total_ordering
import json
import os
import shutil
import shlex
from typing import Any, Dict, List, Optional, Tuple, Union

from . import _actions as actions
from . import run_action
from ..app import App
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..runner.command import Command
from ..steps import Step
from ..ui_framework import (
    CursesLines,
    CursesLinePart,
    Interaction,
    nonblocking_notification,
    error_notification,
)
from ..utils import abs_user_path


class Severity(IntEnum):
    info = 10
    minor = 20
    major = 30
    critical = 40
    blocker = 50

    # If ansible-lint ever gives us something we don't expect, return this.
    # In practice, we reverse-sort, so this will always be last.
    unknown = -1

    @classmethod
    def _missing_(cls, value):
        """
        If ansible-lint ever gives us something we don't expect return something
        that tells us.
        """
        return Severity.unknown


def severity_to_color(severity: Severity) -> int:
    if severity == "minor":
        return 5
    elif severity == "major":
        return 3
    elif severity in ("critical", "blocker"):
        return 1
    elif severity == "info":
        return 6
    return 0


def color_menu(colno: int, colname: str, entry: Dict[str, Any]) -> Tuple[int, int]:
    return (severity_to_color(entry["severity"]), 0)


def content_heading(obj: Dict, screen_w: int) -> Union[CursesLines, None]:
    check_name = obj["check_name"]
    check_name = check_name + (" " * (screen_w - len(check_name)))

    return (
        (
            CursesLinePart(
                column=0,
                string=abs_user_path(obj["location"]["path"]),
                color=0,
                decoration=curses.A_BOLD,
            ),
        ),
        (
            CursesLinePart(
                column=0,
                string=check_name,
                color=severity_to_color(obj["severity"]),
                decoration=curses.A_UNDERLINE,
            ),
        ),
    )


def filter_content_keys(obj: Dict[Any, Any]) -> Dict[Any, Any]:
    """when showing content, filter out some keys"""
    return {k: v for k, v in obj.items() if not k.startswith("__")}


def massage_issues(issues: List[Dict]) -> List[Dict]:
    out = []
    for issue in issues:
        issue["__message"] = issue["check_name"].split("] ", 1)[1].capitalize()
        issue["__path"] = abs_user_path(issue["location"]["path"])
        if isinstance(issue["location"]["lines"]["begin"], collections.Mapping):
            issue["__line"] = issue["location"]["lines"]["begin"]
        else:
            issue["__line"] = issue["location"]["lines"]["begin"]
        out.append(issue)
    return out


@actions.register
class Action(App):
    """:lint"""

    KEGEX = r"^lint(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        super().__init__(args=args, logger_name=__name__, name="lint")

    def _fatal(self, msg: str, rc: int = 1) -> Tuple[str, str, int]:
        self._logger.error(msg)

        if self._args.mode == "interactive":
            notification = error_notification(messages=[msg])
            self._interaction.ui.show(notification)
        else:
            raise RuntimeError(msg)

        return "", "", rc

    def _run_runner(self) -> Tuple[str, str, int]:
        """Spin up runner to run ansible-lint, either in an exec env or not."""

        kwargs = {
            "container_engine": self._args.container_engine,
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "navigator_mode": self._args.mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": self._args.set_environment_variable,
            "private_data_dir": self._args.ansible_runner_artifact_dir,
            "rotate_artifacts": self._args.ansible_runner_rotate_artifacts_count,
            "timeout": self._args.ansible_runner_timeout,
            "host_cwd": os.getcwd(),
        }

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs.update(
                {"container_volume_mounts": self._args.execution_environment_volume_mounts}
            )

        if isinstance(self._args.container_options, list):
            kwargs.update({"container_options": self._args.container_options})

        cmd_args = ["-qq", "--offline"]

        if self._args.mode == "interactive":
            cmd_args += [
                "--nocolor",
                "-f",
                "codeclimate",
            ]

        if isinstance(self._args.lint_config, str):
            cmd_args += [
                "-c",
                self._args.lint_config,
            ]

        if isinstance(self._args.lintables, str):
            # Does it actually exist?
            if not os.path.exists(self._args.lintables):
                return self._fatal(
                    "The given path `{0}` does not exist.".format(self._args.lintables)
                )
            cmd_args.append(self._args.lintables)

        kwargs["cmdline"] = cmd_args

        runner = Command(executable_cmd="ansible-lint", **kwargs)
        return runner.run()

    def run_stdout(self) -> int:
        """Run in oldschool mode, just stdout."""
        self._logger.debug("lint requested in stdout mode")
        out, err, rc = self._run_runner()
        return rc

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        """Handle :lint

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """

        self._logger.debug("lint requested")
        _, exit_messages = self._update_args(
            ["lint"] + shlex.split(interaction.action.match.groupdict()["params"] or "")
        )

        # Set up interaction
        self._prepare_to_run(app, interaction)

        # ...but then if there were config errors after parsing our args, fatal on them.
        if exit_messages:
            # Configurator injects the "Command provided: ..." message as an exit message.
            # However, for showing a fatal modal, we don't need it. So nuke it if it's there.
            if len(exit_messages) > 1 and exit_messages[0].message.startswith("Command provided: "):
                exit_messages = exit_messages[1:]
            self._fatal("; ".join(msg.message for msg in exit_messages))
            return None

        self.stdout = self._calling_app.stdout

        notification = nonblocking_notification(messages=["Linting, this may take a minute..."])
        interaction.ui.show(notification)
        out, err, rc = self._run_runner()

        # Quick sanity check, make sure we actually have a result to parse.
        if rc != 0 and "ansible-lint: No such file or directory" in out:
            installed_or_ee = (
                "in the execution environment you are using"
                if self._args.execution_environment
                else "installed"
            )
            self._fatal(
                "ansible-lint executable could not be found. Ensure 'ansible-lint' "
                f"is {installed_or_ee} and try again."
            )
            return None

        try:
            issues = json.loads(out)
        except json.JSONDecodeError as e:
            self._logger.debug("Failed to parse 'ansible-lint' JSON respnose: %s", str(e))
            self._logger.error(f"Output was: {out}")
            notification = error_notification(
                messages=[
                    "Could not parse 'ansible-lint' output.",
                ]
            )
            self._interaction.ui.show(notification)
            return None

        issues = massage_issues(issues)
        issues = sorted(issues, key=lambda i: Severity[i["severity"]], reverse=True)
        self.steps.append(self._build_main_menu(issues))

        while True:
            self.update()
            self._take_step()

            if not self.steps:
                break

            if self.steps.current.name == "quit":
                return self.steps.current

        self._prepare_to_exit(interaction)
        return None

    def _take_step(self) -> None:
        """take one step"""
        result = None
        if isinstance(self.steps.current, Interaction):
            result = run_action(self.steps.current.name, self.app, self.steps.current)
        elif isinstance(self.steps.current, Step):
            if self.steps.current.show_func:
                current_index = self.steps.current.index
                self.steps.current.show_func()
                self.steps.current.index = current_index

            if self.steps.current.type == "menu":
                result = self._interaction.ui.show(
                    obj=self.steps.current.value,
                    columns=self.steps.current.columns,
                    color_menu_item=color_menu,
                )
            elif self.steps.current.type == "content":
                result = self._interaction.ui.show(
                    obj=self.steps.current.value,
                    index=self.steps.current.index,
                    content_heading=content_heading,
                    filter_content_keys=filter_content_keys,
                )

        if result is None:
            self.steps.back_one()
        else:
            self.steps.append(result)

    def _build_main_menu(self, issues: List[Dict]):
        columns = [
            "severity",
            "__message",
            "__path",
            "__line",
        ]

        return Step(
            name="lint_result",
            columns=columns,
            tipe="menu",
            value=issues,
            select_func=lambda: self._build_lint_result(issues),
        )

    def _build_lint_result(self, issues: List[Dict]):
        return Step(
            name="singular_lint_result",
            tipe="content",
            value=issues,
            index=self.steps.current.index,
        )
