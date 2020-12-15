""" :stream """
import logging

from . import _actions as actions
from ..app import App
from ..ui import Interaction


@actions.register
class Action:
    """:stream"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^st(?:ream)?$"

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: App) -> Interaction:
        """Handle :stream

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("stream requested")

        previous_scroll = interaction.ui.scroll()
        interaction.ui.scroll(0)
        auto_scroll = True
        while True:
            app.update()

            new_scroll = len(app.stdout)
            if auto_scroll:
                interaction.ui.scroll(new_scroll)
            obj = "\n".join(app.stdout)
            next_interaction: Interaction = interaction.ui.show(obj=obj, xform="source.ansi")
            if next_interaction.name != "refresh":
                break

            if interaction.ui.scroll() < new_scroll and auto_scroll:
                self._logger.debug("autoscroll disabled")
                auto_scroll = False
            elif interaction.ui.scroll() >= new_scroll and not auto_scroll:
                self._logger.debug("autoscroll enabled")
                auto_scroll = True

        interaction.ui.scroll(previous_scroll)
        return next_interaction
