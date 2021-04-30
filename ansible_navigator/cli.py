""" start here
"""
import logging
import os
import sys
import signal
import time


from argparse import Namespace
from copy import deepcopy
from curses import wrapper
from functools import partial
from typing import List
from typing import Tuple

from .action_runner import ActionRunner

from .configuration_subsystem import ApplicationConfiguration
from .configuration_subsystem import Configurator
from .configuration_subsystem import Constants as C
from .configuration_subsystem import NavigatorConfiguration

from .utils import check_for_ansible
from .utils import env_var_is_file_path
from .utils import error_and_exit_early
from .utils import get_and_check_collection_doc_cache
from .utils import get_conf_path
from .utils import set_ansible_envar


APP_NAME = "ansible_navigator"

logger = logging.getLogger(APP_NAME)


def setup_logger(args):
    """set up the logger

    :param args: The cli args
    :type args: argparse namespace
    """
    if os.path.exists(args.log_file):
        with open(args.log_file, "w"):
            pass
    hdlr = logging.FileHandler(args.log_file)
    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d %(levelname)s '%(name)s.%(funcName)s' %(message)s",
        datefmt="%y%m%d%H%M%S",
    )
    formatter.converter = time.gmtime
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(getattr(logging, args.log_level.upper()))


def find_config() -> Tuple[List[str], str]:
    """
    Find a configuration file, logging each step.
    Return (log messages, path).
    If the config can't be found/loaded, use default settings.
    If it's found but empty or not well formed, bail out.
    """
    pre_logger_msgs = []
    config_path = None
    # Check if the conf path is set via an env var
    cfg_env_var = "ANSIBLE_NAVIGATOR_CONFIG"
    env_config_path, msgs = env_var_is_file_path(cfg_env_var, "config")
    pre_logger_msgs += msgs

    # Check well know locations
    found_config_path, msgs = get_conf_path(
        "ansible-navigator", allowed_extensions=["yml", "yaml", "json"]
    )
    pre_logger_msgs += msgs

    # Pick the envar set first, followed by found, followed by leave as none
    if env_config_path is not None:
        config_path = env_config_path
        pre_logger_msgs.append(f"Using config file at {config_path} set by {cfg_env_var}")
    elif found_config_path is not None:
        config_path = found_config_path
        pre_logger_msgs.append(f"Using config file at {config_path} in search path")
    else:
        pre_logger_msgs.append(
            "No valid config file found, using all default values for configuration."
        )
    return pre_logger_msgs, config_path


def parse_and_update(
    params: List, args: ApplicationConfiguration, exit_on_errors: bool = False
) -> Tuple[List[str], Namespace]:
    """Build a configuration"""

    pre_logger_msgs, config_path = find_config()

    configurator = Configurator(
        params=params,
        settings_file_path=config_path,
        application_configuration=args,
        save_as_intitial=True,
    )

    msgs, errors = configurator.configure()

    for msg in msgs:
        pre_logger_msgs.append(msg[1])

    if errors and exit_on_errors:
        error_and_exit_early(errors)

    if args.internals.collection_doc_cache is C.NOT_SET:
        msgs, cache = get_and_check_collection_doc_cache(
            args.internals.share_directory, args.collection_doc_cache_path
        )
        args.internals.collection_doc_cache = cache

    return pre_logger_msgs, args


def run(args: Namespace) -> None:
    """run the appropriate app"""
    try:
        if args.app in ["run", "config", "inventory", "doc"] and args.mode == "stdout":
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
    args = deepcopy(NavigatorConfiguration)

    pre_logger_msgs, args = parse_and_update(sys.argv[1:], args=args, exit_on_errors=True)

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
