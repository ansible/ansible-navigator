""" Build the argpaser
"""

from argparse import ArgumentParser
from argparse import SUPPRESS

from .definitions import Config


class Parser:
    """Build the args"""

    # pylint: disable=too-few-public-methods
    def __init__(self, config: Config):
        self._config = config
        self._base_parser = ArgumentParser(add_help=False)
        self._configure_base()
        self.parser = ArgumentParser(parents=[self._base_parser])
        self._subparsers = self.parser.add_subparsers(
            title="Subcommands",
            help="additional help",
            dest="app",
            metavar="{command} --help",
        )
        self._configure_subparsers()

    def _add_parser(self, parser, entry) -> None:
        if not entry.internal:
            help_str = f"{entry.description} (default: {entry.value.default})"
            params = {"default": SUPPRESS, "help": help_str}
            params.update(entry.argparse_params)
            if entry.cli_parameters is None:
                parser.add_argument(entry.name, **params)
            else:
                params["dest"] = entry.name
                parser.add_argument(entry.cli_parameters.short, entry.cli_parameters.long, **params)


    def _configure_base(self) -> None:
        for entry in self._config.entries:
            if not entry.subcommands:
                self._add_parser(self._base_parser, entry)

    def _configure_subparsers(self) -> None:
        for subcommand in self._config.subcommands:
            parser = self._subparsers.add_parser(
                subcommand.name,
                help=subcommand.description,
                description=f"{subcommand.name}: {subcommand.description}",
                parents=[self._base_parser],
            )
            for entry in self._config.entries:
                if subcommand.name in entry.subcommands:
                    self._add_parser(parser, entry)
