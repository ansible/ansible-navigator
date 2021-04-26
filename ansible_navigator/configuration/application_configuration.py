""" the ansible-navigator configuration
"""
import os

from .application_post_processor import ApplicationPostProcessor
from .definitions import Config
from .definitions import CliParameters
from .definitions import SubCommand
from .definitions import Entry
from .definitions import EntryValue

from ..utils import oxfordcomma


def abs_user_path(fpath):
    """Resolve a path"""
    return os.path.abspath(os.path.expanduser(fpath))


def generate_editor_command():
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

ApplicationConfiguration = Config(
    application_name="ansible-navigator",
    post_processor=ApplicationPostProcessor(),
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
            description="Placeholder for subcommand name",
            subcommand_value=True,
            value=EntryValue(default="welcome"),
        ),
        Entry(
            name="cmdline",
            description="Placeholder for argparse remainder",
            value=EntryValue(default=[]),
        ),
        Entry(
            name="container_engine",
            choices=["podman", "docker"],
            cli_parameters=CliParameters(short="--ce"),
            description="Specify the container engine",
            value=EntryValue(default="podman"),
        ),
        Entry(
            name="editor_command",
            cli_parameters=CliParameters(short="--ecmd"),
            description="Specify the editor comamnd",
            settings_file_path_override="editor.command",
            value=EntryValue(default=generate_editor_command()),
        ),
        Entry(
            name="editor_console",
            choices=[True, False],
            cli_parameters=CliParameters(short="--econ"),
            description="Specify if the editor is console based",
            settings_file_path_override="editor.console",
            value=EntryValue(default=True),
        ),
        Entry(
            name="execution_environment",
            choices=[True, False],
            cli_parameters=CliParameters(short="--ee"),
            description="Enable the use of an execution environment",
            value=EntryValue(default=True),
        ),
        Entry(
            name="execution_environment_image",
            cli_parameters=CliParameters(short="--eei"),
            description="The name of the execution environment image",
            value=EntryValue(default="image_here"),
        ),
        Entry(
            name="inventory",
            cli_parameters=CliParameters(action="append", nargs="+", short="-i"),
            description="Specify an inventory path",
            settings_file_path_override="inventories",
            subcommands=["inventory", "run"],
            value=EntryValue(),
        ),
        Entry(
            name="inventory_column",
            cli_parameters=CliParameters(action="append", nargs="+", short="--ic"),
            description="Specify a host attribute to show in the inventory view",
            settings_file_path_override="inventory-columns",
            subcommands=["inventory", "run"],
            value=EntryValue(),
        ),
        Entry(
            name="log_file",
            cli_parameters=CliParameters(short="--lf"),
            description="Specify the full path for the ansible-navigator log file",
            settings_file_path_override="logging.file",
            value=EntryValue(default=abs_user_path("./ansible-navigator.log")),
        ),
        Entry(
            name="log_level",
            choices=["debug", "info", "warning", "error", "critical"],
            cli_parameters=CliParameters(short="--ll"),
            description="Specify the ansible-navigator log level",
            settings_file_path_override="logging.level",
            value=EntryValue(default="warning"),
        ),
        Entry(
            name="mode",
            choices=["stdout", "interactive"],
            cli_parameters=CliParameters(short="-m"),
            description="Specify the user-interface mode",
            value=EntryValue(default="interactive"),
        ),
        Entry(
            name="osc4",
            choices=[True, False],
            cli_parameters=CliParameters(short="--osc4"),
            description="Enable terminal color changing support with OSC4",
            value=EntryValue(default=True),
        ),
        Entry(
            name="pass_environment_variable",
            cli_parameters=CliParameters(action="append", nargs="+", short="--penv"),
            description="Specify an exiting environment variable to be passed through to and set \
                within the execution enviroment (--penv MY_VAR)",
            settings_file_path_override="pass-environment-variables",
            value=EntryValue(),
        ),
        Entry(
            name="playbook",
            cli_parameters=CliParameters(positional=True),
            description="Specify the playbook name",
            subcommands=["run"],
            value=EntryValue(),
        ),
        Entry(
            name="playbook_artifact",
            cli_parameters=CliParameters(positional=True),
            description="Specify the path to a playbook artifact",
            subcommands=["load"],
            value=EntryValue(),
        ),
        Entry(
            name="plugin_name",
            cli_parameters=CliParameters(positional=True),
            description="Specify the plugin name",
            settings_file_path_override="documentation.plugin.name",
            subcommands=["doc"],
            value=EntryValue(),
        ),
        Entry(
            name="plugin_type",
            cli_parameters=CliParameters(short="--pt"),
            description=f"Specify the plugin type, {oxfordcomma(PLUGIN_TYPES, 'or')}",
            settings_file_path_override="documentation.plugin.type",
            subcommands=["doc"],
            value=EntryValue(default="module"),
        ),
        Entry(
            name="set_environment_variable",
            cli_parameters=CliParameters(action="append", nargs="+", short="--senv"),
            description="Specify an environment variable and a value to be set within the \
                execution enviroment (--senv MY_VAR=42)",
            settings_file_path_override="set-environment-variables",
            value=EntryValue(),
        ),
    ],
)
