""" :rerun """
import logging
from . import _actions as actions
from ..player import Player as App
from ..ui import Interaction


# pylint: disable=protected-access


@actions.register
class Action:
    """:rerun"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^rr|rerun?$"

    def __init__(self):
        self._logger = logging.getLogger()

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: App) -> bool:
        """Handle :rerun

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("rerun requested")
        app.rerun()
        return False
