""" initialization helpers that are used early in application
initialization and are specific to ansible_navigator
"""
import importlib.util
import logging
import os
import sys
import sysconfig

from distutils.spawn import find_executable

from typing import Dict
from typing import List
from typing import NoReturn
from typing import Union
from typing import Tuple

from .configuration_subsystem import ApplicationConfiguration
from .configuration_subsystem import Configurator
from .configuration_subsystem import Constants as C

from .utils import environment_variable_is_file_path
from .utils import find_configuration_directory_or_file_path
from .utils import LogMessage
from ._version import __version__ as VERSION


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


def error_and_exit_early(errors) -> NoReturn:
    """get out of here fast"""
    template = "\x1b[31m[ERROR]: {msg}\x1b[0m"
    for error in errors:
        print(template.format(msg=error))
    sys.exit(1)


def find_config() -> Tuple[List[str], List[str], Union[None, str]]:
    """
    Find a configuration file, logging each step.
    Return (log messages, path).
    If the config can't be found/loaded, use default settings.
    If it's found but empty or not well formed, bail out.
    """
    messages = []
    errors = []
    config_path = None

    # Check if the conf path is set via an env var
    cfg_env_var = "ANSIBLE_NAVIGATOR_CONFIG"
    new_messages, new_errors, env_config_path = environment_variable_is_file_path(
        env_var=cfg_env_var, kind="config"
    )
    messages.extend(new_messages)
    errors.extend(new_errors)
    if errors:
        return messages, errors, config_path

    # Check well know locations
    new_messages, new_errors, found_config_path = find_configuration_directory_or_file_path(
        "ansible-navigator", allowed_extensions=["yml", "yaml", "json"]
    )
    messages.extend(new_messages)
    errors.extend(new_errors)
    if errors:
        return messages, errors, config_path

    # Pick the envar set first, followed by found, followed by leave as none
    if env_config_path is not None:
        config_path = env_config_path
        message = f"Using config file at {config_path} set by {cfg_env_var}"
        messages.append(LogMessage(level=logging.DEBUG, message=message))
    elif found_config_path is not None:
        config_path = found_config_path
        message = f"Using config file at {config_path} in search path"
        messages.append(LogMessage(level=logging.DEBUG, message=message))
    else:
        message = "No valid config file found, using all default values for configuration."
        messages.append(LogMessage(level=logging.DEBUG, message=message))
    return messages, errors, config_path


def get_and_check_collection_doc_cache(
    share_directory: str, collection_doc_cache_path: str
) -> Tuple[List[LogMessage], List[str], Dict]:
    """ensure the collection doc cache
    has the current version of the application
    as a safeguard, always delete and rebuild if not
    """
    messages: List[LogMessage] = []
    errors: List[str] = []
    collecion_cache = {}

    try:
        os.makedirs(os.path.dirname(collection_doc_cache_path), exist_ok=True)
    except OSError as exc:
        errors.append("Problem creating directory strurcture for collection doc cache.")
        errors.append(f" Error was: {str(exc)}")
        errors.append(f"Attempted to create {os.path.dirname(collection_doc_cache_path)}")
        return messages, errors, collecion_cache

    message = f"Collection doc cache: 'path' is '{collection_doc_cache_path}'"
    messages.append(LogMessage(level=logging.DEBUG, message=message))
    collection_cache = _get_kvs(share_directory, collection_doc_cache_path)
    if "version" in collection_cache:
        cache_version = collection_cache["version"]
    else:
        cache_version = None
    message = f"Collection doc cache: 'current version' is '{cache_version}'"
    messages.append(LogMessage(level=logging.DEBUG, message=message))
    if cache_version is None or cache_version != VERSION:
        message = "Collection doc cache: version was empty or incorrect, rebuilding"
        messages.append(LogMessage(level=logging.INFO, message=message))
        collection_cache.close()
        os.remove(collection_doc_cache_path)
        collection_cache.__init__(collection_doc_cache_path)
        collection_cache["version"] = VERSION
        cache_version = collection_cache["version"]
        message = f"Collection doc cache: 'current version' is '{cache_version}'"
        messages.append(LogMessage(level=logging.INFO, message=message))
    collection_cache.close()
    return messages, errors, collection_cache


def _get_kvs(share_directory, path):
    """Retrieve a key value store given a path"""
    spec_path = os.path.join(share_directory, "utils", "key_value_store.py")
    spec = importlib.util.spec_from_file_location("kvs", spec_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.KeyValueStore(path)


# pylint: disable=inconsistent-return-statements
def get_share_directory(app_name) -> Tuple[List[str], List[str], str]:
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
    share_directory = os.path.join(os.path.dirname(__file__), "..", "share", app_name)
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


def parse_and_update(
    params: List,
    args: ApplicationConfiguration,
    apply_previous_cli_entries: Union[C, List[str]] = C.NONE,
    save_as_initial: bool = False,
) -> Tuple[List[str], List[str]]:
    """Build a configuration"""
    messages: List[str] = []
    errors: List[str] = []

    new_messages, new_errors, config_path = find_config()
    messages.extend(new_messages)
    errors.extend(new_errors)
    if errors:
        return messages, errors

    configurator = Configurator(
        params=params,
        settings_file_path=config_path,
        application_configuration=args,
        apply_previous_cli_entries=apply_previous_cli_entries,
        save_as_intitial=save_as_initial,
    )

    new_messages, new_errors = configurator.configure()
    messages.extend(new_messages)
    errors.extend(new_errors)
    if errors:
        return messages, errors

    if args.internals.collection_doc_cache is C.NOT_SET:
        new_messages, new_errors, cache = get_and_check_collection_doc_cache(
            args.internals.share_directory, args.collection_doc_cache_path
        )
        messages.extend(new_messages)
        errors.extend(new_errors)
        if errors:
            return messages, errors
        args.internals.collection_doc_cache = cache

    set_ansible_envar()

    for entry in args.entries:
        message = f"Running with {entry.name} as '{entry.value.current}'"
        message += f" ({type(entry.value.current).__name__}/{entry.value.source.value})"
        messages.append(LogMessage(level=logging.DEBUG, message=message))

    return messages, errors


def set_ansible_envar() -> Tuple[List[LogMessage], List[str]]:
    """Set an envar if not set, runner will need this"""
    messages, errors, ansible_config_path = find_configuration_directory_or_file_path("ansible.cfg")
    if errors:
        return messages, errors

    # set as env var, since we hand env vars over to runner
    if ansible_config_path and not os.getenv("ANSIBLE_CONFIG"):
        os.environ.setdefault("ANSIBLE_CONFIG", ansible_config_path)
        message = f"ANSIBLE_CONFIG set to '{ansible_config_path}'"
        messages.append(LogMessage(level=logging.DEBUG, message=message))
    return messages, errors
