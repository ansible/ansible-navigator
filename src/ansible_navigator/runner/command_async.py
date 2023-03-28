"""Implementation of the asynchronous invocation of ``ansible-runner``.

Herein lies the ability to invoke ``ansible-runner`` in an async fashion.
A queue is provided and ``ansible-runner`` uses ``pexpect`` to parse
standard out and error from the command run and populates the
queue with messages.
"""

from copy import deepcopy
from queue import Queue

from ansible_runner import run_command_async

from .command_base import CommandBase


class CommandAsync(CommandBase):
    """A wrapper for the asynchronous runner."""

    def __init__(self, executable_cmd: str, queue: Queue, write_job_events: bool, **kwargs):
        """Initialize the arguments for the ``run_command_async`` interface of ``ansible-runner``.

        For common arguments refer to the documentation of the ``CommandBase`` class.

        :param executable_cmd: The command to be invoked
        :param queue: The queue to post events from ``ansible-runner``
        :param write_job_events: Allows job_events to be processed by ``ansible-runner``
        :param kwargs: The arguments for the async runner call
        """
        self._queue = queue
        self._write_job_events = write_job_events
        super().__init__(executable_cmd, **kwargs)

    def _event_handler(self, event):
        """Handle the event from ansible-runner.

        :param event: The event from ansible-runner
        :returns: The value of ``self._write_job_events``, a boolean
        """
        self._logger.debug("ansible-runner event handle: %s", event)
        new_event = deepcopy(event)
        self._queue.put(new_event)
        return self._write_job_events

    def run(self):
        """Initiate the execution of the runner command in async mode.

        :returns: The runner thread
        """
        self.generate_run_command_args()
        self._runner_args.update({"event_handler": self._event_handler})
        thread, self.ansible_runner_instance = run_command_async(**self._runner_args)
        self.status = "running"
        return thread
