""" start here
"""
import logging
import os
import sys
import signal


from argparse import ArgumentParser, Namespace
from typing import List
from typing import Union


from configparser import ConfigParser
from distutils.spawn import find_executable

from curses import wrapper
from .cli_args import CliArgs
from .action_runner import ActionRunner
from .player import Player
from .utils import find_ini_config_file
from .web_xterm_js import WebXtermJs

logger = logging.getLogger()

APP_NAME = "winston"


def check_for_ansible() -> None:
    """check for the ansible-playbook command, runner will need it"""
    ansible_location = find_executable("ansible-playbook")
    if not ansible_location:
        msg = [
            "The 'ansible-playbook' command could not be found or was not executable,",
            "ansible is required when running without an Ansible Execution Environment.",
            "Try one of",
            "     'pip install ansible-base'",
            "     'pip install ansible-core'",
            "     'pip install ansible'",
            "or simply",
            "     '-ee' or '--execution-environment'",
            "to use an Ansible Execution Enviroment",
        ]

        logger.critical("\n".join(msg))
        print("\x1b[31m[ERROR]: {msg}".format(msg="\n".join(msg)))
        sys.exit(1)
    else:
        logger.debug("ansible-playbook found at %s", ansible_location)


def set_ansible_envar():
    """Set an envar if not set, runner will need this"""
    ansible_config = find_ini_config_file("ansible")
    # set as env var, since we hand env vars over to runner
    if ansible_config and not os.getenv("ANSIBLE_CONFIG"):
        os.environ.setdefault("ANSIBLE_CONFIG", ansible_config)
        logger.debug("ANSIBLE_CONFIG set to %s", ansible_config)


def update_args(
    config_file: Union[str, None], args: Namespace, parser: ArgumentParser
) -> List[str]:
    # pylint: disable=too-many-nested-blocks
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
        if config_file and config.has_section("default"):
            cdict = dict(config)
            section = cdict.get("default")
            if section:
                for key, value in section.items():
                    if (arg_value := getattr(args, key, None)) and arg_value is not None:
                        default: Union[None, str] = parser.get_default(key)
                        if isinstance(arg_value, bool):
                            bool_key: bool = section.getboolean(key)
                            if bool_key != arg_value == default:
                                msg = f"{key} was default, using entry '{key}={bool_key}' as bool"
                                msgs.append(msg)
                                setattr(args, key, bool_key)
                        elif default == arg_value != value:
                            msg = f"{key} was default, using entry '{key}={value}"
                            msgs.append(msg)
                            setattr(args, key, value)
                    if hasattr(args, key) and getattr(args, key) is None:
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


def main():
    """start here"""

    # pylint: disable=too-many-branches

    parser = CliArgs(APP_NAME).parser
    args, cmdline = parser.parse_known_args()
    args.cmdline = cmdline

    config_file = find_ini_config_file(APP_NAME)
    ua_msgs = update_args(config_file, args, parser)

    args.logfile = os.path.abspath(args.logfile)
    setup_logger(args)

    for msg in ua_msgs:
        logger.debug(msg)

    handle_ide(args)

    if hasattr(args, "artifact") and args.artifact:
        args.artifact = os.path.abspath(args.artifact)

    if args.app == "load" and not os.path.exists(args.artifact):
        parser.error(f"The file specified with load could not be found. {args.load}")

    for key, value in vars(args).items():
        logger.debug("Running with %s=%s %s", key, value, type(value))

    os.environ.setdefault("ESCDELAY", "25")
    os.system("clear")

    if not hasattr(args, "requires_ansible") or args.requires_ansible:
        if not args.execution_environment:
            check_for_ansible()
        set_ansible_envar()

    if args.web:
        args.no_osc4 = True

    if not args.app:
        args.app = "welcome"
        args.value = None

    args.share_dir = os.path.join(sys.prefix, "share", APP_NAME)

    try:
        if args.app in ["playbook", "playquietly"]:
            app = Player(args=args).playbook
            if args.web:
                WebXtermJs().run(func=app)
            else:
                app()
        else:
            if args.app == "explore":
                app = Player(args=args).explore
            elif args.app == "load":
                app = Player(args=args).load
            else:
                app = ActionRunner(args=args).run
            if args.web:
                WebXtermJs().run(curses_app=app)
            else:
                wrapper(app)
    except KeyboardInterrupt:
        logger.warning("Dirty exit, killing the pid")
        os.kill(os.getpid(), signal.SIGTERM)


if __name__ == "__main__":
    main()
