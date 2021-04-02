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
from .config import ARGPARSE_TO_CONFIG, NavigatorConfig
from .action_runner import ActionRunner
from .utils import (
    check_for_ansible,
    get_and_check_collection_doc_cache,
    get_conf_dir,
    set_ansible_envar,
    Sentinel,
)
from .yaml import yaml, SafeLoader

APP_NAME = "ansible_navigator"
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


def update_args(args: Namespace) -> List[str]:
    """
    Updates args with the corresponding config values (or their defaults) unless
    explicitly specified by the user.

    NOTE:
    argparse, in its infinite wisdom, doesn't allow us to check whether a
    parameter was actually supplied or not, on the commandline. That is, if we
    get something that matches the default value on the arg, we have no way of
    knowing if the user supplied a value that matched the default, or if they
    just didn't specify the field at all. To compensate for this, all options
    which are "defaultable" via config have an argparse default of
    util.Sentinel.

    ---

    How this function works (in practice):
    1) We iterate over all defaultable args (given in config.ARGPARSE_TO_CONFIG)
    2) If the attribute doesn't exist in args at all, it's not relevant to this
       (sub)command, so move on and ignore it.
    3) If the current value of the arg is *not* Sentinel, then the user
       specified some value on the CLI; leave it alone.
    4) If the value *is* Sentinel, then the user didn't specify a value on the
       CLI, so look in config. If it exists in the user's config, pull the value
       out and use it. Otherwise, fallback to the default config.
    5) (should never happen) If the value doesn't exist in default config, we
       will get a KeyError back from the config subsystem. We let that bubble up
       and catch it by the global exception handler.
    """

    msgs = []

    # If no config file was parsed and added to args, there's nothing to do
    if not hasattr(args, "config") or not args.config:
        msgs.append("No config file parsed, no default parameters to override.")
        return msgs

    # Iterate through each "defaultable" (config-file-settable) path and do the
    # deed.
    for attr, path in ARGPARSE_TO_CONFIG.items():
        if not hasattr(args, attr):
            # If the attribute doesn't exist at all, skip it.
            # This probably means it's in a subparser that isn't relevant to the
            # command currently being run by the user.
            continue

        if getattr(args, attr) is not Sentinel:
            # Not Sentinel means that the user specified it. Leave it alone!
            continue

        # If we made it here, then the user didn't specify the argument.
        # If this ever throws KeyError, it's because something was added to the
        # ARGPARSE_TO_CONFIG mapping, but the key path in the default config
        # doesn't exist. There's not much to do in this case, so fall back to
        # the general exception handler (whenever it exists) and let it be the
        # thing that tells the user the bad news.
        value = args.config.get(path)
        msgs.append("Setting arg {0} to {1} via config".format(attr, value))
        setattr(args, attr, value)

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


def setup_config() -> Tuple[List[str], NavigatorConfig]:
    pre_logger_msgs = []
    found_config = False

    if os.path.exists("ansible-navigator.yml"):
        # If there's a local config, use it
        found_config = True
        config_path = "ansible-navigator.yml"
        pre_logger_msgs.append("Found a config file in current working directory; using it.")
    else:
        # Otherwise, try to find it a different way
        config_dir, msgs = get_conf_dir()
        pre_logger_msgs += msgs
        if config_dir is not None:
            config_path = os.path.join(config_dir, "ansible-navigator.yml")
            if os.path.exists(config_path):
                pre_logger_msgs.append("Found config file at {0}".format(config_path))
                found_config = True
            else:
                pre_logger_msgs.append(
                    "Found config directory at {0} but ansible-navigator.yml did not exist".format(
                        config_dir
                    )
                )
        else:
            # error_and_exit_early("Could not find config directory")
            pre_logger_msgs.append("Could not find config directory, using all defaults.")

    config = {}
    if found_config:
        with open(config_path, "r") as config_fh:
            try:
                config = yaml.load(config_fh, Loader=SafeLoader)
            except ScannerError:
                error_and_exit_early(
                    "Config file at {0} but it failed to parse it.".format(config_path)
                )

    if found_config and config and config.get("ansible-navigator"):
        # If the config file was found and has the key we expect, log and use it
        pre_logger_msgs.append("Successfully parsed config file")
        return pre_logger_msgs, NavigatorConfig(config)
    elif not found_config:
        # If the config file wasn't found, that's still okay. In this case, we
        # instantiate NavigatorConfig with an empty dict.
        return pre_logger_msgs, NavigatorConfig(config)
    else:
        # But if we found a config and it looks wrong (missing toplevel key or is
        # somehow otherwise empty/null), bail out!
        error_and_exit_early(
            "Config file was empty, null, or did not contain an 'ansible-navigator' key"
        )


def parse_and_update(params: List, error_cb: Callable = None) -> Tuple[List[str], Namespace]:
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    """parse some params and update"""
    parser = CliArgs(APP_NAME).parser

    if error_cb:
        parser.error = error_cb  # type: ignore
    args, cmdline = parser.parse_known_args(params)
    args.cmdline = cmdline

    pre_logger_msgs = []
    config_msgs, config = setup_config()
    pre_logger_msgs += config_msgs
    args.config = config
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
        # Would like to do this when importing config values in update_args()
        # and make use of NavigatorConfig#get's fmt param some day.
        args.artifact = args.artifact.format(
            playbook_dir=os.path.dirname(args.playbook),
            playbook_name=os.path.splitext(os.path.basename(args.playbook))[0])

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
