"""A mechanism to start the main application loop for the text user interface.

An instance of :class:`~ansible_navigator.action_runner.ActionRunner`
is invoked once, after settings are parsed. A loop is entered and only
exited when the user requests to quit.

After initializing the user interface, an :class:`~ansible_navigator.ui_framework.ui.Interaction`
is created from the fully initialized settings, and the requested
action is run.

From that point forward flow control of the application is handled
by each action in the action stack, control returned here when
``:quit`` is requested by the user.
"""

from typing import TYPE_CHECKING

from ansible_navigator.actions import kegexes
from ansible_navigator.actions import run_action

from .action_base import ActionBase
from .configuration_subsystem.definitions import ApplicationConfiguration
from .constants import GRAMMAR_DIR
from .constants import TERMINAL_COLORS_PATH
from .constants import THEME_PATH
from .steps import Steps
from .ui_framework import Interaction
from .ui_framework import UIConfig
from .ui_framework import UserInterface


if TYPE_CHECKING:
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    from typing import Any

    Window = Any

DEFAULT_REFRESH = 100


class ActionRunner(ActionBase):
    """A single action runner."""

    def __init__(self, args: ApplicationConfiguration) -> None:
        """Initialize the ActionRunner class.

        :param args: The current application configuration
        """
        super().__init__(args, name="action_runner")
        self._ui: UserInterface
        self.steps: Steps = Steps()

    def initialize_ui(self, refresh: int) -> None:
        """Initialize the user interface.

        :param refresh: The refresh for the UI
        :type refresh: int
        """
        config = UIConfig(
            color=self._args.display_color,
            colors_initialized=False,
            grammar_dir=GRAMMAR_DIR,
            osc4=self._args.osc4,
            terminal_colors_path=TERMINAL_COLORS_PATH,
            theme_path=THEME_PATH,
        )
        self._logger.debug("grammar path = %s", config.grammar_dir)
        self._logger.debug("theme path = %s", config.theme_path)
        self._logger.debug("terminal colors path = %s", config.terminal_colors_path)

        self._ui = UserInterface(
            screen_min_height=3,
            kegexes=kegexes,
            refresh=refresh,
            ui_config=config,
        )

    def run(self, _screen: Window) -> None:
        # pylint: disable=protected-access
        """Run the app.

        Initialize the UI.
        Create an interaction based on the app name from the current settings.
        Run the action, passing the interaction.

        :param _screen: The screen instance from the curses wrapper call
        """
        self.initialize_ui(DEFAULT_REFRESH)
        name, action = self._action_match(self._args.app)
        if name and action:
            interaction = Interaction(
                name=name,
                action=action,
                menu=None,
                content=None,
                ui=self._ui._ui,
            )
            self._run_app(interaction)

    def _run_app(self, initial_interaction: Interaction) -> None:
        """Enter the endless app loop.

        :param initial_interaction: The initial interaction for app start
        """
        while True:
            if not self.steps:
                self.steps.append(initial_interaction)

            if isinstance(self.steps.current, Interaction):
                interaction = run_action(self.steps.current.name, self.app, self.steps.current)
            if interaction is None:
                self.steps.back_one()
                if not self.steps:
                    break
            elif interaction.name == "quit":
                break
            else:
                self.steps.append(interaction)
