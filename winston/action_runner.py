""" jump to one action
"""

from collections import deque
import winston.actions as actions

from .app import App
from .explorer_ui import ExplorerUi as Ui
from .step import Step
from .ui import Interaction


class ActionRunner(App):

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """the playbook ui"""

    def __init__(self, args):
        super().__init__(args)

        self.actions = actions
        self._ui = None

    def initialize_ui(self, refresh: int) -> None:
        """initialize the user interface

        :param refresh: The refresh for the ui
        :type refresh: int
        """
        self._ui = Ui(
            screen_miny=3,
            no_osc4=self.args.no_osc4,
            kegexes=self.actions.kegexes,
            refresh=refresh,
        )

    def run(self, _screen) -> None:
        # pylint: disable=protected-access
        """Run with the interface and runner"""
        self.initialize_ui(-1)
        self.step = Step(self.args.app, "content", None)
        self.step.previous = self.step
        action = self._ui._action_match(" ".join(filter(None, (self.args.app, self.args.value))))
        interaction = Interaction(action=action, menu=None, content=None, ui=self._ui._ui)
        self._run_app(interaction)

    def _run_app(self, interaction: Interaction) -> None:
        """enter the endless loop"""
        # pylint: disable=too-many-branches
        initial = interaction
        ique = deque([interaction])
        while True:

            interaction = self.actions.run(
                action=ique[-1].action.name,
                app=self,
                interaction=ique[-1],
            )

            if isinstance(interaction, Interaction):
                if interaction.action.name == "quit":
                    return
                ique.append(interaction)
            elif isinstance(interaction, bool):
                if interaction is True:
                    ique.pop()
                elif interaction is False:
                    if len(ique) == 1:
                        pass
                    else:
                        ique.pop()
                        ique.pop()
                        if not ique:
                            ique.append(initial)
            else:
                self._logger.debug("Invalid response from action: %s", interaction)
                interaction = False
