""" ansible_runner sync and async with
event handler
"""
import sys
import logging
import os
import time
from ansible_runner import Runner  # type: ignore
from ansible_runner import run_command_async, run_command

from typing import Tuple


class BaseRunner:
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        container_engine=None,
        execution_environment=None,
        ee_image=False,
        navigator_mode=None,
        container_volume_mounts=None,
        container_options=None,
        container_workdir=None,
    ) -> None:
        """BaseRunner class handle common argument for ansible-runner interface class

        Args:
            container_engine ([str], optional): container engine used to isolate execution. Defaults to podman.
            execution_environment ([bool], optional): Boolean argument controls execution environment enable or not. Defaults to False.
            ee_image ([str], optional): Container image to use when running an command. Defaults to None.
            navigator_mode ([str], optional): Valid value is either ``stdout`` or ``interactive``. If value is set to ``stdout`` passed the
                                              ``stdin`` of current running process is passed to ``ansible-runner`` which enables receiving commandline
                                              prompts after the executing the command. If value is set to ``interactive`` the ``ansible-navigator`` will
                                              run using text user interface (TUI).
            container_volume_mounts ([list], optional): List of bind mounts in the form ``host_dir:/container_dir:labels``. Defaults to None.
            container_options ([str], optional): List of container options to pass to execution engine. Defaults to None.
            container_workdir ([str], optional): The working directory within the container. Defaults to None.
        """
        self._ce = container_engine
        self._ee = execution_environment
        self._eei = ee_image
        self._navigator_mode = navigator_mode

        self.cancelled = False
        self.finished = False
        self.status = None
        self._logger = logging.getLogger(__name__)
        self._runner_args = {}
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

    def __init__(self, executable_cmd, cmdline=None, playbook=None, inventory=None, **kwargs):
        """Base class to handle common arguments of ``run_command`` interface for ``ansible-runner``
        Args:
            executable_cmd ([str]): The command to be invoked.
            cmdline ([list], optional): A list of arguments to be passed to the executable command. Defaults to None.
            playbook ([str], optional): The playbook file name to run. Defaults to None.
            inventory ([list], optional): List of path to the inventory files. Defaults to None.
        """
        self._executable_cmd = executable_cmd
        self._cmdline = cmdline if cmdline else []
        self._playbook = playbook
        self._inventory = inventory
        super(CommandBaseRunner, self).__init__(**kwargs)

    def generate_run_command_args(self) -> None:
        """generate arguments required to be passed to ansible-runner"""
        if self._playbook:
            self._cmdline.append(self._playbook)
            self._runner_args.update({"cwd": os.path.dirname(os.path.abspath(self._playbook))})

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

    def __init__(self, executable_cmd, queue, **kwargs):
        """class to handle arguments of ``run_command_async`` interface for ``ansible-runner``.
           For common arguments refer documentation of ``CommandBaseRunner`` class

        Args:
            executable_cmd ([str]): The command to be invoked.
            queue ([Queue]): The queue to post events from ``anisble-runner``
        """
        self._eventq = None
        self._queue = queue
        super(CommandRunnerAsync, self).__init__(executable_cmd, **kwargs)

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
        _runner = run_command(**self._runner_args)
        while not self.finished:
            time.sleep(0.01)
            continue
        out = _runner.stdout.read()
        if hasattr(_runner, "stderr"):
            err = _runner.stderr.read()
        else:
            err = ""
        return out, err
