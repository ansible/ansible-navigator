"""Some utilities that are specific to ansible_navigator."""
from __future__ import annotations

import ast
import datetime
import decimal
import html
import logging
import os
import re
import shlex
import shutil
import zoneinfo

from collections.abc import Iterable
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from jinja2 import Environment
from jinja2 import StrictUndefined
from jinja2 import TemplateError

from .definitions import GOLDEN_RATIO
from .definitions import ExitMessage
from .definitions import LogMessage


logger = logging.getLogger(__name__)


def oxfordcomma(listed, condition):
    """Format a list into a sentence.

    :param listed: List of string entries to modify
    :param condition: String to splice into string, usually 'and'
    :returns: Modified string
    """
    listed = [f"'{entry!s}'" for entry in listed]
    if len(listed) == 0:
        return ""
    if len(listed) == 1:
        return listed[0]
    if len(listed) == 2:
        return f"{listed[0]} {condition} {listed[1]}"
    return f"{', '.join(listed[:-1])} {condition} {listed[-1]}"


def abs_user_path(file_path: str) -> str:
    """Resolve a path.

    :param file_path: The file path to resolve
    :returns: Resolved file path
    """
    return os.path.abspath(os.path.expanduser(os.path.expandvars(file_path)))


def check_for_ansible() -> tuple[list[LogMessage], list[ExitMessage]]:
    """Check for the ansible-playbook command, runner will need it.

    :returns: Exit messages if not found, messages if found
    """
    messages: list[LogMessage] = []
    exit_messages: list[ExitMessage] = []
    ansible_location = shutil.which("ansible-playbook")
    if not ansible_location:
        msg_parts = [
            "The 'ansible-playbook' command could not be found or was not executable,",
            "ansible is required when running without an Ansible Execution Environment.",
            "Try one of",
            "     'pip install ansible-base'",
            "     'pip install ansible-core'",
            "     'pip install ansible'",
            "or simply",
            "     '-ee' or '--execution-environment'",
            "to use an Ansible Execution Environment",
        ]
        exit_messages.append(ExitMessage(message="\n".join(msg_parts)))
        return messages, exit_messages
    message = f"ansible-playbook found at {ansible_location}"
    messages.append(LogMessage(level=logging.INFO, message=message))
    return messages, exit_messages


def check_playbook_type(playbook: str) -> str:
    """Determine if given playbook is a file, fqcn playbook or something else.

    Note: These checks are added to directly access a playbook provided by a collection
    i.e. `namespace.collection.playbook_name` fqcn format.

    :param playbook: given playbook
    :returns: playbook type
    """
    playbook_type = "file"
    playbook_path = str(playbook)
    if os.path.exists(playbook_path) is False:
        playbook_type = "missing"
    if os.path.exists(playbook_path) is False and len(playbook_path.split(".")) >= 3:
        playbook_type = "fqcn"
    return playbook_type


def clear_screen() -> None:
    """Print blank lines on the screen, preserving scrollback.

    Note: In certain cases, xterm.js based terminals show stdout
    under the initial curses output.

    Rather than issuing :command:`clear`, print blank lines to
    preserve the user's scrollback buffer.
    """
    affected_terminals = ["vscode"]
    if os.environ.get("TERM_PROGRAM") in affected_terminals:
        for _line in range(shutil.get_terminal_size().lines):
            print()


def console_width() -> int:
    """Get a console width based on common screen widths.

    :returns: The console width
    """
    width = shutil.get_terminal_size().columns
    if width <= 80:
        return width
    if width <= 132:
        return max(80, round_half_up(width / GOLDEN_RATIO))
    return 132


# TODO: Replace this with something type-safe.
def dispatch(obj, replacements):
    """Make the replacement based on type.

    :param obj: An obj in which replacements will be made
    :param replacements: The things to replace
    :returns: Variable obj
    """
    if isinstance(obj, dict):
        obj = {k: dispatch(v, replacements) for k, v in obj.items()}
    elif isinstance(obj, list):
        obj = [dispatch(l, replacements) for l in obj]  # noqa: E741
    elif isinstance(obj, str):
        for replacement in replacements:
            obj = obj.replace(replacement[0], replacement[1])
    return obj


