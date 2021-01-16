""" Build the args
"""

import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, _SubParsersAction


def _abs_user_path(fpath):
    """don't overload the ap type"""
    return os.path.abspath(os.path.expanduser(fpath))


class CustomHelpFormatter(ArgumentDefaultsHelpFormatter):
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
        self._blogs()
        self._collections()
        self._config()
        self._doc()
        self._inventory()
        self._load()
        self._explore()
        self._playbook()
        self._playquietly()

    def _add_subparser(self, name: str, desc: str) -> ArgumentParser:
        return self._subparsers.add_parser(
            name,
            help=desc,
            description=f"{name}: {desc}",
            formatter_class=CustomHelpFormatter,
            parents=[self._base_parser],
        )

    def _base(self) -> None:
        self._ee_params(self._base_parser)
        self._inventory_columns(self._base_parser)
        self._ide_params(self._base_parser)
        self._log_params(self._base_parser)
        self._no_osc4_params(self._base_parser)
        self._web_params(self._base_parser)

    def _blogs(self) -> None:
        blogs = (
            ("blog", "Check out the recent Ansible blog entries"),
            ("bullhorn", "Catch up on the latest bullhorn issues"),
            ("redhat", "See the latest from Red Hat"),
        )
        for entry in blogs:
            parser = self._add_subparser(*entry)
            parser.set_defaults(value=None, requires_ansible=False)

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
        parser.add_argument(
            "value",
            metavar="plugin",
            help="The name of the plugin",
            type=str,
        )
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
            default="module",
            metavar="",
        )
        parser.set_defaults(requires_ansible=True)

    @staticmethod
    def _ee_params(parser: ArgumentParser) -> None:
        parser.add_argument(
            "-ce",
            "--container-engine",
            help="Specify the container engine to run the Execution Environment",
            choices=["podman", "docker"],
            default="podman",
        )
        parser.add_argument(
            "-ee",
            "--execution-environment",
            action="store_true",
            help="Run the playbook in an Execution Environment",
        )
        parser.add_argument(
            "-eei",
            "--ee-image",
            help="Specify the name of the container image containing an Execution Environment",
            default="quay.io/ansible/ansible-runner:devel",
        )

    def _explore(self) -> None:
        parser = self._add_subparser("explore", "Run playbook(s) interactive")
        self._playbook_params(parser)
        self._inventory_params(parser)

    @staticmethod
    def _ide_params(parser: ArgumentParser) -> None:
        parser.add_argument(
            "--ide",
            help="Specify the current ide",
            choices=["pycharm", "vim", "vscode"],
            default="vim",
        )

    @staticmethod
    def _inventory_columns(parser: ArgumentParser) -> None:
        parser.add_argument(
            "--inventory_columns",
            help=(
                "Additional columns to be shown in the inventory views,"
                " comma delimited, eg 'xxx,yyy,zzz'"
            ),
            default="",
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
            default=[],
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

    def _log_params(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-lf",
            "--logfile",
            default=f"./{self._app_name}.log",
            dest="logfile",
            help="Specify the application log file location",
        )
        parser.add_argument(
            "-ll",
            "--loglevel",
            default="info",
            dest="loglevel",
            choices=["debug", "info", "warning", "error", "critical"],
            help="Specify the application log level",
            type=str,
        )

    @staticmethod
    def _no_osc4_params(parser: ArgumentParser) -> None:
        parser.add_argument(
            "-no-osc4",
            action="store_true",
            help="Disable OSC-4 support (xterm.js color fix)",
        )

    def _playbook(self) -> None:
        parser = self._add_subparser("playbook", "Run playbook(s)")
        self._playbook_params(parser)
        self._inventory_params(parser)

    def _playquietly(self) -> None:
        parser = self._add_subparser("playquietly", "Run playbook(s) quietly")
        self._playbook_params(parser)
        self._inventory_params(parser)

    @staticmethod
    def _playbook_params(parser: ArgumentParser) -> None:
        parser.add_argument(
            "playbook",
            nargs="?",
            help="The name of the playbook(s) to run",
            type=_abs_user_path,
        )
        parser.add_argument(
            "-a",
            "--artifact",
            help="Specify the artifact file name for playbook results",
            default="<playbook_dir>/<playbook_name>_artifact.json",
        )
        parser.set_defaults(requires_ansible=True)

    @staticmethod
    def _web_params(parser: ArgumentParser) -> None:
        parser.add_argument(
            "--web",
            action="store_true",
            help="Run the application in a browser rather than the current terminal",
        )
