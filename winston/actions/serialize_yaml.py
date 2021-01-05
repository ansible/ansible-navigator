""" :yaml """
import logging
from . import _actions as actions
from ..app_public import AppPublic
from ..ui_framework import Interaction


@actions.register
class Action:
    """:yaml"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^y(?:aml)?$"

    def __init__(self, args):
        self._args = args
        self._logger = logging.getLogger(__name__)

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Handle :yaml

        :param interaction: The interaction from the user, action and value
        :type interaction: dict
        """
        self._logger.debug("yaml requested")
        if interaction.ui is not None:
            interaction.ui.scroll(0)
            xform = interaction.ui.xform("source.yaml", default=True)
            self._logger.debug("Serialization set to %s", xform)
