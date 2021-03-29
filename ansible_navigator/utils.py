""" some utilities that didn't fit elsewhere
"""
import ast

import logging
import importlib.util
import html
import os
import stat

from distutils.spawn import find_executable
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Union

from jinja2 import Environment, TemplateError

from ._version import __version__ as VERSION

logger = logging.getLogger(__name__)

try:
    from ansible.errors import AnsibleError  # type: ignore
    from ansible.template import Templar  # type: ignore

    HAS_ANSIBLE = True
except ImportError:
    HAS_ANSIBLE = False


# Same usage as ansible.utils.sentinel.Sentinel.
class Sentinel:
    def __new__(cls):
        return cls


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
        obj = [dispatch(l, replacements) for l in obj]  # noqa: E741
    elif isinstance(obj, str):
        for replacement in replacements:
            obj = obj.replace(replacement[0], replacement[1])
    return obj


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


def get_and_check_collection_doc_cache(args, collection_doc_cache_fname: str) -> Tuple[List, Dict]:
    """ensure the collection doc cache
    has the current version of the application
    as a safeguard, always delete and rebuild if not
    """
    messages = []
    os.makedirs(args.cache_dir, exist_ok=True)
    collection_doc_cache_path = f"{args.cache_dir}/{collection_doc_cache_fname}"
    messages.append(f"Collection doc cache: path={collection_doc_cache_path}")
    collection_cache = _get_kvs(args, collection_doc_cache_path)
    if "version" in collection_cache:
        cache_version = collection_cache["version"]
    else:
        cache_version = None
    messages.append(f"Collection doc cache: current version={cache_version}")
    if cache_version is None or cache_version != VERSION:
        messages.append("Collection doc cache: version was empty or incorrect, rebuilding")
        collection_cache.close()
        os.remove(collection_doc_cache_path)
        collection_cache.__init__(collection_doc_cache_path)
        collection_cache["version"] = VERSION
        cache_version = collection_cache["version"]
        messages.append(f"Collection doc cache: current version={cache_version}")
    collection_cache.close()
    return messages, collection_cache


def _get_kvs(args, collection_doc_cache_path):
    spec = importlib.util.spec_from_file_location(
        "kvs", f"{args.share_dir}/utils/key_value_store.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.KeyValueStore(collection_doc_cache_path)
