""" :filter """
import logging
from . import _actions as actions
from ..app_public import AppPublic
from ..ui_framework import Interaction


@actions.register
class Action:
    """:filter"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^f(ilter)?(\s(?P<regex>.*))?$"

    def __init__(self, args):
        self._args = args
        self._logger = logging.getLogger(__name__)

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Handle :filter

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("filter requested")
        menu_filter = interaction.action.match.groupdict()["regex"]
        interaction.ui.menu_filter(menu_filter)
        self._logger.debug("requested filter set to %s", menu_filter)
