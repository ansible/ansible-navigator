""" documentation updater
"""
import difflib
import logging
import os
import sys
import tempfile

from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from argparse import Namespace

from copy import copy
from shutil import copyfile
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import yaml


from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.definitions import Entry

from ansible_navigator.utils import oxfordcomma

logger = logging.getLogger()

APP = "ansible-navigator"

PARAM_HEADER = ("Name", "Description", "Settings")
PARAM_TABLE_HEADER = [
    ".. list-table:: {}",
    "  :widths: 2 3 5",
    "  :header-rows: 1",
]
RST_FIRST_ROW_ENTRY = "  * - {}"
RST_ADDITONAL_ROW_ENTRY = "    - {}"
RST_NL_CELL_FIRST = "    - | {}"
RST_NL_IN_CELL = "      | {}"
SUBCOMMAND_TABLE_HEADER = [
    ".. list-table:: {}",
    "  :widths: 1 3 3 1",
    "  :header-rows: 1",
]


def _file_diff(current: str, should_be: str):
    """diff 2 files"""
    with open(current, "r") as current_f:
        with open(should_be, "r") as should_f:
            diff = difflib.unified_diff(
                current_f.read().splitlines(),
                should_f.read().splitlines(),
                fromfile="current",
                tofile="should_be",
            )
    return list(diff)


def _rst_generate_row(row: Tuple) -> List:
    """generate an r for an rst list table"""
    data = []
    data.append(RST_FIRST_ROW_ENTRY.format(row[0]))
    for row_part in row[1:]:
        if isinstance(row_part, str):
            data.append(RST_ADDITONAL_ROW_ENTRY.format(row_part))
        elif isinstance(row_part, tuple):
            data.append(RST_NL_CELL_FIRST.format(row_part[0]))
            for nl_cell in row_part[1:]:
                if isinstance(nl_cell, str):
                    data.append(RST_NL_IN_CELL.format(nl_cell))
                elif isinstance(nl_cell, list):
                    data.extend(nl_cell)
    return data


def _params_generate_tables(param_details: Dict) -> List:
    """generate tables for paramters"""
    tables = []
    table = copy(PARAM_TABLE_HEADER)
    table[0] = table[0].format("**General parameters**")
    table.append("")
    table.extend(_rst_generate_row(PARAM_HEADER))

    for entry in NavigatorConfiguration.entries:
        if not isinstance(entry.subcommands, list):
            row = _params_row_for_entry(entry=entry, param_details=param_details)
            table.extend(_rst_generate_row(row))
    tables.extend(table)
    tables.extend(["", "|", "|", ""])
    for subcommand in NavigatorConfiguration.subcommands:
        entries = [
            entry
            for entry in NavigatorConfiguration.entries
            if isinstance(entry.subcommands, list) and subcommand.name in entry.subcommands
        ]
        if entries:
            table = copy(PARAM_TABLE_HEADER)
            table[0] = table[0].format(f"**Subcommand: {subcommand.name}**")
            table.append("")
            table.extend(_rst_generate_row(PARAM_HEADER))
            for entry in entries:
                row = _params_row_for_entry(entry=entry, param_details=param_details)
                table.extend(_rst_generate_row(row))
            tables.extend(table)
            tables.extend(["", "|", ""])
    return tables


def _params_get_param_file_entry(param_details: Dict, path: str) -> Union[None, Dict[Any, Any]]:
    """get a param from the details files"""
    path_parts = path.split(".")
    data = param_details
    try:
        for key in path_parts:
            data = data[key]
        return data
    except KeyError:
        return None


def _params_retrieve_details(filename: str) -> Dict:
    """load the param details file"""
    with open(filename) as fhand:
        details = yaml.load(fhand, Loader=yaml.SafeLoader)
        return details


def _params_row_for_entry(entry: Entry, param_details: Dict) -> Tuple:
    """create a row entry for a param"""
    if entry.cli_parameters is None:
        cli_parameters = "positional"
    else:
        if entry.cli_parameters.short:
            cli_parameters = (
                f"`{entry.cli_parameters.short}` or"
                f" `--{entry.cli_parameters.long_override or entry.name_dashed}`"
            )
        else:
            cli_parameters = "positional"

    path = entry.settings_file_path("ansible-navigator")
    yaml_like = ["", "      .. code-block:: yaml", ""]
    for idx, path_part in enumerate(path.split(".")):
        yaml_like.append(f"{(2*idx+12) * ' '}{path_part}:")
    yaml_like.append("")

    path = entry.settings_file_path(APP) + ".default-value-override"
    default_override = _params_get_param_file_entry(param_details=param_details, path=path)
    logging.debug("%s: default_value_override: %s", entry.name, default_override)
    if isinstance(default_override, str):
        default = default_override
    else:
        if isinstance(entry.value.default, str):
            default = entry.value.default
        else:
            default = "No default value set"

    choices = oxfordcomma(entry.choices, "or")
    envvar = entry.environment_variable(APP.replace("-", "_"))

    settings = []
    if choices:
        settings.append(f"**Choices:** {choices}")
    if default is not None:
        settings.append(f"**Default:** {default}")
    if cli_parameters is not None:
        settings.append(f"**CLI:** {cli_parameters}")
    if envvar is not None:
        settings.append(f"**ENV:** {envvar}")
    if yaml_like is not None:
        settings.extend(["**Settings file:**", yaml_like])

    row = (entry.name_dashed, entry.short_description, tuple(settings))
    return row


