"""``:json`` command implementation."""
import logging

from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..content_defs import ContentFormat
from ..ui_framework import Interaction
from . import _actions as actions


@actions.register
class Action:
    """``:json`` command implementation."""

    KEGEX = r"^j(?:son)?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:json`` action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Execute the ``:json`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        """
        self._logger.debug("json requested")
        if interaction.ui is not None:
            interaction.ui.scroll(0)
            content_format = interaction.ui.content_format(ContentFormat.JSON, default=True)
            self._logger.debug("Content format set to %s", content_format)
