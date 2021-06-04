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
from .image_manager import ImagePuller
from .initialization import parse_and_update
from .initialization import error_and_exit_early
from .utils import ExitMessage
from .utils import ExitPrefix
from .utils import LogMessage

APP_NAME = "ansible-navigator"
PKG_NAME = "ansible_navigator"

logger = logging.getLogger(PKG_NAME)


def pull_image(args):
    """pull the image if required"""
    image_puller = ImagePuller(
        container_engine=args.container_engine,
        image=args.execution_environment_image,
        pull_policy=args.pull_policy,
    )
    image_puller.assess()
    if image_puller.assessment.exit_messages:
        error_and_exit_early(image_puller.assessment.exit_messages)
    if image_puller.assessment.pull_required:
        image_puller.prologue_stdout()
        image_puller.pull_stdout()
    if image_puller.assessment.exit_messages:
        error_and_exit_early(image_puller.assessment.exit_messages)


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
    log_level = getattr(logging, args.log_level.upper())
    logger.setLevel(log_level)
    logger.info("New %s instance, logging initialized", APP_NAME)

    # set ansible-runner logs
    runner_logger = logging.getLogger("ansible-runner")
    runner_logger.setLevel(log_level)
    runner_logger.addHandler(hdlr)
    logger.info("New ansible-runner instance, logging initialized")


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
    messages: List[LogMessage] = []
    exit_messages: List[ExitMessage] = []

    args = deepcopy(NavigatorConfiguration)
    messages.extend(args.internals.initialization_messages)
    exit_messages.extend(args.internals.initialization_exit_messages)

    # may have exit messages eg, share directory
    # from instantiation of NavigatorConfiguration
    if not exit_messages:
        new_messages, new_exit_messages = parse_and_update(sys.argv[1:], args=args, initial=True)
        messages.extend(new_messages)
        exit_messages.extend(new_exit_messages)

    # In case of errors, the configuration will have rolled back
    # but a viable log file is still needed, set to default since
    # it cannot be determined if the error is log file location related
    if exit_messages:
        args.entry("log_file").value.current = args.entry("log_file").value.default
        args.entry("log_level").value.current = "debug"
        exit_msg = f"Configuration failed, using default log file location: {args.log_file}."
        exit_msg += f" Log level set to {args.log_level}"
        exit_messages.append(ExitMessage(message=exit_msg))
        exit_msg = f"Review the hints and log file to see what went wrong: {args.log_file}"
        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))

    try:
        Path(args.log_file).touch()
        setup_logger(args)
    except Exception as exc:  # pylint: disable=broad-except
        exit_msg = "The log file path or logging engine could not be setup."
        exit_msg += " No log file will be available, please check the log file"
        exit_msg += f" path setting. The error was {str(exc)}"
        exit_messages.append(ExitMessage(message=exit_msg))
        error_and_exit_early(exit_messages=exit_messages)

    for entry in messages:
        logger.log(level=entry.level, msg=entry.message)

    if exit_messages:
        for exit_msg in exit_messages:
            logger.log(level=exit_msg.level, msg=exit_msg.message)
        error_and_exit_early(exit_messages=exit_messages)

    os.environ.setdefault("ESCDELAY", "25")

    if args.execution_environment:
        pull_image(args)

    return_code = run(args)
    if return_code:
        sys.exit(return_code)


if __name__ == "__main__":
    main()
