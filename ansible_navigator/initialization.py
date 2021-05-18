""" initialization helpers that are used early in application
initialization and are specific to ansible_navigator
"""
import importlib.util
import logging
import os
import sys

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


def error_and_exit_early(errors) -> NoReturn:
    """get out of here fast"""
    template = "\x1b[31m[ERROR]: {msg}\x1b[0m"
    for error in errors:
        print(template.format(msg=error))
    sys.exit(1)


def find_config() -> Tuple[List[LogMessage], List[str], Union[None, str]]:
    """
    Find a configuration file, logging each step.
    Return (log messages, path).
    If the config can't be found/loaded, use default settings.
    If it's found but empty or not well formed, bail out.
    """
    messages: List[LogMessage] = []
    errors: List[str] = []
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
    collecion_cache: Dict[str, Dict] = {}

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


def parse_and_update(
    params: List,
    args: ApplicationConfiguration,
    apply_previous_cli_entries: Union[C, List[str]] = C.NONE,
    initial: bool = False,
) -> Tuple[List[LogMessage], List[str]]:
    """Build a configuration"""
    messages: List[LogMessage] = []
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
        initial=initial,
    )

    new_messages, new_errors = configurator.configure()
    messages.extend(new_messages)
    errors.extend(new_errors)
    if errors:
        return messages, errors

    if args.internals.collection_doc_cache is C.NOT_SET:
        mount_collection_cache = True
        message = "Collection doc cache not mounted"
        messages.append(LogMessage(level=logging.DEBUG, message=message))
    elif args.initial.collection_doc_cache_path != args.collection_doc_cache_path:
        mount_collection_cache = True
        message = "Collection doc cache path changed"
        messages.append(LogMessage(level=logging.DEBUG, message=message))
    else:
        mount_collection_cache = False

    if mount_collection_cache:
        new_messages, new_errors, cache = get_and_check_collection_doc_cache(
            args.internals.share_directory, args.collection_doc_cache_path
        )
        messages.extend(new_messages)
        errors.extend(new_errors)
        if errors:
            return messages, errors
        args.internals.collection_doc_cache = cache

    for entry in args.entries:
        message = f"Running with {entry.name} as '{entry.value.current}'"
        message += f" ({type(entry.value.current).__name__}/{entry.value.source.value})"
        messages.append(LogMessage(level=logging.DEBUG, message=message))

    return messages, errors
