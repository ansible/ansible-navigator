""" some utilities that are specific to ansible_navigator
"""
import ast

import logging
import html
import os
import stat
import sys
import sysconfig

from distutils.spawn import find_executable

from typing import Any
from typing import List
from typing import Mapping
from typing import NamedTuple
from typing import Optional
from typing import Tuple
from typing import Union

from jinja2 import Environment, TemplateError


logger = logging.getLogger(__name__)

try:
    from ansible.errors import AnsibleError  # type: ignore
    from ansible.template import Templar  # type: ignore

    HAS_ANSIBLE = True
except ImportError:
    HAS_ANSIBLE = False


class LogMessage(NamedTuple):
    """An object ot hold a message destin for the logger"""

    level: int
    message: str


def abs_user_path(fpath: str) -> str:
    """Resolve a path"""
    return os.path.abspath(os.path.expanduser(fpath))


def check_for_ansible() -> Tuple[bool, str]:
    """check for the ansible-playbook command, runner will need it"""
    ansible_location = find_executable("ansible-playbook")
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
            "to use an Ansible Execution Enviroment",
        ]
        return False, "\n".join(msg_parts)
    msg = f"ansible-playbook found at {ansible_location}"
    return True, msg


def dispatch(obj, replacements):
    """make the replacement based on type

    :param obj: an obj in which replacements will be made
    :type obj: any
    :param replacements: the things to replace
    :type replacements: tuple of tuples
    """
    if isinstance(obj, dict):
        obj = {k: dispatch(v, replacements) for k, v in obj.items()}
    elif isinstance(obj, list):
        obj = [dispatch(l, replacements) for l in obj]  # noqa: E741
    elif isinstance(obj, str):
        for replacement in replacements:
            obj = obj.replace(replacement[0], replacement[1])
    return obj


def escape_moustaches(obj):
    """escape moustaches

    :param obj: something
    :type obj: any
    :return: the obj with replacements made
    :rtype: any
    """
    replacements = (("{", "U+007B"), ("}", "U+007D"))
    return dispatch(obj, replacements)


def environment_variable_is_file_path(
    env_var: str, kind: str
) -> Tuple[List[LogMessage], List[str], Optional[str]]:
    """check if a given env var is a vialbe file path, if so return that path"""
    messages: List[LogMessage] = []
    errors: List[str] = []
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
    return messages, errors, file_path


def find_configuration_file_in_directory(
    path: str, filename: str, allowed_extensions: List
) -> Tuple[List[LogMessage], List[str], Optional[str]]:
    """check if filename is present in given path with allowed
    extensions. If multiple files are present it throws an error
    as only a single valid config file can be present in the
    given path.
    """
    messages: List[LogMessage] = []
    errors: List[str] = []
    config_files_found = []
    config_file = None
    valid_file_names = [
        f"{filename}.{allowed_extension}" for allowed_extension in allowed_extensions
    ]
    for name in valid_file_names:
        candidate_config_path = os.path.join(path, name)
        if not os.path.exists(candidate_config_path):
            message = f"Skipping {path}/{name} because it does not exist"
            messages.append(LogMessage(level=logging.DEBUG, message=message))
            continue
        config_files_found.append(candidate_config_path)

    if len(config_files_found) > 1:
        error = "only one file among '{0}' should be present under" " directory '{1}'".format(
            ", ".join(valid_file_names), path
        )
        error += " instead multiple config files" " found '{0}'".format(
            ", ".join(config_files_found)
        )
        errors.append(error)
        return messages, errors, config_file

    if len(config_files_found) == 1:
        config_file = config_files_found[0]

    return messages, errors, config_file


