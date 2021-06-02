""" the ansible-navigator configuration
"""
import logging
import os

from types import SimpleNamespace
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

from .definitions import ApplicationConfiguration
from .definitions import CliParameters
from .definitions import Constants as C
from .definitions import Entry
from .definitions import EntryValue
from .definitions import SubCommand

from .navigator_post_processor import NavigatorPostProcessor

from ..utils import ExitMessage, get_share_directory
from ..utils import abs_user_path
from ..utils import oxfordcomma
from ..utils import LogMessage

from .._version import __version__ as VERSION

APP_NAME = "ansible_navigator"

initialization_messages: List[LogMessage] = []
initialization_exit_messages: List[ExitMessage] = []

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
    messages, exit_messages, share_directory = get_share_directory(APP_NAME)
    initialization_messages.extend(messages)
    initialization_exit_messages.extend(exit_messages)
    return share_directory


class Internals(SimpleNamespace):
    # pylint: disable=too-few-public-methods
    """a place to hold object that need to be carried
    from application initiation to the rest of the app
    """

    action_packages: Tuple[str] = ("ansible_navigator.actions",)
    collection_doc_cache: Union[C, Dict] = C.NOT_SET
    initialization_exit_messages = initialization_exit_messages
    initialization_messages = initialization_messages
    share_directory: str = generate_share_directory()


navigator_subcommds = [
    SubCommand(name="collections", description="Explore available collections"),
    SubCommand(
        name="config",
        description="Explore the current ansible configuration",
        epilog=(
            "Note: With '--mode stdout', 'ansible-navigator config' additionally supports"
            " the same parameters as the 'ansible-config' command."
            " For more information about these, try "
            " 'ansible-navigator config --help-config --mode stdout'"
        ),
    ),
    SubCommand(
        name="doc",
        description="Review documentation for a module or plugin",
        epilog=(
            "Note: With '--mode stdout', 'ansible-navigator doc' additionally supports"
            " the same parameters as the 'ansible-doc' command."
            " For more information about these, try "
            " 'ansible-navigator doc --help-doc --mode stdout'"
        ),
    ),
    SubCommand(
        name="images",
        description="Explore execution environment images",
    ),
    SubCommand(
        name="inventory",
        description="Explore an inventory",
        epilog=(
            "Note: With '--mode stdout', 'ansible-navigator inventory' additionally supports"
            " the same parameters as the 'ansible-inventory' command."
            " For more information about these, try "
            " 'ansible-navigator inventory --help-inventory --mode stdout'"
        ),
    ),
    SubCommand(name="replay", description="Explore a previous run using a playbook artifact"),
    SubCommand(
        name="run",
        description="Run a playbook",
        epilog=(
            "Note: 'ansible-navigator run' additionally supports"
            " the same parameters as the 'ansible-playbook' command."
            " For more information about these, try "
            " 'ansible-navigator run --help-playbook --mode stdout'"
        ),
    ),
    SubCommand(name="welcome", description="Start at the welcome page"),
]

