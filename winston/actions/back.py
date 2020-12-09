""" esc, ie back """
import logging

from . import _actions as actions
from ..app import App
from ..ui import Interaction


@actions.register
class Action:
    """esc, ie back"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^\^\[|\x1b$"

    def __init__(self):
        self._logger = logging.getLogger()

    def run(self, interaction: Interaction, app: App) -> bool:
        """Handle <esc>

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("back requested")
        interaction.ui.scroll(0)
        # if seeing a menu, and going back to a menu, clear the menu filter
        if app.step.type == "menu" and app.step.previous.type == "menu":
            interaction.ui.menu_filter(None)

        self._logger.debug("Stepping back from %s to %s", app.step.name, app.step.previous.name)
        app.step = app.step.previous
        return False
