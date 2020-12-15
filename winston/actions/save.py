""" :save """
import logging

from . import _actions as actions
from ..app import App
from ..ui import Interaction


@actions.register
class Action:
    """:save"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^s(?:ave)?\s(?P<filename>.*)$"

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: App) -> None:
        """Handle :save

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("save requested")
        filename = interaction.action.match.groupdict()["filename"]
        app.write_artifact(filename)
