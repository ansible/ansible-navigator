"""
This action provides ansible-lint results through ansible-navigator.
Internally, it works by using ansible-runner to execute ansible-lint (optionally
in an execution environment). When running ansible-lint, it passes
``-f codeclimate`` which requests JSON output on stdout. The JSON output contains
a list of issues which we then report in the ansible-navigator UI.

We allow users to dig into an individual issue using the standard :<lineno>
commands, to learn more about the issue.

The full specification for ansible-lint's use of JSON (for the codeclimate
formatter) can be found in src/ansiblelint/formatters/__init__.py in the
ansible-lint codebase.
"""

import curses
import json
import os
import shlex

from collections.abc import Mapping
from enum import IntEnum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from ..action_base import ActionBase
from ..action_defs import RunStdoutReturn
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..runner.command import Command
from ..steps import Step
from ..ui_framework import CursesLine
from ..ui_framework import CursesLinePart
from ..ui_framework import CursesLines
from ..ui_framework import Interaction
from ..ui_framework import error_notification
from ..ui_framework import nonblocking_notification
from ..ui_framework import success_notification
from ..utils.functions import abs_user_path
from . import _actions as actions
from . import run_action


class Severity(IntEnum):
    """
    A mapping from ansible-lint severity to an integer represented internally.
    Primarily used for sorting.
    """

    INFO = 10
    MINOR = 20
    MAJOR = 30
    CRITICAL = 40
    BLOCKER = 50

    # If ansible-lint ever gives us something we don't expect, return this.
    # In practice, we reverse-sort, so this will always be last.
    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        """
        If ansible-lint ever gives us something we don't expect return something
        that tells us.
        """
        return Severity.UNKNOWN


def severity_to_color(severity: str) -> int:
    """Convert severity to curses colors."""
    if severity == "minor":
        return 5
    if severity == "major":
        return 3
    if severity in ("critical", "blocker"):
        return 1
    if severity == "info":
        return 6
    return 0


def color_menu(colno: int, colname: str, entry: Dict[str, Any]) -> Tuple[int, int]:
    # pylint: disable=unused-argument
    """Color the menu."""
    return (severity_to_color(entry["severity"]), 0)


def content_heading(obj: Dict, screen_w: int) -> CursesLines:
    """Generate the content heading."""
    check_name = obj["check_name"]
    check_name = check_name + (" " * (screen_w - len(check_name)))
    path_line = f"PATH: {abs_user_path(obj['location']['path'])}"
    check_name_line = f"MESSAGE: {check_name}"

    return CursesLines(
        (
            CursesLine(
                (
                    CursesLinePart(
                        column=0,
                        string=path_line,
                        color=0,
                        decoration=curses.A_BOLD,
                    ),
                ),
            ),
            CursesLine(
                (
                    CursesLinePart(
                        column=0,
                        string=check_name_line,
                        color=severity_to_color(obj["severity"]),
                        decoration=curses.A_UNDERLINE,
                    ),
                ),
            ),
        ),
    )


def filter_content_keys(obj: Dict[Any, Any]) -> Dict[Any, Any]:
    """when showing content, filter out some keys"""
    ignored_keys = ("fingerprint",)
    return {k: v for k, v in obj.items() if not k.startswith("__") and k not in ignored_keys}


def massage_issue(issue: Dict) -> Dict:
    """Massage an issue by injecting some useful keys with strings for rendering."""
    massaged = issue.copy()
    massaged["__message"] = issue["check_name"].split("] ", 1)[1].capitalize()
    massaged["__path"] = abs_user_path(issue["location"]["path"])
    if isinstance(issue["location"]["lines"]["begin"], Mapping):
        massaged["__line"] = issue["location"]["lines"]["begin"]["line"]
    else:
        massaged["__line"] = issue["location"]["lines"]["begin"]
    massaged["issue_path"] = f"{massaged['__path']}:{massaged['__line']}"
    return massaged


