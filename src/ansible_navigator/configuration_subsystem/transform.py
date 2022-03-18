"""Methods of transforming the settings."""

import textwrap

from typing import Dict
from typing import List
from typing import Tuple

from ..content_defs import ContentView
from ..utils.compatibility import importlib_resources
from ..utils.serialize import SerializationFormat
from ..utils.serialize import serialize
from .definitions import ApplicationConfiguration
from .definitions import Constants
from .definitions import SettingsEntry
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


def to_sample(settings: ApplicationConfiguration) -> Tuple[str, str]:
    """Load and clean the settings sample.

    :param settings: The application settings
    :returns: One selectively commented sample, one uncommented
    """
    # pylint: disable=too-many-locals
    with importlib_resources.open_text(
        "ansible_navigator.package_data",
        "settings-sample.template.yml",
    ) as fh:

        file_contents = fh.read().splitlines()

    # Remove anything before the `---`
    yaml_doc_start = file_contents.index("---")

    template_lines = file_contents[yaml_doc_start:]

    # Find all anchors
    indices: List[Tuple[str, int, SettingsEntry]] = []
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
