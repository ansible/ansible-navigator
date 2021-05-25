""" :sample_working, this is a non-blocking form
"""
import time
from . import _actions as actions
from ..app import App
from ..app_public import AppPublic
from ..ui_framework import Interaction
from ..ui_framework import nonblocking_notification


@actions.register
class Action(App):
    """handle :sample_working"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^sample_working$"

    def __init__(self, args):
        super().__init__(args=args, logger_name=__name__, name="sample_working")

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Handle :doc

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("sample working requested")
        self._prepare_to_run(app, interaction)
        messages = ["Please wait, this won't take long, about 3 seconds, really."]

        form = nonblocking_notification(messages)
        interaction.ui.show(form)
        time.sleep(3)

        self._prepare_to_exit(interaction)
