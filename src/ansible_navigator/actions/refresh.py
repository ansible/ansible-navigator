"""refresh"""
import logging

from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction
from . import _actions as actions


@actions.register
class Action:
    """refresh"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^KEY_F\(5\)$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the refresh action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    # pylint: disable=no-self-use
    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Handle :refresh

        :param interaction: The interaction from the user
        :param app: The app instance
        """
        # Just in case the user switched tasks with +,- etc
        # change previous, since this interaction is on the stack
        if interaction.content:
            app.steps.previous.index = interaction.action.value
