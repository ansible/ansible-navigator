""" ansible_runner API's interface
"""
import shutil
import sys
import logging
import os

from queue import Queue
from tempfile import gettempdir
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from ansible_runner import Runner  # type: ignore
from ansible_runner import get_ansible_config
from ansible_runner import get_inventory
from ansible_runner import get_plugin_docs
from ansible_runner import run_command
from ansible_runner import run_command_async


class BaseRunner:
    """BaseRunner class"""

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        private_data_dir: Optional[str] = None,
        container_engine: Optional[str] = None,
        execution_environment: Optional[bool] = False,
        execution_environment_image: Optional[str] = None,
        navigator_mode: Optional[str] = None,
        container_volume_mounts: Optional[List] = None,
        container_options: Optional[List] = None,
        container_workdir: Optional[str] = None,
        set_environment_variable: Optional[Dict] = None,
        pass_environment_variable: Optional[List] = None,
        host_cwd: Optional[str] = None,
    ) -> None:
        """BaseRunner class handle common argument for ansible-runner interface class

        Args:
            private_data_dir ([str], optional): The directory containing all runner metadata
                                                needed to invoke the runner module. Output
                                                artifacts will also be stored here for later
                                                consumption.
            container_engine ([str], optional): container engine used to isolate execution.
                                                Defaults to podman. # noqa: E501
            execution_environment ([bool], optional): Boolean argument controls execution
                                                      environment enable or not. Defaults to False.
            execution_environment_image ([str], optional): Container image to use when
                                                           running an command.
                                                           Defaults to None.
            navigator_mode ([str], optional): Valid value is either ``stdout`` or ``interactive``.
                                              If value is set to ``stdout`` passed the
                                              ``stdin`` of current running process is passed to
                                              ``ansible-runner`` which enables receiving commandline
                                              prompts after the executing the command. If value is
                                              set to ``interactive`` the ``ansible-navigator`` will
                                              run using text user interface (TUI).
            container_volume_mounts ([list], optional): List of bind mounts in the form
                                                        ``host_dir:/container_dir:labels``.
                                                        Defaults to None.
            container_options ([str], optional): List of container options to pass to execution
                                                 engine. Defaults to None.
            container_workdir ([str], optional): The working directory within the container.
                                                 Defaults to None.
            host_cwd ([str], optional): The current local working directory. Defaults to None.
                                   If value of execution_environment is set to True this
                                   path will be volume mounted within the execution enviornment
            set_environment_variable([dict], optional): Dict of user requested envvars to set
            pass_environment_variable([list], optional): List of user requested envvars to pass
        """
        if private_data_dir:
            self._private_data_dir = private_data_dir
        else:
            self._private_data_dir = os.path.join(gettempdir(), "ansible-navigator")

        self._ce = container_engine
        self._ee = execution_environment
        self._eei = execution_environment_image
        self._navigator_mode = navigator_mode
        self._set_environment_variable: Dict[str, Any] = (
            set_environment_variable if isinstance(set_environment_variable, dict) else {}
        )
        self._pass_environment_variable: List[str] = (
            pass_environment_variable if isinstance(pass_environment_variable, list) else []
        )
        self._host_cwd = host_cwd
        self.ansible_runner_instance: Runner
        self.cancelled: bool = False
        self.finished: bool = False
        self.status: Optional[str] = None
        self._logger = logging.getLogger(__name__)
        self._runner_args: Dict = {}
        self._runner_artifact_dir: Optional[str] = None
        if self._ee:
            self._runner_args.update(
                {
                    "container_image": self._eei,
                    "process_isolation_executable": self._ce,
                    "process_isolation": True,
                    "container_volume_mounts": container_volume_mounts,
                    "container_options": container_options,
                    "container_workdir": container_workdir,
                }
            )
        self._runner_args.update(
            {
                "private_data_dir": self._private_data_dir,
                "json_mode": True,
                "quiet": True,
                "cancel_callback": self.runner_cancelled_callback,
                "finished_callback": self.runner_finished_callback,
                "artifacts_handler": self.runner_artifacts_handler,
            }
        )
        self._add_env_vars_to_args()

        if self._host_cwd:
            self._runner_args.update({"host_cwd": self._host_cwd})

        if self._navigator_mode == "stdout":
            self._runner_args.update(
                {"input_fd": sys.stdin, "output_fd": sys.stdout, "error_fd": sys.stderr}
            )

    def __del__(self):
        """
        class destructor, handle runner artifact file deletion
        """
        if self._runner_artifact_dir and os.path.exists(self._runner_artifact_dir):
            self._logger.debug(
                "delete ansible-runner artifact directory at path %s", self._runner_artifact_dir
            )
            shutil.rmtree(self._runner_artifact_dir, ignore_errors=True)

    def runner_artifacts_handler(self, artifact_dir):
        """
        ansible-runner callback to handle artifacts after each runner innvocation
        Args:
            artifact_dir ([str]): The directory path of artifact directory for current
                                  runner invocation.
        """
        self._logger.debug("ansible-runner artifact_dir set to: '%s'", artifact_dir)
        self._runner_artifact_dir = artifact_dir

    def runner_cancelled_callback(self):
        """check by runner to see if it should cancel"""
        return self.cancelled

    def runner_finished_callback(self, runner: Runner):
        """called when runner finishes

        Args:
            runner (Runner): a runner instance
        """
        self.status = runner.status
        self.finished = True

    def _add_env_vars_to_args(self):
        self._runner_args["envvars"] = {
            k: v for k, v in os.environ.items() if k.startswith("ANSIBLE_")
        }
        self._runner_args["envvars"].update(self._set_environment_variable)
        for env_var in self._pass_environment_variable:
            value = os.environ.get(env_var)
            if value is None:
                self._logger.warning(
                    "Pass through environment variable `%s`" " not currently set, discarded",
                    env_var,
                )
            else:
                self._runner_args["envvars"][env_var] = value


