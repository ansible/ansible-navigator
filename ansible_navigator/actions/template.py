""" {{ }} """
import html

from collections.abc import Mapping
from typing import Union

from . import _actions as actions
from ..utils import templar

from ..app import App
from ..app_public import AppPublic

from ..ui_framework import warning_notification
from ..ui_framework import Interaction

from ..utils import remove_dbl_un


@actions.register
class Action(App):
    """{{ }}"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^{{.*}}$"

    def __init__(self, args):
        super().__init__(args=args, logger_name=__name__, name="template")

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        """Handle :{{ }}

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("template requested '%s'", interaction.action.value)
        self._prepare_to_run(app, interaction)

        type_msgs = ["Current content passed for templating is not a dictionary."]
        type_msgs.append("[HINT] Use 'this' to reference it (e.g. {{ this[0] }}")

        if interaction.content:
            if isinstance(interaction.content.showing, Mapping):
                template_vars = interaction.content.showing
                type_msgs = []
            else:
                template_vars = {"this": interaction.content.showing}

        elif interaction.menu:
            obj = [
                {remove_dbl_un(k): v for k, v in c.items() if k in interaction.menu.columns}
                for c in interaction.menu.current
            ]
            if interaction.ui.menu_filter():
                obj = [
                    e
                    for e in obj
                    if interaction.ui.menu_filter().search(" ".join(str(v) for v in e.values()))
                ]

            template_vars = {"this": obj}
        else:
            self._logger.error("No menu or content found")
            return None

        previous_scroll = interaction.ui.scroll()
        interaction.ui.scroll(0)

        errors, templated = templar(
            string=str(interaction.action.value), template_vars=template_vars
        )
        if errors:
            msgs = ["Errors encountered while templating input"] + errors
            msgs.extend(type_msgs)
            interaction.ui.show(warning_notification(msgs))
            return None

        if isinstance(templated, str):
            templated = html.unescape(templated)

        while True:
            app.update()
            xform = "source.txt" if isinstance(templated, str) else ""
            next_interaction: Interaction = interaction.ui.show(obj=templated, xform=xform)
            if next_interaction.name != "refresh":
                break

        interaction.ui.scroll(previous_scroll)
        self._prepare_to_exit(interaction)
        return next_interaction
