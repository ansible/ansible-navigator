""" start here
"""
import configparser
import itertools
import logging
import os
import sys
import sysconfig
import signal
import time

from argparse import _SubParsersAction
from argparse import ArgumentParser
from argparse import Namespace
from functools import partial
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from yaml.scanner import ScannerError


from curses import wrapper

from .cli_args import CliArgs
from .config import NavigatorConfig
from .action_runner import ActionRunner
from .utils import check_for_ansible
from .utils import get_and_check_collection_doc_cache
from .utils import set_ansible_envar
from .utils import Sentinel
from .yaml import yaml, SafeLoader

APP_NAME = "ansible_navigator"
APP_PRETTY_NAME = "ansible-navigator"
COLLECTION_DOC_CACHE_FNAME = "collection_doc_cache.db"

logger = logging.getLogger(APP_NAME)


def _get_share_dir() -> Optional[str]:
    """
    returns datadir (e.g. /usr/share/ansible_nagivator) to use for the
    ansible-launcher data files. First found wins.
    """

    # Development path
    # We want the share directory to resolve adjacent to the directory the code lives in
    # as that's the layout in the source.
    path = os.path.join(os.path.dirname(__file__), "..", "share", APP_NAME)
    if os.path.exists(path):
        return path

    # ~/.local/share/APP_NAME
    userbase = sysconfig.get_config_var("userbase")
    if userbase is not None:
        path = os.path.join(userbase, "share", APP_NAME)
        if os.path.exists(path):
            return path

    # /usr/share/APP_NAME  (or the venv equivalent)
    path = os.path.join(sys.prefix, "share", APP_NAME)
    if os.path.exists(path):
        return path

    # /usr/share/APP_NAME  (or what was specified as the datarootdir when python was built)
    datarootdir = sysconfig.get_config_var("datarootdir")
    if datarootdir is not None:
        path = os.path.join(datarootdir, APP_NAME)
        if os.path.exists(path):
            return path

    # /usr/local/share/APP_NAME
    prefix = sysconfig.get_config_var("prefix")
    if prefix is not None:
        path = os.path.join(prefix, "local", "share", APP_NAME)
        if os.path.exists(path):
            return path

    # No path found above
    return None


def _get_conf_dir(filename: Optional[str] = None) -> (Optional[str], List[str]):
    """
    returns config dir (e.g. /etc/ansible-nagivator). First found wins.
    If a filename is given, ensures the file exists in the directory.
    """

    potential_paths = []
    msgs = []

    # Development path
    path = os.path.join(os.path.dirname(__file__), "..", "etc", APP_PRETTY_NAME)
    potential_paths.append(path)

    # ~/.config/APP_PRETTY_NAME
    path = os.path.join(os.path.expanduser("~"), ".config", APP_PRETTY_NAME)
    potential_paths.append(path)

    # /etc/APP_PRETTY_NAME
    path = os.path.join("/", "etc", APP_PRETTY_NAME)
    potential_paths.append(path)

    # /usr/local/etc/APP_PRETTY_NAME
    prefix = sysconfig.get_config_var("prefix")
    if prefix:
        path = os.path.join(prefix, "local", "etc", APP_PRETTY_NAME)
        potential_paths.append(path)

    for path in potential_paths:
        must_exist = os.join(path, filename) if filename is not None else path
        if not os.path.exists(must_exist):
            continue

        try:
            perms = os.stat(path)
            if perms.st_mode & stat.S_IWOTH:
                msgs.append('Ignoring potential configuration directory {0} because it is world-writable.')
                continue
            return path
        except OSError:
            continue

    return None


class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(
        self, parser, section, option, value, defaults
    ):  # pylint: disable=too-many-arguments
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)


class NoSuch:  # pylint: disable=too-few-public-methods
    """sentinal"""


def error_and_exit_early(msg):
    """get out of here fast"""
    print(f"\x1b[31m[ERROR]: {msg}\x1b[0m")
    sys.exit(1)


def get_param(
    parser: ArgumentParser, name: str
) -> Tuple[Union[str, None], Union[str, List, None], Any]:
    # pylint: disable=protected-access

    """get the param from the argparser
    try short and long variations, _ or -
    """
    variations = [
        f"-{name}",
        f"--{name}",
        f"-{name.replace('_', '-')}",
        f"--{name.replace('_', '-')}",
    ]

    for action in parser._actions:
        if any((v in action.option_strings for v in variations)):
            return action.dest, action.default, action.type
        if name == action.dest and action.nargs == "?":
            return action.dest, action.default, action.type
        if isinstance(action, _SubParsersAction):
            for _parser_name, sub_parser in action.choices.items():
                sub_parser_dest, sub_parser_default, sub_parser_type = get_param(sub_parser, name)
                if sub_parser_dest is not None:
                    return sub_parser_dest, sub_parser_default, sub_parser_type
    return None, None, None


