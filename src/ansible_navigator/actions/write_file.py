"""``:write`` command implementation."""

import logging
import re

from pathlib import Path
from typing import Any

from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.content_defs import ContentView
from ansible_navigator.content_defs import SerializationFormat
from ansible_navigator.ui_framework import Interaction
from ansible_navigator.utils.functions import expand_path
from ansible_navigator.utils.functions import remove_dbl_un
from ansible_navigator.utils.serialize import serialize_write_file

from . import _actions as actions


JSON_EXTENSION = ".json"


@actions.register
class Action:
    """``:write`` command implementation."""

    KEGEX = r"^w(?:rite)?(?P<force>!)?\s+(?P<append>>>)?\s*(?P<filename>.+)$"

    def __init__(self, args: ApplicationConfiguration) -> None:
        """Initialize the ``:write`` action.

        Args:
            args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    def _determine_file_mode(
        self,
        filename: str,
        match: dict[str, str],
    ) -> str | None:
        """Determine the file open mode based on append/force flags.

        Args:
            filename: The resolved filename path
            match: The regex match groupdict from the interaction

        Returns:
            The file mode string ('a' or 'w'), or None if the operation should be aborted
        """
        if match["append"]:
            if not Path(filename).exists() and not match["force"]:
                self._logger.warning(
                    "Append operation failed because %s does not exist, force with !",
                    filename,
                )
                return None
            return "a"

        if Path(filename).exists() and not match["force"]:
            self._logger.warning(
                "Write operation failed because %s exists, force with !",
                filename,
            )
            return None
        return "w"

    @staticmethod
    def _resolve_content(interaction: Interaction) -> Any:
        """Resolve the content to write from the interaction.

        Args:
            interaction: The interaction from the user

        Returns:
            The content object to be written
        """
        if interaction.content:
            return interaction.content.showing

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
            return obj

        return None

    @staticmethod
    def _write_content(
        obj: Any,
        filename: str,
        file_mode: str,
        write_as: str,
    ) -> None:
        """Write the resolved content to a file in the determined format.

        Args:
            obj: The content to write
            filename: The target file path
            file_mode: The file open mode ('a' or 'w')
            write_as: The file extension determining serialization format
        """
        if write_as == ".txt":
            file = expand_path(filename)
            with file.open(file_mode, encoding="utf-8") as fh:
                fh.write(obj)
        elif write_as == ".yaml":
            serialize_write_file(
                content=obj,
                content_view=ContentView.NORMAL,
                file=Path(filename),
                file_mode=file_mode,
                serialization_format=SerializationFormat.YAML,
            )
        elif write_as == JSON_EXTENSION:
            serialize_write_file(
                content=obj,
                content_view=ContentView.NORMAL,
                file=Path(filename),
                file_mode=file_mode,
                serialization_format=SerializationFormat.JSON,
            )

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Execute the ``:write`` request for mode interactive.

        Args:
            interaction: The interaction from the user
            app: The app instance

        Returns:
            Nothing
        """
        self._logger.debug("write requested as %s", interaction.action.value)
        match = interaction.action.match.groupdict()
        filename = str(expand_path(match["filename"]))

        file_mode = self._determine_file_mode(filename, match)
        if file_mode is None:
            return

        obj = self._resolve_content(interaction)

        if isinstance(obj, str):
            write_as = ".txt"
        elif re.match(r"^.*\.y(?:a)?ml$", filename):
            write_as = ".yaml"
        elif filename.endswith(".json"):
            write_as = ".json"
        else:
            write_as = interaction.ui.content_format().value.file_extension

        self._write_content(obj, filename, file_mode, write_as)
        self._logger.info("Wrote to '%s' with mode '%s' as '%s'", filename, file_mode, write_as)
