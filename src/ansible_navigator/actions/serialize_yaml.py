""":yaml"""
import logging

from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction
from . import _actions as actions


@actions.register
class Action:
    """:yaml"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^y(?:aml)?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:yaml`` action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Handle :yaml

        :param interaction: The interaction from the user, action and value
        :param app: The app instance
        """
        self._logger.debug("yaml requested")
        if interaction.ui is not None:
            interaction.ui.scroll(0)
            xform = interaction.ui.xform("source.yaml", default=True)
            self._logger.debug("Serialization set to %s", xform)