NavigatorConfiguration = ApplicationConfiguration(
    application_name=APP_NAME,
    application_version=VERSION,
    internals=Internals(),
    post_processor=NavigatorPostProcessor(),
    subcommands=navigator_subcommds,
    entries=[
        Entry(
            name="app",
            apply_to_subsequent_cli=C.NONE,
            choices=[subcommand.name for subcommand in navigator_subcommds],
            short_description="Subcommands",
            subcommand_value=True,
            value=EntryValue(default="welcome"),
        ),
        Entry(
            name="cmdline",
            apply_to_subsequent_cli=C.SAME_SUBCOMMAND,
            settings_file_path_override="ansible.cmdline",
            short_description="Extra parameters passed to the corresponding command",
            value=EntryValue(),
        ),
        Entry(
            name="collection_doc_cache_path",
            cli_parameters=CliParameters(short="--cdcp"),
            short_description="The path to collection doc cache",
            value=EntryValue(default=generate_cache_path()),
        ),
        Entry(
            name="config",
            cli_parameters=CliParameters(short="-c", metavar="CONFIG_FILE"),
            environment_variable_override="ansible_config",
            settings_file_path_override="ansible.config",
            short_description="Specify the path to the ansible configuration file",
            subcommands=["config"],
            value=EntryValue(),
        ),
        Entry(
            name="container_engine",
            choices=["auto", "podman", "docker"],
            cli_parameters=CliParameters(short="--ce"),
            settings_file_path_override="execution-environment.container-engine",
            short_description="Specify the container engine (auto=podman then docker)",
            value=EntryValue(default="auto"),
        ),
        Entry(
            name="display_color",
            change_after_initial=False,
            choices=[True, False],
            cli_parameters=CliParameters(short="--dc"),
            environment_variable_override="no_color",
            settings_file_path_override="color.enable",
            short_description="Enable the use of color in the display",
            value=EntryValue(default=True),
        ),
        Entry(
            name="editor_command",
            cli_parameters=CliParameters(short="--ecmd"),
            settings_file_path_override="editor.command",
            short_description="Specify the editor command",
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
            short_description="Enable or disable the use of an execution environment",
            value=EntryValue(default=True),
        ),
        Entry(
            name="execution_environment_image",
            cli_parameters=CliParameters(short="--eei"),
            settings_file_path_override="execution-environment.image",
            short_description="Specify the name of the execution environment image",
            value=EntryValue(default="quay.io/ansible/ansible-runner:devel"),
        ),
        Entry(
            name="execution_environment_volume_mounts",
            cli_parameters=CliParameters(action="append", nargs="+", short="--eev"),
            settings_file_path_override="execution-environment.volume-mounts",
            short_description=(
                "Specify volume to be bind mounted within an execution environment"
                " (--eev /home/user/test:/home/user/test:Z)"
            ),
            value=EntryValue(),
        ),
        Entry(
            name="help_config",
            choices=[True, False],
            cli_parameters=CliParameters(short="--hc", action="store_true"),
            short_description="Help options for ansible-config command in stdout mode",
            subcommands=["config"],
            value=EntryValue(default=False),
        ),
        Entry(
            name="help_doc",
            choices=[True, False],
            cli_parameters=CliParameters(short="--hd", action="store_true"),
            short_description="Help options for ansible-doc command in stdout mode",
            subcommands=["doc"],
            value=EntryValue(default=False),
        ),
        Entry(
            name="help_inventory",
            choices=[True, False],
            cli_parameters=CliParameters(short="--hi", action="store_true"),
            short_description="Help options for ansible-inventory command in stdout mode",
            subcommands=["inventory"],
            value=EntryValue(default=False),
        ),
        Entry(
            name="help_playbook",
            choices=[True, False],
            cli_parameters=CliParameters(short="--hp", action="store_true"),
            short_description="Help options for ansible-playbook command in stdout mode",
            subcommands=["run"],
            value=EntryValue(default=False),
        ),
        Entry(
            name="inventory",
            cli_parameters=CliParameters(action="append", nargs="+", short="-i"),
            environment_variable_override="ansible_navigator_inventories",
            settings_file_path_override="ansible.inventories",
            short_description="Specify an inventory file path or comma separated host list",
            subcommands=["inventory", "run"],
            value=EntryValue(),
        ),
        Entry(
            name="inventory_column",
            cli_parameters=CliParameters(action="append", nargs="+", short="--ic"),
            environment_variable_override="ansible_navigator_inventory_columns",
            settings_file_path_override="inventory-columns",
            short_description="Specify a host attribute to show in the inventory view",
            subcommands=["inventory", "run"],
            value=EntryValue(),
        ),
        Entry(
            name="log_append",
            choices=[True, False],
            cli_parameters=CliParameters(short="--la"),
            short_description=(
                "Specify if log messages should be appended to an existing log file,"
                " otherwise a new log file will be created per session"
            ),
            settings_file_path_override="logging.append",
            value=EntryValue(default=True),
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
            settings_file_path_override="color.osc4",
            short_description="Enable or disable terminal color changing support with OSC 4",
            value=EntryValue(default=True),
        ),
        Entry(
            name="pass_environment_variable",
            cli_parameters=CliParameters(action="append", nargs="+", short="--penv"),
            environment_variable_override="ansible_navigator_pass_environment_variables",
            settings_file_path_override="execution-environment.environment-variables.pass",
            short_description=(
                "Specify an exiting environment variable to be passed through"
                " to and set within the execution environment (--penv MY_VAR)"
            ),
            value=EntryValue(),
        ),
        Entry(
            name="playbook",
            cli_parameters=CliParameters(positional=True),
            short_description="Specify the playbook name",
            settings_file_path_override="ansible.playbook",
            subcommands=["run"],
            value=EntryValue(),
        ),
        Entry(
            name="playbook_artifact_enable",
            choices=[True, False],
            cli_parameters=CliParameters(short="--pae"),
            settings_file_path_override="playbook-artifact.enable",
            short_description="Enable or disable the creation of artifacts for"
            " completed playbooks. Note: not compatible with '--mode stdout' when playbooks"
            " require user input",
            subcommands=["run"],
            value=EntryValue(default=True),
        ),
        Entry(
            name="playbook_artifact_replay",
            cli_parameters=CliParameters(positional=True),
            settings_file_path_override="playbook-artifact.replay",
            short_description="Specify the path for the playbook artifact to replay",
            subcommands=["replay"],
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
            choices=PLUGIN_TYPES,
            cli_parameters=CliParameters(short="-t", long_override="--type"),
            settings_file_path_override="documentation.plugin.type",
            short_description=f"Specify the plugin type, {oxfordcomma(PLUGIN_TYPES, 'or')}",
            subcommands=["doc"],
            value=EntryValue(default="module"),
        ),
        Entry(
            name="pull_policy",
            choices=["always", "missing", "never", "tag"],
            cli_parameters=CliParameters(short="--pp"),
            settings_file_path_override="execution-environment.pull-policy",
            short_description=(
                "Specify the image pull policy."
                " always:Always pull the image,"
                " missing:Pull if not locally available,"
                " never:Never pull the image,"
                " tag:if the image tag is 'latest', always pull the image,"
                " otherwise pull if not locally available"
            ),
            value=EntryValue(default="tag"),
        ),
        Entry(
            name="set_environment_variable",
            cli_parameters=CliParameters(action="append", nargs="+", short="--senv"),
            environment_variable_override="ansible_navigator_set_environment_variables",
            settings_file_path_override="execution-environment.environment-variables.set",
            short_description=(
                "Specify an environment variable and a value to be set within the"
                " execution environment (--senv MY_VAR=42)"
            ),
            value=EntryValue(),
        ),
    ],
)
