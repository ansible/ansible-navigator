""" :rerun """
import copy
import logging
from . import _actions as actions
from ..app_public import AppPublic
from ..ui_framework import Interaction


# pylint: disable=protected-access


@actions.register
class Action:
    """:rerun"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^rr|rerun?$"

    def __init__(self, args):
        self._args = args
        self._logger = logging.getLogger(__name__)

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Handle :rerun

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("rerun requested")
        this = copy.copy(app.steps.current)
        app.rerun()
        # ensure we are last on the stack
        if app.steps.current != this:
            app.steps.append(this)
