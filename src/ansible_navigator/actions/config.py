"""Config subcommand implementation."""
import curses
import os
import re
import shlex
import shutil

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from .._yaml import Loader
from .._yaml import yaml
from ..app import App
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..runner import AnsibleConfig
from ..runner import Command
from ..steps import Step
from ..ui_framework import CursesLinePart
from ..ui_framework import CursesLines
from ..ui_framework import Interaction
from ..ui_framework import nonblocking_notification
from ..ui_framework import warning_notification
from . import _actions as actions
from . import run_action


def color_menu(colno: int, colname: str, entry: Dict[str, Any]) -> Tuple[int, int]:
    # pylint: disable=unused-argument
    """Provide a color for a collections menu entry in one column.

    :param colno: The column number
    :param colname: The column name
    :param entry: The menu entry
    :returns: The color and decoration
    """
    if entry["__default"] is False:
        return 3, 0
    return 2, 0


def content_heading(obj: Any, screen_w: int) -> Union[CursesLines, None]:
    """Create a heading for config content.

    :param obj: The content going to be shown
    :param screen_w: The current screen width
    :return: The heading
    """
    heading = []
    string = obj["option"].replace("_", " ")
    if obj["__default"] is False:
        string += f" (current: {obj['__current_value']})  (default: {obj['default']})"
        color = 3
    else:
        string += f" (current/default: {obj['__current_value']})"
        color = 2

    string = string + (" " * (screen_w - len(string) + 1))

    heading.append(
        tuple(
            [
                CursesLinePart(
                    column=0,
                    string=string,
                    color=color,
                    decoration=curses.A_UNDERLINE,
                ),
            ],
        ),
    )
    return tuple(heading)


def filter_content_keys(obj: Dict[Any, Any]) -> Dict[Any, Any]:
    """Filter out some keys when showing collection content.

    :param obj: The object from which keys should be removed
    :returns: The object with keys removed
    """
    return {k: v for k, v in obj.items() if not k.startswith("__")}


