"""
This action provides ansible-lint results through ansible-navigator.
Internally, it works by using ansible-runner to execute ansible-lint (optionally
in an execution environment). When running ansible-lint, it passes
`-f codeclimate` which requests JSON output on stdout. The JSON output contains
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
from ..runner.api import CommandRunner
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

    # ui_framework.menu_builder.MenuBuilder will str() whatever it is given.
    def __str__(self):
        if self == Severity.unknown:
            return "<unknown>"
        return self.name


@dataclass
@total_ordering
class LintResult:
    """A single result, parsed from Ansible Lint."""

    raw: dict
    message: str
    severity: Severity
    line: int
    column: Optional[int]
    path: str
    description: str

    def __lt__(self, other):
        """Allow for easy sorting of results by severity."""
        return self.severity < other.severity

    @staticmethod
    def from_raw(issue: Dict[str, Any]):
        """
        Massages the raw JSON output into our LintResult structure and returns a
        a list of them.
        """

        column = None
        # This will be a dict if we have a line + column, otherwise an int
        # with just the line number.
        if isinstance(issue["location"]["lines"]["begin"], collections.Mapping):
            line = issue["location"]["lines"]["begin"]["line"]
            column = issue["location"]["lines"]["begin"]["column"]
        else:
            line = issue["location"]["lines"]["begin"]

        # The codeclimate formatter combines the rule id and message, so we
        # parse them out.
        msg_split = issue["check_name"].split("] ", 1)
        # admonition = msg_split[0][1:]  # take off the beginning [
        msg = msg_split[1]

        return LintResult(
            raw=issue,
            message=msg,
            severity=Severity[issue["severity"]],
            line=line,
            column=column,
            path=abs_user_path(issue["location"]["path"]),
            description=issue["description"],
        )


def severity_to_color(severity: Severity) -> int:
    if severity == Severity.minor:
        return 5
    elif severity == Severity.major:
        return 3
    elif severity in (Severity.critical, Severity.blocker):
        return 1
    elif severity == Severity.info:
        return 6
    return 0


def color_menu(colno: int, colname: str, entry: Dict[str, Any]) -> Tuple[int, int]:
    return (severity_to_color(entry["severity"]), 0)


def content_heading(obj: LintResult, screen_w: int) -> Union[CursesLines, None]:
    check_name = obj.raw["check_name"]
    check_name = check_name + (" " * (screen_w - len(check_name)))

    return (
        (
            CursesLinePart(
                column=0,
                string=obj.path,
                color=0,
                decoration=curses.A_BOLD,
            ),
        ),
        (
            CursesLinePart(
                column=0,
                string=check_name,
                color=severity_to_color(obj.severity),
                decoration=curses.A_UNDERLINE,
            ),
        ),
    )


# TODO: I'd really like this to be a step-level thing. I want to be able to
# pass a callable to manipulate data (in this case, dig into obj.raw) before
# it is rendered, without having to do this at an action-global level.
def filter_content_keys(obj: LintResult) -> Dict[Any, Any]:
    return obj.raw


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

        ansible_lint_path = "ansible-lint"
        if not self._args.execution_environment:
            ansible_lint_path_maybe = shutil.which("ansible-lint")
            if ansible_lint_path_maybe is None:
                err = "'ansible-lint' executable not found, therefore cannot lint."
                return self._fatal(err, 127)
            ansible_lint_path = ansible_lint_path_maybe

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
            "wrap_sh": True,
        }

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs.update(
                {"container_volume_mounts": self._args.execution_environment_volume_mounts}
            )

        if isinstance(self._args.container_options, list):
            kwargs.update({"container_options": self._args.container_options})

        cmd_args = []

        if self._args.mode == "interactive":
            cmd_args += [
                "-f",
                "codeclimate",
            ]

        if isinstance(self._args.lint_config, str):
            # TODO: Can we check this for existence somehow? Or is it too config
            #       dependent? The mountpoint could be anywhere, I suppose...
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
            # lint acts weirdly if we're not in the right directory.
            kwargs["container_workdir"] = self._args.lintables
            cmd_args.append(self._args.lintables)

            # TODO: Is there a better way to do this auto-mounting? I bet there
            # is! But in the 'ansible-playbook' case, ansible-runner weirdly
            # hardcodes the auto-mount: https://git.io/JoQjT
            volmount = "{0}:{1}:Z".format(self._args.lintables, self._args.lintables)
            if "container_volume_mounts" in kwargs:
                kwargs["container_volume_mounts"].append(volmount)
            else:
                kwargs["container_volume_mounts"] = [volmount]

        kwargs["cmdline"] = cmd_args

        runner = CommandRunner(executable_cmd=ansible_lint_path, **kwargs)
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
        self._update_args(
            ["lint"] + shlex.split(interaction.action.match.groupdict()["params"] or "")
        )
        self._prepare_to_run(app, interaction)
        self.stdout = self._calling_app.stdout

        notification = nonblocking_notification(messages=["Linting, this may take a minute..."])
        interaction.ui.show(notification)

        # TODO: This is blocking... We could probably make it use the async
        # command runner instead.
        out, err, rc = self._run_runner()

        try:
            issues = json.loads(out)
        except json.JSONDecodeError as e:
            self._logger.debug("json decode error: %s", str(e))
            self._logger.error("Failed to parse 'ansible-lint' JSON response")
            notification = error_notification(
                messages=[
                    "Could not parse 'ansible-lint' output.",
                ]
            )
            self._interaction.ui.show(notification)
            return None

        issues = [LintResult.from_raw(issue) for issue in issues]
        issues = sorted(issues, key=lambda i: i.severity, reverse=True)
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
                    obj=[asdict(x) for x in self.steps.current.value],
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

    def _build_main_menu(self, issues: List[LintResult]):
        columns = [
            "severity",
            "message",
            "path",
            "line",
            "column",
        ]

        return Step(
            name="lint_result",
            columns=columns,
            tipe="menu",
            value=issues,
            select_func=lambda: self._build_lint_result(issues),
        )

    def _build_lint_result(self, issues: List[LintResult]):
        return Step(
            name="singular_lint_result",
            tipe="content",
            value=issues,
            index=self.steps.current.index,
        )
