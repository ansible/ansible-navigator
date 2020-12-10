""" :json """
import logging
from . import _actions as actions
from ..app import App
from ..ui import Interaction


@actions.register
class Action:
    """:json"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^j(?:son)?$"

    def __init__(self):
        self._logger = logging.getLogger()

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: App) -> bool:
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
            return True
        return False
