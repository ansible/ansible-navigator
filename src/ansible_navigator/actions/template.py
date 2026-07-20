"""Template command implementation.

Processor of a template request at the single line prompt. e.g. {{ }}
"""

from __future__ import annotations

import html

from collections.abc import Mapping
from typing import TYPE_CHECKING
from typing import Any

from ansible_navigator.action_base import ActionBase
from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.ui_framework import Interaction
from ansible_navigator.ui_framework import warning_notification
from ansible_navigator.utils.functions import remove_dbl_un
from ansible_navigator.utils.functions import templar

from . import _actions as actions


if TYPE_CHECKING:
    from ansible_navigator.app_public import AppPublic
    from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration


@actions.register
class Action(ActionBase):
    """Template command implementation."""

    KEGEX = r"^{{\s*(?P<params>.*?)\s*}}$"

    def __init__(self, args: ApplicationConfiguration) -> None:
        """Initialize the template action.

        Args:
            args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="template")

    def _resolve_template_vars(
        self,
        interaction: Interaction,
    ) -> tuple[dict[str, Any], list[str]] | None:
        """Resolve template variables from the current interaction content or menu.

        Args:
            interaction: The interaction from the user

        Returns:
            A tuple of (template_vars, type_msgs) or None if no content is available
        """
        type_msgs = ["Current content passed for templating is not a dictionary."]
        type_msgs.append("[HINT] Use 'this' to reference it (e.g. {{ this[0] }}")

        if interaction.content:
            if isinstance(interaction.content.showing, Mapping):
                return dict(interaction.content.showing), []
            return {"this": interaction.content.showing}, type_msgs

        if interaction.menu:
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
            return {"this": obj}, type_msgs

        self._logger.error("No menu or content found")
        return None

    @staticmethod
    def _determine_content_format(
        requested: str,
        templated: Any,
    ) -> ContentFormat | None:
        """Determine the content format based on the requested parameter and templated value.

        Args:
            requested: The requested template parameter string
            templated: The templated output value

        Returns:
            The content format or None
        """
        if requested == "examples":
            return ContentFormat.YAML_TXT
        if requested == "readme":
            return ContentFormat.MARKDOWN
        if isinstance(templated, str):
            return ContentFormat.TXT
        return None

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction | None:
        """Execute the templating request for mode interactive.

        Args:
            interaction: The interaction from the user
            app: The app instance

        Returns:
            The pending
            :class:`~ansible_navigator.ui_framework.ui.Interaction` or
            :data:`None`
        """
        self._logger.debug("template requested '%s'", interaction.action.value)
        self._prepare_to_run(app, interaction)

        resolved = self._resolve_template_vars(interaction)
        if resolved is None:
            return None
        template_vars, type_msgs = resolved

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

        requested = self._interaction.action.match.groupdict()["params"]
        content_format = self._determine_content_format(requested, templated)

        while True:
            app.update()
            next_interaction: Interaction = interaction.ui.show(
                obj=templated,
                content_format=content_format,
            )
            if next_interaction.name != "refresh":
                break

        interaction.ui.scroll(previous_scroll)
        self._prepare_to_exit(interaction)
        return next_interaction
