""" :sample_notification, this is a blocking form
"""
from . import _actions as actions
from ..app import App
from ..app_public import AppPublic
from ..ui_framework import Interaction
from ..ui_framework import dict_to_form
from ..ui_framework import form_to_dict
from ..yaml import yaml

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


@actions.register
class Action(App):
    """handle :sample_notification"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^sample_notification$"

    def __init__(self, args):
        super().__init__(args=args, logger_name=__name__, name="sample_form")

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> Interaction:
        """Handle :doc

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("sample notification requested")
        self._prepare_to_run(app, interaction)

        form_data = yaml.safe_load(FORM)
        form = dict_to_form(form_data["form"])
        interaction.ui.show(form)
        as_dict = form_to_dict(form)
        self._logger.debug("form response: %s", as_dict)

        while True:
            self._calling_app.update()
            next_interaction: Interaction = interaction.ui.show(obj=as_dict)
            if next_interaction.name != "refresh":
                break

        self._prepare_to_exit(interaction)
        return next_interaction
