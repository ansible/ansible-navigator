"""Produce a diagnostics report in json format."""
import json
import sys
import traceback

from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

from pkg_resources import working_set

from .command_runner import Command
from .command_runner import CommandRunner
from .configuration_subsystem import ApplicationConfiguration
from .configuration_subsystem import to_effective
from .configuration_subsystem import to_sources
from .image_manager import introspect
from .image_manager import introspector
from .utils.functions import ExitMessage
from .utils.functions import LogMessage
from .utils.functions import now_iso
from .utils.functions import shlex_join
from .utils.serialize import Loader
from .utils.serialize import yaml


class C:  # pylint: disable=invalid-name
    """Color constants."""

    GREY = "\033[90m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    END = "\033[0m"


def collecting(info_type: str):
    """Output information to the console.

    :param info_type: The type of information being collected
    """
    information = f"Collecting {info_type} information".ljust(50, ".")
    working(information)


def finish(info_type: str):
    """Output information to the console.

    :param info_type: The type of information being collected
    """
    information = f"\r{info_type.capitalize()} information collected.\033[K"
    success(information)


def fail(message: str):
    """Output information to the console.

    :param message: The message to output
    """
    print(f"{C.RED}{message}{C.END}")


def success(message: str):
    """Output information to the console.

    :param message: The message to output
    """
    print(f"{C.GREEN}{message}{C.END}")


def working(message: str):
    """Output information to the console.

    :param message: The message to output
    """
    print(f"{C.GREY}{message}{C.END}", end="", flush=True)


def run(
    args: ApplicationConfiguration,
    messages: List[LogMessage],
    exit_messages=List[ExitMessage],
):
    """Collect as much information as possible about everything and dump to a json file.

    :param args: The current settings
    :param messages: The current log messages
    :param exit_messages: The current exit messages
    """
    try:
        _run(args, messages, exit_messages)
    except Exception:  # pylint: disable=broad-except
        time = now_iso("local")
        path = Path(f"show_tech_{time}.json")
        path.write_text(
            json.dumps({"__ERROR__": traceback.format_exc().splitlines()}, indent=4),
            encoding="utf-8",
        )
        fail("Diagnostics failed, written to: {path}")
        sys.exit(1)


def _run(
    args: "ApplicationConfiguration", messages: List[LogMessage], exit_messages=List[ExitMessage]
):
    """Collect as much information as possible about everything and dump to a json file.

    :param args: The current settings
    :param messages: The current log messages
    :param exit_messages: The current exit messages
    """
    full_details: Dict[str, Any] = {}
    full_details[
        "__WARNING__"
    ] = "The following output may contain sensitive data, please review it carefully."

    info_type = "basic"
    collecting(info_type)
    full_details["basics"] = {
        "application_name": args.application_name,
        "application_version": args.application_version,
        "action_packages": args.internals.action_packages,
        "original_command": shlex_join(sys.argv),
        "settings_file_path": str(args.internals.settings_file_path),
        "settings_source": str(args.internals.settings_source),
        "share_directory": args.internals.share_directory,
    }
    finish(info_type)

    info_type = "container_engine"
    collecting(info_type)
    full_details["container_engines"] = {}
    commands = [
        Command(identity="podman", command="podman --version", post_process=lambda c: c),
        Command(identity="docker", command="docker --version", post_process=lambda c: c),
    ]
    CommandRunner().run_single_proccess(commands)
    for command in commands:
        full_details["container_engines"][command.identity] = {
            "return_code": command.return_code,
            "selected": args.container_engine == command.identity,
            "stdout": command.stdout,
            "stderr": command.stderr,
        }
    finish(info_type)

    info_type = "initialization"
    collecting(info_type)
    full_details["initialization"] = {
        "messages": [msg.message for msg in messages],
        "exit_messages": [msg.message for msg in exit_messages],
    }
    finish(info_type)

    info_type = "execution_environment"
    collecting(info_type)
    details, errors, return_code = introspector.run(
        image_name=args.execution_environment_image,
        container_engine=args.container_engine,
    )
    details = {"details": details, "errors": errors, "return_code": return_code}
    full_details["execution_environment"] = details
    finish(info_type)

    info_type = "local_system"
    collecting(info_type)
    results = introspect.main(serialize=False, process_model="multi_thread")
    if results:
        full_details["local"] = {"errors": results.pop("errors")}
        for section, information in results.items():
            # pylint: disable=invalid-sequence-index
            full_details["local"][section] = information["details"]
    finish(info_type)

    info_type = "python_dependencies"
    collecting(info_type)
    full_details["python_packages"] = sorted(
        [
            f"{i.key}=={i.version} {i.location}"
            for i in working_set  # pylint: disable=not-an-iterable
        ]
    )
    finish(info_type)

    info_type = "settings"
    collecting(info_type)
    full_details["settings"] = {
        "effective": to_effective(args),
        "sources": to_sources(args),
    }
    finish(info_type)

    info_type = "settings_file"
    collecting(info_type)
    if args.internals.settings_file_path:
        contents = Path(args.internals.settings_file_path).read_text(encoding="utf-8")
        full_details["settings"]["settings_file_contents"] = yaml.load(contents, Loader=Loader)
    else:
        full_details["settings"]["settings_file_contents"] = {}
    finish(info_type)

    time = now_iso("local")
    path = Path(f"show_tech_{time}.json")
    path.write_text(json.dumps(full_details, indent=4), encoding="utf-8")
    success(f"Diagnostics written to: {path}.")
    sys.exit(0)
