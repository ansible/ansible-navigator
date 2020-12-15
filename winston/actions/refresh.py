""" refresh"""
import logging

from . import _actions as actions
from ..app import App
from ..ui import Interaction


@actions.register
class Action:
    """refresh"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^KEY_F\(5\)$"

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    # pylint: disable=no-self-use
    def run(self, interaction: Interaction, app: App) -> None:
        """Handle :refresh

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        # this is noisy but helpful when needed
        # self._logger.debug("refresh requested")

        # Just in case the user switched tasks with +,- etc
        # change previous, since this interaction is on the stack
        if interaction.content:
            app.steps.previous.index = interaction.action.value
