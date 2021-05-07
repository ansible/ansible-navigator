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


from ..configuration_subsystem import NavigatorConfiguration
from ..configuration_subsystem.definitions import Entry

from ..utils import oxfordcomma

logger = logging.getLogger()

APP = "ansible-navigator"

PARAM_HEADER = (
    "Name",
    "Description",
    "Default",
    "Choices",
    "CLI paramters",
    "Environment variable",
    "Settings file (ansible-navigator.)",
)
RST_TABLE_HEADER = [
    ".. list-table:: {}",
    "  :header-rows: 1",
]
RST_FIRST_ROW_ENTRY = "  * - {}"
RST_ADDITONAL_ROW_ENTRY = "    - {}"


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
        data.append(RST_ADDITONAL_ROW_ENTRY.format(row_part))
    return data


def _params_generate_tables(param_details: Dict) -> List:
    """generate tables for paramters"""
    tables = []
    table = copy(RST_TABLE_HEADER)
    table[0] = table[0].format("General parameters")
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
            table = copy(RST_TABLE_HEADER)
            table[0] = table[0].format(f"Subcommand: {subcommand.name}")
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
                f"{entry.cli_parameters.short} or"
                " --{entry.cli_parameters.long_override or entry.name_dashed}"
            )
        else:
            cli_parameters = "positional"

    path = entry.settings_file_path(APP) + ".default-value-override"
    default_override = _params_get_param_file_entry(param_details=param_details, path=path)
    if isinstance(default_override, str):
        default = default_override
    else:
        if isinstance(entry.value.default, str):
            default = entry.value.default
        else:
            default = "No default value set"

    choices = oxfordcomma(entry.choices, "or")
    row = (
        entry.name_dashed,
        entry.short_description,
        default,
        choices,
        cli_parameters,
        entry.environment_variable(APP.replace("-", "_")),
        entry.settings_file_path("")[1:],
    )
    return row


def _subcommands_generate_tables() -> List:
    """generate the subcommand table"""
    table = RST_TABLE_HEADER
    table[0] = table[0].format("Available subcommands")
    table.append("")
    table.extend(
        _rst_generate_row(("Name", "Description", "CLI Example", "Colon command", "Description"))
    )
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
        start = current.index(f"  start-{marker}-tables")
        end = current.index(f"  end-{marker}-tables")
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
    _update_file(tables, filename, "parameters")


def _update_subcommands_tables(args: Namespace, filename: str):
    """update the table of subcommands"""
    # pylint: disable=unused-argument
    tables = _subcommands_generate_tables()
    _update_file(tables, filename, "subcommands")


def main():
    """
    The entry point
    """
    doc_dir = os.path.realpath(os.path.join(__file__, "..", "..", "..", "docs"))

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--pt",
        "--param_table_file",
        help="The path to the file containing the parameter table",
        default=os.path.join(doc_dir, "configuration.rst"),
    )
    parser.add_argument(
        "--pd",
        "--param_details_file",
        help="The path to the file containing the parameter details",
        default=os.path.join(doc_dir, "param_details.yml"),
    )
    parser.add_argument(
        "--sf",
        "--subcommand_file",
        help="The path to the file containing the subcommand table",
        default=os.path.join(doc_dir, "subcommands.rst"),
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
    logger.setLevel(getattr(logging, args.ll.upper()))

    args.pd = os.path.abspath(os.path.expanduser(args.pd))
    args.pt = os.path.abspath(os.path.expanduser(args.pt))
    args.sf = os.path.abspath(os.path.expanduser(args.sf))

    if args.diff:
        errors = []
        for entry in ((args.pt, _update_params_tables), (args.sf, _update_subcommands_tables)):
            current = entry[0]
            update_func = entry[1]
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, os.path.basename(current))
            copyfile(current, temp_file)
            update_func(args, temp_file)
            different = _file_diff(current, temp_file)
            if different:
                errors.extend([current] + different)
        if errors:
            errors.insert(0, "Documentation update required, run the doc updater")
            sys.exit("\n".join(errors))
    else:
        _update_params_tables(args, args.pt)
        _update_subcommands_tables(args, args.sf)


if __name__ == "__main__":
    main()
