""" :log """
from . import _actions as actions
from ..app import App
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction


@actions.register
class Action(App):
    """:log"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^l(?:og)?$"

    def __init__(self, args: ApplicationConfiguration):
        super().__init__(args=args, logger_name=__name__, name="log")

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Handle :log

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("log requested")
        self._prepare_to_run(app, interaction)

        auto_scroll = True
        while True:
            self._calling_app.update()
            with open(self._args.log_file) as fhand:
                dalog = fhand.read()

            new_scroll = len(dalog.splitlines())
            if auto_scroll:
                interaction.ui.scroll(new_scroll)

            interaction = interaction.ui.show(obj=dalog, xform="text.log")
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
