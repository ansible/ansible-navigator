""" the ansible-navigator configuration
"""
import logging
import os

from types import SimpleNamespace
from typing import Dict
from typing import Tuple
from typing import Union

from .definitions import ApplicationConfiguration
from .definitions import CliParameters
from .definitions import Constants as C
from .definitions import Entry
from .definitions import EntryValue
from .definitions import SubCommand

from .navigator_post_processor import NavigatorPostProcessor

from ..utils import get_share_directory
from ..utils import abs_user_path
from ..utils import oxfordcomma
from ..utils import LogMessage

from .._version import __version__ as VERSION

APP_NAME = "ansible_navigator"

initialization_messages = []
initialization_errors = []

PLUGIN_TYPES = (
    "become",
    "cache",
    "callback",
    "cliconf",
    "connection",
    "httpapi",
    "inventory",
    "lookup",
    "module",
    "netconf",
    "shell",
    "strategy",
    "vars",
)


def generate_editor_command() -> str:
    """Generate a default for editor_command if EDITOR is set"""
    editor = os.environ.get("EDITOR")
    if editor is None:
        message = "EDITOR environment variable not set"
        initialization_messages.append(LogMessage(level=logging.DEBUG, message=message))
        command = "vi +{line_number} {filename}"
    else:
        message = "EDITOR environment variable set as '{editor}'"
        initialization_messages.append(LogMessage(level=logging.DEBUG, message=message))
        command = "%s {filename}" % os.environ.get("EDITOR")
    message = f"Default editor_command set to: {command}"
    initialization_messages.append(LogMessage(level=logging.DEBUG, message=message))
    return command


def generate_cache_path():
    """Generate a path for the collection cache"""
    file_name = "collection_doc_cache.db"
    cache_home = os.environ.get("XDG_CACHE_HOME", f"{os.path.expanduser('~')}/.cache")
    cache_path = os.path.join(cache_home, APP_NAME.replace("_", "-"), file_name)
    message = f"Default collection_doc_cache_path set to: {cache_path}"
    initialization_messages.append(LogMessage(level=logging.DEBUG, message=message))
    return cache_path


def generate_share_directory():
    """Generate a share director"""
    messages, errors, share_directory = get_share_directory(APP_NAME)
    initialization_messages.extend(messages)
    initialization_errors.extend(errors)
    return share_directory


class Internals(SimpleNamespace):
    # pylint: disable=too-few-public-methods
    """a place to hold object that need to be carried
    from apllication initiation to the rest of the app
    """

    action_packages: Tuple[str] = ("ansible_navigator.actions",)
    collection_doc_cache: Union[C, Dict] = C.NOT_SET
    initialization_errors = initialization_errors
    initialization_messages = initialization_messages
    share_directory: str = generate_share_directory()


