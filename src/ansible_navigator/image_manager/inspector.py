"""Definitions for image inspection."""

from __future__ import annotations

import json
import re

from collections.abc import Iterable
from typing import Any

from ansible_navigator.command_runner import Command
from ansible_navigator.command_runner import CommandRunner
from ansible_navigator.utils.functions import pascal_to_snake


class ImagesInspect:
    """Functionality for inspecting container images."""

    def __init__(self, container_engine: str, ids: list[str]) -> None:
        """Initialize the container image inspector.

        Args:
            container_engine: The name of the container engine to use
            ids: The ids of the container images to inspect
        """
        self._container_engine = container_engine
        self._image_ids = ids

    @property
    def commands(self) -> list[Command]:
        """Generate image inspection commands.

        Returns:
            List of image inspection command objects
        """
        return [
            Command(
                identity=image_id,
                command=f"{self._container_engine} inspect {image_id}",
                post_process=self.parse,
            )
            for image_id in self._image_ids
        ]

    @staticmethod
    def parse(command: Command) -> None:
        """Parse the image inspection command output.

        Args:
            command: Image inspection command object
        """
        obj = json.loads(command.stdout)
        snake = pascal_to_snake(obj[0])
        command.details = snake


class ImagesList:
    """Functionality for listing container images."""

    def __init__(self, container_engine: str) -> None:
        """Initialize the container image lister.

        Args:
            container_engine: The name of the container engine to use
        """
        self._container_engine = container_engine

    @property
    def commands(self) -> list[Command]:
        """Generate image lister commands.

        Returns:
            List of the image lister commands
        """
        return [
            Command(
                identity="images",
                command=f"{self._container_engine} images",
                post_process=self.parse,
            ),
        ]

    @staticmethod
    def parse(command: Command) -> None:
        """Parse the image lister command output.

        Args:
            command: Image lister command object
        """
        if command.stdout:
            images = command.stdout.splitlines()
            re_2omo = re.compile(r"\s{2,}")
            headers = [key.lower().replace(" ", "_") for key in re_2omo.split(images.pop(0))]
            local_images = [
                dict(zip(headers, re_2omo.split(line), strict=False)) for line in images
            ]
            valid_images = [image for image in local_images if image["tag"] != "<none>"]
            command.details = valid_images


def inspect_all(container_engine: str) -> tuple[list[dict[str, Any]], str]:
    """Run inspect against all images in the list.

    Args:
        container_engine: Name of the container engine

    Returns:
        List of all image values and stderr, if applicable

    Raises:
        TypeError: If there is a typing error
    """
    cmd_runner = CommandRunner()
    images_list_class = ImagesList(container_engine=container_engine)
    result = cmd_runner.run_single_process(commands=images_list_class.commands)
    images_list = result[0]
    if images_list.errors:
        return [], images_list.errors
    if images_list.stderr and not images_list.details:
        return [], images_list.stderr
    if not isinstance(images_list.details, Iterable):
        raise TypeError
    images = {image["image_id"]: image for image in images_list.details}
    image_ids = [image["image_id"] for image in images.values()]
    images_inspect_class = ImagesInspect(container_engine=container_engine, ids=image_ids)
    inspects = cmd_runner.run_single_process(commands=images_inspect_class.commands)
    for inspect in inspects:
        images[inspect.identity]["inspect"] = {"details": inspect.details, "errors": inspect.errors}
    return list(images.values()), images_list.stderr
