# cspell:ignore envvars
"""Herein lies the base class for all interaction with ansible-runner.

Attributes common to all ansible-runner calls are defined within the base class.
"""
from __future__ import annotations

import logging
import os
import shutil
import sys
import tempfile

from typing import Any

from ansible_runner import Runner


class Base:
    """Base class for ansible-runner calls."""

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        private_data_dir: str | None = None,
        container_engine: str | None = None,
        execution_environment: bool | None = False,
        execution_environment_image: str | None = None,
        navigator_mode: str | None = None,
        container_volume_mounts: list | None = None,
        container_options: list | None = None,
        container_workdir: str | None = None,
        set_environment_variable: dict | None = None,
        pass_environment_variable: list | None = None,
        host_cwd: str | None = None,
        rotate_artifacts: int | None = None,
        timeout: int | None = None,
    ) -> None:
        """Handle the common argument for the ansible-runner interface class.

        :param container_engine: Container engine used to isolate execution
        :param container_options: List of container options to pass to execution engine
        :param execution_environment: Boolean argument that enable execution environment support
        :param execution_environment_image: Container image to use when running an command
        :param navigator_mode: Valid value is either ``stdout`` or ``interactive``. If value is
            set to ``stdout`` passed the ``stdin`` of current running process
            is passed to ``ansible-runner`` which enables receiving command
            line prompts after the executing the command. If value is set to
            ``interactive`` the ``ansible-navigator` will run using
            text user interface (TUI).
        :param container_volume_mounts: List of bind mounts in the form
            ``host_dir:/container_dir:labels``
        :param container_workdir: The working directory within the container
        :param host_cwd: The current local working directory. If value of execution_environment is
            set to True this path will be volume mounted within the execution environment.
        :param set_environment_variable: Dict of user requested environment variables to set
        :param private_data_dir: The directory containing all runner metadata needed to invoke
            the runner module. Output artifacts will also be stored here for
            later consumption.
        :param pass_environment_variable: List of user requested environment variables to pass
        :param rotate_artifacts: Keep at most n artifact directories
        :param timeout: The timeout value in seconds that will be passed to either ``pexpect`` of
            ``subprocess`` invocation (based on ``runner_mode`` selected) while
            executing command. It the timeout is triggered it will force cancel
            the execution.
        """
        self._logger = logging.getLogger(__name__)

        self._set_private_data_directory(private_data_dir)
        self._ce = container_engine
        self._ee = execution_environment
        self._eei = execution_environment_image
        self._navigator_mode = navigator_mode
        self._set_environment_variable: dict[str, Any] = (
            set_environment_variable if isinstance(set_environment_variable, dict) else {}
        )
        self._pass_environment_variable: list[str] = (
            pass_environment_variable if isinstance(pass_environment_variable, list) else []
        )
        self._host_cwd = host_cwd
        self._rotate_artifacts = rotate_artifacts if isinstance(rotate_artifacts, int) else None
        self._timeout = timeout if isinstance(timeout, int) else None
        self.ansible_runner_instance: Runner
        self.cancelled: bool = False
        self.finished: bool = False
        self.status: str | None = None
        self._runner_args: dict = {}

        # when the ce is podman, set the container user to root
        if self._ce == "podman":
            if container_options:
                container_options.append("--user=root")
            else:
                container_options = ["--user=root"]

        if self._ee:
            self._runner_args.update(
                {
                    "container_image": self._eei,
                    "process_isolation_executable": self._ce,
                    "process_isolation": True,
                    "container_volume_mounts": container_volume_mounts,
                    "container_options": container_options,
                    "container_workdir": container_workdir,
                },
            )
        self._runner_args.update(
            {
                "private_data_dir": self._private_data_dir,
                "json_mode": True,
                "quiet": True,
                "cancel_callback": self.runner_cancelled_callback,
                "finished_callback": self.runner_finished_callback,
                "timeout": self._timeout,
            },
        )
        if self._rotate_artifacts is not None:
            self._runner_args["rotate_artifacts"] = self._rotate_artifacts

        self._add_env_vars_to_args()

        if self._host_cwd:
            # ensure the CWD ends with a trailing slash
            host_cwd = os.path.join(self._host_cwd, "")
            self._runner_args["host_cwd"] = host_cwd

        if self._navigator_mode == "stdout":
            self._runner_args.update(
                {
                    "input_fd": sys.stdin,
                    "output_fd": sys.stdout,
                    "error_fd": sys.stderr,
                },
            )

    def __del__(self):
        """Drop the private_data_dir if it is temporary."""
        if (
            self._private_data_dir_is_tmp
            and self._private_data_dir
            and os.path.exists(self._private_data_dir)
        ):
            self._logger.debug(
                "delete temporary ansible-runner private_data_dir at path %s",
                self._private_data_dir,
            )
            shutil.rmtree(self._private_data_dir, ignore_errors=True)

    @staticmethod
    def _generate_tmp_directory():
        """Generate a tmp directory for artifacts.

        :returns: Temporary directory path
        """
        return tempfile.mkdtemp(prefix="ansible-navigator_")

    def _set_private_data_directory(self, provided: str | None) -> None:
        """Set the private data directory to the provided, the username, or a uuid.

        :param provided: Data directory path
        """
        if isinstance(provided, str):
            if os.access(provided, os.W_OK | os.R_OK | os.X_OK):
                private_data_directory = provided
                source = "user provided"
            else:
                self._logger.debug("Provided private data dir `%s` was not user writable", provided)
                private_data_directory = self._generate_tmp_directory()
                source = "user provided, but changed to tmp location due to permissions"
        else:
            private_data_directory = self._generate_tmp_directory()
            source = "not user provided, used tmp location"

        self._private_data_dir_is_tmp = source != "user provided"
        self._private_data_dir = private_data_directory
        self._logger.debug("private data dir %s: %s", source, self._private_data_dir)

    def runner_cancelled_callback(self):
        """Check by runner to see if it should cancel.

        :returns: Boolean cancelled value
        """
        return self.cancelled

    def runner_finished_callback(self, runner: Runner):
        """Call when runner finishes.

        :param runner: A runner instance
        """
        self.status = runner.status
        self.finished = True

    def _add_env_vars_to_args(self):
        """Add environment variables to runner args."""
        self._runner_args["envvars"] = {
            k: v for k, v in os.environ.items() if k.startswith("ANSIBLE_")
        }
        self._runner_args["envvars"].update(self._set_environment_variable)
        for env_var in self._pass_environment_variable:
            value = os.environ.get(env_var)
            if value is None:
                self._logger.warning(
                    "Pass through environment variable `%s` not currently set, discarded",
                    env_var,
                )
            else:
                self._runner_args["envvars"][env_var] = value
