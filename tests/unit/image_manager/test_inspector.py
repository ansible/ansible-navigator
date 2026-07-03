"""Unit tests for image inspector command generation."""

import json

from ansible_navigator.image_manager.inspector import ImagesInspect
from ansible_navigator.image_manager.inspector import ImagesList
from ansible_navigator.command_runner.command_runner import Command


def test_images_list_command_for_docker_unchanged() -> None:
    """Ensure Docker image listing command shape is unchanged."""
    commands = ImagesList(container_engine="docker").commands
    assert len(commands) == 1
    assert commands[0].command == "docker images"


def test_images_list_command_for_container() -> None:
    """Ensure Apple Container uses image list."""
    commands = ImagesList(container_engine="container").commands
    assert len(commands) == 1
    assert commands[0].command == "container image list"


def test_images_inspect_command_for_docker_unchanged() -> None:
    """Ensure Docker image inspection command shape is unchanged."""
    commands = ImagesInspect(container_engine="docker", ids=["sha256:abc"]).commands
    assert len(commands) == 1
    assert commands[0].command == "docker inspect sha256:abc"


def test_images_inspect_command_for_container() -> None:
    """Ensure Apple Container uses image inspect."""
    commands = ImagesInspect(container_engine="container", ids=["sha256:abc"]).commands
    assert len(commands) == 1
    assert commands[0].command == "container image inspect sha256:abc"


def test_images_list_parse_for_container_json() -> None:
    """Ensure Apple Container image list JSON is normalized for navigator."""
    command = Command(identity="images", command="container image list", post_process=ImagesList.parse)
    command.stdout = json.dumps(
        [
            {
                "configuration": {"name": "ghcr.io/example/demo:latest"},
                "id": "sha256:abc",
            },
        ],
    )

    ImagesList.parse(command)

    assert command.details == [
        {
            "repository": "ghcr.io/example/demo",
            "tag": "latest",
            "image_id": "sha256:abc",
        },
    ]
