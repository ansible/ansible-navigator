"""Template command implementation.

Processor of a template request at the single line prompt. e.g. {{ }}
"""
import html
import re
import textwrap

from collections.abc import Mapping
from typing import Optional

from ..action_base import ActionBase
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..content_defs import ContentFormat
from ..ui_framework import Interaction
from ..ui_framework import warning_notification
from ..utils.functions import remove_dbl_un
from ..utils.functions import templar
from . import _actions as actions


@actions.register
class Action(ActionBase):
    """Template command implementation."""

    KEGEX = r"^{{.*}}$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the template action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="template")

    @staticmethod
    def _string_format(value: str) -> str:
        template_str = re.match(r"{{\s*(?P<word>\S+)\s*}}", value)
        if template_str:
            match_dict = template_str.groupdict()
            if match_dict["word"] == "readme":
                return "text.html.markdown"
            if match_dict["word"] == "examples":
                return "source.yaml"
        return "source.txt"

    def run(self, interaction: Interaction, app: AppPublic) -> Optional[Interaction]:
        """Execute the templating request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction` or
            :data:`None`
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
            string=str(interaction.action.value),
            template_vars=template_vars,
        )
        if errors:
            msgs = ["Errors encountered while templating input"] + errors
            msgs.extend(type_msgs)
            interaction.ui.show_form(warning_notification(msgs))
            return None

        if isinstance(templated, str):
            templated = html.unescape(templated)
            templated = templated.strip()
            templated = textwrap.dedent(templated)
            serialization_format = self._string_format(str(interaction.action.value))
        else:
            serialization_format = ""

        while True:
            app.update()
            serialization_format = ContentFormat.TXT if isinstance(templated, str) else None
            next_interaction: Interaction = interaction.ui.show(
                obj=templated,
                content_format=serialization_format,
            )
            if next_interaction.name != "refresh":
                break

        interaction.ui.scroll(previous_scroll)
        self._prepare_to_exit(interaction)
        return next_interaction