def update_args(args: Namespace) -> List[str]:
    """
    Updates args with the corresponding values in the "argument-defaults"
    portion of the ansible-navigator config file.

    NOTE:
    argparse, in its infinite wisdom, doesn't allow us to check whether a
    parameter was actually supplied or not, on the commandline. That is, if we
    get something that matches the default value on the arg, we have no way of
    knowing if the user supplied that (default) value, or if they just didn't
    specify the field at all. This represents a BUG in how we handle default
    values here, but I don't think we have an easy way around it.

    As a practical example of the consequences: If a config file has
    `loglevel: error` and the user specifies `--loglevel info` (which is the
    default for loglevel), we will end up using error.
    """

    msgs = []

    # If no config file was parsed and added to args, there's nothing to do
    if not hasattr(args, 'config') or not args.config:
        msgs.append('No config file parsed, no default parameters to override.')
        return msgs

    defaults = config.get(['ansible-navigator', 'argument-defaults'], {})
    msgs = []
    if config_file:
        msgs.append(f"Using {config_file}")
        config = configparser.ConfigParser(interpolation=EnvInterpolation())
        try:
            config.read(config_file)
        except Exception as exc:  # pylint:disable=broad-except
            error_and_exit_early(str(exc))
        if config_file:
            cdict = dict(config)
            for section_name, section in cdict.items():
                if section_name in ["default", args.app]:
                    for key, value in section.items():
                        dest, default, tipe = get_param(parser, key)
                        msgs.append(f"ini entry: {key} matched to arg: {dest}")
                        if dest:
                            arg_value = getattr(args, dest, Sentinel())
                            if arg_value == default or isinstance(arg_value, Sentinel):
                                if isinstance(default, bool):
                                    bool_key: bool = section.getboolean(key)
                                    msg = f"{dest} was default, "
                                    msg += f"using entry '{bool_key}'"
                                    msgs.append(msg)
                                    setattr(args, dest, bool_key)
                                elif [] == default:
                                    use_value = [value.split(",")]
                                    setattr(args, dest, use_value)
                                    msg = f"{dest} was default list, "
                                    msg += f"using entry.split(',') '{use_value}'"
                                    msgs.append(msg)
                                else:
                                    if isinstance(tipe, int):
                                        inted = int(value)
                                        setattr(args, dest, inted)
                                    elif callable(tipe):
                                        called = tipe(value)
                                        setattr(args, dest, called)
                                    else:
                                        setattr(args, dest, value)
                                    msg = f"{dest} was not provided, using '{value}'"
                                    msgs.append(msg)

    else:
        msgs.append("No config file file found")
    return msgs


def setup_logger(args):
    """set up the logger

    :param args: The cli args
    :type args: argparse namespace
    """
    if os.path.exists(args.logfile):
        with open(args.logfile, "w"):
            pass
    hdlr = logging.FileHandler(args.logfile)
    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d %(levelname)s '%(name)s.%(funcName)s' %(message)s",
        datefmt="%y%m%d%H%M%S",
    )
    formatter.converter = time.gmtime
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(getattr(logging, args.loglevel.upper()))


