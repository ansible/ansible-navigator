""" ansible_runner w/ queue and
event handler
"""
import sys
import logging
import os
from ansible_runner import Runner  # type: ignore
from ansible_runner import run_command_async


class CommandRunner:
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """a runner wrapper"""

    def __init__(self, args, queue):
        self._ce = args.container_engine
        self._cmdline = args.cmdline
        self._ee = args.execution_environment
        self._eei = args.ee_image
        self._eventq = None
        self._inventory = args.inventory
        self._logger = logging.getLogger(__name__)
        self._playbook = args.playbook
        self._queue = queue
        self._app = args.app
        self.cancelled = False
        self.finished = False
        self.status = None
        self._navigator_mode = args.navigator_mode
        self._executable_cmd = {
            "config": "ansible-config",
            "doc": "ansible-doc",
            "galaxy": "ansible-galaxy",
            "inventory": "ansible-inventory",
            "run": "ansible-playbook",
            "test": "ansible-test",
        }.get(args.app, None)

    def runner_finished_callback(self, runner: Runner):
        """called when runner finishes

        :param runner: a runner instance
        :type runner: Runner
        """
        self.status = runner.status
        self.finished = True

    def runner_cancelled_callback(self):
        """check by runner to see if it should cancel"""
        return self.cancelled

    def _event_handler(self, event):
        self._queue.put(event)

    def run(self):
        """run"""
        runner_args = {}

        if self._executable_cmd is None:
            raise ValueError(f"ansible command not found for app '{self._app}'")

        if self._ee:
            runner_args.update(
                {
                    "container_image": self._eei,
                    "process_isolation_executable": self._ce,
                    "process_isolation": True,
                }
            )

        if self._playbook:
            self._cmdline.append(self._playbook)
            runner_args.update({"cwd": os.path.dirname(os.path.abspath(self._playbook))})

        for inv in self._inventory:
            self._cmdline.extend(["-i", inv])

        runner_args.update(
            {
                "executable_cmd": self._executable_cmd,
                "cmdline_args": self._cmdline,
                "json_mode": True,
                "quiet": True,
                "envvars": {k: v for k, v in os.environ.items() if k.startswith("ANSIBLE_")},
                "private_data_dir": ".",
                "event_handler": self._event_handler,
                "cancel_callback": self.runner_cancelled_callback,
                "finished_callback": self.runner_finished_callback,
            }
        )

        if self._navigator_mode == "stdout":
            runner_args.update(
                {"input_fd": sys.stdin, "output_fd": sys.stdout, "error_fd": sys.stderr}
            )

        for key, value in runner_args.items():
            self._logger.debug("Runner arg: %s:%s", key, value)

        thread, _runner = run_command_async(**runner_args)
        self.status = "running"
        return thread
