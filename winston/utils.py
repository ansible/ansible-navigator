""" some utilities that didn't fit elsewhere
"""
import ast

import logging
import html
import os
import stat
from math import floor
import re

from distutils.spawn import find_executable
from pathlib import Path
from typing import Any
from typing import List
from typing import Mapping
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


def human_time(seconds: int) -> str:
    """convert seconds into huma readable
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


def to_list(thing: Union[str, List]) -> List:
    """convert something to a list if necessary"""
    if not isinstance(thing, list):
        return [thing]
    return thing


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


def convert_percentages(dicts: List, keys: List, pbar_width: int) -> List:
    """convert a string % to a little progress bar
    not recursive
    80% = 80%|XXXXXXXX  |

    :pararm dicts: a list fo dictionaries
    :type dicts: list of dictionaries
    :param keys: The keys to convert in each dictionary
    :type keys: list of str
    :param pbar_width: The width of the progress bar
    :type pbar_width: int
    """
    for idx, entry in enumerate(dicts):
        for key in [k for k in entry.keys() if k in keys]:
            value = entry[key]
            if re.match(r"^\d{1,3}%$", str(value)):
                numx = floor(pbar_width / 100 * int(value[0:-1]))
                entry["_" + key] = value
                entry[key] = "{value} {numx}".format(
                    value=value.rjust(4), numx=("\u2587" * numx).ljust(pbar_width)
                )
        dicts[idx] = entry
    return dicts


def distribute(available, weights):
    """distrubute some available fairly
    across a list of numbers

    :param available: the total
    :type available: int
    :param weights: numbers
    :type weights: list of int
    """
    distributed_amounts = []
    total_weights = sum(weights)
    for weight in weights:
        weight = float(weight)
        pcent = weight / total_weights
        distributed_amount = round(pcent * available)
        distributed_amounts.append(distributed_amount)
        total_weights -= weight
        available -= distributed_amount
    return distributed_amounts


def escape_moustaches(obj):
    """escape moustaches

    :param obj: something
    :type obj: any
    :return: the obj with replacements made
    :rtype: any
    """
    replacements = (("{", "U+007B"), ("}", "U+007D"))
    return dispatch(obj, replacements)


def unescape_moustaches(obj):
    """unescape moustaches

    :param obj: something
    :type obj: any
    :return: the obj with replacements made
    :rtype: any
    """
    replacements = (("U+007B", "{"), ("U+007D", "}"))
    return dispatch(obj, replacements)


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
        obj = [dispatch(l, replacements) for l in obj]
    elif isinstance(obj, str):
        for replacement in replacements:
            obj = obj.replace(replacement[0], replacement[1])
    return obj


def find_ini_config_file(app_name: str) -> Optional[str]:
    """ Load config file(first found is used): ENV, CWD, HOME, /etc/app_name """

    path = None
    potential_paths = []
    filename = f"{app_name}.cfg"

    # Environment setting
    path_from_env = os.getenv(f"{app_name}_config".upper())
    if path_from_env is not None:
        path_from_env = os.path.abspath(path_from_env)
        if os.path.isdir(path_from_env):
            path_from_env = os.path.join(path_from_env, filename)
        potential_paths.append(path_from_env)

    # Current working directory
    warn_cmd_public = False
    try:
        cwd = os.getcwd()
        perms = os.stat(cwd)
        cwd_cfg = os.path.join(cwd, filename)
        if perms.st_mode & stat.S_IWOTH:
            if os.path.exists(cwd_cfg):
                warn_cmd_public = True
        else:
            potential_paths.append(cwd_cfg)
    except OSError:
        pass

    potential_paths.append(f"{str(Path.home())}{filename}")
    potential_paths.append(f"/etc/{app_name}/{filename}")

    for path in potential_paths:
        if os.path.exists(path) and os.access(path, os.R_OK):
            break
        path = ""

    if path_from_env != path and warn_cmd_public:
        logger.warning(
            "%s is being run in a world writable directory (%s)," " ignoring it as an %s source.",
            app_name.capitalize(),
            cwd,
            app_name,
        )

    return path or None


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


def set_ansible_envar() -> None:
    """Set an envar if not set, runner will need this"""
    ansible_config = find_ini_config_file("ansible")
    # set as env var, since we hand env vars over to runner
    if ansible_config and not os.getenv("ANSIBLE_CONFIG"):
        os.environ.setdefault("ANSIBLE_CONFIG", ansible_config)
        logger.debug("ANSIBLE_CONFIG set to %s", ansible_config)