def _subcommands_generate_tables() -> List:
    """generate the subcommand table"""
    table = SUBCOMMAND_TABLE_HEADER
    table[0] = table[0].format("Available subcommands")
    table.append("")
    table.extend(_rst_generate_row(("Name", "Description", "CLI Example", "Colon command")))
    for subcommand in NavigatorConfiguration.subcommands:
        subcommand_details = (
            subcommand.name,
            subcommand.description,
            f"ansible-navigator {subcommand.name} --help",
            f":{subcommand.name}",
        )
        table.extend(_rst_generate_row(subcommand_details))
    return table


def _update_file(content: List, filename: str, marker: str) -> None:
    """insert text into a file given a marker"""
    try:
        with open(filename) as fhand:
            current = fhand.read().splitlines()
    except FileNotFoundError:
        logging.error("%s not found", filename)
        sys.exit(1)
    try:
        start = current.index(f"  start-{marker}")
        end = current.index(f"  end-{marker}")
    except ValueError:
        logging.error("Content anchors not found in %s", filename)
        sys.exit(1)
    if start and end:
        new = current[0 : start + 1] + content + current[end - 1 :]
        with open(filename, "w") as fhand:
            fhand.write("\n".join(new))
            fhand.write("\n")
        logging.info("%s updated", filename)


def _update_params_tables(args: Namespace, filename: str):
    """update the tables of parameters"""
    param_details = _params_retrieve_details(args.pd)
    tables = _params_generate_tables(param_details)
    _update_file(tables, filename, "parameters-tables")


def _update_sample_settings(args: Namespace, filename: str):
    """update the settings sample"""
    with open(args.ss) as fhand:
        settings = fhand.read().splitlines()
    not_commented = ["ansible-navigator:", "logging:", "level:"]
    for idx, line in enumerate(settings):
        if not any(nc in line for nc in not_commented):
            settings[idx] = "    # " + line
        else:
            settings[idx] = "    " + line
    settings = [".. code-block:: yaml", ""] + settings
    _update_file(settings, filename, "settings-sample")


def _update_subcommands_tables(args: Namespace, filename: str):
    """update the table of subcommands"""
    # pylint: disable=unused-argument
    tables = _subcommands_generate_tables()
    _update_file(tables, filename, "subcommands-table")


def main():
    """
    The entry point
    """
    doc_dir = os.path.realpath(os.path.join(__file__, "..", "..", "docs"))

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--pts",
        "--param-table-settings-file",
        help="The path to the file containing the parameter table and setting example",
        default=os.path.join(doc_dir, "settings.rst"),
    )
    parser.add_argument(
        "--pd",
        "--param-details-file",
        help="The path to the file containing the parameter details",
        default=os.path.join(doc_dir, "param_details.yml"),
    )
    parser.add_argument(
        "--sf",
        "--subcommand-file",
        help="The path to the file containing the subcommand table",
        default=os.path.join(doc_dir, "subcommands.rst"),
    )
    parser.add_argument(
        "--ss",
        "--settings_source",
        help="The path to the settings source",
        default=os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "tests",
                "fixtures",
                "unit",
                "configuration_subsystem",
                "ansible-navigator.yml",
            )
        ),
    )
    parser.add_argument(
        "--diff", dest="diff", help="Only check for differences", action="store_true"
    )
    parser.add_argument(
        "--ll",
        "--log-level",
        help="Set the log level",
        choices=["debug", "info", "warning", "error", "critical"],
        default="error",
    )

    args = parser.parse_args()
    hdlr = logging.StreamHandler()
    logger.setLevel(getattr(logging, args.ll.upper()))
    formatter = logging.Formatter(fmt="%(levelname)s '%(funcName)s' %(message)s")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    for arg in (args.pd, args.pts, args.sf):
        arg = os.path.abspath(os.path.expanduser(arg))

    updates = (
        (args.pts, _update_params_tables),
        (args.pts, _update_sample_settings),
        (args.sf, _update_subcommands_tables),
    )

    errors = []
    for entry in updates:
        current = entry[0]
        update_func = entry[1]
        if args.diff:
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, os.path.basename(current))
            copyfile(current, temp_file)
            update_func(args, temp_file)
            different = _file_diff(current, temp_file)
            if different:
                errors.extend([current] + different)
        else:
            entry[1](args, entry[0])

    if errors:
        errors.insert(0, "Documentation update required, run the doc updater")
        sys.exit("\n".join(errors))


if __name__ == "__main__":
    main()
