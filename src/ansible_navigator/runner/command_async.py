""" Herewith lies the ability to invoke ansible-runner
in an async fashion. A queue is provided and ansible-runner
uses pexpect to parse standout and error from the command run
and populates the queue with messages
"""

from queue import Queue
from ansible_runner import run_command_async

from .command_base import CommandBase


class CommandAsync(CommandBase):
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
        """Initiate the execution of the runner command in async mode"""
        self.generate_run_command_args()
        self._runner_args.update({"event_handler": self._event_handler})
        thread, self.ansible_runner_instance = run_command_async(**self._runner_args)
        self.status = "running"
        return thread
