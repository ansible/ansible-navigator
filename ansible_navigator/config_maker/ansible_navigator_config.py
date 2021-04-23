from .definitions import Config
from .definitions import CliParameters
from .definitions import SubCommand
from .definitions import Entry
from .definitions import EntryValue

from .ansible_navigator_post_process import PostProcess

CONFIG = Config(
    application_name="ansible-navigator",
    subcommands=[
        SubCommand(name="inventory", description="Inventory"),
        SubCommand(name="config", description="Configuration"),
        SubCommand(name="doc", description="Documentation"),
        SubCommand(name="run", description="Run"),
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
    ],
)
