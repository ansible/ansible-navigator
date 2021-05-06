""" jump to one action
"""

from ansible_navigator.actions import kegexes
from ansible_navigator.actions import run_action

from .app import App
from .steps import Steps
from .ui_framework import Interaction
from .ui_framework import UserInterface

DEFAULT_REFRESH = 5000


class ActionRunner(App):

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """the playbook ui"""

    def __init__(self, args):
        super().__init__(args, name="action_runner")
        self._ui = None
        self.steps: Steps = Steps()

    def initialize_ui(self, refresh: int) -> None:
        """initialize the user interface

        :param refresh: The refresh for the ui
        :type refresh: int
        """
        self._ui = UserInterface(
            screen_miny=3,
            osc4=self._args.osc4,
            kegexes=kegexes,
            refresh=refresh,
            share_directory=self._args.internals.share_directory,
        )

    def run(self, _screen) -> None:
        # pylint: disable=protected-access
        """Run with the interface and runner"""
        self.initialize_ui(DEFAULT_REFRESH)
        requested = " ".join(filter(None, (self._args.app, vars(self._args).get("value", ""))))
        name, action = self._action_match(requested)
        if name and action:
            interaction = Interaction(
                name=name, action=action, menu=None, content=None, ui=self._ui._ui
            )
            self._run_app(interaction)

    def _run_app(self, initial_interaction: Interaction) -> None:
        """enter the endless loop"""
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
