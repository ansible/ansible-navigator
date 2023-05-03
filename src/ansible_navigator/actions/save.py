"""``:save`` command implementation."""
import logging

from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.ui_framework import Interaction

from . import _actions as actions


@actions.register
class Action:
    """``:save`` command implementation."""

    KEGEX = r"^s(?:ave)?\s(?P<filename>.*)$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:save`` action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Execute the ``:save`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        """
        self._logger.debug("save requested")
        filename = interaction.action.match.groupdict()["filename"]
        app.write_artifact(filename)
