""":help"""
import os

from ..app import App
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction
from . import _actions as actions


@actions.register
class Action(App):
    """:help"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^h(?:elp)?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:help`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="help")

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Handle :help

        :param interaction: The interaction from the user
        :param app: The app instance
        :return: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction`
        """
        self._logger.debug("help requested")
        self._prepare_to_run(app, interaction)

        with open(
            os.path.join(self._args.internals.share_directory, "markdown", "help.md"),
            encoding="utf-8",
        ) as fhand:
            help_md = fhand.read()

        while True:
            interaction = interaction.ui.show(obj=help_md, xform="text.html.markdown")
            app.update()
            if interaction.name != "refresh":
                break

        self._prepare_to_exit(interaction)
        return interaction
