"""some utilities that are specific to ansible_navigator
"""
import ast
import decimal
import html
import logging
import os
import re
import shlex
import shutil
import sys
import sysconfig

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Iterable
from typing import List
from typing import Mapping
from typing import NamedTuple
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

from jinja2 import Environment
from jinja2 import StrictUndefined
from jinja2 import TemplateError


logger = logging.getLogger(__name__)


class Colors(Enum):
    """ANSI color codes"""

    RED = "\033[0;31m"
    YELLOW = "\033[33m"
    END = "\033[0m"


class ExitPrefix(Enum):
    """An exit message prefix"""

    ERROR = "ERROR"
    HINT = "HINT"

    @classmethod
    def _longest(cls):
        return max(len(member) for member in cls.__members__)

    def __str__(self):
        return f"{' ' * (self._longest() - len(self.name))}[{self.name}]: "


@dataclass
class ExitMessage:
    """An object to hold a message to present when exiting."""

    #: The message that will be presented
    message: str
    #: The prefix for the message, used for formatting
    prefix: ExitPrefix = ExitPrefix.ERROR

    @property
    def color(self):
        """return a color for the prefix"""
        if self.prefix is ExitPrefix.ERROR:
            return Colors.RED.value
        if self.prefix is ExitPrefix.HINT:
            return Colors.YELLOW.value
        raise ValueError("Missing color mapping")

    @property
    def level(self):
        """return a log level"""
        if self.prefix is ExitPrefix.ERROR:
            return logging.ERROR
        if self.prefix is ExitPrefix.HINT:
            return logging.INFO
        raise ValueError("Missing logging level mapping")

    def __str__(self):
        if "NO_COLOR" in os.environ:
            return f"{self.prefix}{self.message}"
        return f"{self.color}{self.prefix}{self.message}{Colors.END.value}"


class LogMessage(NamedTuple):
    """An object to hold a message destined for the logger"""

    level: int
    message: str


def oxfordcomma(listed, condition):
    """Format a list into a sentence"""
    listed = [f"'{str(entry)}'" for entry in listed]
    if len(listed) == 0:
        return ""
    if len(listed) == 1:
        return listed[0]
    if len(listed) == 2:
        return f"{listed[0]} {condition} {listed[1]}"
    return f"{', '.join(listed[:-1])} {condition} {listed[-1]}"


def abs_user_path(file_path: str) -> str:
    """Resolve a path"""
    return os.path.abspath(os.path.expanduser(os.path.expandvars(file_path)))


def check_for_ansible() -> Tuple[List[LogMessage], List[ExitMessage]]:
    """check for the ansible-playbook command, runner will need it
    returns exit messages if not found, messages if found
    """
    messages: List[LogMessage] = []
    exit_messages: List[ExitMessage] = []
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


def clear_screen() -> None:
    """print blank lines on the screen, preserving scrollback

    Note: In certain cases, xterm.js based terminals show stdout
    under the initial curses output, this was found with vscode

    Rather than issuing :command:`clear`, print blank lines to
    preserve the user's scrollback buffer.
    """
    affected_terminals = ["vscode"]
    if os.environ.get("TERM_PROGRAM") in affected_terminals:
        for _line in range(shutil.get_terminal_size().lines):
            print()


