""" :stream """
import logging

from typing import Union
from . import _actions as actions
from ..player import Player as App
from ..ui import Interaction


@actions.register
class Action:
    """:stream"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^st(?:ream)?$"

    def __init__(self):
        self._logger = logging.getLogger()

    def run(self, interaction: Interaction, app: App) -> Union[Interaction, None]:
        """Handle :stream

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("stream requested")
        if hasattr(app, "stdout"):
            previous_scroll = interaction.ui.scroll()
            interaction.ui.scroll(0)
            auto_scroll = True
            while True:
                new_scroll = len(app.stdout)
                if auto_scroll:
                    interaction.ui.scroll(new_scroll)
                obj = "\n".join(app.stdout)
                interaction = interaction.ui.show(obj=obj, xform="source.ansi")
                app.update()
                if interaction.action.name != "refresh":
                    break

                if interaction.ui.scroll() < new_scroll and auto_scroll:
                    self._logger.debug("autoscroll disabled")
                    auto_scroll = False
                elif interaction.ui.scroll() >= new_scroll and not auto_scroll:
                    self._logger.debug("autoscroll enabled")
                    auto_scroll = True

            interaction.ui.scroll(previous_scroll)
            return interaction
        self._logger.debug("stdout unavailable")
        if hasattr(app, "steps"):
            self._logger.debug("stepping back in %s", app.name)
            app.steps.back_one()
        return None
