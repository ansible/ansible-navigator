"""Menu selection implementation.

Processor of a menu selection from a numeric key press
or entry at the single line prompt. e.g ``:42``
"""

import logging

from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.ui_framework import Interaction

from . import _actions as actions


@actions.register
class Action:
    """Menu selection implementation."""

    KEGEX = r"^\d+$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the select action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Execute a menu selection for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        """
        self._logger.debug("selection made")
        interaction.ui.scroll(0)
        interaction.ui.clear()
        this = app.steps.back_one()  # remove this
        app.steps.current.index = interaction.action.value  # update index
        app.steps.append(app.steps.current.select_func())  # add next
        app.steps.append(this)  # put this back on stack
        self._logger.debug(
            "Requested next step in %s will be %s",
            app.name,
            app.steps.previous.name,
        )
