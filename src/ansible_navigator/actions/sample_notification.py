"""``:sample_notification`` command implementation."""

from ansible_navigator.action_base import ActionBase
from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.ui_framework import Interaction
from ansible_navigator.ui_framework import dict_to_form
from ansible_navigator.ui_framework import form_to_dict
from ansible_navigator.utils.serialize import yaml

from . import _actions as actions


# cspell:disable
FORM = """
form:
  title:  BLOCKING NOTIFICATION
  title_color: 1
  fields:
    - name: info
      information:
      - Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
      - labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
      - laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
      - velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non,
      - sunt in culpa qui officia deserunt mollit anim id est laborum.
      type: information
  type: notification
"""
# cspell:enable


@actions.register
class Action(ActionBase):
    """``:sample_notification`` command implementation."""

    KEGEX = r"^sample_notification$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:sample_notification`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="sample_form")

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Execute the ``:sample_notification`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction`
        """
        self._logger.debug("sample notification requested")
        self._prepare_to_run(app, interaction)

        form_data = yaml.safe_load(FORM)
        form = dict_to_form(form_data["form"])
        interaction.ui.show_form(form)
        as_dict = form_to_dict(form)
        self._logger.debug("form response: %s", as_dict)

        while True:
            self._calling_app.update()
            next_interaction: Interaction = interaction.ui.show(obj=as_dict)
            if next_interaction.name != "refresh":
                break

        self._prepare_to_exit(interaction)
        return next_interaction
