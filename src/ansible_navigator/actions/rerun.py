"""``:rerun`` command implementation."""
import copy
import logging

from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.ui_framework import Interaction

from . import _actions as actions


@actions.register
class Action:
    """``:rerun`` command implementation."""

    KEGEX = r"^rr|rerun?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:rerun`` action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Execute the ``:rerun`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        """
        self._logger.debug("rerun requested")
        this = copy.copy(app.steps.current)
        app.rerun()
        # ensure we are last on the stack
        if app.steps.current != this:
            app.steps.append(this)
