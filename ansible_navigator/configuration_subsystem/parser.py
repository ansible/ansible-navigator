""" Build the argpaser
"""

from argparse import ArgumentParser
from argparse import _SubParsersAction
from argparse import SUPPRESS

from typing import Any
from typing import Dict
from typing import Tuple
from typing import Union

from .definitions import ApplicationConfiguration
from .definitions import Constants as C

from ..utils import oxfordcomma
from .._version import __version__


class Parser:
    """Build the args"""

    # pylint: disable=too-few-public-methods
    def __init__(self, config: ApplicationConfiguration):
        self._config = config
        self._base_parser = ArgumentParser(add_help=False)
        self._configure_base()
        self.parser = ArgumentParser(parents=[self._base_parser])
        self._subparsers = self._add_subcommand_holder()
        self._configure_subparsers()

    @staticmethod
    def generate_argument(entry) -> Tuple[Any, Union[Any, str, None], Dict[str, Any]]:
        """Generate an argparse argument"""
        kwargs = {}
        help_strings = [entry.short_description]
        if entry.choices:
            lower_choices = (str(choice).lower() for choice in entry.choices)
            help_strings.append(f"(choices: {oxfordcomma(lower_choices, 'or')})")
        if entry.value.default is not C.NOT_SET:
            help_strings.append(f"(default: '{str(entry.value.default).lower()}')")
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

        if entry.cli_parameters.metavar is not None:
            kwargs["metavar"] = entry.cli_parameters.metavar

        if entry.cli_parameters.action is not None:
            kwargs["action"] = entry.cli_parameters.action

        return entry.cli_parameters.short, long, kwargs

    def _add_parser(self, parser, entry) -> None:
        if entry.cli_parameters:
            short, long, kwargs = self.generate_argument(entry)
            if not all((short, long)):
                parser.add_argument(entry.name, **kwargs)
            else:
                parser.add_argument(short, long, **kwargs)

    def _add_subcommand_holder(self) -> _SubParsersAction:
        subcommand_value = [
            entry for entry in self._config.entries if entry.subcommand_value is True
        ]
        if len(subcommand_value) == 0:
            raise ValueError("No entry with subparser value defined")
        if len(subcommand_value) > 1:
            raise ValueError("Multiple entries with subparser value defined")
        entry = subcommand_value[0]
        return self.parser.add_subparsers(
            title=entry.short_description,
            dest=entry.name,
            metavar="{subcommand} --help",
        )

    def _configure_base(self) -> None:
        self._base_parser.add_argument(
            "--version", action="version", version="%(prog)s " + __version__
        )

        for entry in self._config.entries:
            if entry.subcommands is C.ALL:
                self._add_parser(self._base_parser, entry)

    def _configure_subparsers(self) -> None:
        for subcommand in self._config.subcommands:
            parser = self._subparsers.add_parser(
                subcommand.name,
                epilog=subcommand.epilog,
                help=subcommand.description,
                description=f"{subcommand.name}: {subcommand.description}",
                parents=[self._base_parser],
            )
            for entry in self._config.entries:
                if isinstance(entry.subcommands, list) and subcommand.name in entry.subcommands:
                    self._add_parser(parser, entry)
