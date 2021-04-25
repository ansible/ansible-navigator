import os
from .definitions import Config
from .definitions import CliParameters
from .definitions import SubCommand
from .definitions import Entry
from .definitions import EntryValue

from ansible_navigator.utils import oxfordcomma

from .application_post_processor import ApplicationPostProcessor

def generate_editor_command():
    """generate a command for EDITOR is env var is set"""
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
    post_processor = ApplicationPostProcessor(),
    subcommands=[
        SubCommand(name="collections", description="Explore available collections"),
        SubCommand(name="config", description="Explore the current ansible configuration"),
        SubCommand(name="doc", description="Review documentation for a module or plugin"),
        SubCommand(name="inventory", description="Explore an inventory"),
        SubCommand(name="run", description="Run a playbook"),
    ],
    entries=[
        Entry(
            name="app",
            description="Placeholder for subcommand name",
            value=EntryValue(default="welcome"),
        ),
        Entry(
            name="cmdline",
            description="Placeholder for argparse remainder",
            value=EntryValue(default=""),
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
            description="An inventory path",
            subcommands=["inventory", "run"],
            value=EntryValue(default=[]),
        ),
        Entry(
            name="playbook",
            cli_parameters=CliParameters(nargs="?", positional=True),
            description="Specify the playbook name",
            subcommands=['run'],
            value=EntryValue()
        ),
        Entry(
            name="plugin_name",
            cli_parameters=CliParameters(nargs="?", positional=True),
            description="Specify the plugin name",
            settings_file_path_override="documentation.plugin.name",
            subcommands=['doc'],
            value=EntryValue()
        ),
        Entry(
            name="plugin_type",
            cli_parameters=CliParameters(short="--pt"),
            description=f"Specify the plugin type, {oxfordcomma(PLUGIN_TYPES, 'or')}",
            settings_file_path_override="documentation.plugin.type",
            subcommands=['doc'],
            value=EntryValue(default="module")
        )
    ],
)