# TODO: Replace this with something type-safe.
def dispatch(obj, replacements):
    """make the replacement based on type

    :param obj: an obj in which replacements will be made
    :type obj: Any
    :param replacements: the things to replace
    :type replacements: Tuple[Tuple[Any]]
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
    """escape moustaches

    :param obj: something
    :return: the obj with replacements made
    """
    replacements = (("{", "U+007B"), ("}", "U+007D"))
    return dispatch(obj, replacements)


def environment_variable_is_file_path(
    env_var: str,
    kind: str,
) -> Tuple[List[LogMessage], List[ExitMessage], Optional[str]]:
    """check if a given environment var is a viable file path, if so return that path"""
    messages: List[LogMessage] = []
    exit_messages: List[ExitMessage] = []
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


def find_settings_file() -> Tuple[List[LogMessage], List[ExitMessage], Union[None, str]]:
    """find the settings file as
    ./ansible-navigator.(.yml,.yaml,.json)
    ~/.ansible-navigator.(.yml,.yaml,.json)
    """

    messages: List[LogMessage] = []
    exit_messages: List[ExitMessage] = []
    allowed_extensions = ["yml", "yaml", "json"]
    potential_paths: List[List[str]] = []
    found_files: List[str] = []

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


def flatten_list(data_list) -> List:
    """flatten a list of lists"""
    if isinstance(data_list, list):
        return [a for i in data_list for a in flatten_list(i)]
    return [data_list]


def get_share_directory(app_name) -> Tuple[List[LogMessage], List[ExitMessage], Union[None, str]]:
    # pylint: disable=too-many-return-statements
    """
    returns datadir (e.g. /usr/share/ansible_nagivator) to use for the
    ansible-launcher data files. First found wins.
    """
    messages: List[LogMessage] = []
    exit_messages: List[ExitMessage] = []
    share_directory = None

    def debug_log(directory: str, found: bool, description: str):
        template = "Share directory '{directory}' {status} ({description})"
        formatted = template.format(
            directory=directory,
            status="found" if found else "not found",
            description=description,
        )
        msg = LogMessage(level=logging.DEBUG, message=formatted)
        messages.append(msg)

    # Development path
    # We want the share directory to resolve adjacent to the directory the code lives in
    # as that's the layout in the source.
    share_directory = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "share", app_name),
    )
    description = "development path"
    if os.path.exists(share_directory):
        debug_log(share_directory, True, description)
        return messages, exit_messages, share_directory
    debug_log(share_directory, False, description)

    # ~/.local/share/APP_NAME
    userbase = sysconfig.get_config_var("userbase")
    description = "userbase"
    if userbase is not None:
        share_directory = os.path.join(userbase, "share", app_name)
        if os.path.exists(share_directory):
            debug_log(share_directory, True, description)
            return messages, exit_messages, share_directory
    debug_log(share_directory, False, description)

    # /usr/share/APP_NAME  (or the venv equivalent)
    share_directory = os.path.join(sys.prefix, "share", app_name)
    description = "sys.prefix"
    if os.path.exists(share_directory):
        debug_log(share_directory, True, description)
        return messages, exit_messages, share_directory
    debug_log(share_directory, False, description)

    # /usr/share/APP_NAME  (or what was specified as the datarootdir when python was built)
    datarootdir = sysconfig.get_config_var("datarootdir")
    description = "datarootdir"
    if datarootdir is not None:
        share_directory = os.path.join(datarootdir, app_name)
        if os.path.exists(share_directory):
            debug_log(share_directory, True, description)
            return messages, exit_messages, share_directory
    debug_log(share_directory, False, description)

    # /Library/Python/x.y/share/APP_NAME  (common on macOS)
    datadir = sysconfig.get_paths().get("data")
    description = "datadir"
    if datadir is not None:
        share_directory = os.path.join(datadir, "share", app_name)
        if os.path.exists(share_directory):
            debug_log(share_directory, True, description)
            return messages, exit_messages, share_directory
    debug_log(share_directory, False, description)

    # /usr/local/share/APP_NAME
    prefix = sysconfig.get_config_var("prefix")
    description = "prefix"
    if prefix is not None:
        share_directory = os.path.join(prefix, "local", "share", app_name)
        if os.path.exists(share_directory):
            debug_log(share_directory, True, description)
            return messages, exit_messages, share_directory
    debug_log(share_directory, False, description)

    exit_msg = "Unable to find a viable share directory"
    exit_messages.append(ExitMessage(message=exit_msg))
    return messages, exit_messages, None


def divmod_int(numerator: Union[int, float], denominator: Union[int, float]) -> Tuple[int, int]:
    """Return the result of divmod, as a tuple of integers."""
    quotient, remainder = divmod(numerator, denominator)
    return int(quotient), int(remainder)


def human_time(seconds: Union[int, float]) -> str:
    """Convert seconds into human readable 00d00h00m00s format."""
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


PASCAL_REGEX = re.compile("((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")


def pascal_to_snake(obj):
    """convert a pascal cased object
    into a snake cased object recursively
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
    if sys.version_info >= (3, 9):
        return child.is_relative_to(parent)
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def remove_ansi(string):
    """strip ansi code from a str"""
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
    """remove a __ from the beginning of a string"""
    if string.startswith("__"):
        return string.replace("__", "", 1)
    return string


def round_half_up(number: Union[float, int]) -> int:
    """Round a number to the nearest integer with ties going away from zero.

    This is different the round() where exact halfway cases are rounded to the nearest
    even result instead of away from zero. (e.g. round(2.5) = 2, round(3.5) = 4).

    This will always round based on distance from zero. (e.g round(2.5) = 3, round(3.5) = 4).

    :param number: The number to round
    :return: The rounded number as an it
    """
    rounded = decimal.Decimal(number).quantize(decimal.Decimal("1"), rounding=decimal.ROUND_HALF_UP)
    return int(rounded)


def shlex_join(tokens: Iterable[str]) -> str:
    """Concatenate the tokens of a list and return a string.

    ``shlex.join`` was new in version 3.8

    :param tokens: The iterable of strings to join
    :returns: The iterable joined with spaces
    """
    if sys.version_info >= (3, 8):
        return shlex.join(split_command=tokens)
    return " ".join(shlex.quote(token) for token in tokens)


def str2bool(value: Any) -> bool:
    """Convert some commonly used values
    to a boolean
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
def templar(string: str, template_vars: Mapping) -> Tuple[List[str], Any]:
    """template some string with jinja2
    always to and from json so we return an object if it is

    :param string: The template string
    :param template_vars: The vars used to render the template
    :return: A list of errors and either the result of templating or original string
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
        errors.append(f"The error was: {str(exc)}")
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


def to_list(thing: Union[str, List, Tuple, Set, None]) -> List:
    """convert something to a list if necessary"""
    if isinstance(thing, (list, tuple, set)):
        converted_value = list(thing)
    elif thing is not None:
        converted_value = [thing]
    else:
        converted_value = []
    return converted_value


def unescape_moustaches(obj: Any) -> Mapping:
    """unescape moustaches

    :param obj: something
    :return: the obj with replacements made
    """
    replacements = (("U+007B", "{"), ("U+007D", "}"))
    return dispatch(obj, replacements)
