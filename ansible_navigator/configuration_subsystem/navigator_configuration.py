""" the ansible-navigator configuration
"""
import os

from .definitions import ApplicationConfiguration
from .definitions import CliParameters
from .definitions import Entry
from .definitions import EntryValue
from .definitions import SubCommand
from .definitions import Subset

from .navigator_post_processor import NavigatorPostProcessor

from ..utils import abs_user_path
from ..utils import oxfordcomma


def generate_editor_command() -> str:
    """Generate a default for editor_command if EDITOR is set"""
    if "EDITOR" in os.environ:
        command = "%s {filename}" % os.environ.get("EDITOR")
    else:
        command = "vi +{line_number} {filename}"
    return command


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

NavigatorConfiguration = ApplicationConfiguration(
    application_name="ansible-navigator",
    post_processor=NavigatorPostProcessor(),
    subcommands=[
        SubCommand(name="collections", description="Explore available collections"),
        SubCommand(name="config", description="Explore the current ansible configuration"),
        SubCommand(name="doc", description="Review documentation for a module or plugin"),
        SubCommand(name="inventory", description="Explore an inventory"),
        SubCommand(name="load", description="Explore a playbook artifact"),
        SubCommand(name="run", description="Run a playbook"),
    ],
    entries=[
        Entry(
            name="app",
            apply_to_subsequent_cli=Subset.NONE,
            short_description="Subcommands",
            subcommand_value=True,
            value=EntryValue(default="welcome"),
        ),
        Entry(
            name="cmdline",
            apply_to_subsequent_cli=Subset.SAME_SUBCOMMAND,
            short_description="Placeholder for argparse remainder",
            value=EntryValue(default=[]),
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
            value=EntryValue(default="image_here"),
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
            name="playbook_artifact",
            cli_parameters=CliParameters(positional=True),
            short_description="Specify the path to a playbook artifact",
            subcommands=["load"],
            value=EntryValue(),
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
            cli_parameters=CliParameters(short="--pt"),
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
