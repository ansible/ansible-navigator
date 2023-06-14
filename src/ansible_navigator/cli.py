# cspell:ignore getpid, gmtime, msecs
"""Navigator entry point."""
from __future__ import annotations

import filecmp
import logging
import os
import signal
import sys

from copy import deepcopy
from curses import wrapper
from importlib.metadata import version
from importlib.util import find_spec
from pathlib import Path
from shutil import copyfile

from .action_defs import ActionReturn
from .action_defs import RunInteractiveReturn
from .action_defs import RunReturn
from .action_defs import RunStdoutReturn
from .action_runner import ActionRunner
from .actions import run_action_stdout
from .configuration_subsystem import Constants
from .configuration_subsystem import NavigatorConfiguration
from .configuration_subsystem.definitions import ApplicationConfiguration
from .image_manager import ImagePuller
from .initialization import error_and_exit_early
from .initialization import parse_and_update
from .logger import setup_logger
from .utils.compatibility import importlib_metadata
from .utils.definitions import ExitMessage
from .utils.definitions import ExitPrefix
from .utils.definitions import LogMessage
from .utils.functions import clear_screen
from .utils.functions import generate_cache_path
from .utils.packaged_data import path_to_file


__version__: Constants | str
try:
    from ._version import version as __version__
except ImportError:
    __version__ = Constants.NOT_SET


APP_NAME = "ansible-navigator"
PKG_NAME = "ansible_navigator"

logger = logging.getLogger(PKG_NAME)


def cache_scripts() -> None:
    """Cache the scripts used to introspect the container image."""
    scripts = ("catalog_collections.py", "image_introspect.py")
    for script in scripts:
        src = path_to_file(filename=script)
        cache_path = generate_cache_path(app_name=APP_NAME)
        cache_path.mkdir(parents=True, exist_ok=True)
        dst = cache_path / script
        message = f"No update required for {src} to {dst}"
        try:
            if not filecmp.cmp(src, dst):
                copyfile(src, dst)
                message = f"Updated {src} to {dst} (outdated)"
        except FileNotFoundError:
            copyfile(src, dst)
            message = f"Copied {src} to {dst} (missing)"
        logger.log(level=logging.DEBUG, msg=message)


def log_dependencies() -> list[LogMessage]:
    """Retrieve installed packages and log as debug.

    :returns: All packages, version and location
    """
    pkgs = []
    found = []
    messages: list[LogMessage] = []
    for _python_name, pkg_names in importlib_metadata.packages_distributions().items():
        for pkg_name in pkg_names:
            if pkg_name not in found:
                found.append(pkg_name)
                try:
                    spec = find_spec(pkg_name)
                except ModuleNotFoundError:
                    message = f"Package '{pkg_name}' is missing"
                    messages.append(LogMessage(level=logging.DEBUG, message=message))
                    continue
                _location = spec.origin if spec else ""
                _version = version(pkg_name)
                pkgs.append(f"{pkg_name}=={_version} {_location}")

    pkgs.sort()
    messages = [LogMessage(level=logging.DEBUG, message=pkg) for pkg in pkgs]
    return messages


def pull_image(args):
    """Pull the image if required.

    :param args: Copy of NavigatorConfiguration
    """
    image_puller = ImagePuller(
        container_engine=args.container_engine,
        image=args.execution_environment_image,
        arguments=args.pull_arguments,
        pull_policy=args.pull_policy,
    )
    image_puller.assess()
    if image_puller.assessment.exit_messages:
        error_and_exit_early(image_puller.assessment.exit_messages)
    if image_puller.assessment.pull_required:
        image_puller.prologue_stdout()
        image_puller.pull_stdout()


def run(args: ApplicationConfiguration) -> ActionReturn:
    """Run the appropriate subcommand.

    :param args: The current application settings
    :returns: A message to display and a return code
    """
    if args.mode == "stdout":
        try:
            result = run_action_stdout(args.app.replace("-", "_"), args)
            return result
        except KeyboardInterrupt:
            logger.warning("Dirty exit, killing the pid")
            os.kill(os.getpid(), signal.SIGTERM)
            return RunStdoutReturn(message="", return_code=1)
    elif args.mode == "interactive":
        try:
            clear_screen()
            wrapper(ActionRunner(args=args).run)
            return RunInteractiveReturn(message="", return_code=0)
        except KeyboardInterrupt:
            logger.warning("Dirty exit, killing the pid")
            os.kill(os.getpid(), signal.SIGTERM)
            return RunInteractiveReturn(message="", return_code=1)
    return RunReturn(message="", return_code=0)


def main():
    """Start application here."""
    messages: list[LogMessage] = log_dependencies()
    exit_messages: list[ExitMessage] = []

    args = deepcopy(NavigatorConfiguration)
    args.application_version = __version__
    args.internals.initializing = True
    messages.extend(args.internals.initialization_messages)
    exit_messages.extend(args.internals.initialization_exit_messages)

    # may have exit messages e.g., share directory
    # from instantiation of NavigatorConfiguration
    if not exit_messages:
        new_messages, new_exit_messages = parse_and_update(sys.argv[1:], args=args)
        messages.extend(new_messages)
        exit_messages.extend(new_exit_messages)

    # In case of errors, the configuration will have rolled back
    # but a viable log file is still needed, set to default since
    # it cannot be determined if the error is log file location related
    if exit_messages:
        args.entry("log_file").value.current = args.entry("log_file").value.default
        args.entry("log_level").value.current = "debug"
        exit_msg = f"Configuration failed, using default log file location. ({args.log_file})"
        exit_msg += f" Log level set to {args.log_level}"
        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.NOTE))
        exit_msg = "Review the hints and log file to see what went wrong."
        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))

    try:
        Path(args.log_file).touch()
        setup_logger(args)
    except Exception as exc:  # noqa: BLE001
        exit_msg = "The log file path or logging engine could not be setup."
        exit_msg += " No log file will be available, please check the log file"
        exit_msg += f" path setting. The error was {exc!s}"
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
        cache_scripts()

    run_return = run(args)
    run_message = f"{run_return.message}\n"
    if run_return.return_code != 0 and run_return.message:
        sys.stderr.write(run_message)
        sys.exit(run_return.return_code)
    elif run_return.return_code != 0:
        sys.exit(run_return.return_code)
    elif run_return.message:
        sys.stdout.write(run_message)


if __name__ == "__main__":
    main()
