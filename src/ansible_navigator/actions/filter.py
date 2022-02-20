"""``:filter`` command implementation."""
import logging

from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction
from . import _actions as actions


@actions.register
class Action:
    """``:filter`` command implementation."""

    KEGEX = r"^f(ilter)?(\s(?P<regex>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:filter`` action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Execute the ``:filter`` request.

        :param interaction: The interaction from the user
        :param app: The app instance
        """
        self._logger.debug("filter requested")
        menu_filter = interaction.action.match.groupdict()["regex"]
        interaction.ui.menu_filter(menu_filter)
        self._logger.debug("requested filter set to %s", menu_filter)
