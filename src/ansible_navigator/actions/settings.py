"""The ``settings`` subcommand action."""
from __future__ import annotations

from dataclasses import asdict
from functools import partial

from ansible_navigator.action_base import ActionBase
from ansible_navigator.action_defs import RunStdoutReturn
from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem import PresentableSettingsEntries
from ansible_navigator.configuration_subsystem import PresentableSettingsEntry
from ansible_navigator.configuration_subsystem import to_effective
from ansible_navigator.configuration_subsystem import to_presentable
from ansible_navigator.configuration_subsystem import to_sample
from ansible_navigator.configuration_subsystem import to_schema
from ansible_navigator.configuration_subsystem import to_sources
from ansible_navigator.configuration_subsystem.definitions import Constants
from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.steps import StepType
from ansible_navigator.steps import TypedStep
from ansible_navigator.ui_framework import Color
from ansible_navigator.ui_framework import CursesLine
from ansible_navigator.ui_framework import CursesLinePart
from ansible_navigator.ui_framework import CursesLines
from ansible_navigator.ui_framework import Decoration
from ansible_navigator.ui_framework import Interaction
from ansible_navigator.utils.print import print_to_stdout

from . import _actions as actions
from . import run_action


def color_menu(colno: int, colname: str, entry: PresentableSettingsEntry) -> tuple[int, int]:
    """Color the menu.

    :param colno: Column number
    :param colname: Column name
    :param entry: Column value
    :returns: Constants that curses uses to color a line of text
    """
    if entry.default:
        return Color.GREEN, Color.BLACK
    return Color.YELLOW, Color.BLACK


CONTENT_HEADING_DEFAULT = "{name} (current value/default value: {current_value})"
CONTENT_HEADING_NOT_DEFAULT = (
    "{name} (current value: {current_value})  (default value: {default_value})"
)


def content_heading(obj: PresentableSettingsEntry, screen_w: int) -> CursesLines:
    """Create a heading for the setting entry showing.

    :param obj: The content going to be shown
    :param screen_w: The current screen width
    :returns: The heading
    """
    if obj.default:
        text = CONTENT_HEADING_DEFAULT.format(**asdict(obj))
        color = Color.GREEN
    else:
        text = CONTENT_HEADING_NOT_DEFAULT.format(**asdict(obj))
        color = Color.YELLOW

    fill_characters = screen_w - len(text) + 1
    heading_line = f"{text}{' ' * fill_characters}"

    line_part = CursesLinePart(
        column=0,
        string=heading_line,
        color=color,
        decoration=Decoration.UNDERLINE,
    )
    return CursesLines((CursesLine((line_part,)),))


@actions.register
class Action(ActionBase):
    """The action class for the settings subcommand."""

    KEGEX = r"^se(?:ttings)?$"

    def __init__(self, args):
        """Initialize the ``:settings`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="settings")
        self._settings: PresentableSettingsEntries

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Handle the ``settings`` subcommand in mode ``interactive``.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction` or
            :data:`None`
        """
        self._logger.debug("settings requested")
        self._prepare_to_run(app, interaction)
        self._settings = to_presentable(self._args)
        self.steps.append(self._build_main_menu())

        while True:
            self._calling_app.update()
            self._take_step()

            if not self.steps:
                break

            if self.steps.current.name == "quit":
                return self.steps.current

        self._prepare_to_exit(interaction)
        return None

    def run_stdout(self) -> RunStdoutReturn:
        """Handle settings in mode stdout.

        :returns: RunStdoutReturn
        """
        self._logger.debug("settings requested in stdout mode")

        dump = partial(
            print_to_stdout,
            use_color=self._args.display_color,
        )
        if self._args.entry("settings_schema").value.source is not Constants.DEFAULT_CFG:
            dump(content=to_schema(self._args), content_format=ContentFormat.JSON)
            return RunStdoutReturn(message="", return_code=0)

        dumped = False
        if self._args.settings_effective:
            dump(content=to_effective(self._args), content_format=ContentFormat.YAML)
            dumped = True
        if self._args.settings_sample:
            dump(content=to_sample(self._args)[0], content_format=ContentFormat.YAML_TXT)
            dumped = True
        if self._args.settings_sources:
            dump(content=to_sources(self._args), content_format=ContentFormat.YAML)
            dumped = True
        if dumped:
            return RunStdoutReturn(message="", return_code=0)

        dump(content=to_presentable(self._args), content_format=ContentFormat.YAML)
        return RunStdoutReturn(message="", return_code=0)

    def _build_main_menu(self) -> TypedStep:
        """Build the main menu of settings.

        :returns: The settings menu definition
        """
        step = TypedStep[PresentableSettingsEntry](
            name="all_options",
            columns=["name", "default", "source", "current"],
            select_func=self._build_settings_content,
            step_type=StepType.MENU,
        )
        step.value = self._settings
        return step

    def _build_settings_content(self) -> TypedStep:
        """Build the content for one settings entry.

        :returns: The option's content
        """
        step = TypedStep[PresentableSettingsEntry](
            name="setting_content",
            step_type=StepType.CONTENT,
        )
        step.index = self.steps.current.index
        step.value = self._settings
        return step

    def _take_step(self) -> None:
        """Take one step in the stack of steps."""
        result = None
        if isinstance(self.steps.current, Interaction):
            result = run_action(self.steps.current.name, self.app, self.steps.current)
        elif isinstance(self.steps.current, TypedStep):
            if self.steps.current.show_func:
                current_index = self.steps.current.index
                self.steps.current.show_func()
                self.steps.current.index = current_index

            if self.steps.current.step_type is StepType.MENU:
                result = self._interaction.ui.show(
                    obj=self.steps.current.value,
                    columns=self.steps.current.columns,
                    color_menu_item=color_menu,
                )
            elif self.steps.current.step_type is StepType.CONTENT:
                result = self._interaction.ui.show(
                    obj=self.steps.current.value,
                    index=self.steps.current.index,
                    content_heading=content_heading,
                )

        if result is None:
            self.steps.back_one()
        else:
            self.steps.append(result)
