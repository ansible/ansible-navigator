""" :filter """
import logging
from . import _actions as actions
from ..app import App
from ..ui import Interaction


@actions.register
class Action:
    """ :filter """

    # pylint: disable=too-few-public-methods

    KEGEX = r"^f(ilter)?(\s(?P<regex>.*))?$"

    def __init__(self):
        self._logger = logging.getLogger()

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: App) -> None:
        """Handle :filter

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("filter requested")
        interaction.ui.scroll(0)
        menu_filter = interaction.action.match.groupdict()["regex"]
        interaction.ui.menu_filter(menu_filter)
        self._logger.debug("requested filter set to %s", menu_filter)

        if hasattr(app, "steps"):
            app.steps.back_one()

        return None
