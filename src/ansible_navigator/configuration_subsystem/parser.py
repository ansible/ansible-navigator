"""Build the argument parser."""
from __future__ import annotations

from argparse import SUPPRESS
from argparse import ArgumentParser
from argparse import HelpFormatter
from argparse import _SubParsersAction
from typing import Any

from .definitions import ApplicationConfiguration
from .definitions import Constants as C


class Parser:
    """Build the args."""

    def __init__(self, config: ApplicationConfiguration):
        """Initialize the command line interface parameter parser.

        :param config: The current settings for the application
        """
        self._config = config
        self._base_parser = ArgumentParser(add_help=False)
        self._configure_base()
        self.parser = ArgumentParser(
            parents=[self._base_parser],
            formatter_class=CustomHelpFormatter,
            add_help=False,
        )
        self._subparsers = self._add_subcommand_holder()
        self._configure_subparsers()

    @staticmethod
    def generate_argument(entry) -> tuple[Any, Any, dict[str, Any]]:
        """Generate an argparse argument.

        :param entry: Single settings entry
        :returns: Long and short cli parameters, and dictionary of parsed arguments
        """
        kwargs = {}
        help_strings = [entry.short_description]
        if entry.choices:
            lower_choices = (str(choice).lower() for choice in entry.choices)
            help_strings.append(f"({'|'.join(lower_choices)})")

        has_default = entry.value.default is not C.NOT_SET
        not_store = entry.cli_parameters.action not in ("store_true", "store_false")
        if has_default and not_store:
            help_strings.append(f"(default: {str(entry.value.default).lower()})")
        kwargs["help"] = " ".join(help_strings)

        kwargs["default"] = SUPPRESS

        if entry.cli_parameters.positional:
            long = None
            if entry.cli_parameters.nargs is None:
                kwargs["nargs"] = "?"
            else:
                kwargs["nargs"] = entry.cli_parameters.nargs
        else:
            long = entry.cli_parameters.long_override or f"--{entry.name_dashed}"
            kwargs["dest"] = entry.name
            if entry.cli_parameters.nargs is not None:
                kwargs["nargs"] = entry.cli_parameters.nargs
            if entry.cli_parameters.const is not None:
                kwargs["const"] = entry.cli_parameters.const

        if entry.cli_parameters.action is not None:
            kwargs["action"] = entry.cli_parameters.action

        return entry.cli_parameters.short, long, kwargs

    def _add_parser(self, group, entry) -> None:
        """Add a parser to the subparsers.

        :param group: The group to add the parser to
        :param entry: The entry to add
        """
        if entry.cli_parameters:
            short, long, kwargs = self.generate_argument(entry)
            if not all((short, long)):
                group.add_argument(entry.name, **kwargs)
            else:
                group.add_argument(short, long, **kwargs)

    def _add_subcommand_holder(self) -> _SubParsersAction:
        """Add the subparsers holder.

        :raises ValueError: if zero or more than one subcommand is found
        :returns: The subparsers action
        """
        subcommand_value = [
            entry for entry in self._config.entries if entry.subcommand_value is True
        ]
        if len(subcommand_value) == 0:
            msg = "No entry with subparser value defined"
            raise ValueError(msg)
        if len(subcommand_value) > 1:
            msg = "Multiple entries with subparser value defined"
            raise ValueError(msg)
        entry = subcommand_value[0]
        return self.parser.add_subparsers(
            title=entry.short_description,
            dest=entry.name,
            metavar="{subcommand} --help",
        )

    def _configure_base(self) -> None:
        """Configure the base parser."""
        group = self._base_parser.add_argument_group("Options (global)")
        group.add_argument(
            "-h",
            "--help",
            action="help",
            default=SUPPRESS,
            help="Show this help message and exit",
        )

        if isinstance(self._config.application_version, C):
            version = self._config.application_version.value
        else:
            version = self._config.application_version
        group.add_argument(
            "--version",
            action="version",
            help="Show the application version and exit",
            version="%(prog)s " + version,
        )

        for entry in self._config.entries:
            if entry.subcommands is C.ALL:
                self._add_parser(group=group, entry=entry)

    def _configure_subparsers(self) -> None:
        """Configure the subparsers."""
        for subcommand in self._config.subcommands:
            parser = self._subparsers.add_parser(
                subcommand.name,
                epilog=subcommand.epilog,
                help=subcommand.description,
                description=f"{subcommand.name}: {subcommand.description}",
                parents=[self._base_parser],
                formatter_class=CustomHelpFormatter,
                add_help=False,
            )
            group = parser.add_argument_group(f"Options ({subcommand.name} subcommand)")
            for entry in self._config.entries:
                if isinstance(entry.subcommands, list) and subcommand.name in entry.subcommands:
                    self._add_parser(group=group, entry=entry)


class CustomHelpFormatter(HelpFormatter):
    """A custom help formatter."""

    def __init__(self, prog):
        """Initialize the help formatter.

        :param prog: The program name
        """
        long_string = "--rac  --ansible-runner-rotate-artifacts-count"
        # 3 here accounts for the spaces in the ljust(6) below
        HelpFormatter.__init__(
            self,
            prog=prog,
            indent_increment=1,
            max_help_position=len(long_string) + 3,
        )

    def _format_action_invocation(self, action):
        """Format the action invocation.

        :param action: The action to format
        :raises ValueError: If more than 2 options are given
        :returns: The formatted action invocation
        """
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            (metavar,) = self._metavar_formatter(action, default)(1)
            return metavar

        if len(action.option_strings) == 1:
            return action.option_strings[0]

        if len(action.option_strings) == 2:
            # Account for a --1234 --long-option-name
            msg = f"{action.option_strings[0].ljust(6)} {action.option_strings[1]}"
            return msg
        msg = "Too many option strings"
        raise ValueError(msg)

    def _format_usage(self, usage, actions, groups, prefix):
        """Format the usage.

        :param usage: The usage
        :param actions: The actions
        :param groups: The groups
        :param prefix: The prefix
        :returns: The formatted usage
        """
        prefix = "Usage:" if prefix is None else ""
        options = "[options]" if actions else ""
        return " ".join(p for p in (prefix, self._prog, options) if p != "") + "\n\n"
