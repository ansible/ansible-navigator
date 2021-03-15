""" {{ }} """
import html
import logging

from collections.abc import Mapping
from typing import Union

from . import _actions as actions
from ..utils import templar
from ..app_public import AppPublic
from ..ui_framework import Interaction


@actions.register
class Action:
    """{{ }}"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^{{.*}}$"

    def __init__(self, args):
        self._args = args
        self._logger = logging.getLogger(__name__)

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        """Handle :{{ }}

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("template requested '%s'", interaction.action.value)

        if interaction.content:
            if isinstance(interaction.content.showing, Mapping):
                template_vars = interaction.content.showing
            else:
                template_vars = {"this": interaction.content.showing}
                self._logger.info(
                    "Object passed for templating not a dictionary, " "use 'this' to access it"
                )
            templated = templar(string=str(interaction.action.value), template_vars=template_vars)

        elif interaction.menu:
            obj = [
                {k: v for k, v in c.items() if k in interaction.menu.columns}
                for c in interaction.menu.current
            ]
            if interaction.ui.menu_filter():
                obj = [
                    e
                    for e in obj
                    if interaction.ui.menu_filter().search(" ".join(str(v) for v in e.values()))
                ]
            template_vars = {"this": obj}
            self._logger.info("a menu is a list of dictionaries. use 'this' to access it")
        else:
            self._logger.error("No menu or content found")
            return None

        previous_scroll = interaction.ui.scroll()
        interaction.ui.scroll(0)

        templated = templar(string=str(interaction.action.value), template_vars=template_vars)
        if isinstance(templated, str):
            templated = html.unescape(templated)

        while True:
            app.update()
            xform = "source.txt" if isinstance(templated, str) else ""
            next_interaction: Interaction = interaction.ui.show(obj=templated, xform=xform)
            if next_interaction.name != "refresh":
                break

        interaction.ui.scroll(previous_scroll)
        return next_interaction
