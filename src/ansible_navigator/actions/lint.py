# cspell:ignore fqcn,FQCN

"""This action provides ansible-lint results through ansible-navigator.

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
from __future__ import annotations

import json
import os
import shlex

from collections.abc import Mapping
from datetime import datetime
from enum import IntEnum
from typing import Any

from ansible_navigator.action_base import ActionBase
from ansible_navigator.action_defs import RunStdoutReturn
from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.runner.command import Command
from ansible_navigator.steps import Step
from ansible_navigator.ui_framework import Color
from ansible_navigator.ui_framework import CursesLine
from ansible_navigator.ui_framework import CursesLinePart
from ansible_navigator.ui_framework import CursesLines
from ansible_navigator.ui_framework import Decoration
from ansible_navigator.ui_framework import Interaction
from ansible_navigator.ui_framework import error_notification
from ansible_navigator.ui_framework import nonblocking_notification
from ansible_navigator.ui_framework import success_notification
from ansible_navigator.utils.functions import abs_user_path
from ansible_navigator.utils.functions import remove_ansi
from ansible_navigator.utils.functions import time_stamp_for_file

from . import _actions as actions
from . import run_action


class Severity(IntEnum):
    """A mapping from ansible-lint severity to an integer represented internally.

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
        """Return unknown if ansible-lint ever returns something unexpected.

        :param value: The value
        :returns: A severity unknown
        """
        return Severity.UNKNOWN


def severity_to_color(severity: str) -> int:
    """Convert severity to curses colors.

    :param severity: The severity to convert to a color
    :returns: A color for the severity
    """
    if severity == "minor":
        return Color.MAGENTA
    if severity == "major":
        return Color.YELLOW
    if severity in ("critical", "blocker"):
        return Color.RED
    if severity == "info":
        return Color.CYAN
    return Color.BLACK


def color_menu(colno: int, colname: str, entry: dict[str, Any]) -> tuple[int, int]:
    """Color the menu.

    :param colno: The column number
    :param colname: The column name
    :param entry: The current content entry
    :returns: The foreground and background color
    """
    return (severity_to_color(entry["severity"]), Color.BLACK)


def content_heading(obj: dict, screen_w: int) -> CursesLines:
    """Generate the content heading.

    :param obj: The content for which the heading will be generated
    :param screen_w: The current screen width
    :returns: The content heading
    """
    check_line = f"Message: {obj['check_name']}"
    location = f"Location: {obj['issue_path']}"
    fill_characters = screen_w - len(location) + 1
    location_line = f"{location}{' ' * fill_characters}"

    line_1_part_1 = CursesLinePart(
        column=0,
        string=check_line,
        color=severity_to_color(obj["severity"]),
        decoration=Decoration.NORMAL,
    )
    line_2_part_1 = CursesLinePart(
        column=0,
        string=location_line,
        color=severity_to_color(obj["severity"]),
        decoration=Decoration.UNDERLINE,
    )
    return CursesLines((CursesLine((line_1_part_1,)), CursesLine((line_2_part_1,))))


def filter_content_keys(obj: dict[Any, Any]) -> dict[Any, Any]:
    """Filter out internal keys.

    :param obj: The content from which the content keys will be filtered
    :returns: The content without the internal keys
    """
    ignored_keys = ("fingerprint",)
    return {k: v for k, v in obj.items() if not k.startswith("__") and k not in ignored_keys}


def massage_issue(issue: dict) -> dict:
    """Massage an issue by injecting some useful keys with strings for rendering.

    :param issue: The issue reported
    :returns: The issue reformatted
    """
    massaged = issue.copy()
    massaged["__severity"] = massaged["severity"].capitalize()
    # Version 6.1 and before of ansible-lint used this syntax
    # "check_name": "[fqcn-builtins] Use FQCN for builtin actions."
    # Version 6.2 and later use this syntax
    # check_name": "fqcn-builtins", "description": "Use FQCN for builtin actions."
    if issue["check_name"].startswith("["):
        massaged["__message"] = issue["check_name"].split("]")[1].strip()
    else:
        massaged["__message"] = issue["description"]
    massaged["__path"] = abs_user_path(issue["location"]["path"])
    if isinstance(issue["location"]["lines"]["begin"], Mapping):
        massaged["__line"] = issue["location"]["lines"]["begin"]["line"]
    else:
        massaged["__line"] = issue["location"]["lines"]["begin"]
    massaged["issue_path"] = f"{massaged['__path']}:{massaged['__line']}"
    return massaged


MENU_COLUMNS = [
    "__severity",
    "__message",
    "__path",
    "__line",
]


