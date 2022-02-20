"""``:back`` command implementation.

Additionally triggered by the escape key.
"""
import logging

from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..steps import Step
from ..ui_framework import Interaction
from . import _actions as actions


@actions.register
class Action:
    """``:back`` command implementation."""

    KEGEX = r"^\^\[|\x1b|back$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:back`` action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Execute the ``:back`` request.

        :param interaction: The interaction from the user
        :param app: The app instance
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
                "Stepping back in %s from %s to %s",
                app.name,
                step.name,
                app.steps.current.name,
            )
        else:
            self._logger.debug("Return to %s, at last step", app.name)

        app.steps.append(this)  # put this back on
