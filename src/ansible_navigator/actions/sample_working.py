""":sample_working, this is a non-blocking form
"""
import time

from ..action_base import ActionBase
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction
from ..ui_framework import nonblocking_notification
from . import _actions as actions


@actions.register
class Action(ActionBase):
    """handle :sample_working"""

    KEGEX = r"^sample_working$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:sample_working`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="sample_working")

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Handle :doc

        :param interaction: The interaction from the user
        :param app: The app instance
        """
        self._logger.debug("sample working requested")
        self._prepare_to_run(app, interaction)
        messages = ["Please wait, this won't take long, about 3 seconds, really."]

        form = nonblocking_notification(messages)
        interaction.ui.show(form)
        time.sleep(3)

        self._prepare_to_exit(interaction)
