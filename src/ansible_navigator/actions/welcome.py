"""Welcome subcommand implementation."""

from ..action_base import ActionBase
from ..app_public import AppPublic
from ..configuration_subsystem.definitions import ApplicationConfiguration
from ..content_defs import ContentFormat
from ..ui_framework import Interaction
from ..utils.packaged_data import retrieve_content
from . import _actions as actions


WELCOME = """

"""


@actions.register
class Action(ActionBase):
    """Welcome subcommand implementation."""

    KEGEX = r"^welcome$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:welcome`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="welcome")

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Execute the ``:welcome`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction`
        """
        self._logger.debug("welcome requested")
        self._prepare_to_run(app, interaction)

        welcome_md = retrieve_content(filename="welcome.md")
        while True:
            self._calling_app.update()
            interaction = interaction.ui.show(
                obj=welcome_md,
                content_format=ContentFormat.MARKDOWN,
            )
            app.update()
            if interaction.name != "refresh":
                break

        self._prepare_to_exit(interaction)
        return interaction
