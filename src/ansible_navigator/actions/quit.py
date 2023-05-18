"""``:quit`` command implementation."""
import logging

from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.ui_framework import Interaction

from . import _actions as actions


@actions.register
class Action:
    """``:quit`` command implementation."""

    KEGEX = r"q(?:uit)?(?P<exclamation>!)?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:quit`` action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Handle a request to quit the application from the user interface.

        The application exit is ultimately handled by
        :class:`~ansible_navigator.action_runner.ActionRunner` so return immediately,
        passing the ``:quit`` request backwards through the stack of actions that are on the stack.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction`
        """
        self._logger.debug("quit was requested as: %s", interaction.action.value)
        return interaction