def find_configuration_directory_or_file_path(
    filename: Optional[str] = None, allowed_extensions: Optional[List] = None
) -> Tuple[List[LogMessage], List[str], Optional[str]]:
    """
    returns config dir (e.g. /etc/ansible-navigator) if filename is None and
    config file path if filename provided. First found wins.
    If a filename is given, ensures the file exists in the directory.

    TODO: This is a pretty expensive function (lots of statting things on disk).
          We should probably cache the potential paths somewhere, eventually.
    """
    messages: List[LogMessage] = []
    errors: List[str] = []

    config_path: Union[None, str] = None
    potential_paths: List[str] = []

    # .ansible-navigator of current direcotry
    potential_paths.append(".ansible-navigator")

    # Development path
    path = os.path.join(os.path.dirname(__file__), "..", "etc", "ansible-navigator")
    potential_paths.append(path)

    # ~/.config/ansible-navigator
    path = os.path.join(os.path.expanduser("~"), ".config", "ansible-navigator")
    potential_paths.append(path)

    # /etc/ansible-navigator
    path = os.path.join("/", "etc", "ansible-navigator")
    potential_paths.append(path)

    # /usr/local/etc/ansible-navigator
    prefix = sysconfig.get_config_var("prefix")
    if prefix:
        path = os.path.join(prefix, "local", "etc", "ansible-navigator")
        potential_paths.append(path)

    for path in potential_paths:
        if allowed_extensions:
            if not filename:
                error = f"allowed_extensions '{allowed_extensions}' requires filename to be set"
                errors.append(error)
                return messages, errors, config_path

            new_messages, new_errors, config_path = find_configuration_file_in_directory(
                path, filename, allowed_extensions
            )
            messages.extend(new_messages)
            errors.extend(new_errors)
            if errors:
                return messages, errors, config_path

            if config_path is None:
                continue
        else:
            config_path = os.path.join(path, filename) if filename is not None else path
            if not os.path.exists(config_path):
                message = f"Skipping {path} because required file {filename} does not exist"
                messages.append(LogMessage(level=logging.DEBUG, message=message))
                continue

        try:
            perms = os.stat(path)
            if perms.st_mode & stat.S_IWOTH:
                message = f"Ignoring configuration directory {path} because it is world-writable."
                messages.append(LogMessage(level=logging.DEBUG, message=message))
                continue
            return messages, errors, config_path
        except OSError:
            continue
    return messages, errors, config_path


def flatten_list(lyst) -> List:
    """flatten a list of lists"""
    if isinstance(lyst, list):
        return [a for i in lyst for a in flatten_list(i)]
    return [lyst]


def get_share_directory(app_name) -> Tuple[List[LogMessage], List[str], Union[None, str]]:
    """
    returns datadir (e.g. /usr/share/ansible_nagivator) to use for the
    ansible-launcher data files. First found wins.
    """
    messages: List[LogMessage] = []
    errors: List[str] = []
    share_directory = None

    # Development path
    # We want the share directory to resolve adjacent to the directory the code lives in
    # as that's the layout in the source.
    share_directory = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "share", app_name)
    )
    message = "Share directory {0} (development path)"
    if os.path.exists(share_directory):
        messages.append(LogMessage(level=logging.DEBUG, message=message.format("found")))
        return messages, errors, share_directory
    messages.append(LogMessage(level=logging.DEBUG, message=message.format("not found")))

    # ~/.local/share/APP_NAME
    userbase = sysconfig.get_config_var("userbase")
    message = "Share directory {0} (userbase)"
    if userbase is not None:
        share_directory = os.path.join(userbase, "share", app_name)
        if os.path.exists(share_directory):
            messages.append(LogMessage(level=logging.DEBUG, message=message.format("found")))
            return messages, errors, share_directory
    messages.append(LogMessage(level=logging.DEBUG, message=message.format("not found")))

    # /usr/share/APP_NAME  (or the venv equivalent)
    share_directory = os.path.join(sys.prefix, "share", app_name)
    message = "Share directory {0} (sys.prefix)"
    if os.path.exists(share_directory):
        messages.append(LogMessage(level=logging.DEBUG, message=message.format("found")))
        return messages, errors, share_directory
    messages.append(LogMessage(level=logging.DEBUG, message=message.format("not found")))

    # /usr/share/APP_NAME  (or what was specified as the datarootdir when python was built)
    datarootdir = sysconfig.get_config_var("datarootdir")
    message = "Share directory {0} (datarootdir)"
    if datarootdir is not None:
        share_directory = os.path.join(datarootdir, app_name)
        if os.path.exists(share_directory):
            messages.append(LogMessage(level=logging.DEBUG, message=message.format("found")))
            return messages, errors, share_directory
    messages.append(LogMessage(level=logging.DEBUG, message=message.format("not found")))

    # /usr/local/share/APP_NAME
    prefix = sysconfig.get_config_var("prefix")
    message = "Share directory {0} (prefix)"
    if prefix is not None:
        share_directory = os.path.join(prefix, "local", "share", app_name)
        if os.path.exists(share_directory):
            messages.append(LogMessage(level=logging.DEBUG, message=message.format("found")))
            return messages, errors, share_directory
    messages.append(LogMessage(level=logging.DEBUG, message=message.format("not found")))

    errors.append("Unable to find a viable share directory")
    return messages, errors, None


