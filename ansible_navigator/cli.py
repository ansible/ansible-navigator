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

from .action_runner import ActionRunner

from .configuration_subsystem import ApplicationConfiguration
from .configuration_subsystem import NavigatorConfiguration

from .initialization import parse_and_update
from .initialization import error_and_exit_early

APP_NAME = "ansible_navigator"

logger = logging.getLogger(APP_NAME)


def setup_logger(args: ApplicationConfiguration) -> None:
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
    setattr(formatter, "converter", time.gmtime)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(getattr(logging, args.log_level.upper()))


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
    messages: List[str] = []
    errors: List[str] = []

    args = deepcopy(NavigatorConfiguration)
    messages.extend(args.internals.initialization_messages)
    errors.extend(args.internals.initialization_errors)
    if errors:
        error_and_exit_early(errors)

    new_messages, new_errors = parse_and_update(sys.argv[1:], args=args, save_as_initial=True)
    messages.extend(new_messages)
    errors.extend(new_errors)
    if errors:
        error_and_exit_early(errors)

    setup_logger(args)
    for entry in messages:
        logger.log(level=entry.level, msg=entry.message)

    os.environ.setdefault("ESCDELAY", "25")
    os.system("clear")

    run(args)


if __name__ == "__main__":
    main()