class CommandBaseRunner(BaseRunner):
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """a runner async wrapper"""

    def __init__(
        self,
        executable_cmd: str,
        cmdline: Optional[List] = None,
        playbook: Optional[str] = None,
        inventory: Optional[List] = None,
        **kwargs
    ):
        """Base class to handle common arguments of ``run_command`` interface for ``ansible-runner``
        Args:
            executable_cmd ([str]): The command to be invoked.
            cmdline ([list], optional): A list of arguments to be passed to the executable command.
                                        Defaults to None.
            playbook ([str], optional): The playbook file name to run. Defaults to None.
            inventory ([list], optional): List of path to the inventory files. Defaults to None.
        """
        self._executable_cmd = executable_cmd
        self._cmdline: List[str] = cmdline if isinstance(cmdline, list) else []
        self._playbook = playbook
        self._inventory: List[str] = inventory if isinstance(inventory, list) else []
        super().__init__(**kwargs)

    def generate_run_command_args(self) -> None:
        """generate arguments required to be passed to ansible-runner"""
        if self._playbook:
            self._cmdline.insert(0, self._playbook)

        for inv in self._inventory:
            self._cmdline.extend(["-i", inv])

        self._runner_args.update(
            {"executable_cmd": self._executable_cmd, "cmdline_args": self._cmdline}
        )

        if self._navigator_mode == "stdout":
            self._runner_args.update(
                {"input_fd": sys.stdin, "output_fd": sys.stdout, "error_fd": sys.stderr}
            )

        for key, value in self._runner_args.items():
            self._logger.debug("Runner arg: %s:%s", key, value)


class CommandRunnerAsync(CommandBaseRunner):
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """a runner async wrapper"""

    def __init__(self, executable_cmd: str, queue: Queue, **kwargs):
        """class to handle arguments of ``run_command_async`` interface for ``ansible-runner``.
           For common arguments refer documentation of ``CommandBaseRunner`` class

        Args:
            executable_cmd ([str]): The command to be invoked.
            queue ([Queue]): The queue to post events from ``ansible-runner``
        """
        self._eventq = None
        self._queue = queue
        super().__init__(executable_cmd, **kwargs)

    def _event_handler(self, event):
        self._logger.debug("ansible-runner event handle: %s", event)
        self._queue.put(event)

    def run(self):
        """run"""
        self.generate_run_command_args()
        self._runner_args.update({"event_handler": self._event_handler})
        thread, self.ansible_runner_instance = run_command_async(**self._runner_args)
        self.status = "running"
        return thread


class CommandRunner(CommandBaseRunner):
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """a runner wrapper"""

    def run(self) -> Tuple[str, str]:
        """run"""

        self.generate_run_command_args()
        out, err = run_command(**self._runner_args)
        return out, err


