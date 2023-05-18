"""Methods of transforming the settings."""
from __future__ import annotations

import json
import textwrap

from typing import Any

from ansible_navigator.utils.dict_merge import in_place_list_replace
from ansible_navigator.utils.functions import shlex_join
from ansible_navigator.utils.packaged_data import retrieve_content

from .definitions import ApplicationConfiguration
from .definitions import Constants
from .definitions import SettingsEntry
from .definitions import SettingsFileType
from .defs_presentable import PresentableSettingsEntries
from .defs_presentable import PresentableSettingsEntry
from .utils import create_settings_file_sample


def to_effective(
    settings: ApplicationConfiguration,
) -> SettingsFileType:
    """Transform the current settings into a settings file.

    :param settings: The current settings
    :returns: The settings represented as settings file
    """
    rebuilt: dict = {}
    for entry in settings.entries:
        path = entry.settings_file_path(prefix=settings.application_name_dashed)
        if not isinstance(entry.value.current, Constants):
            current: bool | int | str | dict | list = entry.value.current
            # It is necessary to un post-process here
            if path == "ansible-navigator.ansible.cmdline":
                # post-processed into a list
                current = shlex_join(entry.value.current)
            elif path == "ansible-navigator.execution-environment.volume-mounts":
                current = []
                for mount in entry.value.current:
                    parts = mount.split(":")
                    v_mount = {"src": parts[0], "dest": parts[1]}
                    if len(parts) == 3:
                        v_mount["options"] = parts[2]
                    current.append(v_mount)

            partial = create_settings_file_sample(
                settings_path=path,
                placeholder=current,
            )
            in_place_list_replace(rebuilt, partial)
    return SettingsFileType(rebuilt)


def to_sources(settings: ApplicationConfiguration) -> dict[str, str]:
    """Transform the current settings into representation of sources.

    :param settings: The current settings
    :returns: The settings sourced represented as a dictionary of path, source
    """
    sources = {}
    for entry in settings.entries:
        path = entry.settings_file_path(prefix=settings.application_name_dashed)
        sources[path] = str(entry.value.source)
    sources["settings_file_path"] = str(settings.internals.settings_file_path)
    sources["settings_file_source"] = str(settings.internals.settings_source)
    return sources


def to_presentable(settings: ApplicationConfiguration) -> PresentableSettingsEntries:
    """Transform the current settings into a structure that can be presented with the TUI.

    :param settings: The current settings
    :returns: The settings represented as a list of dictionaries
    """
    settings_list = []

    all_subcommands = sorted(subcommand.name for subcommand in settings.subcommands)

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


def to_schema(settings: ApplicationConfiguration) -> dict[str, Any]:
    """Build a json schema from the settings using the stub schema.

    :param settings: The application settings
    :returns: The json schema
    """
    file_contents = retrieve_content("settings-schema.partial.json")
    partial_schema = json.loads(file_contents)

    for entry in settings.entries:
        subschema: dict = partial_schema["properties"]
        dot_parts = entry.settings_file_path(prefix=settings.application_name_dashed).split(".")
        for part in dot_parts[:-1]:
            if isinstance(subschema, dict):
                subschema = subschema.get(part, {}).get("properties")
        subschema[dot_parts[-1]]["description"] = entry.short_description
        if entry.choices:
            # choice may be a tuple, so make a list
            choices = list(entry.choices)
            if subschema[dot_parts[-1]].get("type") == "array":
                # A list of items
                subschema[dot_parts[-1]]["items"]["enum"] = choices
            else:
                # A single item
                subschema[dot_parts[-1]]["enum"] = choices
        if entry.value.schema_default is not Constants.NOT_SET:
            if entry.value.schema_default is not Constants.NONE:
                subschema[dot_parts[-1]]["default"] = entry.value.schema_default
        elif entry.value.default is not Constants.NOT_SET:
            subschema[dot_parts[-1]]["default"] = entry.value.default

    if isinstance(settings.application_version, Constants):
        version = settings.application_version.value
    else:
        version = settings.application_version
    # get only major version info for the schema:
    version = ".".join(version.split(".")[:1])

    partial_schema["version"] = version
    partial_schema["title"] = partial_schema["title"].format(version=version)

    return partial_schema


def to_sample(settings: ApplicationConfiguration) -> tuple[str, str]:
    """Load and clean the settings sample.

    :param settings: The application settings
    :returns: One selectively commented sample, one uncommented
    """
    # pylint: disable=too-many-locals

    file_contents = retrieve_content(filename="settings-sample.template.yml").splitlines()

    # Remove anything before the `---`
    yaml_doc_start = file_contents.index("---")

    template_lines = file_contents[yaml_doc_start:]

    # Find all anchors
    indices: list[tuple[str, int, SettingsEntry]] = []
    for entry in settings.entries:
        dot_path = entry.settings_file_path(prefix="")
        indent = "  " * len(dot_path.split("."))  # indent 2 spaces for each part
        comment_index = template_lines.index(f"{indent}# {{{{ {dot_path} }}}}")
        indices.append((indent, comment_index, entry))

    # Replace anchors with the short description
    sorted_entries = sorted(indices, key=lambda t: -t[1])
    for indent, comment_index, entry in sorted_entries:
        description = [f"{indent}# {line}" for line in textwrap.wrap(entry.short_description)]
        template_lines = (
            template_lines[0:comment_index] + description + template_lines[comment_index + 1 :]
        )

    populated_lines = template_lines

    no_comment = ["---", "ansible-navigator:", "logging:", "level: debug", "append: False"]
    commented_lines = []
    for line in populated_lines:
        if any(entry in line for entry in no_comment):
            commented_lines.append(line)
        else:
            commented_lines.append(f"# {line}")

    commented = "\n".join(commented_lines) + "\n"
    uncommented = "\n".join(populated_lines) + "\n"

    return commented, uncommented
