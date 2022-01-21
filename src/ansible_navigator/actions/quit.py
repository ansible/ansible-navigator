""":quit
"""
import logging
from . import _actions as actions
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction


@actions.register
class Action:
    """handle :quit"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"q(?:uit)?(?P<exclamation>!)?$"

    def __init__(self, args: ApplicationConfiguration):
        self._args = args
        self._logger = logging.getLogger(__name__)

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Handle a request to quit the application.

        :param interaction: The interaction from the user
        :param app: The app instance
        """
        # : quit will be handled in the app
        self._logger.debug("quit was requested as: %s", interaction.action.value)
        return interaction
