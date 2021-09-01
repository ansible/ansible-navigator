""" :help """
import os
from . import _actions as actions
from ..app import App
from ..app_public import AppPublic
from ..ui_framework import Interaction


@actions.register
class Action(App):
    """:help"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^h(?:elp)?$"

    def __init__(self, args):
        super().__init__(args=args, logger_name=__name__, name="help")

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Handle :help

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("help requested")
        self._prepare_to_run(app, interaction)

        with open(
            os.path.join(self._args.internals.share_directory, "markdown", "help.md")
        ) as fhand:
            help_md = fhand.read()

        while True:
            interaction = interaction.ui.show(obj=help_md, xform="text.html.markdown")
            app.update()
            if interaction.name != "refresh":
                break

        self._prepare_to_exit(interaction)
        return interaction
