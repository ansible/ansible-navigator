"""Methods of transforming the settings."""

from .definitions import ApplicationConfiguration
from .defs_presentable import PresentableSettingsEntries
from .defs_presentable import PresentableSettingsEntry


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
