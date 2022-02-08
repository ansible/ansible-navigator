""":log"""
from ..app import App
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction
from . import _actions as actions


@actions.register
class Action(App):
    """:log"""

    KEGEX = r"^l(?:og)?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:exec`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="log")

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Handle :log

        :param interaction: The interaction from the user
        :param app: The app instance
        :return: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction`
        """
        self._logger.debug("log requested")
        self._prepare_to_run(app, interaction)

        auto_scroll = True
        while True:
            self._calling_app.update()
            with open(self._args.log_file, encoding="utf-8") as fh:
                dalog = fh.read()

            new_scroll = len(dalog.splitlines())
            if auto_scroll:
                interaction.ui.scroll(new_scroll)

            interaction = interaction.ui.show(obj=dalog, serialization_format="text.log")
            if interaction.name != "refresh":
                break

            if interaction.ui.scroll() < new_scroll and auto_scroll:
                self._logger.debug("autoscroll disabled")
                auto_scroll = False
            elif interaction.ui.scroll() >= new_scroll and not auto_scroll:
                self._logger.debug("autoscroll enabled")
                auto_scroll = True

        self._prepare_to_exit(interaction)
        return interaction
