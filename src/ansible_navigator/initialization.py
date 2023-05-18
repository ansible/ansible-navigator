"""Initialization helpers that are used early in application initialization.

These helpers are specific to ansible_navigator.
"""
from __future__ import annotations

import logging
import os
import sys

from typing import NoReturn

from ._version_doc_cache import __version_collection_doc_cache__ as VERSION_CDC
from .configuration_subsystem import Configurator
from .configuration_subsystem import Constants as C
from .configuration_subsystem.definitions import ApplicationConfiguration
from .diagnostics import DiagnosticsCollector
from .utils.definitions import ExitMessage
from .utils.definitions import ExitMessages
from .utils.definitions import ExitPrefix
from .utils.definitions import LogMessage
from .utils.functions import console_width
from .utils.functions import environment_variable_is_file_path
from .utils.functions import find_settings_file
from .utils.key_value_store import KeyValueStore


def error_and_exit_early(exit_messages: list[ExitMessage]) -> NoReturn:
    """Exit the application early.

    :param exit_messages: List of all exit messages to be printed
    """
    color = "NO_COLOR" not in os.environ
    printable = ExitMessages(messages=exit_messages).to_strings(color=color, width=console_width())
    print("\n".join(printable), file=sys.stderr)
    sys.exit(1)


def find_config() -> tuple[list[LogMessage], list[ExitMessage], str | None, C]:
    """Find a configuration file, logging each step.

    If the config can't be found/loaded, use default settings.
    If it's found but empty or not well formed, bail out.

    :returns: All log messages and config path
    """
    messages: list[LogMessage] = []
    exit_messages: list[ExitMessage] = []
    config_path = None
    settings_source = C.NONE

    # Check if the configuration file path is set via an environment var
    cfg_env_var = "ANSIBLE_NAVIGATOR_CONFIG"
    new_messages, new_exit_messages, env_config_path = environment_variable_is_file_path(
        env_var=cfg_env_var,
        kind="config",
    )
    messages.extend(new_messages)
    exit_messages.extend(new_exit_messages)
    if exit_messages:
        return messages, exit_messages, config_path, settings_source

    # Find the setting file
    new_messages, new_exit_messages, found_config_path = find_settings_file()

    messages.extend(new_messages)
    exit_messages.extend(new_exit_messages)
    if exit_messages:
        return messages, exit_messages, config_path, settings_source

    # Pick the environment variable set first, followed by found, followed by leave as none
    if env_config_path is not None:
        config_path = env_config_path
        settings_source = C.ENVIRONMENT_VARIABLE
        message = f"Using settings file at {config_path} set by {cfg_env_var}"
        messages.append(LogMessage(level=logging.DEBUG, message=message))
    elif found_config_path is not None:
        config_path = found_config_path
        settings_source = C.SEARCH_PATH
        message = f"Using settings file at {config_path} in search path"
        messages.append(LogMessage(level=logging.DEBUG, message=message))
    else:
        message = "No valid settings file found, using all default values for settings."
        messages.append(LogMessage(level=logging.DEBUG, message=message))
    return messages, exit_messages, config_path, settings_source


def get_and_check_collection_doc_cache(
    collection_doc_cache_path: str,
) -> tuple[list[LogMessage], list[ExitMessage], KeyValueStore | None]:
    """Ensure the collection doc cache has current application version as a safeguard.

    Always delete and rebuild if not.

    :param collection_doc_cache_path: Path for collection documentation cache
    :returns: All messages and collection cache or None
    """
    messages: list[LogMessage] = []
    exit_messages: list[ExitMessage] = []
    message = f"Collection doc cache: 'path' is '{collection_doc_cache_path}'"
    messages.append(LogMessage(level=logging.DEBUG, message=message))

    path_errors = []
    doc_cache_dir = os.path.dirname(collection_doc_cache_path)
    try:
        os.makedirs(doc_cache_dir, exist_ok=True)
    except OSError as exc:
        path_errors.append(f"Problem making directory: {doc_cache_dir}")
        path_errors.append(f"Error was: {exc!s}")

    if not os.access(os.path.dirname(collection_doc_cache_path), os.W_OK):
        path_errors.append("Directory not writable")

    if not os.access(os.path.dirname(collection_doc_cache_path), os.R_OK):
        path_errors.append("Directory not readable")

    if path_errors:
        exit_msgs = ["Problem while building the collection doc cache."]
        exit_msgs.extend(path_errors)
        exit_messages.extend([ExitMessage(message=exit_msg) for exit_msg in exit_msgs])
        exit_msg = "Try again without '--cdcp' or try '--cdcp ~/collection_doc_cache.db"
        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
        return messages, exit_messages, None

    collection_cache: KeyValueStore = KeyValueStore(collection_doc_cache_path)
    cache_version = collection_cache["version"] if "version" in collection_cache else None
    message = f"Collection doc cache: 'current version' is '{cache_version}'"
    messages.append(LogMessage(level=logging.DEBUG, message=message))
    if cache_version is None or cache_version != VERSION_CDC:
        message = "Collection doc cache: version was empty or incorrect, rebuilding"
        messages.append(LogMessage(level=logging.INFO, message=message))
        collection_cache.close()
        os.remove(collection_doc_cache_path)
        collection_cache = KeyValueStore(collection_doc_cache_path)
        collection_cache["version"] = VERSION_CDC
        cache_version = collection_cache["version"]
        message = f"Collection doc cache: 'current version' is '{cache_version}'"
        messages.append(LogMessage(level=logging.INFO, message=message))
    collection_cache.close()
    return messages, exit_messages, collection_cache


