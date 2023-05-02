"""The settings file migration base class."""
from __future__ import annotations

from ansible_navigator.content_defs import ContentView
from ansible_navigator.content_defs import SerializationFormat
from ansible_navigator.utils.ansi import COLOR
from ansible_navigator.utils.ansi import changed
from ansible_navigator.utils.ansi import info
from ansible_navigator.utils.serialize import Loader
from ansible_navigator.utils.serialize import serialize_write_file
from ansible_navigator.utils.serialize import yaml

from .definitions import Migration


class SettingsFile(Migration):
    """The settings file migration base class."""

    name = "Settings file migration base class"

    def __init__(self):
        """Initialize the settings file migration."""
        super().__init__()
        self.content: dict = {}
        self._backup_suffix = ".v0"

    def run(self, *args, **kwargs) -> None:
        """Perform the settings file migration.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        """
        if not self.content:
            with self.settings_file_path.open("r", encoding="utf-8") as f:
                try:
                    self.content = yaml.load(f, Loader=Loader)
                except (yaml.scanner.ScannerError, yaml.parser.ParserError):
                    return

        if not self.content:
            return

        # Check if any of the migrations are needed
        if self.check:
            self.run_steps()
            self.was_needed = self.needed_now
            return

        # Not check and wasn't needed
        if not self.was_needed:
            return

        self.run_steps()

        # Something may have gone wrong
        if self.needed_now:
            return

        # Back up the current
        backup = self.settings_file_path.rename(
            self.settings_file_path.with_suffix(self._backup_suffix),
        )
        info(color=COLOR, message=f"Backup: {backup}")

        # Write the new file
        if self.settings_file_path.suffix in (".yml", ".yaml"):
            serialization_format = SerializationFormat.YAML
        elif self.settings_file_path.suffix == ".json":
            serialization_format = SerializationFormat.JSON

        serialize_write_file(
            content=self.content,
            content_view=ContentView.NORMAL,
            file_mode="w",
            file=self.settings_file_path,
            serialization_format=serialization_format,
        )
        changed(color=COLOR, message=f"Updated: {self.settings_file_path}")

        return