@actions.register
class Action(App):
    """Config subcommand implementation."""

    KEGEX = r"^config(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:config`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="config")

        self._config: Union[List[Any], None] = None
        self._runner: Union[AnsibleConfig, Command]

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        """Execute the ``config`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :return: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction` or
            :data:`None`
        """
        self._logger.debug("config requested in interactive mode")
        self._prepare_to_run(app, interaction)

        notification = nonblocking_notification(
            messages=[
                "Collecting the ansible configuration, this may take a minute...",
            ],
        )
        interaction.ui.show(notification)

        self._update_args(
            [self._name] + shlex.split(self._interaction.action.match.groupdict()["params"] or ""),
        )

        self._run_runner()
        if self._config is None:
            self._prepare_to_exit(interaction)
            return None

        self.steps.append(self._build_main_menu())

        while True:
            self._calling_app.update()
            self._take_step()

            if not self.steps:
                break

            if self.steps.current.name == "quit":
                return self.steps.current

        self._prepare_to_exit(interaction)
        return None

    def run_stdout(self) -> Union[None, int]:
        """Execute the ``config`` request for mode stdout.

        :returns: Nothing or the error code
        """
        self._logger.debug("config requested in stdout mode")
        response = self._run_runner()
        if response:
            _, _, ret_code = response
            return ret_code
        return None

    def _take_step(self) -> None:
        """Take a step based on the current step or step back."""
        result = None
        if isinstance(self.steps.current, Interaction):
            result = run_action(self.steps.current.name, self.app, self.steps.current)
        elif isinstance(self.steps.current, Step):
            if self.steps.current.show_func:
                current_index = self.steps.current.index
                self.steps.current.show_func()
                self.steps.current.index = current_index

            if self.steps.current.type == "menu":
                result = self._interaction.ui.show(
                    obj=self.steps.current.value,
                    columns=self.steps.current.columns,
                    color_menu_item=color_menu,
                )
            elif self.steps.current.type == "content":
                result = self._interaction.ui.show(
                    obj=self.steps.current.value,
                    index=self.steps.current.index,
                    content_heading=content_heading,
                    filter_content_keys=filter_content_keys,
                )

        if result is None:
            self.steps.back_one()
        else:
            self.steps.append(result)

    def _build_main_menu(self):
        """Build the menu of configuration options.

        :returns: The config menu definition
        """
        return Step(
            name="all_options",
            columns=["option", "__default", "source", "via", "__current_value"],
            select_func=self._build_option_content,
            tipe="menu",
            value=self._config,
        )

    def _build_option_content(self):
        """Build the content for one configuration option.

        :returns: The option's content
        """
        return Step(
            name="option_content",
            tipe="content",
            value=self._config,
            index=self.steps.current.index,
        )

    def _run_runner(self) -> Optional[Tuple]:
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        """Use the runner subsystem to retrieve the configuration.

        :raises RuntimeError: When the ansible-config command cannot be found with execution
            environment support disabled.
        :returns: For mode interactive nothing. For mode stdout the
            output, errors and return code from runner.
        """
        if isinstance(self._args.set_environment_variable, dict):
            set_env_vars = {**self._args.set_environment_variable}
        else:
            set_env_vars = {}

        if self._args.display_color is False:
            set_env_vars["ANSIBLE_NOCOLOR"] = "1"

        kwargs = {
            "container_engine": self._args.container_engine,
            "host_cwd": os.getcwd(),
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "navigator_mode": self._args.mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": set_env_vars,
            "private_data_dir": self._args.ansible_runner_artifact_dir,
            "rotate_artifacts": self._args.ansible_runner_rotate_artifacts_count,
            "timeout": self._args.ansible_runner_timeout,
        }

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs.update(
                {"container_volume_mounts": self._args.execution_environment_volume_mounts},
            )

        if isinstance(self._args.container_options, list):
            kwargs.update({"container_options": self._args.container_options})

        if self._args.mode == "interactive":
            self._runner = AnsibleConfig(**kwargs)
            kwargs = {}
            if isinstance(self._args.config, str):
                kwargs["config_file"] = self._args.config
            list_output, list_output_err = self._runner.fetch_ansible_config("list", **kwargs)
            dump_output, dump_output_err = self._runner.fetch_ansible_config("dump", **kwargs)
            if list_output_err:
                msg = f"Error occurred while fetching ansible config (list): '{list_output_err}'"
                self._logger.error(msg)
            if dump_output_err:
                msg = f"Error occurred while fetching ansible config (dump): '{dump_output_err}'"
                self._logger.error(msg)

            err_msg = "\n".join(set((list_output_err, dump_output_err)))
            if "ERROR!" in err_msg or not list_output or not dump_output:
                warn_msg = ["Errors were encountered while gathering the configuration:"]
                if err_msg:
                    warn_msg += err_msg.splitlines()
                if not list_output or not dump_output:
                    warn_msg.append("The configuration could not be gathered.")
                warning = warning_notification(warn_msg)
                self._interaction.ui.show(warning)
            else:
                self._parse_and_merge(list_output, dump_output)
        else:
            if self._args.execution_environment:
                ansible_config_path = "ansible-config"
            else:
                exec_path = shutil.which("ansible-config")
                if exec_path is None:
                    msg = "'ansible-config' executable not found"
                    self._logger.error(msg)
                    raise RuntimeError(msg)
                ansible_config_path = exec_path

            if isinstance(self._args.cmdline, list):
                pass_through_arg = self._args.cmdline.copy()
            else:
                pass_through_arg = []

            if self._args.help_config is True:
                pass_through_arg.append("--help")

            if isinstance(self._args.config, str):
                pass_through_arg.extend(["--config", self._args.config])

            kwargs.update({"cmdline": pass_through_arg})

            self._runner = Command(executable_cmd=ansible_config_path, **kwargs)
            stdout_return = self._runner.run()
            return stdout_return
        return (None, None, None)

    def _parse_and_merge(self, list_output, dump_output) -> None:
        """Parse the list and dump output. Merge dump into list.

        :param list_output: The output from config list
        :param dump_output: The output from config dump
        :returns: Nothing
        """
        try:
            parsed = yaml.load(list_output, Loader=Loader)
            self._logger.debug("yaml loading list output succeeded")
        except yaml.YAMLError as exc:
            self._logger.debug("error yaml loading list output: '%s'", str(exc))
            return None

        regex = re.compile(r"^(?P<variable>\S+)\((?P<source>.*)\)\s=\s(?P<current>.*)$")
        for line in dump_output.splitlines():
            extracted = regex.match(line)
            if extracted:
                variable = extracted.groupdict()["variable"]
                try:
                    source = yaml.load(extracted.groupdict()["source"], Loader=Loader)
                except yaml.YAMLError:
                    source = extracted.groupdict()["source"]
                try:
                    current = yaml.load(extracted.groupdict()["current"], Loader=Loader)
                except yaml.YAMLError:
                    current = extracted.groupdict()["current"]
                try:
                    if isinstance(source, dict):
                        parsed[variable]["source"] = list(source.keys())[0]
                        parsed[variable]["via"] = list(source.values())[0]
                    else:
                        parsed[variable]["source"] = source
                        parsed[variable]["via"] = source
                    parsed[variable]["current"] = current
                    parsed[variable]["__current_value"] = extracted.groupdict()["current"]
                except KeyError:
                    self._logger.error("variable '%s' not found in list output")
                    return None
            else:
                self._logger.error("Unparsable dump entry: %s", line)
                return None

        for key, value in parsed.items():
            value["option"] = key
            if value["source"] == "default":
                value["__default"] = True
            else:
                value["__default"] = False

        self._config = list(parsed.values())
        self._logger.debug("parsed and merged list and dump successfully")
        return None
