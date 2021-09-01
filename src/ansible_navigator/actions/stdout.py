""" :stdout """

from . import _actions as actions
from ..app import App
from ..app_public import AppPublic
from ..ui_framework import Interaction


@actions.register
class Action(App):
    """:stdout"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^st(?:dout)?$"

    def __init__(self, args):
        super().__init__(args=args, logger_name=__name__, name="stdout")

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Handle :stdout

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("stdout requested")
        self._prepare_to_run(app, interaction)

        auto_scroll = True
        while True:
            self._calling_app.update()

            new_scroll = len(self._calling_app.stdout)
            if auto_scroll:
                interaction.ui.scroll(new_scroll)
            obj = "\n".join(app.stdout)
            next_interaction: Interaction = interaction.ui.show(obj=obj, xform="source.ansi")
            if next_interaction.name != "refresh":
                break

            if interaction.ui.scroll() < new_scroll and auto_scroll:
                self._logger.debug("autoscroll disabled")
                auto_scroll = False
            elif interaction.ui.scroll() >= new_scroll and not auto_scroll:
                self._logger.debug("autoscroll enabled")
                auto_scroll = True

        self._prepare_to_exit(interaction)
        return next_interaction
