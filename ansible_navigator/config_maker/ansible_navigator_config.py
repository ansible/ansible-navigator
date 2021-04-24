import os
from .definitions import Config
from .definitions import CliParameters
from .definitions import SubCommand
from .definitions import Entry
from .definitions import EntryValue

from ansible_navigator.utils import oxfordcomma

from .ansible_navigator_post_process import PostProcess

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

CONFIG = Config(
    application_name="ansible-navigator",
    post_processor = PostProcess(),
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
            cli_parameters=CliParameters(short="", long=""),
            description="Placeholder for subcommand name",
            internal=True,
            value=EntryValue(default="welcome"),
        ),
        Entry(
            name="cmdline",
            cli_parameters=CliParameters(short="", long=""),
            description="Placeholder for argparse remainder",
            internal=True,
            value=EntryValue(default=""),
        ),
        Entry(
            name="editor_command",
            cli_parameters=CliParameters(short="--ecmd", long="--editor-command"),
            description="Specify the editor comamnd",
            settings_file_path_override="editor.command",
            value=EntryValue(default=generate_editor_command()),
        ),
        Entry(
            name="editor_console",
            choices=[True, False],
            cli_parameters=CliParameters(short="--econ", long="--editor-console"),
            description="Specify if the editor is console based",
            settings_file_path_override="editor.console",
            value=EntryValue(default=True),
        ),
        Entry(
            name="execution_environment",
            choices=[True, False],
            cli_parameters=CliParameters(short="--ee", long="--execution-environment"),
            description="Enable the use of an execution environment",
            value=EntryValue(default=True),
        ),
        Entry(
            name="execution_environment_image",
            cli_parameters=CliParameters(short="--eei", long="--execution-environment-image"),
            description="The name of the execution environment image",
            value=EntryValue(default="image_here"),
        ),
        Entry(
            name="inventory",
            argparse_params={"action": "append", "nargs": "+"},
            cli_parameters=CliParameters(short="-i", long="--inventory"),
            description="An inventory path",
            subcommands=["inventory", "run"],
            value=EntryValue(default=[]),
        ),
        Entry(
            name="playbook",
            argparse_params=({"nargs": '?'}),
            description=f"Specify the playbook name",
            subcommands=['run'],
            value=EntryValue()
        ),
        Entry(
            name="plugin_name",
            argparse_params=({"nargs": '?'}),
            description=f"Specify the plugin name",
            settings_file_path_override="documentation.plugin.name",
            subcommands=['doc'],
            value=EntryValue()
        ),
        Entry(
            name="plugin_type",
            cli_parameters=CliParameters(short="--pt", long="--plugin-type"),
            description=f"Specify the plugin type, {oxfordcomma(PLUGIN_TYPES, 'or')}",
            settings_file_path_override="documentation.plugin.type",
            subcommands=['doc'],
            value=EntryValue()
        )
    ],
)