def human_time(seconds: int) -> str:
    """convert seconds into human readable
    00d00h00m00s format"""
    sign_string = "-" if seconds < 0 else ""
    seconds = abs(int(seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return "%s%dd%dh%dm%ds" % (sign_string, days, hours, minutes, seconds)
    if hours > 0:
        return "%s%dh%dm%ds" % (sign_string, hours, minutes, seconds)
    if minutes > 0:
        return "%s%dm%ds" % (sign_string, minutes, seconds)
    return "%s%ds" % (sign_string, seconds)


def oxfordcomma(listed, condition):
    """Format a list into a sentance"""
    listed = [f"'{str(entry)}'" for entry in listed]
    if len(listed) == 0:
        return ""
    if len(listed) == 1:
        return listed[0]
    if len(listed) == 2:
        return f"{listed[0]} {condition} {listed[1]}"
    return f"{', '.join(listed[:-1])} {condition} {listed[-1]}"


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


def templar(string: str, template_vars: Mapping) -> Any:
    """template some string with jinja2
    always to and from json so we return an object if it is

    :param string: The template string
    :type: string: str
    :param template_vars: The vars used to render the template
    :type template_vars: dict
    """
    # hide the jinja that may be in the template_vars
    template_vars = escape_moustaches(template_vars)

    if HAS_ANSIBLE:
        logger.info("Ansible installed, Ansible's plugins will be available")

        ansible_templar = Templar(loader=None)
        ansible_templar.available_variables = template_vars
        try:
            result = ansible_templar.template(string)
        except AnsibleError as exc:
            result = str(exc)

    else:
        logger.info("Ansible not installed, only jinja plugins will be availble")
        env = Environment(autoescape=True)
        try:
            template = env.from_string(string)
            result = template.render(template_vars)
        except TemplateError as exc:
            result = str(exc)
            logging.debug(str(exc))

        # We may have gotten the __repr__ of a python object
        # so let's try and turn it back
        try:
            logging.debug("original templated string: %s", result)
            escaped = html.unescape(result)
            logging.debug("html escaped temaplted str: %s", escaped)
            result = ast.literal_eval(escaped)
        except SyntaxError as exc:
            logging.debug("Could not ast parse templated string")
            logging.debug("error was: %s", str(exc))
            logging.debug("attempted on %s", result)

    result = unescape_moustaches(result)
    return result


def to_list(thing: Union[str, List]) -> List:
    """convert something to a list if necessary"""
    if not isinstance(thing, list):
        return [thing]
    return thing


def unescape_moustaches(obj):
    """unescape moustaches

    :param obj: something
    :type obj: any
    :return: the obj with replacements made
    :rtype: any
    """
    replacements = (("U+007B", "{"), ("U+007D", "}"))
    return dispatch(obj, replacements)
