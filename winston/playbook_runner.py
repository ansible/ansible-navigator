""" ansible_runner w/ queue and
event handler
"""
import logging
import os
from ansible_runner import Runner  # type: ignore
from ansible_runner import run_async


class PlaybookRunner:
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
        self.cancelled = False
        self.finished = False
        self.status = None

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

        runner_args = {
            "json_mode": True,
            "quiet": True,
            "event_handler": self._event_handler,
            "envvars": {k: v for k, v in os.environ.items() if k.startswith("ANSIBLE_")},
            "cancel_callback": self.runner_cancelled_callback,
            "finished_callback": self.runner_finished_callback,
        }
        if self._ee:
            inventory = ["-i", self._inventory] if self._inventory else []
            add_args = {
                "cli_execenv_cmd": "playbook",
                "cmdline": [self._playbook] + inventory + self._cmdline,
                "container_image": self._eei,
                "private_data_dir": ".",
                "process_isolation_executable": self._ce,
                "process_isolation": True,
            }
        else:
            add_args = {
                "cmdline": " ".join(self._cmdline),
                "inventory": self._inventory,
                "playbook": self._playbook,
            }
        runner_args.update(add_args)
        for key, value in runner_args.items():
            self._logger.debug("Runner arg: %s:%s", key, value)

        thread, _runner = run_async(**runner_args)
        self.status = "running"
        return thread
