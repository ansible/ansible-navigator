""" esc, ie back """
import logging

from . import _actions as actions
from ..app_public import AppPublic
from ..steps import Step
from ..ui_framework import Interaction


@actions.register
class Action:
    """esc, ie back"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^\^\[|\x1b|back$"

    def __init__(self, args):
        self._args = args
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Handle <esc>

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("back requested")
        interaction.ui.scroll(0)
        interaction.ui.clear()
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
            self._logger.debug("Return to %s, at last step", app.name)

        app.steps.append(this)  # put this back on