def escape_moustaches(obj: Mapping) -> Mapping:
    """Escape moustaches.

    :param obj: Variable that may contain moustaches
    :returns: The obj with replacements made
    """
    replacements = (("{", "U+007B"), ("}", "U+007D"))
    return dispatch(obj, replacements)


def environment_variable_is_file_path(
    env_var: str,
    kind: str,
) -> tuple[list[LogMessage], list[ExitMessage], str | None]:
    """Check if a given environment variable is a viable file path, and if so, return that path.

    :param env_var: Environment variable to check for a file path
    :param kind: Type of file
    :returns: Log messages and file path

    """
    messages: list[LogMessage] = []
    exit_messages: list[ExitMessage] = []
    file_path = None
    candidate_path = os.environ.get(env_var)
    if candidate_path is None:
        messages.append(LogMessage(level=logging.DEBUG, message=f"No {kind} file set by {env_var}"))
    else:
        message = f"Found a {kind} file at {candidate_path} set by {env_var}"
        messages.append(LogMessage(level=logging.DEBUG, message=message))
        if os.path.isfile(candidate_path) and os.path.exists(candidate_path):
            file_path = candidate_path
            message = f"{kind.capitalize()} file at {file_path} set by {env_var} is viable"
            messages.append(LogMessage(level=logging.DEBUG, message=message))
            exp_path = os.path.abspath(os.path.expanduser(file_path))
            if exp_path != file_path:
                message = f"{kind.capitalize()} resolves to {exp_path}"
                messages.append(LogMessage(level=logging.DEBUG, message=message))
                file_path = exp_path
        else:
            message = f"{env_var} set as {candidate_path} but not valid"
            messages.append(LogMessage(level=logging.DEBUG, message=message))
    return messages, exit_messages, file_path


def find_settings_file() -> tuple[list[LogMessage], list[ExitMessage], str | None]:
    """Find the settings file.

    Find the file at ./ansible-navigator.(.yml,.yaml,.json),
    or ~/.ansible-navigator.(.yml,.yaml,.json).

    :returns: Log messages and correct settings file to use
    """
    messages: list[LogMessage] = []
    exit_messages: list[ExitMessage] = []
    allowed_extensions = ["yml", "yaml", "json"]
    potential_paths: list[list[str]] = []
    found_files: list[str] = []

    potential_paths.append([os.path.expanduser("~"), ".ansible-navigator"])
    potential_paths.append([os.getcwd(), "ansible-navigator"])

    for path in potential_paths:
        message = f"Looking in {path[0]}"
        messages.append(LogMessage(level=logging.DEBUG, message=message))

        candidates = [os.path.join(path[0], f"{path[1]}.{ext}") for ext in allowed_extensions]
        message = f"Looking for {oxfordcomma(candidates, 'and')}"
        messages.append(LogMessage(level=logging.DEBUG, message=message))

        found = [file for file in candidates if os.path.exists(file)]
        message = f"Found {len(found)}: {oxfordcomma(found, 'and')}"
        messages.append(LogMessage(level=logging.DEBUG, message=message))

        if len(found) > 1:
            exit_msg = f"Only one file among {oxfordcomma(candidates, 'and')}"
            exit_msg += f" should be present in {path[0]}"
            exit_msg += f" Found: {oxfordcomma(found, 'and')}"
            exit_messages.append(ExitMessage(message=exit_msg))
            return messages, exit_messages, None
        found_files.extend(found)

    message = f"All found {len(found_files)}: {oxfordcomma(found_files, 'and')}"
    messages.append(LogMessage(level=logging.DEBUG, message=message))

    use = found_files[-1] if found_files else None
    message = f"Using: {use}"
    messages.append(LogMessage(level=logging.DEBUG, message=message))

    return messages, exit_messages, use


def flatten_list(data_list) -> list:
    """Flatten a list of lists.

    :param data_list: List to flatten
    :returns: Flattened list
    """
    if isinstance(data_list, list):
        return [a for i in data_list for a in flatten_list(i)]
    return [data_list]


def generate_cache_path(app_name: str) -> Path:
    """Return the path to the cache directory.

    :param app_name: Name of application - currently ansible_navigator
    :returns: Path to the cache directory
    """
    cache_home = os.environ.get("XDG_CACHE_HOME", f"{os.path.expanduser('~')}/.cache")
    return Path(cache_home) / app_name


