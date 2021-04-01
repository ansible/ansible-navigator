""" ansible_runner sync and async with
event handler
"""
import sys
import logging
import os

from queue import Queue
from typing import Tuple
from typing import Optional
from typing import List
from typing import Dict

from ansible_runner import Runner  # type: ignore
from ansible_runner import run_command_async, run_command, get_ansible_config


class BaseRunner:
    """BaseRunner class"""

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        container_engine: Optional[str] = None,
        execution_environment: Optional[bool] = False,
        ee_image: Optional[str] = None,
        navigator_mode: Optional[str] = None,
        container_volume_mounts: Optional[List] = None,
        container_options: Optional[List] = None,
        container_workdir: Optional[str] = None,
        cwd: Optional[str] = None,
    ) -> None:
        """BaseRunner class handle common argument for ansible-runner interface class

        Args:
            container_engine ([str], optional): container engine used to isolate execution.
                                                Defaults to podman. # noqa: E501
            execution_environment ([bool], optional): Boolean argument controls execution
                                                      environment enable or not. Defaults to False.
            ee_image ([str], optional): Container image to use when running an command.
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
            cwd ([str], optional): The current local working directory. Defaults to None.
        """
        self._ce = container_engine
        self._ee = execution_environment
        self._eei = ee_image
        self._navigator_mode = navigator_mode
        self._cwd = cwd
        self.cancelled: bool = False
        self.finished: bool = False
        self.status: Optional[str] = None
        self._logger = logging.getLogger(__name__)
        self._runner_args: Dict = {}
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
                "json_mode": True,
                "quiet": True,
                "envvars": {k: v for k, v in os.environ.items() if k.startswith("ANSIBLE_")},
                "cancel_callback": self.runner_cancelled_callback,
                "finished_callback": self.runner_finished_callback,
            }
        )
        if self._cwd:
            self._runner_args.update({"cwd": self._cwd})

        if self._navigator_mode == "stdout":
            self._runner_args.update(
                {"input_fd": sys.stdin, "output_fd": sys.stdout, "error_fd": sys.stderr}
            )

    def runner_finished_callback(self, runner: Runner):
        """called when runner finishes

        Args:
            runner (Runner): a runner instance
        """
        self.status = runner.status
        self.finished = True

    def runner_cancelled_callback(self):
        """check by runner to see if it should cancel"""
        return self.cancelled


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
        self._cmdline = cmdline if cmdline else []
        self._playbook = playbook
        self._inventory = inventory
        super().__init__(**kwargs)

    def generate_run_command_args(self) -> None:
        """generate arguments required to be passed to ansible-runner"""
        if self._playbook:
            self._cmdline.append(self._playbook)
            self._runner_args.update({"cwd": os.path.dirname(os.path.abspath(self._playbook))})

        if self._inventory:
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
            queue ([Queue]): The queue to post events from ``anisble-runner``
        """
        self._eventq = None
        self._queue = queue
        super().__init__(executable_cmd, **kwargs)

    def _event_handler(self, event):
        self._queue.put(event)

    def run(self):
        """run"""
        self.generate_run_command_args()
        self._runner_args.update({"event_handler": self._event_handler})
        thread, _runner = run_command_async(**self._runner_args)
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
