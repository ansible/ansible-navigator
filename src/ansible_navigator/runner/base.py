# cspell:ignore envvars
"""Herewithin lies the base class for all interaction with
ansible-runner. Attributes common to all ansible-runner calls
are defined within the base class
"""


import logging
import os
import shutil
import sys
import tempfile

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from ansible_runner import Runner  # type: ignore[import]


class Base:
    """Base class"""

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-instance-attributes
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
        rotate_artifacts: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> None:
        """Base class handle common argument for ansible-runner interface class

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
                                              ``ansible-runner`` which enables receiving command
                                              line prompts after the executing the command. If value
                                              is set to ``interactive`` the ``ansible-navigator``
                                              will run using text user interface (TUI).
            container_volume_mounts ([list], optional): List of bind mounts in the form
                                                        ``host_dir:/container_dir:labels``.
                                                        Defaults to None.
            container_options ([list], optional): List of container options to pass to execution
                                                  engine. Defaults to None.
            container_workdir ([str], optional): The working directory within the container.
                                                 Defaults to None.
            host_cwd ([str], optional): The current local working directory. Defaults to None.
                                   If value of execution_environment is set to True this
                                   path will be volume mounted within the execution environment
            set_environment_variable([dict], optional): Dict of user requested environment
                                                        variables to set
            pass_environment_variable([list], optional): List of user requested environment
                                                         variables to pass
            rotate_artifacts ([int], optional): Keep at most n artifact directories
            timeout ([int], optional): The timeout value in seconds that will be passed to either
                                       ``pexpect`` of ``subprocess`` invocation
                                       (based on ``runner_mode`` selected) while executing command.
                                       It the timeout is triggered it will force cancel the
                                       execution.
        """
        self._logger = logging.getLogger(__name__)

        self._set_private_data_directory(private_data_dir)
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
        self._rotate_artifacts = rotate_artifacts if isinstance(rotate_artifacts, int) else None
        self._timeout = timeout if isinstance(timeout, int) else None
        self.ansible_runner_instance: Runner
        self.cancelled: bool = False
        self.finished: bool = False
        self.status: Optional[str] = None
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
                },
            )
        self._runner_args.update(
            {
                "private_data_dir": self._private_data_dir,
                "json_mode": True,
                "quiet": True,
                "cancel_callback": self.runner_cancelled_callback,
                "finished_callback": self.runner_finished_callback,
                "artifacts_handler": self.runner_artifacts_handler,
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
                {"input_fd": sys.stdin, "output_fd": sys.stdout, "error_fd": sys.stderr},
            )

    def __del__(self):
        """Drop the artifact directory when the rotation is disabled."""
        if (
            self._rotate_artifacts is not None
            and self._runner_artifact_dir
            and os.path.exists(self._runner_artifact_dir)
        ):

            self._logger.debug(
                "delete ansible-runner artifact directory at path %s",
                self._runner_artifact_dir,
            )
            shutil.rmtree(self._runner_artifact_dir, ignore_errors=True)

    @staticmethod
    def _generate_tmp_directory():
        """generate a tmp directory for artifacts"""
        return tempfile.mkdtemp(prefix="ansible-navigator_")

    def _set_private_data_directory(self, provided: Union[str, None]) -> None:
        """Set the private data directory to the provided, the username, or a uuid"""

        if isinstance(provided, str):
            if os.access(provided, os.W_OK | os.R_OK | os.X_OK):
                private_data_directory = provided
                source = "user provided"
            else:
                self._logger.debug("Provided private data dir `%s` was not user writable")
                private_data_directory = self._generate_tmp_directory()
                source = "user provided, but changed to tmp location due to permissions"
        else:
            private_data_directory = self._generate_tmp_directory()
            source = "not user provided, used tmp location"

        self._private_data_dir = private_data_directory
        self._logger.debug("private data dir %s: %s", source, self._private_data_dir)

    def runner_artifacts_handler(self, artifact_dir):
        """
        ansible-runner callback to handle artifacts after each runner invocation

        Args:
            artifact_dir ([str]): The directory path of artifact directory for current \
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
