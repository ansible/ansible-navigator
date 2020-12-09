r""" :\d+[0-9] etc """
import logging
from . import _actions as actions
from ..app import App
from ..ui import Interaction


# pylint: disable=protected-access


@actions.register
class Action:
    r""":\d+|[0-9]"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^\d+$"

    def __init__(self):
        self._logger = logging.getLogger()

    def run(self, interaction: Interaction, app: App) -> bool:
        """Handle :[0-n]

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("selection made")
        interaction.ui.scroll(0)
        app.step.index = interaction.action.value
        app.step = app.step.next
        self._logger.debug("Stepped forward to %s[%s]", app.step.name, interaction.action.value)
        return False
