""" :settings
"""
from . import _actions as actions
from ..app import App
from ..app_public import AppPublic
from ..ui_framework import Interaction


@actions.register
class Action(App):
    """handle :settings"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^se(?:ttings)?$"

    def __init__(self, args):
        super().__init__(args=args, logger_name=__name__, name="settings")

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Handle settings interactive

        :param interaction: The interaction from the user
        :param app: The app instance
        """
        self._logger.debug("settings requested")
        self._prepare_to_run(app, interaction)

        while True:
            self._calling_app.update()
            next_interaction: Interaction = interaction.ui.show(["settings called"])
            if next_interaction.name != "refresh":
                break

        self._prepare_to_exit(interaction)
        return next_interaction

    def run_stdout(self) -> int:
        """Handle :settings stdout"""
        print("settings called")
        return 0