@actions.register
class Action(ActionBase):
    """:lint"""

    KEGEX = r"^lint(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        self._issues: List[Dict[str, Any]] = []
        super().__init__(args=args, logger_name=__name__, name="lint")

    @property
    def is_interactive(self):
        """are we interactive?"""
        return self._args.mode == "interactive"

    def _fatal(self, msg: str) -> None:
        self._logger.error(msg)

        if self.is_interactive:
            notification = error_notification(messages=[msg])
            self._interaction.ui.show_form(notification)
        else:
            raise RuntimeError(msg)

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
            kwargs["container_volume_mounts"] = self._args.execution_environment_volume_mounts

        if isinstance(self._args.container_options, list):
            kwargs["container_options"] = self._args.container_options

        cmd_args = ["-qq", "--offline"]

        if self.is_interactive:
            cmd_args += [
                "--nocolor",
                "-f",
                "codeclimate",
            ]
        elif not self._args.display_color:
            cmd_args.append("--nocolor")

        if isinstance(self._args.lint_config, str):
            cmd_args += [
                "-c",
                self._args.lint_config,
            ]

        if isinstance(self._args.lintables, str):
            # Does it actually exist?
            if not os.path.exists(self._args.lintables):
                self._fatal(f"The given path `{self._args.lintables}` does not exist.")
                return "", "", 1
            cmd_args.append(self._args.lintables)

        kwargs["cmdline"] = cmd_args

        runner = Command(executable_cmd="ansible-lint", **kwargs)
        return runner.run()

    def run_stdout(self) -> RunStdoutReturn:
        """Run in oldschool mode, just stdout."""
        self._logger.debug("lint requested in stdout mode")
        _, _, rc = self._run_runner()  # pylint: disable=invalid-name
        return RunStdoutReturn(message="", return_code=rc)

    def _pull_out_json_or_fatal(self, stdout: str) -> Optional[str]:
        # pylint: disable=no-self-use
        """
        Attempt to pull out JSON line from ansible-lint raw output.

        Note that stdout and stderr get munged together by docker/podman, so we
        need to do some trickery to try to figure out the actual JSON line vs,
        say, ansible warnings.
        """

        # We want the last (non empty) line of output. This should hopefully be
        # the JSON we need.
        for line in reversed(stdout.splitlines()):
            if not line:
                continue
            return line

    def run(self, interaction: Interaction, app: AppPublic) -> Optional[Interaction]:
        # pylint: disable=too-many-return-statements
        """Handle :lint

        :param interaction: The interaction from the user
        :param app: The app instance
        """

        self._logger.debug("lint requested")

        # Set up interaction
        self._prepare_to_run(app, interaction)

        updated = self._update_args(
            ["lint"] + shlex.split(interaction.action.match.groupdict()["params"] or ""),
        )

        if not updated:
            self._prepare_to_exit(interaction)
            return None

        notification = nonblocking_notification(messages=["Linting, this may take a minute..."])
        interaction.ui.show_form(notification)
        out, _, rc = self._run_runner()  # pylint: disable=invalid-name
        self._logger.debug("Output from ansible-lint run (rc=%d): %s", rc, out)

        # Quick sanity check, make sure we actually have a result to parse.
        if rc != 0 and "ansible-lint: No such file or directory" in out:
            installed_or_ee = (
                "in the execution environment you are using"
                if self._args.execution_environment
                else "installed"
            )
            self._fatal(
                "ansible-lint executable could not be found. Ensure 'ansible-lint' "
                f"is {installed_or_ee} and try again.",
            )
            self._prepare_to_exit(interaction)
            return None

        out_without_warnings = self._pull_out_json_or_fatal(out)
        if out_without_warnings is None:
            self._prepare_to_exit(interaction)
            return None

        try:
            raw_issues = json.loads(out_without_warnings)
        except json.JSONDecodeError as exc:
            self._logger.debug("Failed to parse 'ansible-lint' JSON response: %s", str(exc))
            notification = error_notification(
                messages=[
                    "Could not parse 'ansible-lint' output.",
                ],
            )
            self._interaction.ui.show_form(notification)
            self._prepare_to_exit(interaction)
            return None

        if len(raw_issues) == 0:
            notification = success_notification(messages=["Congratulations, no lint issues found!"])
            self._interaction.ui.show_form(notification)
            self._prepare_to_exit(interaction)
            return None

        issues = [massage_issue(issue) for issue in raw_issues]
        self._issues = sorted(issues, key=lambda i: Severity[i["severity"].upper()], reverse=True)
        self.steps.append(self._build_main_menu())

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

    def _build_main_menu(self):
        columns = [
            "severity",
            "__message",
            "__path",
            "__line",
        ]

        return Step(
            name="lint_result",
            columns=columns,
            step_type="menu",
            value=self._issues,
            select_func=self._build_lint_result,
        )

    def _build_lint_result(self):
        return Step(
            name="singular_lint_result",
            step_type="content",
            value=self._issues,
            index=self.steps.current.index,
        )
