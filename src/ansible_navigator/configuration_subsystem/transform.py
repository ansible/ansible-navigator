"""Methods of transforming the settings."""

from typing import Dict

from ..content_defs import ContentView
from ..utils.serialize import SerializationFormat
from ..utils.serialize import serialize
from .definitions import ApplicationConfiguration
from .definitions import Constants
from .defs_presentable import PresentableSettingsEntries
from .defs_presentable import PresentableSettingsEntry
from .schema import PARTIAL_SCHEMA


def to_presentable(settings: ApplicationConfiguration) -> PresentableSettingsEntries:
    """Transform the current settings into a structure that can be presented with the TUI.

    :param settings: The current settings
    :returns: The settings represented as a list of dictionaries
    """
    settings_list = []

    all_subcommands = sorted([subcommand.name for subcommand in settings.subcommands])

    settings_file_entry = PresentableSettingsEntry.for_settings_file(
        all_subcommands=all_subcommands,
        application_name=settings.application_name_dashed,
        internals=settings.internals,
    )
    settings_list.append(settings_file_entry)

    settings_file_path = settings_file_entry.current_settings_file
    for entry in settings.entries:
        human_readable_entry = PresentableSettingsEntry.from_settings_entry(
            entry=entry,
            all_subcommands=all_subcommands,
            application_name_dashed=settings.application_name_dashed,
            settings_file_path=settings_file_path,
        )
        settings_list.append(human_readable_entry)

    settings_list.sort()
    return PresentableSettingsEntries(tuple(settings_list))


def to_schema(settings: ApplicationConfiguration) -> str:
    """Build a json schema from the settings using the stub schema.

    :param settings: The application settings
    :returns: The json schema
    """
    for entry in settings.entries:
        subschema: Dict = PARTIAL_SCHEMA["properties"]
        dot_parts = entry.settings_file_path(prefix=settings.application_name_dashed).split(".")
        for part in dot_parts[:-1]:
            if isinstance(subschema, dict):
                subschema = subschema.get(part, {}).get("properties")
        subschema[dot_parts[-1]]["description"] = entry.short_description
        if entry.choices:
            subschema[dot_parts[-1]]["enum"] = entry.choices
        if entry.value.default is not Constants.NOT_SET:
            subschema[dot_parts[-1]]["default"] = entry.value.default

    PARTIAL_SCHEMA["version"] = settings.application_version
    return serialize(
        content=PARTIAL_SCHEMA,
        content_view=ContentView.NORMAL,
        serialization_format=SerializationFormat.JSON,
    )