def _diagnose(
    args: ApplicationConfiguration,
    exit_messages: list[ExitMessage],
    messages: list[LogMessage],
    should_diagnose: bool,
):
    """Direct to the diagnostic information writer or return.

    :param args: Application configuration
    :param exit_messages: List of exit messages
    :param messages: List of log messages
    :param should_diagnose: Whether to show tech info
    :returns: All messages and exit messages
    """
    if should_diagnose:
        DiagnosticsCollector(args=args, messages=messages, exit_messages=exit_messages).run()
    else:
        return messages, exit_messages


def parse_and_update(
    params: list,
    args: ApplicationConfiguration,
    apply_previous_cli_entries: C | list[str] = C.NONE,
    attach_cdc=False,
) -> tuple[list[LogMessage], list[ExitMessage]]:
    """Build a configuration.

    Return after the CDC is mounted, even if exit messages are generated, the CDC may still
    be needed. e.g. ``:collections --ee NotBool``.

    :param params: A list of parameters e.g. ['-x', 'value']
    :param args: The application args
    :param apply_previous_cli_entries: Should previous params from the CLI be applied
    :param attach_cdc: Should the collection doc cache be attached to the args.internals
    :returns: Log and exit messages
    """
    messages: list[LogMessage] = []
    exit_messages: list[ExitMessage] = []
    should_diagnose = "--diagnostics" in params

    (
        new_messages,
        new_exit_messages,
        args.internals.settings_file_path,
        args.internals.settings_source,
    ) = find_config()
    messages.extend(new_messages)
    exit_messages.extend(new_exit_messages)
    if exit_messages:
        return _diagnose(
            args=args,
            exit_messages=exit_messages,
            messages=messages,
            should_diagnose=should_diagnose,
        )

    configurator = Configurator(
        params=params,
        application_configuration=args,
        apply_previous_cli_entries=apply_previous_cli_entries,
        skip_roll_back=should_diagnose,
    )

    new_messages, new_exit_messages = configurator.configure()
    messages.extend(new_messages)
    exit_messages.extend(new_exit_messages)

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

    if mount_collection_cache and isinstance(args.collection_doc_cache_path, str):
        new_messages, new_exit_messages, cache = get_and_check_collection_doc_cache(
            args.collection_doc_cache_path,
        )
        messages.extend(new_messages)
        exit_messages.extend(new_exit_messages)
        if cache is None:
            # There's nothing to be done here, it cannot be attached.
            return _diagnose(
                args=args,
                exit_messages=exit_messages,
                messages=messages,
                should_diagnose=should_diagnose,
            )
        if attach_cdc:
            args.internals.collection_doc_cache = cache
            message = "Collection doc cache attached to args.internals"
            messages.append(LogMessage(level=logging.DEBUG, message=message))
        else:
            message = "Collection doc cache not attached to args.internals"
            messages.append(LogMessage(level=logging.DEBUG, message=message))

    if exit_messages:
        return _diagnose(
            args=args,
            exit_messages=exit_messages,
            messages=messages,
            should_diagnose=should_diagnose,
        )

    for entry in args.entries:
        message = f"Running with {entry.name} as '{entry.value.current}'"
        message += f" ({type(entry.value.current).__name__}/{entry.value.source.value})"
        messages.append(LogMessage(level=logging.DEBUG, message=message))

    return _diagnose(
        args=args,
        exit_messages=exit_messages,
        messages=messages,
        should_diagnose=should_diagnose,
    )
