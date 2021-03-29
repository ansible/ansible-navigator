""" ansible_runner sync and async with
event handler
"""
import itertools
import logging
import os
import time
from ansible_runner import Runner  # type: ignore
from ansible_runner import run_async, run

from typing import Tuple


class BaseRunner:
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """a base runner wrapper"""

    def __init__(self, args) -> None:
        self._ce = args.container_engine if hasattr(args, "container_engine") else None
        self._cmdline = args.cmdline if hasattr(args, "cmdline") else None
        self._ee = args.execution_environment if hasattr(args, "execution_environment") else None
        self._eei = args.ee_image if hasattr(args, "ee_image") else None
        self._inventory = args.inventory if hasattr(args, "inventory") else None
        self._logger = logging.getLogger(__name__)
        self._playbook = args.playbook if hasattr(args, "playbook") else None
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


class CommandRunnerAsync(BaseRunner):
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """a runner async wrapper"""

    def __init__(self, args, queue):
        self._eventq = None
        self._queue = queue
        super(CommandRunnerAsync, self).__init__(args)

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
            inventory = [["-i", inv] for inv in self._inventory] if self._inventory else []
            inventory = list(itertools.chain.from_iterable(inventory))
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


class CommandRunner(BaseRunner):
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """a runner wrapper"""

    def run(self) -> Tuple[str, str]:
        """run"""

        runner_args = {
            "json_mode": True,
            "quiet": True,
            "envvars": {k: v for k, v in os.environ.items() if k.startswith("ANSIBLE_")},
            "cancel_callback": self.runner_cancelled_callback,
            "finished_callback": self.runner_finished_callback,
        }
        if self._ee:
            inventory = [["-i", inv] for inv in self._inventory] if self._inventory else []
            inventory = list(itertools.chain.from_iterable(inventory))
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

        _runner = run(**runner_args)
        while not self.finished:
            time.sleep(0.01)
            continue
        out = _runner.stdout.read()
        if hasattr(_runner, "stderr"):
            err = _runner.stderr.read()
        else:
            err = ""
        return out, err