NavigatorConfiguration = ApplicationConfiguration(
    application_name=APP_NAME,
    application_version=VERSION,
    internals=Internals(),
    post_processor=NavigatorPostProcessor(),
    subcommands=[
        SubCommand(name="collections", description="Explore available collections"),
        SubCommand(name="config", description="Explore the current ansible configuration"),
        SubCommand(name="doc", description="Review documentation for a module or plugin"),
        SubCommand(name="inventory", description="Explore an inventory"),
        SubCommand(name="load", description="Explore a playbook artifact"),
        SubCommand(name="run", description="Run a playbook"),
        SubCommand(name="welcome", description="Start at the welcome page"),
    ],
    entries=[
        Entry(
            name="app",
            apply_to_subsequent_cli=C.NONE,
            short_description="Subcommands",
            subcommand_value=True,
            value=EntryValue(default="welcome"),
        ),
        Entry(
            name="cmdline",
            apply_to_subsequent_cli=C.SAME_SUBCOMMAND,
            short_description="Placeholder for argparse remainder",
            value=EntryValue(),
        ),
        Entry(
            name="collection_doc_cache_path",
            short_description="The path to collection doc cache",
            subcommands=C.NONE,
            value=EntryValue(default=generate_cache_path()),
        ),
        Entry(
            name="container_engine",
            choices=["podman", "docker"],
            cli_parameters=CliParameters(short="--ce"),
            settings_file_path_override="execution-environment.container-engine",
            short_description="Specify the container engine",
            value=EntryValue(default="podman"),
        ),
        Entry(
            name="editor_command",
            cli_parameters=CliParameters(short="--ecmd"),
            settings_file_path_override="editor.command",
            short_description="Specify the editor comamnd",
            value=EntryValue(default=generate_editor_command()),
        ),
        Entry(
            name="editor_console",
            choices=[True, False],
            cli_parameters=CliParameters(short="--econ"),
            settings_file_path_override="editor.console",
            short_description="Specify if the editor is console based",
            value=EntryValue(default=True),
        ),
        Entry(
            name="execution_environment",
            choices=[True, False],
            cli_parameters=CliParameters(short="--ee"),
            settings_file_path_override="execution-environment.enabled",
            short_description="Enable the use of an execution environment",
            value=EntryValue(default=True),
        ),
        Entry(
            name="execution_environment_image",
            cli_parameters=CliParameters(short="--eei"),
            description="The name of the execution environment image",
            settings_file_path_override="execution-environment.image",
            short_description="Enable the use of an execution environment",
            value=EntryValue(default="quay.io/ansible/ansible-runner:devel"),
        ),
        Entry(
            name="inventory",
            cli_parameters=CliParameters(action="append", nargs="+", short="-i"),
            environment_variable_override="inventories",
            settings_file_path_override="inventories",
            short_description="Specify inventory file path or comma separated host list",
            subcommands=["inventory", "run"],
            value=EntryValue(),
        ),
        Entry(
            name="inventory_column",
            cli_parameters=CliParameters(action="append", nargs="+", short="--ic"),
            environment_variable_override="inventory_columns",
            settings_file_path_override="inventory-columns",
            short_description="Specify a host attribute to show in the inventory view",
            subcommands=["inventory", "run"],
            value=EntryValue(),
        ),
        Entry(
            name="log_file",
            cli_parameters=CliParameters(short="--lf"),
            short_description="Specify the full path for the ansible-navigator log file",
            settings_file_path_override="logging.file",
            value=EntryValue(default=abs_user_path("./ansible-navigator.log")),
        ),
        Entry(
            name="log_level",
            choices=["debug", "info", "warning", "error", "critical"],
            cli_parameters=CliParameters(short="--ll"),
            short_description="Specify the ansible-navigator log level",
            settings_file_path_override="logging.level",
            value=EntryValue(default="warning"),
        ),
        Entry(
            name="mode",
            change_after_initial=False,
            choices=["stdout", "interactive"],
            cli_parameters=CliParameters(short="-m"),
            short_description="Specify the user-interface mode",
            value=EntryValue(default="interactive"),
        ),
        Entry(
            name="osc4",
            choices=[True, False],
            cli_parameters=CliParameters(short="--osc4"),
            short_description="Enable terminal color changing support with OSC4",
            value=EntryValue(default=True),
        ),
        Entry(
            name="pass_environment_variable",
            cli_parameters=CliParameters(action="append", nargs="+", short="--penv"),
            environment_variable_override="pass_environment_variables",
            settings_file_path_override="execution-environment.environment-variables.pass",
            short_description=(
                "Specify an exiting environment variable to be passed through"
                " to and set within the execution enviroment (--penv MY_VAR)"
            ),
            value=EntryValue(),
        ),
        Entry(
            name="playbook",
            cli_parameters=CliParameters(positional=True),
            short_description="Specify the playbook name",
            subcommands=["run"],
            value=EntryValue(),
        ),
        Entry(
            name="playbook_artifact_enable",
            choices=[True, False],
            cli_parameters=CliParameters(short="--pae"),
            settings_file_path_override="playbook-artifact.enable",
            short_description="Enable the creation of artifacts for completed playbooks",
            subcommands=["run"],
            value=EntryValue(default=True),
        ),
        Entry(
            name="playbook_artifact_load",
            cli_parameters=CliParameters(positional=True),
            settings_file_path_override="playbook-artifact.load",
            short_description="Specify the path for the playbook artifact to load",
            subcommands=["load"],
            value=EntryValue(),
        ),
        Entry(
            name="playbook_artifact_save_as",
            cli_parameters=CliParameters(short="--pas"),
            settings_file_path_override="playbook-artifact.save-as",
            short_description="Specify the name for artifacts created from completed playbooks",
            subcommands=["run"],
            value=EntryValue(default="{playbook_dir}/{playbook_name}-artifact-{ts_utc}.json"),
        ),
        Entry(
            name="plugin_name",
            cli_parameters=CliParameters(positional=True),
            settings_file_path_override="documentation.plugin.name",
            short_description="Specify the plugin name",
            subcommands=["doc"],
            value=EntryValue(),
        ),
        Entry(
            name="plugin_type",
            cli_parameters=CliParameters(short="-t", long_override="--type"),
            settings_file_path_override="documentation.plugin.type",
            short_description=f"Specify the plugin type, {oxfordcomma(PLUGIN_TYPES, 'or')}",
            subcommands=["doc"],
            value=EntryValue(default="module"),
        ),
        Entry(
            name="set_environment_variable",
            cli_parameters=CliParameters(action="append", nargs="+", short="--senv"),
            environment_variable_override="set_environment_variables",
            settings_file_path_override="execution-environment.environment-variables.set",
            short_description="Specify an environment variable and a value to be set within the \
                execution enviroment (--senv MY_VAR=42)",
            value=EntryValue(),
        ),
    ],
)
