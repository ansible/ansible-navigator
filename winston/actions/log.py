""" :log """
import logging
from . import _actions as actions
from ..app import App
from ..ui import Interaction


@actions.register
class Action:
    """:log"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^l(?:og)?$"

    def __init__(self):
        self._logger = logging.getLogger()

    def run(self, interaction: Interaction, app: App) -> Interaction:
        """Handle :log

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("log requested")
        previous_scroll = interaction.ui.scroll()
        interaction.ui.scroll(0)
        auto_scroll = True
        while True:
            with open(app.args.logfile) as fhand:
                dalog = fhand.read()

            new_scroll = len(dalog.splitlines())
            if auto_scroll:
                interaction.ui.scroll(new_scroll)

            interaction = interaction.ui.show(obj=dalog, xform="text.log")
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
