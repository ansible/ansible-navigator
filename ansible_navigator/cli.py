""" start here
"""
import json
import logging
import os
import sys
import sysconfig
import signal
import time

from argparse import Namespace
from curses import wrapper
from functools import partial
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple

from .cli_args import CliArgs
from .config import NavigatorConfig
from .action_runner import ActionRunner

from .utils import check_for_ansible
from .utils import error_and_exit_early
from .utils import flatten_list
from .utils import get_and_check_collection_doc_cache
from .utils import set_ansible_envar
from .utils import Sentinel

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
    1) If the attribute doesn't exist in args at all, it's not relevant to this
       (sub)command, so move on and ignore it.
    2) If the current value of the arg is *not* Sentinel, then the user
       specified some value on the CLI; leave it alone.
    3) If the value *is* Sentinel, then the user didn't specify a value on the
       CLI, so look in config. If it exists in the user's config, pull the value
       out and use it. Otherwise, fallback to the default config.
    4) (should never happen) If the value doesn't exist in default config, we
       will get a KeyError back from the config subsystem. We let that bubble up
       and catch it by the global exception handler.
    """

    msgs = []

    # If no config file was parsed and added to args, there's nothing to do
    if not hasattr(args, "config") or not args.config:
        msgs.append("No config file parsed, no default parameters to override.")
        return msgs

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
    # pylint: disable=too-many-locals
    """parse some params and update"""
    parser = CliArgs(APP_NAME).parser

    if error_cb:
        parser.error = error_cb  # type: ignore
    args, cmdline = parser.parse_known_args(params)
    args.cmdline = cmdline

    pre_logger_msgs: List[str] = []
    config = NavigatorConfig()
    args.config = config
    pre_logger_msgs += update_args(args)

    args.logfile = os.path.abspath(os.path.expanduser(args.logfile))

    # post process inventory
    if hasattr(args, "inventory"):
        # The default argparse value is [Sentinel] for default detection purposes
        # at this point it's been set to a user value so we can remove any Sentinels
        args.inventory = [i for i in args.inventory if i is not Sentinel]
        # because the default argpars for inventory is a list, new invetories get added as a list
        args.inventory = flatten_list(args.inventory)
        args.inventory = [os.path.abspath(os.path.expanduser(i)) for i in args.inventory]
        if not args.inventory and args.app == "inventory":
            parser.error("an inventory is required when using the inventory explorer")

    # post process load
    if args.app == "load" and not os.path.exists(args.value):
        parser.error(f"The file specified with load could not be found. {args.load}")

    # post process pass_environment_variable
    if hasattr(args, "pass_environment_variable"):
        args.pass_environment_variable = [
            i for i in args.pass_environment_variable if i is not Sentinel
        ]
        args.pass_environment_variable = flatten_list(args.pass_environment_variable)

    # post process playbook
    #   don't expand "" (the default)
    if hasattr(args, "playbook") and args.playbook:
        args.playbook = os.path.abspath(os.path.expanduser(args.playbook))

    # post process set_environment_variable
    if hasattr(args, "set_environment_variable"):
        # command line will be a list, settings file is a dict
        if isinstance(args.set_environment_variable, list):
            args.set_environment_variable = [
                i for i in args.set_environment_variable if i is not Sentinel
            ]
            args.set_environment_variable = flatten_list(args.set_environment_variable)
            set_envs = {}
            for env_var in args.set_environment_variable:
                parts = env_var.split("=")
                if len(parts) != 2:
                    error_and_exit_early(
                        "The following set-environment-variable"
                        f" entry could not be parsed: {env_var}"
                    )
                set_envs[parts[0]] = parts[1]
            args.set_environment_variable = set_envs
        # coming from settings, ensure everything is a string
        # we will json dump incase there is complext structure
        for key, value in args.set_environment_variable.items():
            if not isinstance(value, str):
                args.set_environment_variable[key] = json.dumps(value)

    # post process welcome
    if not args.app:
        args.app = "welcome"
        args.mode = "interactive"
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
    args.parse_and_update = parse_and_update

    for key, value in sorted(vars(args).items()):
        pre_logger_msgs.append(f"Running with {key} as {value} {type(value)}")

    return pre_logger_msgs, args


def run(args: Namespace) -> None:
    """run the appropriate app"""
    try:
        if args.app in ["run", "config", "inventory"] and args.mode == "stdout":
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

    run(args)


if __name__ == "__main__":
    main()
