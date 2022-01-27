r""":\d+[0-9] etc"""
import logging

from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction
from . import _actions as actions


@actions.register
class Action:
    r""":\d+|[0-9]"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^\d+$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the select action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Handle :[0-n]

        :param interaction: The interaction from the user
        :param app: The app instance
        """
        self._logger.debug("selection made")
        interaction.ui.scroll(0)
        interaction.ui.clear()
        this = app.steps.back_one()  # remove this
        app.steps.current.index = interaction.action.value  # update index
        app.steps.append(app.steps.current.select_func())  # add next
        app.steps.append(this)  # put this back on stack
        self._logger.debug(
            "Requested next step in %s will be %s",
            app.name,
            app.steps.previous.name,
        )
