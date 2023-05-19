"""Scripts that generates documentation from the settings definitions."""
from __future__ import annotations

import logging

from copy import copy
from pathlib import Path
from re import match

import mkdocs_gen_files

from ansible_navigator.configuration_subsystem import Constants as C
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.definitions import SettingsEntry
from ansible_navigator.utils.functions import oxfordcomma
from ansible_navigator.version import __version__


logger = logging.getLogger(__name__)

DOCS_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = DOCS_DIR.parent.parent
TEST_SETTINGS_FIXTURE = (
    PROJECT_DIR
    / "tests"
    / "fixtures"
    / "unit"
    / "configuration_subsystem"
    / "ansible-navigator.yml"
)
DOCS_SETTINGS_SAMPLE = PROJECT_DIR / "docs" / ".generated" / "ansible-navigator.yml"
DOCS_SETTINGS_DUMP = PROJECT_DIR / "docs" / ".generated" / "settings-dump.md"
DOCS_SUBCOMMANDS_OVERVIEW = PROJECT_DIR / "docs" / ".generated" / "subcommands-overview.md"

APP = "ansible-navigator"

PARAM_TABLE_HEADER = [
    "## {}",
    "",
    "",
]
SUBCOMMAND_TABLE_HEADER = [
    "## {}",
    "",
]


def _mk_row(row: tuple) -> list:
    """Convert a row as a markdown definition list entry.

    :param row: The row tuple, with name, description and list of options
    :returns: a list of markdown strings
    """
    result = f'{row[0]} [¶](#{row[0]}){{: class="headerlink" }} {{ #{row[0]} }}\n\n:   {row[1]}\n\n'
    for entry in row[2:]:
        result += f"    {entry}\n\n"
    return [result]


def md_settings_dump() -> str:
    """Generate a table for each subcommand's settings parameters.

    :returns: A list of tables, one each for each subcommand
    """
    lines: list[str] = []
    table = copy(PARAM_TABLE_HEADER)
    table[0] = table[0].format("General parameters")
    table.append("")

    for entry in NavigatorConfiguration.entries:
        if not isinstance(entry.subcommands, list):
            row = _params_row_for_entry(
                entry=entry,
            )
            table.extend(_mk_row(row))
    lines.append("\n".join(table))
    for subcommand in NavigatorConfiguration.subcommands:
        logger.debug("Processing subcommand: %s", subcommand.name)
        entries = [
            entry
            for entry in NavigatorConfiguration.entries
            if isinstance(entry.subcommands, list) and subcommand.name in entry.subcommands
        ]
        logger.debug("  params %s", tuple(entry.name for entry in entries))
        if entries:
            table = copy(PARAM_TABLE_HEADER)
            table[0] = table[0].format(f"\n\n### Subcommand: {subcommand.name}")
            table.append("")
            for entry in entries:
                row = _params_row_for_entry(
                    entry=entry,
                )
                table.extend(_mk_row(row))
            lines.append("\n".join(table))
            # lines.extend(["", "|", ""])
    return "\n".join(lines)


def _params_row_for_entry(entry: SettingsEntry) -> tuple:
    # pylint: disable=too-many-branches
    """Create a row entry for one settings parameter.

    :param entry: The settings entry for which the row will be generated
    :return: A tuple describing the settings parameter
    """
    if entry.cli_parameters is None:
        cli_parameters = "positional"
    else:
        if entry.cli_parameters.short:
            if entry.cli_parameters.long_override:
                long = entry.cli_parameters.long_override
            else:
                long = f"--{entry.name_dashed}"
            cli_parameters = f"``{entry.cli_parameters.short}`` or ``{long}``"
        else:
            cli_parameters = "positional"

    path = entry.settings_file_path("ansible-navigator")
    indent = 4
    yaml_like = ["", "```yaml title='Settings'", ""]
    for idx, path_part in enumerate(path.split(".")):
        yaml_like.append(f"{(2*idx+indent) * ' '}{path_part}:")
    yaml_like.append("```\n")

    if entry.value.schema_default is not C.NOT_SET:
        default = entry.value.schema_default
    elif entry.value.default is not C.NOT_SET:
        default = entry.value.default
    else:
        default = "No default value set"

    choices = oxfordcomma(entry.choices, "or")
    env_var = entry.environment_variable(APP.replace("-", "_"))

    settings = []
    settings.append(f"**Added in version:** {entry.version_added}")
    if choices:
        settings.append(f"**Choices:** {choices}")
    if default is not None:
        settings.append(f"**Default:** {default}")
    if cli_parameters is not None:
        settings.append(f"**CLI:** {cli_parameters}")
    if env_var is not None:
        settings.append(f"**ENV:** {env_var}")

    settings.extend([f"\n{indent * ' '}".join(yaml_like)])

    row = (entry.name_dashed, entry.short_description, *settings)
    return row


def _subcommands_overview() -> str:
    """Generate the subcommand table.

    :returns: A list of available subcommands
    """
    table = SUBCOMMAND_TABLE_HEADER
    table[0] = table[0].format("Available subcommands")
    table.append("")
    for subcommand in NavigatorConfiguration.subcommands:
        table.append(f"\n{subcommand.name}")
        table.append(f"\n:   {subcommand.description}")
        table.append(f"\n    CLI Example: `ansible-navigator {subcommand.name} --help`")
        table.append(f"\n    Colon command: `:{subcommand.name}`")
        table.append(f"\n    Version added: `:{subcommand.version_added}`")
    return "\n".join(table)


def md_settings_sample() -> str:
    """Generate markdown for navigator settings.

    :returns: a markdown string
    """
    sample_settings = ["```yaml title='Settings'", ""]
    settings = TEST_SETTINGS_FIXTURE.read_text().splitlines()
    not_commented = ["---", "ansible-navigator:", "logging:", "level:"]
    for idx, line in enumerate(settings):
        if idx != 2 and match(r"\s{2}\S", line):
            sample_settings.append("#")
        if not any(nc in line for nc in not_commented):
            sample_settings.append("# " + line)
        else:
            sample_settings.append(line)
    sample_settings.append("```")
    result = "\n".join(sample_settings)
    return result


with mkdocs_gen_files.open(DOCS_SETTINGS_SAMPLE, "w") as f:
    f.write(md_settings_sample())

with mkdocs_gen_files.open(DOCS_SETTINGS_DUMP, "w") as f:
    f.write(md_settings_dump())

with mkdocs_gen_files.open(DOCS_SUBCOMMANDS_OVERVIEW, "w") as f:
    f.write(_subcommands_overview())
