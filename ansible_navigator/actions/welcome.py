""" :welcome """
import logging
import os
from . import _actions as actions
from ..app_public import AppPublic
from ..ui_framework import Interaction


WELCOME = """

"""


@actions.register
class Action:
    """:welcome"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^welcome$"

    def __init__(self, args):
        self._args = args
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Handle :welcome

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        with open(
            os.path.join(app.args.internals.share_directory, "markdown", "welcome.md")
        ) as fhand:
            welcome_md = fhand.read()

        self._logger.debug("welcome requested")
        previous_scroll = interaction.ui.scroll()
        interaction.ui.scroll(0)
        while True:
            interaction = interaction.ui.show(obj=welcome_md, xform="text.html.markdown")
            app.update()
            if interaction.name != "refresh":
                break
        interaction.ui.scroll(previous_scroll)
        return interaction
