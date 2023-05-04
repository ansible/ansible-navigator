"""Image puller."""
from __future__ import annotations

import logging
import shlex
import subprocess

from dataclasses import dataclass

from ansible_navigator.configuration_subsystem import Constants
from ansible_navigator.utils.definitions import ExitMessage
from ansible_navigator.utils.definitions import ExitPrefix
from ansible_navigator.utils.definitions import LogMessage
from ansible_navigator.utils.functions import shlex_join


@dataclass(frozen=False)
class ImageAssessment:
    """Data structure containing the image assessment.

    An ``ImageAssessment`` gets updated after instantiation
    with the determination of whether or not a pull is required.
    """

    messages: list[LogMessage]
    exit_messages: list[ExitMessage]
    pull_required: bool


class ImagePuller:
    # pylint: disable=too-many-instance-attributes
    """Image puller."""

    def __init__(
        self,
        container_engine: str,
        image: str,
        arguments: Constants | list[str],
        pull_policy: str,
    ):
        """Initialize the container image puller.

        :param container_engine: The name of the container engine
        :param image: The name of the image to pull
        :param arguments: Additional arguments to be appended to the pull policy
        :param pull_policy: The current pull policy from the settings
        """
        if isinstance(arguments, list):
            self._arguments = arguments
        else:
            self._arguments = []

        self._assessment = ImageAssessment
        self._container_engine: str = container_engine
        self._exit_messages: list[ExitMessage] = []
        self._image: str = image
        self._image_present: bool
        self._image_tag: str
        self._logger = logging.getLogger(__name__)
        self._messages: list[LogMessage] = []
        self._pull_policy: str = pull_policy
        self._pull_required: bool = False

    def assess(self):
        """Assess the need to pull."""
        self._extract_tag()
        self._check_for_image()
        self._determine_pull()
        if self._pull_policy == "never" and self._image_present is False:
            exit_msg = (
                "Pull policy is set to 'never' and execution environment"
                " image was not found locally"
            )
            self._log_message(message=exit_msg, level=logging.ERROR)
            exit_msg = (
                "Try again with '--pp missing' or manually pull the execution environment image"
            )
            self._log_message(level=logging.INFO, message=exit_msg, hint=True)

        self._assessment = ImageAssessment(
            messages=self._messages,
            exit_messages=self._exit_messages,
            pull_required=self._pull_required,
        )

    @property
    def assessment(self):
        """Return an image assessment.

        :returns: Image assessment
        """
        return self._assessment

    def _check_for_image(self):
        """Check for the image."""
        try:
            cmd_parts = [self._container_engine, "image", "inspect", self._image]
            self._log_message(level=logging.DEBUG, message=f"Command: {shlex_join(cmd_parts)}")
            subprocess.run(
                cmd_parts,
                check=True,
                capture_output=True,
            )
            self._image_present = True

        except subprocess.CalledProcessError as exc:
            self._image_present = False
            stdout = exc.stdout.decode()
            stderr = exc.stderr.decode()
            self._log_message(level=logging.DEBUG, message=f"stdout: {stdout}")
            self._log_message(level=logging.DEBUG, message=f"stderr: {stderr}")
            if "no such image" not in str(exc.stderr).lower():
                message = "Image inspection failed, image assumed to be corrupted or missing"
                self._log_message(level=logging.WARNING, message=message)
                self._log_message(level=logging.WARNING, message=f"stdout: {stdout}")
                self._log_message(level=logging.WARNING, message=f"stderr: {stderr}")

    def _determine_pull(self):
        """Determine if a pull is required."""
        if self._pull_policy == "missing" and self._image_present is False:  # noqa: SIM114
            pull = True
        elif self._pull_policy == "always":  # noqa: SIM114
            pull = True
        elif self._pull_policy == "tag" and self._image_tag == "latest":  # noqa: SIM114
            pull = True
        elif self._pull_policy == "tag" and self._image_present is False:
            pull = True
        else:
            pull = False
        self._pull_required = pull
        self._assessment.pull_required = pull

    def _extract_tag(self):
        """Extract the tag from the image name."""
        image_pieces = self._image.split(":")
        self._image_tag = "latest"
        if len(image_pieces) > 1:
            tag = image_pieces[-1]
            if "/" not in tag:
                # If there's a slash in the tag, it means we were probably given
                # an image name that has a port number but no tag at the end.
                # e.g.: registry.example.com:443/my/image
                # In this case, we /don't/ want "443/my/image" to be considered
                # a tag. Only if the ending doesn't have a slash in it, is it a
                # valid tag.
                self._image_tag = tag
        message = f"Image tag is: {self._image_tag}"
        self._log_message(level=logging.INFO, message=message)

    def _log_message(self, message: str, level: int, hint=False):
        """Log a message.

        :param message: The message to log
        :param level: The logging level
        :param hint: Whether or not the message is a hint
        """
        if level == logging.ERROR:
            self._exit_messages.append(ExitMessage(message=message))
        elif hint:
            self._exit_messages.append(ExitMessage(message=message, prefix=ExitPrefix.HINT))
        else:
            self._messages.append(LogMessage(level=level, message=message))
        self._logger.log(level=level, msg=message)

    def prologue_stdout(self):
        """Print a little value added information about the execution environment."""
        messages = [("Execution environment image name:", self._image)]
        messages.append(("Execution environment image tag:", self._image_tag))
        arguments = shlex_join(self._arguments) or None
        messages.append(("Execution environment pull arguments:", arguments))
        messages.append(("Execution environment pull policy:", self._pull_policy))
        messages.append(("Execution environment pull needed:", self._pull_required))

        width = max(len(m[0]) + len(str(m[1])) + 2 for m in messages)
        print("\u002d" * width)
        print("Execution environment image and pull policy overview")
        print("\u002d" * width)
        column_width = max(len(m[0]) for m in messages)
        for msg, value in messages:
            print(f"{msg.ljust(column_width)} {value!s}")
            self._log_message(message=f"{msg!s}: {value!s}", level=logging.INFO)
        print("\u002d" * width)
        print("Updating the execution environment")
        print("\u002d" * width)

    def _generate_pull_command(self) -> list[str]:
        """Generate the pull command.

        :returns: The list of command parts
        """
        command_line = [self._container_engine, "pull"]
        # In case the settings file has an entry with a space
        # e.g. ``--authfile file.txt``, split all of the entries
        for argument in self._arguments:
            command_line.extend(shlex.split(argument))
        command_line.append(self._image)
        return command_line

    def pull_stdout(self):
        """Pull the image, print to stdout.

        ``podman`` writes errors to stdout and ``docker`` writes to stderr.

        This allows us to capture, log and color the error from ``docker`` but in the case
        of ``podman`` the error is only printed on the screen.

        In both cases, stdout is not captured so the user can see the progress on the screen
        as the pull is happening.
        """
        try:
            command_line = self._generate_pull_command()
            shlex_joined = shlex_join(command_line)
            print(f"Running the command: {shlex_joined}")
            stderr_pipe = subprocess.PIPE if self._container_engine == "docker" else None
            subprocess.run(command_line, check=True, stderr=stderr_pipe)
            self._log_message(level=logging.INFO, message="Execution environment updated")
            self._pull_required = False
            self._assessment.pull_required = False
        except subprocess.CalledProcessError as exc:
            self._log_message(level=logging.ERROR, message="Execution environment pull failed")
            if exc.stderr is not None:
                self._log_message(level=logging.ERROR, message=exc.stderr.decode().strip())
            exit_msg = (
                "Check the execution environment image name, connectivity to and permissions"
                " for the registry, and try again"
            )
            self._log_message(level=logging.INFO, message=exit_msg, hint=True)