def parse_and_update(params: List, error_cb: Callable = None) -> Tuple[List[str], Namespace]:
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    """parse some params and update"""
    parser = CliArgs(APP_NAME).parser

    if error_cb:
        parser.error = error_cb  # type: ignore
    args, cmdline = parser.parse_known_args(params)
    args.cmdline = cmdline

    config_file = find_ini_config_file(APP_NAME)
    pre_logger_msgs = update_args(config_file, args, parser)

    args.logfile = os.path.abspath(os.path.expanduser(args.logfile))

    if args.app == "load" and not os.path.exists(args.value):
        parser.error(f"The file specified with load could not be found. {args.load}")

    if hasattr(args, "inventory"):
        args.inventory = list(itertools.chain.from_iterable(args.inventory))
        args.inventory = [os.path.abspath(os.path.expanduser(i)) for i in args.inventory]
        if not args.inventory and args.app == "inventory":
            parser.error("an inventory is required when using the inventory explorer")

    if hasattr(args, "artifact"):
        if hasattr(args, "playbook") and args.playbook:
            if args.artifact == get_param(parser, "artifact")[1]:
                args.artifact = f"{os.path.splitext(args.playbook)[0]}_artifact.json"

    if not args.app:
        args.app = "welcome"
        args.value = None

    share_dir = _get_share_dir()
    if share_dir is not None:
        args.share_dir = share_dir
    else:
        error_and_exit_early("problem finding share dir")

    if os.path.exists("ansible-navigator.yml"):
        # If there's a local config, use it
        config_path = "ansible-navigator.yml"
        pre_logger_msgs.append("Found a config file in current working directory; using it.")
    else:
        # Otherwise, try to find it a different way
        config_dir = _get_conf_dir()
        if config_dir is not None:
            config_path = os.path.join(config_dir, "ansible-navigator.yml")
            if os.path.exists(config_path):
                pre_logger_msgs.append("Found config file at {0}".format(config_path))
            else:
                # TODO: Is bailing out right? Or just use defaults?
                error_and_exit_early(
                    "Found config directory at {0} but ansible-navigator.yml did not exist".format(
                        config_dir
                    )
                )
        else:
            error_and_exit_early("Could not find config directory")

    with open(config_path, "r") as config_fh:
        try:
            config = yaml.load(config_fh, Loader=SafeLoader)
        except ScannerError:
            error_and_exit_early("Config file at {0} but it failed to parse.".format(config_path))

    if config and config.get("ansible-navigator"):
        pre_logger_msgs.append("Successfully parsed config file")
        args.config = NavigatorConfig(config)
    else:
        error_and_exit_early(
            "Config file was empty, null, or did not contain an 'ansible-navigator' key"
        )

    pre_logger_msgs += update_args(args)

    args.logfile = os.path.abspath(os.path.expanduser(args.logfile))

    if args.app == "load" and not os.path.exists(args.value):
        parser.error(f"The file specified with load could not be found. {args.load}")

    if hasattr(args, "inventory"):
        args.inventory = list(itertools.chain.from_iterable(args.inventory))
        args.inventory = [os.path.abspath(os.path.expanduser(i)) for i in args.inventory]
        if not args.inventory and args.app == "inventory":
            parser.error("an inventory is required when using the inventory explorer")

    if hasattr(args, "artifact"):
        if hasattr(args, "playbook") and args.playbook:
            if args.artifact == get_param(parser, "artifact")[1]:
                args.artifact = f"{os.path.splitext(args.playbook)[0]}_artifact.json"

    if args.web:
        args.no_osc4 = True

    if not args.app:
        args.app = "welcome"
        args.value = None

    share_dir = _get_share_dir()
    if share_dir is not None:
        args.share_dir = share_dir
    else:
        error_and_exit_early("problem finding share dir")

    cache_home = os.environ.get("XDG_CACHE_HOME", f"{os.path.expanduser('~')}/.cache")
    args.cache_dir = f"{cache_home}/{APP_NAME}"
    msgs, args.collection_doc_cache = get_and_check_collection_doc_cache(
        args, COLLECTION_DOC_CACHE_FNAME
    )

    pre_logger_msgs += msgs

    args.original_command = params

    return pre_logger_msgs, args


def run(args: Namespace) -> None:
    """run the appropriate app"""
    try:
        if args.app in ["run", "config"] and args.mode == "stdout":
            try:
                app_action = __import__(
                    f"actions.{args.app}", globals(), fromlist=["Action"], level=1
                )
            except ImportError as exc:
                msg = (
                    f"either action '{args.app}' is invalid or does not support"
                    f" mode '{args.mode}'. Failed with error {exc}"
                )
                logger.error(msg)
                error_and_exit_early(str(msg))

            non_ui_app = partial(app_action.Action(args).run_stdout)
            non_ui_app()
        else:
            wrapper(ActionRunner(args=args).run)
    except KeyboardInterrupt:
        logger.warning("Dirty exit, killing the pid")
        os.kill(os.getpid(), signal.SIGTERM)


def main():
    """start here"""

    # pylint: disable=too-many-branches

    pre_logger_msgs, args = parse_and_update(sys.argv[1:])
    args.parse_and_update = parse_and_update

    setup_logger(args)
    for msg in pre_logger_msgs:
        logger.debug(msg)

    os.environ.setdefault("ESCDELAY", "25")
    os.system("clear")

    if not hasattr(args, "requires_ansible") or args.requires_ansible:
        if not args.execution_environment:
            success, msg = check_for_ansible()
            if success:
                logger.debug(msg)
            else:
                logger.critical(msg)
                error_and_exit_early(msg)
        set_ansible_envar()

    for key, value in vars(args).items():
        logger.debug("Running with %s=%s %s", key, value, type(value))

    run(args)


if __name__ == "__main__":
    main()