def divmod_int(numerator: int | float, denominator: int | float) -> tuple[int, int]:
    """Return the result of divmod, as a tuple of integers.

    :param numerator: Numerator for divmod
    :param denominator: Denominator for divmod
    :returns: Quotient and remainder of divmod
    """
    quotient, remainder = divmod(numerator, denominator)
    return int(quotient), int(remainder)


def human_time(seconds: int | float) -> str:
    """Convert seconds into human readable 00d00h00m00s format.

    :param seconds: Time in seconds
    :returns: Human readable conversion of seconds
    """
    sign_string = "-" if seconds < 0 else ""
    seconds = abs(int(seconds))
    days, seconds = divmod_int(seconds, 86400)
    hours, seconds = divmod_int(seconds, 3600)
    minutes, seconds = divmod_int(seconds, 60)
    if days > 0:
        return f"{sign_string!s}{days:d}d{hours:d}h{minutes:d}m{seconds:d}s"
    if hours > 0:
        return f"{sign_string!s}{hours:d}h{minutes:d}m{seconds:d}s"
    if minutes > 0:
        return f"{sign_string!s}{minutes:d}m{seconds:d}s"
    return f"{sign_string!s}{seconds:d}s"


def is_jinja(string: str) -> bool:
    """Determine if a string is a Jinja2 template.

    :param string: The string to check.
    :return: True if the string is a Jinja2 template, False otherwise.
    """
    try:
        return string.index("{{") < string.index("}}")
    except ValueError:
        return False


def now_iso(time_zone: str) -> str:
    """Return the current time as an ISO 8601 formatted string, given a time zone.

    :param time_zone: The IANA timezone name or local
    :returns: The ISO 8601 formatted time zone string
    """
    if time_zone == "local":
        return datetime.datetime.now(tz=datetime.timezone.utc).astimezone().isoformat()
    try:
        return datetime.datetime.now(tz=zoneinfo.ZoneInfo(time_zone)).isoformat()
    except zoneinfo.ZoneInfoNotFoundError:
        logger.error("The time zone '%s' could not be found. Using UTC.", time_zone)
        return datetime.datetime.now(tz=datetime.timezone.utc).isoformat()


PASCAL_REGEX = re.compile("((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")


def pascal_to_snake(obj):
    """Convert a pascal cased object into a snake cased object recursively.

    :param obj: Pascal cased object
    :returns: Snake cased object
    """
    if isinstance(obj, list):
        working = [pascal_to_snake(x) for x in obj]
        return working
    if isinstance(obj, dict):
        working = {}
        for k, val in obj.items():
            new_key = PASCAL_REGEX.sub(r"_\1", k).lower()
            working[new_key] = pascal_to_snake(val)
        return working
    return obj


def path_is_relative_to(child: Path, parent: Path) -> bool:
    """Return True if the path is relative to another path or False.

    :param child: The path that may be a child
    :param parent: The path that may be a parent
    :returns: Indicates the child is a child of the parent
    """
    return child.is_relative_to(parent)


def remove_ansi(string):
    """Strip ansi code from a str.

    :param string: String to strip ansi code from
    :returns: String without ansi code
    """
    ansi_escape = re.compile(
        r"""
            \x1B  # ESC
            (?:   # 7-bit C1 Fe (except CSI)
                [@-Z\\-_]
            |     # or [ for CSI, followed by a control sequence
                \[
                [0-?]*  # Parameter bytes
                [ -/]*  # Intermediate bytes
                [@-~]   # Final byte
            )
        """,
        re.VERBOSE,
    )
    return ansi_escape.sub("", string)


def remove_dbl_un(string):
    """Remove a __ from the beginning of a string.

    :param string: String to remove __ from
    :returns: String without __
    """
    if string.startswith("__"):
        return string.replace("__", "", 1)
    return string


