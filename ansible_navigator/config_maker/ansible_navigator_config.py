from .definitions import Config
from .definitions import CliParameters
from .definitions import SubCommand
from .definitions import Entry
from .definitions import EntryValue

from ansible_navigator.utils import oxfordcomma

from .ansible_navigator_post_process import PostProcess

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
            name="execution_environment",
            choices=[True, False],
            cli_parameters=CliParameters(short="--ee", long="--execution-environment"),
            description="Enable the use of an execution environment",
            post_process=PostProcess().execution_environment,
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
            post_process=PostProcess().inventory,
            subcommands=["inventory", "run"],
            value=EntryValue(default=[]),
        ),
        Entry(
            name="plugin_name",
            cli_parameters=CliParameters(short="--pn", long="--plugin-name"),
            description=f"Specify the plugin name",
            settings_file_path_override="documentation.plugin.name",
            subcommands=['doc'],
            value=EntryValue(default=None)
        ),
        Entry(
            name="plugin_type",
            cli_parameters=CliParameters(short="-pt", long="--plugin-type"),
            description=f"Specify the plugin type, {oxfordcomma(PLUGIN_TYPES, 'or')}",
            settings_file_path_override="documentation.plugin.type",
            subcommands=['doc'],
            value=EntryValue(default=None)
        )
    ],
)
