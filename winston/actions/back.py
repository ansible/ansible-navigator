""" esc, ie back """
import logging

from . import _actions as actions
from ..app import App
from ..steps import Step
from ..ui import Interaction


@actions.register
class Action:
    """esc, ie back"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^\^\[|\x1b$"

    def __init__(self):
        self._logger = logging.getLogger()

    def run(self, interaction: Interaction, app: App) -> None:
        """Handle <esc>

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("back requested")
        interaction.ui.scroll(0)
        this = app.steps.back_one()  # pop this
        step = app.steps.back_one()  # pop current

        if app.steps:
            if isinstance(step, Step) and isinstance(app.steps.current, Step):
                if step.type == "menu" and app.steps.current.type == "menu":
                    interaction.ui.menu_filter(None)
            self._logger.debug(
                "Stepping back in %s from %s to %s", app.name, step.name, app.steps.current.name
            )
        else:
            self._logger.debug("Stepping out of %s", app.name)

        app.steps.append(this)  # put this back on
