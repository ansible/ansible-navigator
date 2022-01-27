""":welcome"""
import os

from ..app import App
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction
from . import _actions as actions


WELCOME = """

"""


@actions.register
class Action(App):
    """:welcome"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^welcome$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:welcome`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="welcome")

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Handle :welcome

        :param interaction: The interaction from the user
        :param app: The app instance
        :return: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction`
        """
        self._logger.debug("welcome requested")
        self._prepare_to_run(app, interaction)

        with open(
            os.path.join(self._args.internals.share_directory, "markdown", "welcome.md"),
            encoding="utf-8",
        ) as fhand:
            welcome_md = fhand.read()

        while True:
            self._calling_app.update()
            interaction = interaction.ui.show(obj=welcome_md, xform="text.html.markdown")
            app.update()
            if interaction.name != "refresh":
                break

        self._prepare_to_exit(interaction)
        return interaction
