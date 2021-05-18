""" start here
"""
import logging
import os
import sys
import signal
import time

from copy import deepcopy
from curses import wrapper
from typing import List
from pathlib import Path

from .actions import run_action_stdout
from .action_runner import ActionRunner

from .configuration_subsystem import ApplicationConfiguration
from .configuration_subsystem import NavigatorConfiguration

from .initialization import parse_and_update
from .initialization import error_and_exit_early

APP_NAME = "ansible-navigator"
PKG_NAME = "ansible_navigator"

logger = logging.getLogger(PKG_NAME)


def setup_logger(args: ApplicationConfiguration) -> None:
    """set up the logger

    :param args: The cli args
    :type args: argparse namespace
    """
    if os.path.exists(args.log_file) and args.log_append is False:
        os.remove(args.log_file)
    hdlr = logging.FileHandler(args.log_file)
    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d %(levelname)s '%(name)s.%(funcName)s' %(message)s",
        datefmt="%y%m%d%H%M%S",
    )
    setattr(formatter, "converter", time.gmtime)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(getattr(logging, args.log_level.upper()))
    logger.info("New %s instance, logging initialized", APP_NAME)


def run(args: ApplicationConfiguration) -> int:
    """run the appropriate app"""
    try:
        if args.mode == "stdout":
            return_code = run_action_stdout(args.app.replace("-", "_"), args)
            return return_code
        wrapper(ActionRunner(args=args).run)
        return 0
    except KeyboardInterrupt:
        logger.warning("Dirty exit, killing the pid")
        os.kill(os.getpid(), signal.SIGTERM)
        return 1


def main():
    """start here"""
    messages: List[str] = []
    errors: List[str] = []

    args = deepcopy(NavigatorConfiguration)
    messages.extend(args.internals.initialization_messages)
    errors.extend(args.internals.initialization_errors)

    new_messages, new_errors = parse_and_update(sys.argv[1:], args=args, initial=True)
    messages.extend(new_messages)
    errors.extend(new_errors)

    # In case of errors, the configuration will have rolled back
    # but a viable log file is still needed, set to default since
    # it cannot be determined if the error is log file location related
    if errors:
        args.entry("log_file").value.current = args.entry("log_file").value.default
        args.entry("log_level").value.current = "debug"
        error = f"Configuration failed, using default log file location: {args.log_file}."
        error += f" Log level set to {args.log_level}"
        errors.append(error)

    try:
        Path(args.log_file).touch()
        setup_logger(args)
    except Exception as exc:  # pylint: disable=broad-except
        error = "The log file path or logging engine could not be setup."
        error += " No log file will be available, please check the log file"
        error += f" path setting. The error was {str(exc)}"
        errors.append(error)
        error_and_exit_early(errors)

    for entry in messages:
        logger.log(level=entry.level, msg=entry.message)

    if errors:
        for error in errors:
            logger.error(msg=error)
        error_and_exit_early(errors)

    os.environ.setdefault("ESCDELAY", "25")
    # clear if the TERM is set
    if os.environ.get("TERM"):
        os.system("clear")

    return_code = run(args)
    if return_code:
        sys.exit(return_code)


if __name__ == "__main__":
    main()
