""" :help """
import logging
import os
from . import _actions as actions
from ..app_public import AppPublic
from ..ui import Interaction


@actions.register
class Action:
    """:help"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^h(?:elp)?$"

    def __init__(self, args):
        self._args = args
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Handle :help

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("help requested")
        with open(os.path.join(app.args.share_dir, "markdown", "help.md")) as fhand:
            help_md = fhand.read()
        previous_scroll = interaction.ui.scroll()
        interaction.ui.scroll(0)
        while True:
            interaction = interaction.ui.show(obj=help_md, xform="text.html.markdown")
            app.update()
            if interaction.name != "refresh":
                break
        interaction.ui.scroll(previous_scroll)
        return interaction