@actions.register
class Action(ActionBase):
    """Run the lint subcommand."""

    KEGEX = r"^lint(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the action.

        :param args: The current application configuration
        """
        self._modification_times_last_updated: datetime
        self._success_notification_shown: bool = False
        self._issues_menu = Step(
            name="issues_menu",
            step_type="menu",
            columns=MENU_COLUMNS,
            value=[],
            select_func=self._build_issue_content,
        )
        self._current_issue_count = 0
        super().__init__(args=args, logger_name=__name__, name="lint")

    @property
    def is_interactive(self):
        """Determine if interactive.

        :returns: An indication is running in interactive mode
        """
        return self._args.mode == "interactive"

    def _fatal(self, msg: str) -> None:
        """Show a notification if a fatal error has occurred.

        :param msg: The message to display
        :raises RuntimeError: A runtime error if not mode interactive
        """
        self._logger.error(msg)

        if self.is_interactive:
            notification = error_notification(messages=[msg])
            self._interaction.ui.show_form(notification)
        else:
            raise RuntimeError(msg)

    def _run_runner(self) -> tuple[str, str, int]:
        """Spin up runner to run ansible-lint, either in an exec env or not.

        :returns: The output, errors and return code
        """
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
        """Execute the ``doc`` request for mode stdout.

        :returns: A message and return code
        """
        self._logger.debug("lint requested in stdout mode")
        _output, _error, return_code = self._run_runner()
        return RunStdoutReturn(message="", return_code=return_code)

    @staticmethod
    def _pull_out_json_or_fatal(stdout: str) -> str | None:
        """
        Attempt to pull out JSON line from ansible-lint raw output.

        Note that stdout and stderr get munged together by docker/podman, so we
        need to do some trickery to try to figure out the actual JSON line vs,
        say, ansible warnings.

        :param stdout: The stdout from the lint invocation
        :returns: The json string
        """
        # We want the last (non empty) line of output. This should hopefully be
        # the JSON we need.
        for line in reversed(stdout.splitlines()):
            if not line:
                continue
            return line
        return None

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction | None:
        """Execute the ``lint`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction` or
            :data:`None`
        """
        self._logger.debug("lint requested")
        self._prepare_to_run(app, interaction)

        updated = self._update_args(
            ["lint"] + shlex.split(interaction.action.match.groupdict()["params"] or ""),
        )

        if not updated:
            self._prepare_to_exit(interaction)
            return None

        notification = nonblocking_notification(messages=["Linting, this may take a minute..."])
        interaction.ui.show_form(notification)

        self._build_issues_menu()
        if self._current_issue_count == 0:
            self._prepare_to_exit(interaction)
            return None

        self.steps.append(self._issues_menu)

        while True:
            self.update()

            if self._current_issue_count == 0:
                break

            self._interaction.ui.update_status(
                status=f"Issues: {self._current_issue_count}",
                status_color=self._max_severity_color,
            )

            self._take_step()

            if not self.steps:
                break

            if self.steps.current.name == "quit":
                return self.steps.current

        self._prepare_to_exit(interaction)
        return None

    def update(self):
        """Request calling app update, and update modification time if needed."""
        self._calling_app.update()

        # Do this only every 2 seconds
        if (datetime.now() - self._modification_times_last_updated).total_seconds() > 2:
            rerun_lint = self._rerun_needed()
            if rerun_lint:
                self._build_issues_menu()

    @property
    def _max_severity_color(self):
        """Determine the color of the maximum severity issue.

        :returns: The color
        """
        max_severity = max(Severity[i["severity"].upper()].value for i in self._issues_menu.value)
        return severity_to_color(Severity(max_severity).name.lower())

    def _take_step(self) -> None:
        """Take a step based on the current step or step back."""
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

    def _build_issues_menu(self):
        """Build the menu of all issues.

        :returns: Indication of success
        """
        output, _error, return_code = self._run_runner()
        self._logger.debug("Output from ansible-lint run (rc=%d): %s", return_code, output)

        # ansible-lint failed
        if return_code != 0 and "ansible-lint: No such file or directory" in output:
            installed_or_ee = (
                "in the execution environment you are using"
                if self._args.execution_environment
                else "installed"
            )
            self._fatal(
                "ansible-lint executable could not be found. Ensure 'ansible-lint' "
                f"is {installed_or_ee} and try again.",
            )
            self._current_issue_count = 0
            return

        # Could not extract json from response
        out_without_warnings = self._pull_out_json_or_fatal(output)
        if out_without_warnings is None:
            self._current_issue_count = 0
            return

        # De-serialization of json failed
        try:
            raw_issues = json.loads(out_without_warnings)
        except json.JSONDecodeError as exc:
            self._logger.debug("Failed to parse 'ansible-lint' JSON response: %s", str(exc))
            messages = ["Could not parse 'ansible-lint' output."]
            without_ansi = remove_ansi(output)
            messages.extend(without_ansi.splitlines())
            notification = error_notification(messages)
            self._interaction.ui.show_form(notification)
            self._current_issue_count = 0
            return

        # No issues were found
        if len(raw_issues) == 0:
            notification = success_notification(messages=["Congratulations, no lint issues found!"])
            self._interaction.ui.show_form(notification)

        # Update menu
        issues = [massage_issue(issue) for issue in raw_issues]
        self._current_issue_count = len(issues)
        self._issues_menu.value = sorted(
            issues,
            key=lambda i: Severity[i["severity"].upper()],
            reverse=True,
        )

        # Update new content timestamps
        _rerun_lint = self._rerun_needed()
        return

    def _build_issue_content(self):
        """Build the content for one plugin.

        :returns: The plugin's content
        """
        return Step(
            name="issue_content",
            step_type="content",
            value=self.steps.current.value,
            index=self.steps.current.index,
        )

    def _rerun_needed(self) -> bool:
        """Add a modification timestamp to each issue, check for changes.

        :returns: Indication if lint should be rerun
        """
        rerun_lint = False
        checked_paths = []
        for outer_issue in self._issues_menu.value:
            outer_path = outer_issue["__path"]
            if outer_path in checked_paths:
                continue
            checked_paths.append(outer_path)
            unix_ts, iso_ts = time_stamp_for_file(outer_path, self._args.time_zone)
            # Set all issues for the same file
            for inner_issue in self._issues_menu.value:
                inner_path = inner_issue["__path"]
                if inner_path != outer_path:
                    continue

                previous_ts = inner_issue.get("__last_modified")
                inner_issue["last_modified"] = iso_ts
                inner_issue["__last_modified"] = unix_ts

                # The file may be gone or non existent
                if unix_ts is None:
                    continue

                # The may be a first run
                if previous_ts is None:
                    rerun_lint = True
                    continue

                # Has the file changed
                if unix_ts > previous_ts:
                    rerun_lint = True

        self._modification_times_last_updated = datetime.now()
        if rerun_lint:
            self._logger.debug("Files modified")
        return rerun_lint
