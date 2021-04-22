""" Build the args
https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html
"""
import os

from argparse import _SubParsersAction
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from argparse import HelpFormatter

from .config import NavigatorConfig
from .utils import Sentinel


def _abs_user_path(fpath):
    """don't overload the ap type"""
    return os.path.abspath(os.path.expanduser(fpath))


def str2bool(value):
    """convert some commonly used values
    to a boolean
    """
    # if isinstance(value, Sentinel):
    #     return value
    if isinstance(value, bool):
        return value
    if value.lower() in ("yes", "true", "t", "y", "1"):
        return True
    if value.lower() in ("no", "false", "f", "n", "0"):
        return False
    raise ArgumentTypeError("Boolean value expected.")


class CustomHelpFormatter(HelpFormatter):
    """sort the subcommands"""

    def _iter_indented_subactions(self, action):
        try:
            get_subactions = action._get_subactions  # pylint: disable=protected-access
        except AttributeError:
            pass
        else:
            self._indent()
            if isinstance(action, _SubParsersAction):
                for subaction in sorted(get_subactions(), key=lambda x: x.dest):
                    yield subaction
            else:
                for subaction in get_subactions():
                    yield subaction
            self._dedent()


class CliArgs:
    """Build the args"""

    # pylint: disable=too-few-public-methods
    def __init__(self, app_name: str):
        self._navigator_config = NavigatorConfig()

        self._app_name = app_name
        self._base_parser = ArgumentParser(add_help=False)
        self._base()
        self.parser = ArgumentParser(
            formatter_class=CustomHelpFormatter, parents=[self._base_parser]
        )
        self._subparsers = self.parser.add_subparsers(
            title="subcommands",
            description="valid subcommands",
            help="additional help",
            dest="app",
            metavar="{command} --help",
        )
        self._collections()
        self._config()
        self._doc()
        self._inventory()
        self._load()
        self._run()

    def _add_subparser(self, name: str, desc: str) -> ArgumentParser:
        return self._subparsers.add_parser(
            name,
            help=desc,
            description=f"{name}: {desc}",
            formatter_class=CustomHelpFormatter,
            parents=[self._base_parser],
        )

    def _base(self) -> None:
        self._editor_params(self._base_parser)
        self._ee_params(self._base_parser)
        self._inventory_columns(self._base_parser)
        self._log_params(self._base_parser)
        self._no_osc4_params(self._base_parser)
        self._mode(self._base_parser)

    def _collections(self) -> None:
        parser = self._add_subparser("collections", "Explore installed collections")
        parser.set_defaults(requires_ansible=True)

    def _config(self) -> None:
        self._add_subparser("config", "Explore the current ansible configuration")

    def _doc(self) -> None:
        parser = self._add_subparser("doc", "Show a plugin doc")
        self._doc_params(parser)

    def _doc_params(self, parser: ArgumentParser) -> None:
        parser.add_argument("value", metavar="plugin", help="The name of the plugin", type=str)

        self._navigator_config.add_argparse_argument('doc-plugin-type', parser)
        parser.set_defaults(requires_ansible=True)

    def _editor_params(self, parser: ArgumentParser) -> None:
        self._navigator_config.add_argparse_argument('editor-command', parser)
        self._navigator_config.add_argparse_argument('editor-console', parser)

    def _ee_params(self, parser: ArgumentParser) -> None:
        self._navigator_config.add_argparse_argument('container-engine', parser)
        self._navigator_config.add_argparse_argument('execution-environment', parser)
        self._navigator_config.add_argparse_argument('execution-environment-image', parser)
        self._navigator_config.add_argparse_argument('set-environment-variable', parser)
        self._navigator_config.add_argparse_argument('pass-environment-variable', parser)

    def _run(self) -> None:
        parser = self._add_subparser(
            "run", "Run Ansible playbook in either interactive or stdout mode"
        )
        self._playbook_params(parser)
        self._inventory_params(parser)

    def _inventory_columns(self, parser: ArgumentParser) -> None:
        self._navigator_config.add_argparse_argument('inventory-columns', parser)

    def _inventory(self) -> None:
        parser = self._add_subparser("inventory", "Explore inventories")
        self._inventory_params(parser)

    def _inventory_params(self, parser: ArgumentParser) -> None:
        self._navigator_config.add_argparse_argument('inventory', parser)

    def _load(self) -> None:
        parser = self._add_subparser("load", "Load an artifact")
        self._load_params(parser)

    @staticmethod
    def _load_params(parser: ArgumentParser) -> None:
        parser.add_argument(
            "value",
            default=None,
            help="The file name of the artifact",
            metavar="artifact",
            type=_abs_user_path,
        )
        parser.set_defaults(requires_ansible=False)

    def _log_params(self, parser: ArgumentParser) -> None:
        self._navigator_config.add_argparse_argument('log-file', parser)
        self._navigator_config.add_argparse_argument('log-level', parser)

    def _no_osc4_params(self, parser: ArgumentParser) -> None:
        self._navigator_config.add_argparse_argument('no-osc4', parser)

    def _playbook_params(self, parser: ArgumentParser) -> None:
        self._navigator_config.add_argparse_argument('playbook', parser)
        self._navigator_config.add_argparse_argument('playbook-artifact', parser)
        parser.set_defaults(requires_ansible=True)

    def _mode(self, parser: ArgumentParser) -> None:
        self._navigator_config.add_argparse_argument('mode', parser)