class AnsibleCfgRunner(BaseRunner):
    # pylint: disable=too-many-arguments
    """abstraction for ansible-config command-line"""

    def fetch_ansible_config(
        self, action: str, config_file: Optional[str] = None, only_changed: Optional[bool] = None
    ) -> Tuple[str, str]:
        """Run ansible-config command and get the configuration related details

        Args:
            action (str): The configuration fetch action to perform. Valid values are
                          one of ``list``, ``dump``, ``view``. The ``list`` action
                          will fetch all the config options along with config description,
                         ``dump`` action will fetch all the active config and ``view``
                         action will return the active configuration file view.
            config_file (Optional, optional): Path to configuration file, defaults to
                                              first file found in precedence.. Defaults to None.
            only_changed (Optional, optional): The boolean value when set to ``True`` returns only
                                               the configurations that have changed from the
                                               default. This parameter is applicable only when
                                               ``action`` is set to ``dump``.. Defaults to None.

        Returns:
            Tuple[str, str]: Returns a tuple of response and error string (if any).
        """
        return get_ansible_config(
            action, config_file=config_file, only_changed=only_changed, **self._runner_args
        )


class InventoryRunner(BaseRunner):
    # pylint: disable=too-many-arguments
    """abstraction for ansible-inventory command-line"""

    def fetch_inventory(
        self,
        action: str,
        inventories: List,
        response_format: Optional[str] = None,
        host: Optional[str] = None,
        playbook_dir: Optional[str] = None,
        vault_ids: Optional[str] = None,
        vault_password_file: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Run ansible-inventory command and get the inventory related details

        Args:
            action (str): Valid values are one of ``graph``, ``host``, ``list``
                          ``graph`` create inventory graph, ``host`` returns specific
                          host info and works as inventory script and ``list`` output
                          all hosts info and also works as inventory script.
            inventories (List): List of inventory host path.
            response_format (Optional[str], optional): The output format for response. Valid values
                                                       can be one of ``json``, ``yaml``, ``toml``.
                                                       If ``action`` is ``graph`` only allowed
                                                       value is ``json``.
            host (Optional[str], optional): When ``action`` is set to ``host`` this parameter is
                                            used to get the host specific information..
            playbook_dir (Optional[str], optional): This parameter is used to sets the relative
                                                    path for the inventory.
            vault_ids (Optional[str], optional): The vault identity to use.
            vault_password_file (Optional[str], optional): The vault identity to use.

        Returns:
            Tuple[str, str]: Returns a tuple of response and error string (if any).
        """
        return get_inventory(
            action,
            inventories=inventories,
            response_format=response_format,
            host=host,
            playbook_dir=playbook_dir,
            vault_ids=vault_ids,
            vault_password_file=vault_password_file,
            **self._runner_args
        )


class DocRunner(BaseRunner):
    # pylint: disable=too-many-arguments
    """abstraction for ansible-doc command-line"""

    def fetch_plugin_doc(
        self,
        plugin_names: List,
        plugin_type: Optional[str] = None,
        response_format: Optional[str] = "json",
        snippet: Optional[bool] = None,
        playbook_dir: Optional[str] = None,
        module_path: Optional[str] = None,
    ) -> Tuple[Union[Dict[Any, Any], str], Union[Dict[Any, Any], str]]:
        """Run ansible-doc command and get the plugin docs related details

        Args:
            plugin_names (List): The name of the plugins to get docs.
            plugin_type (Optional[str], optional): The type of the plugin mentioned in
                                                   plugins_names. Valid values are ``become``,
                                                   ``cache``, ``callback``, ``cliconf``,
                                                   ``connection``, ``httpapi``, ``inventory``,
                                                   ``lookup``, ``netconf``, ``shell``, ``vars``,
                                                   ``module``, ``strategy``. If the value is not
                                                   provided it defaults to ``module``.
            response_format (Optional[str], optional):  The output format for response.
                            Valid values can be one of ``json`` or ``human`` and the response
                            is either json string or plain text in human readable foramt.
                            Defaults to ``json``.
            snippet (Optional[bool], optional): Show playbook snippet for specified plugin(s).
                                                Defaults to None.
            playbook_dir (Optional[str], optional): This parameter is used to sets the relative
                                                    path to handle playbook adjacent installed
                                                    plugins. Defaults to None.
            module_path (Optional[str], optional): This parameter is prepend colon-separated path(s)
                                                   to module library
                                                   (default=~/.ansible/plugins/modules:
                                                   /usr/share/ansible/plugins/modules).

        Returns:
            Tuple[Union[Dict[Any, Any], str], Union[Dict[Any, Any], str]]: Returns a tuple of
                                                    response and error string. If the value of
                                                    ``response_format`` is ``json`` it returns
                                                    a python dictionary object.
        """
        return get_plugin_docs(
            plugin_names,
            plugin_type=plugin_type,
            response_format=response_format,
            snippet=snippet,
            playbook_dir=playbook_dir,
            module_path=module_path,
            **self._runner_args
        )
