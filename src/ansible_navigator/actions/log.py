"""``:log`` command implementation."""
from ansible_navigator.action_base import ActionBase
from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.ui_framework import Interaction

from . import _actions as actions


@actions.register
class Action(ActionBase):
    """``:log`` command implementation."""

    KEGEX = r"^l(?:og)?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:log`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="log")

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Execute the ``:log`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction`
        """
        self._logger.debug("log requested")
        self._prepare_to_run(app, interaction)

        auto_scroll = True
        while True:
            self._calling_app.update()
            with open(self._args.log_file, encoding="utf-8") as fh:
                log_contents = fh.read()

            new_scroll = len(log_contents.splitlines())
            if auto_scroll:
                interaction.ui.scroll(new_scroll)

            interaction = interaction.ui.show(obj=log_contents, content_format=ContentFormat.LOG)
            if interaction.name != "refresh":
                break

            if interaction.ui.scroll() < new_scroll and auto_scroll:
                self._logger.debug("auto_scroll disabled")
                auto_scroll = False
            elif interaction.ui.scroll() >= new_scroll and not auto_scroll:
                self._logger.debug("auto_scroll enabled")
                auto_scroll = True

        self._prepare_to_exit(interaction)
        return interaction
