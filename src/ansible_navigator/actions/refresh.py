"""Screen refresh implementation."""
import logging

from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.ui_framework import Interaction

from . import _actions as actions


@actions.register
class Action:
    """Screen refresh implementation."""

    KEGEX = r"^KEY_F\(5\)$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the refresh action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Execute the screen refresh request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        """
        # Just in case the user switched tasks with +,- etc
        # change previous, since this interaction is on the stack
        if interaction.content:
            app.steps.previous.index = interaction.action.value
