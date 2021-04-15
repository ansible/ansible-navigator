""" Build the args
https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html
"""
import os
from argparse import ArgumentParser, HelpFormatter, _SubParsersAction

from .config import ARGPARSE_TO_CONFIG
from .config import NavigatorConfig
from .utils import Sentinel


def _abs_user_path(fpath):
    """don't overload the ap type"""
    return os.path.abspath(os.path.expanduser(fpath))


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


class ArgumentParserDefaultFromConfig(ArgumentParser):
    """Manually update the help text with a default value from
    NavigatorConfig, otherwise argparse would simply show Sentinal across
    the board

    The 'dest' for an argparse param is used for the lookup in the
    config, therefore, the argparse dest, and config key need to stay
    in sync
    """

    def __init__(self, *args, **kwargs):
        self.navigator_config = NavigatorConfig(ARGPARSE_TO_CONFIG)
        super().__init__(*args, **kwargs)

    def add_argument(self, *args, **kwargs):
        """add the default to the help"""
        arg_dest = kwargs.get("dest")
        if arg_dest is not None:
            mapped_to = ARGPARSE_TO_CONFIG.get(arg_dest)
            if all((mapped_to, kwargs.get("help"))):
                _config_source, default_value = self.navigator_config.get(mapped_to)
                if not isinstance(default_value, Sentinel):
                    kwargs["help"] += f" (default: {default_value})"
        super().add_argument(*args, **kwargs)


class CliArgs:
    """Build the args"""

    # pylint: disable=too-few-public-methods
    def __init__(self, app_name: str):

        self._app_name = app_name
        self._base_parser = ArgumentParserDefaultFromConfig(add_help=False)
        self._base()
        self.parser = ArgumentParserDefaultFromConfig(
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

    @staticmethod
    def _doc_params(parser: ArgumentParser) -> None:
        parser.add_argument("value", metavar="plugin", help="The name of the plugin", type=str)
        tipes = (
            "become",
            "cache",
            "callback",
            "cliconf",
            "connection",
            "httpapi",
            "inventory",
            "lookup",
            "netconf",
            "shell",
            "vars",
            "module",
            "strategy",
        )
        parser.add_argument(
            "-t",
            "--type",
            help=f'Choose which plugin type: {{{",".join(tipes)}}}',
            choices=tipes,
            default=Sentinel,
            dest="type",
            metavar="",
        )
        parser.set_defaults(requires_ansible=True)

    @staticmethod
    def _editor_params(parser: ArgumentParser) -> None:
        parser.add_argument(
            "--ecmd",
            "--editor-command",
            help="Specify the editor command, filename and line number",
            default=Sentinel,
            dest="editor_command",
        )
        parser.add_argument(
            "--econ",
            "--editor-console",
            help="Specify if the editor is console based",
            default=Sentinel,
            dest="editor_console",
        )

    @staticmethod
    def _ee_params(parser: ArgumentParser) -> None:
        parser.add_argument(
            "--ce",
            "--container-engine",
            help="Specify the container engine to run the Execution Environment",
            choices=["podman", "docker"],
            default=Sentinel,
            dest="container_engine",
        )
        parser.add_argument(
            "--ee",
            "--execution-environment",
            action="store_true",
            dest="execution_environment",
            help="Run the playbook in an Execution Environment",
        )
        parser.add_argument(
            "--eei",
            "--execution-environment-image",
            help="Specify the name of the container image containing an Execution Environment",
            default=Sentinel,
            dest="execution_environment_image",
        )
        parser.add_argument(
            "--senv",
            "--set_environment_variable",
            action="append",
            default=[Sentinel],
            dest="set_environment_variable",
            help="Specify an environment variable and a value to be set within the \
                  execution enviroment (--senv MY_VAR=42)",
            nargs="+",
        )
        parser.add_argument(
            "--penv",
            "--pass_environment_variable",
            action="append",
            default=[Sentinel],
            dest="pass_environment_variable",
            help=(
                "Specify an exiting environment variable to be passed through to and set \
                 within the execution enviroment (--penv MY_VAR)"
            ),
            nargs="+",
        )

    def _run(self) -> None:
        parser = self._add_subparser(
            "run", "Run Ansible playbook in either interactive or stdout mode"
        )
        self._playbook_params(parser)
        self._inventory_params(parser)

    @staticmethod
    def _inventory_columns(parser: ArgumentParser) -> None:
        parser.add_argument(
            "--ic",
            "--inventory-columns",
            help=(
                "Additional columns to be shown in the inventory views,"
                " comma delimited, eg 'xxx,yyy,zzz'"
            ),
            default=Sentinel,
            dest="inventory_columns",
        )

    def _inventory(self) -> None:
        parser = self._add_subparser("inventory", "Explore inventories")
        self._inventory_params(parser)

    @staticmethod
    def _inventory_params(parser: ArgumentParser) -> None:
        parser.add_argument(
            "-i",
            "--inventory",
            help="The inventory/inventories to use",
            action="append",
            nargs="+",
            type=_abs_user_path,
            default=[Sentinel],
            dest="inventory",
        )

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

    def _log_params(self, parser: ArgumentParser) -> None:  # pylint: disable=no-self-use
        parser.add_argument(
            "--lf",
            "--logfile",
            default=Sentinel,
            dest="logfile",
            help="Specify the application log file location",
        )
        parser.add_argument(
            "--ll",
            "--loglevel",
            default=Sentinel,
            dest="loglevel",
            choices=["debug", "info", "warning", "error", "critical"],
            help="Specify the application log level",
            type=str,
        )

    @staticmethod
    def _no_osc4_params(parser: ArgumentParser) -> None:
        parser.add_argument(
            "--no-osc4",
            action="store_true",
            default=Sentinel,
            help="Disable OSC-4 support (xterm.js color fix)",
            dest="no_osc4",
        )

    @staticmethod
    def _playbook_params(parser: ArgumentParser) -> None:
        parser.add_argument(
            "playbook",
            nargs="?",
            help="The name of the playbook(s) to run",
            type=_abs_user_path,
            default=Sentinel,
        )
        parser.add_argument(
            "--pa",
            "--playbook-artifact",
            help="Specify the artifact file name for playbook results",
            default=Sentinel,
            dest="playbook_artifact",
        )
        parser.set_defaults(requires_ansible=True)

    @staticmethod
    def _mode(parser: ArgumentParser) -> None:
        parser.add_argument(
            "-m",
            "--mode",
            default=Sentinel,
            choices=["stdout", "interactive"],
            help="Specify the navigator mode to run",
            type=str,
        )
