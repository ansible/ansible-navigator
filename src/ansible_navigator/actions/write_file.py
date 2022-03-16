"""``:write`` command implementation."""
import logging
import os
import re

from pathlib import Path

from ansible_navigator.content_defs import ContentView
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..content_defs import SerializationFormat
from ..ui_framework import Interaction
from ..utils.functions import remove_dbl_un
from ..utils.serialize import serialize_write_file
from . import _actions as actions


@actions.register
class Action:
    """``:write`` command implementation."""

    KEGEX = r"^w(?:rite)?(?P<force>!)?\s+(?P<append>>>)?\s*(?P<filename>.+)$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:write`` action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    # pylint: disable=unused-argument
    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Execute the ``:write`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: Nothing
        """
        # pylint: disable=too-many-branches
        self._logger.debug("write requested as %s", interaction.action.value)
        match = interaction.action.match.groupdict()
        filename = os.path.abspath(match["filename"])
        if match["append"]:
            if not os.path.exists(filename) and not match["force"]:
                self._logger.warning(
                    "Append operation failed because %s does not exist, force with !",
                    filename,
                )
                return None
            file_mode = "a"
        else:
            if os.path.exists(filename) and not match["force"]:
                self._logger.warning(
                    "Write operation failed because %s exists, force with !",
                    filename,
                )
                return None
            file_mode = "w"

        if interaction.content:
            obj = interaction.content.showing
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

        if isinstance(obj, str):
            write_as = ".txt"
        else:
            if re.match(r"^.*\.y(?:a)?ml$", filename):
                write_as = ".yaml"
            elif filename.endswith(".json"):
                write_as = ".json"
            else:
                write_as = interaction.ui.content_format().value.file_extention

        if write_as == ".txt":
            with open(os.path.abspath(filename), file_mode, encoding="utf-8") as fh:
                fh.write(obj)
        elif write_as == ".yaml":
            serialize_write_file(
                content=obj,
                content_view=ContentView.NORMAL,
                file=Path(filename),
                file_mode=file_mode,
                serialization_format=SerializationFormat.YAML,
            )
        elif write_as == ".json":
            serialize_write_file(
                content=obj,
                content_view=ContentView.NORMAL,
                file=Path(filename),
                file_mode=file_mode,
                serialization_format=SerializationFormat.JSON,
            )
        self._logger.info("Wrote to '%s' with mode '%s' as '%s'", filename, file_mode, write_as)
        return None
