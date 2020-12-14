""" start here
"""
import itertools
import logging
import os
import sys
import signal

from argparse import _SubParsersAction
from argparse import ArgumentParser
from argparse import Namespace
from functools import partial
from typing import Callable
from typing import List
from typing import Tuple
from typing import Union


from configparser import ConfigParser

from curses import wrapper

from .actions.explore import Action as Player

from .cli_args import CliArgs
from .action_runner import ActionRunner
from .utils import check_for_ansible
from .utils import find_ini_config_file
from .utils import set_ansible_envar
from .web_xterm_js import WebXtermJs

logger = logging.getLogger()

APP_NAME = "winston"


class NoSuch:  # pylint: disable=too-few-public-methods
    """sentinal"""


# pylint: disable=protected-access
def get_default(parser: ArgumentParser, section: str, name: str) -> Union[str, NoSuch]:
    """get a default value from the root or subparsers"""
    if section == "default":
        return parser.get_default(name)
    subparser_action = next(
        action for action in parser._actions if isinstance(action, _SubParsersAction)
    )
    choice = subparser_action.choices.get(section, "")
    if isinstance(choice, ArgumentParser):
        if default := choice.get_default(name):
            return default
    return NoSuch()


# pylint: enable=protected-access


def update_args(
    config_file: Union[str, None], args: Namespace, parser: ArgumentParser
) -> List[str]:
    # pylint: disable=too-many-nested-blocks
    # pylint: disable=too-many-branches
    """Update the provided args with ansible.cfg entries

    :param args: the cli args
    :type args: args namespace
    :param parser: the arg parser
    :type parser: ArgParse instance
    """
    msgs = []
    if config_file:
        msgs.append(f"Using {config_file}")
        config = ConfigParser()
        config.read(config_file)
        if config_file:
            cdict = dict(config)
            for section_name, section in cdict.items():
                for key, value in section.items():
                    if hasattr(args, key):
                        if (arg_value := getattr(args, key)) is not None:
                            default = get_default(parser, section_name, key)
                            if isinstance(default, NoSuch):
                                continue

                            if isinstance(arg_value, bool):
                                bool_key: bool = section.getboolean(key)
                                if bool_key != arg_value == default:
                                    msg = (
                                        f"{key} was default, using entry '{key}={bool_key}' as bool"
                                    )
                                    msgs.append(msg)
                                    setattr(args, key, bool_key)
                            elif arg_value == [] and default is None and value:
                                use_value = [value.split(",")]
                                setattr(args, key, use_value)
                                msg = f"{key} was default list, "
                                msg += f"using entry.split(',') '{key}:{use_value}'"
                                msgs.append(msg)
                            elif default == arg_value != value:
                                setattr(args, key, value)
                                msg = f"{key} was default, using entry '{key}={value}'"
                                msgs.append(msg)
                        else:
                            msg = f"{key} was not provided, using entry '{key}={value}'"
                            msgs.append(msg)
                            setattr(args, key, value)
    else:
        msgs.append("No config file file found")
    return msgs


def handle_ide(args: Namespace) -> None:
    """Based on the IDE, set the editor and other args"""
    if args.ide == "vim":
        args.editor = "vi +{line_number} {filename}"
    elif args.ide == "vscode":
        args.editor = "code -g {filename}:{line_number}"
    elif args.ide == "pycharm":
        args.editor = "charm  --line {line_number} {filename}"


def setup_logger(args):
    """set up the logger

    :param args: The cli args
    :type args: argparse namespace
    """
    if os.path.exists(args.logfile):
        with open(args.logfile, "w"):
            pass
    hdlr = logging.FileHandler(args.logfile)
    formatter = logging.Formatter("%(asctime)s %(levelname)s '%(module)s.%(funcName)s' %(message)s")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(getattr(logging, args.loglevel.upper()))


def parse_and_update(params: List, error_cb: Callable = None) -> Tuple[List[str], Namespace]:
    """parse some params and update"""
    parser = CliArgs(APP_NAME).parser

    if error_cb:
        parser.error = error_cb  # type: ignore
    args, cmdline = parser.parse_known_args(params)
    args.cmdline = cmdline

    config_file = find_ini_config_file(APP_NAME)
    pre_logger_msgs = update_args(config_file, args, parser)

    args.logfile = os.path.abspath(args.logfile)
    handle_ide(args)

    if args.app == "load" and not os.path.exists(args.artifact):
        parser.error(f"The file specified with load could not be found. {args.load}")

    if hasattr(args, "inventory"):
        args.inventory = list(itertools.chain.from_iterable(args.inventory))

    if hasattr(args, "artifact"):
        if hasattr(args, "playbook") and args.artifact == get_default(parser, args.app, "artifact"):
            args.artifact = f"{os.path.splitext(args.playbook)[0]}_artifact.json"
        else:
            args.artifact = os.path.abspath(args.artifact)

    if args.web:
        args.no_osc4 = True

    if not args.app:
        args.app = "welcome"
        args.value = None

    args.share_dir = os.path.join(sys.prefix, "share", APP_NAME)
    args.original_command = params

    return pre_logger_msgs, args


def run(args: Namespace) -> None:
    """run the appropriate app"""
    try:
        if args.app in ["playbook", "playquietly"]:
            non_ui_app = partial(Player().playbook, args)
            if args.web:
                WebXtermJs().run(func=non_ui_app)
            else:
                non_ui_app()
        else:
            if args.web:
                WebXtermJs().run(curses_app=ActionRunner(args=args).run)
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
                print(f"\x1b[31m[ERROR]: {msg}")
                sys.exit(1)
        set_ansible_envar()

    for key, value in vars(args).items():
        logger.debug("Running with %s=%s %s", key, value, type(value))

    run(args)


if __name__ == "__main__":
    main()
