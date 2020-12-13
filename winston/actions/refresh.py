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
        self._logger = logging.getLogger()

    # pylint: disable=no-self-use
    def run(self, interaction: Interaction, app: App) -> bool:
        """Handle :refresh

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        # this is noisy but helpful when needed
        # self._logger.debug("refresh requested")

        # pop ourself off the stack
        if hasattr(app, "steps"):
            app.steps.back_one()

        # Just in case the user switched tasks with +,- etc
        if interaction.content:
            if hasattr(app, "steps"):
                app.steps.current.index = interaction.action.value
            else:
                app.step.previous.index = interaction.action.value
        return True
