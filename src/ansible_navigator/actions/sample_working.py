"""``:sample_working`` command implementation."""

import time

from ansible_navigator.action_base import ActionBase
from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.ui_framework import Interaction
from ansible_navigator.ui_framework import nonblocking_notification

from . import _actions as actions


@actions.register
class Action(ActionBase):
    """``:sample_working`` command implementation."""

    KEGEX = r"^sample_working$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:sample_working`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="sample_working")

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Execute the ``:sample_working`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        """
        self._logger.debug("sample working requested")
        self._prepare_to_run(app, interaction)
        messages = ["Please wait, this won't take long, about 3 seconds, really."]

        form = nonblocking_notification(messages)
        interaction.ui.show_form(form)
        time.sleep(3)

        self._prepare_to_exit(interaction)
