""" :json """
import logging
from . import _actions as actions
from ..app_public import AppPublic
from ..ui_framework import Interaction


@actions.register
class Action:
    """:json"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^j(?:son)?$"

    def __init__(self, args):
        self._args = args
        self._logger = logging.getLogger(__name__)

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Handle :json

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("json requested")
        if interaction.ui is not None:
            interaction.ui.scroll(0)
            xform = interaction.ui.xform("source.json", default=True)
            self._logger.debug("Serialization set to %s", xform)