def round_half_up(number: float | int) -> int:
    """Round a number to the nearest integer with ties going away from zero.

    This is different the round() where exact halfway cases are rounded to the nearest
    even result instead of away from zero. (e.g. round(2.5) = 2, round(3.5) = 4).

    This will always round based on distance from zero. (e.g round(2.5) = 3, round(3.5) = 4).

    :param number: The number to round
    :returns: The rounded number as an it
    """
    rounded = decimal.Decimal(number).quantize(decimal.Decimal("1"), rounding=decimal.ROUND_HALF_UP)
    return int(rounded)


def shlex_join(tokens: Iterable[str]) -> str:
    """Concatenate the tokens of a list and return a string.

    :param tokens: The iterable of strings to join
    :returns: The iterable joined with spaces
    """
    return shlex.join(split_command=tokens)


def str2bool(value: Any) -> bool:
    """Convert some commonly used values to a boolean.

    :param value: Value to convert to boolean
    :raises ValueError: If value is not a boolean or string
    :returns: New converted boolean
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        if value.lower() in ("yes", "true"):
            return True
        if value.lower() in ("no", "false"):
            return False
    raise ValueError


# TODO: We are kind-of screwed type-wise by the fact that ast.literal_eval()
#       returns Any. Need to find a better solution... "Any" isn't it.
def templar(string: str, template_vars: Mapping) -> tuple[list[str], Any]:
    """Template some string with jinja2 always to and from json.

    :param string: The template string
    :param template_vars: The vars used to render the template
    :returns: A list of errors and either the result of templating or original string
    """
    errors = []
    # hide the jinja that may be in the template_vars
    template_vars = escape_moustaches(template_vars)

    env = Environment(autoescape=True, undefined=StrictUndefined)
    try:
        template: Any = env.from_string(string)
        result = template.render(template_vars)
    except (ValueError, TemplateError) as exc:
        errors.append(f"Error while templating string: '{string}'")
        errors.append(f"The error was: {exc!s}")
        for error in errors:
            logger.error(error)
        return errors, string

    # We may have gotten the __repr__ of a python object
    # so let's try and turn it back
    try:
        logger.debug("original templated string: %s", result)
        escaped = html.unescape(result)
        logger.debug("html escaped templated str: %s", escaped)
        result = ast.literal_eval(escaped)
    except (ValueError, SyntaxError) as exc:
        logger.debug("Could not ast parse templated string")
        logger.debug("error was: %s", str(exc))
        logger.debug("attempted on %s", result)

    result = unescape_moustaches(result)  # type: ignore[assignment, arg-type]
    return errors, result


def timestamp_to_iso(timestamp: float, time_zone: str) -> str | None:
    """Generate an ISO 8601 date time string from a timestamp.

    :param timestamp: The unix timestamp
    :param time_zone: The time zone
    :returns: The ISO string
    """
    try:
        if time_zone == "local":
            return (
                datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
                .astimezone()
                .isoformat()
            )
        return datetime.datetime.fromtimestamp(
            timestamp,
            tz=zoneinfo.ZoneInfo(time_zone),
        ).isoformat()
    except zoneinfo.ZoneInfoNotFoundError:
        logger.error("The time zone '%s' could not be found. Returning None", time_zone)
        return None


def time_stamp_for_file(path: str, time_zone: str) -> tuple[float | None, str | None]:
    """Get a timestamp for a file path.

    :param path: The file path
    :param time_zone: Time zone
    :returns: The UNIX timestamp and an ISO 8601 string
    """
    try:
        modified = os.path.getmtime(path)
    except FileNotFoundError:
        # It may have been mounted to a different location in the execution environment
        modified = None
    if modified is not None:
        iso_stamp = timestamp_to_iso(timestamp=modified, time_zone=time_zone)
    else:
        iso_stamp = None
    return modified, iso_stamp


def to_list(thing: str | list | tuple | set | None) -> list:
    """Convert something to a list if necessary.

    :param thing: Item to convert to a list
    :returns: Item as a list
    """
    if isinstance(thing, (list, tuple, set)):
        converted_value = list(thing)
    elif thing is not None:
        converted_value = [thing]
    else:
        converted_value = []
    return converted_value


def unescape_moustaches(obj: Any) -> Mapping:
    """Unescape moustaches.

    :param obj: Variable that needs to contain moustaches
    :returns: The obj with replacements made
    """
    replacements = (("U+007B", "{"), ("U+007D", "}"))
    return dispatch(obj, replacements)
