"""Unit tests for image inspector."""

import pytest

from ansible_navigator.command_runner import Command
from ansible_navigator.image_manager.inspector import ImagesInspect
from ansible_navigator.image_manager.inspector import ImagesList


@pytest.mark.parametrize(
    ("container_engine", "expected_inspect_cmd"),
    (
        pytest.param("podman", "podman inspect image_id", id="podman-inspect"),
        pytest.param("docker", "docker inspect image_id", id="docker-inspect"),
        pytest.param("container", "container image inspect image_id", id="container-image-inspect"),
    ),
)
def test_images_inspect_command(
    container_engine: str,
    expected_inspect_cmd: str,
) -> None:
    """Test image inspect command generation.

    Args:
        container_engine: Container engine identifier
        expected_inspect_cmd: Expected command string
    """
    inspector = ImagesInspect(container_engine=container_engine, ids=["image_id"])
    commands = inspector.commands
    assert len(commands) == 1
    assert commands[0].command == expected_inspect_cmd


@pytest.mark.parametrize(
    ("container_engine", "expected_list_cmd"),
    (
        pytest.param(
            "podman",
            f"podman images --format '{ImagesList.FORMAT}'",
            id="podman-images",
        ),
        pytest.param(
            "docker",
            f"docker images --format '{ImagesList.FORMAT}'",
            id="docker-images",
        ),
        pytest.param("container", "container image list", id="container-image-list"),
    ),
)
def test_images_list_command(
    container_engine: str,
    expected_list_cmd: str,
) -> None:
    """Test image list command generation.

    Args:
        container_engine: Container engine identifier
        expected_list_cmd: Expected command string
    """
    lister = ImagesList(container_engine=container_engine)
    commands = lister.commands
    assert len(commands) == 1
    assert commands[0].command == expected_list_cmd


@pytest.mark.parametrize(
    "container_engine",
    (
        pytest.param("docker", id="docker"),
        pytest.param("podman", id="podman"),
    ),
)
def test_images_list_parse(container_engine: str) -> None:
    """Test that Docker/Podman list output from the requested format is parsed.

    Images without a tag are dropped.

    Args:
        container_engine: Container engine identifier
    """
    stdout = (
        "my-image\tlatest\tabc123def456\t2 days ago\t250 MB\n"
        "<none>\t<none>\t0123456789ab\t3 weeks ago\t1.2GB\n"
    )
    cmd = ImagesList(container_engine=container_engine).commands[0]
    cmd.stdout = stdout
    ImagesList.parse(cmd)
    assert cmd.details == [
        {
            "repository": "my-image",
            "tag": "latest",
            "image_id": "abc123def456",
            "created": "2 days ago",
            "size": "250 MB",
        },
    ]


def test_images_list_parse_skips_blank_lines() -> None:
    """Test that blank lines in the list output do not become rows."""
    stdout = "my-image\tlatest\tabc123def456\t2 days ago\t250 MB\n\n"
    cmd = ImagesList(container_engine="docker").commands[0]
    cmd.stdout = stdout
    ImagesList.parse(cmd)
    assert cmd.details == [
        {
            "repository": "my-image",
            "tag": "latest",
            "image_id": "abc123def456",
            "created": "2 days ago",
            "size": "250 MB",
        },
    ]


def test_images_list_parse_rejects_malformed_line() -> None:
    """Test that a line not matching the requested format fails the parse."""
    cmd = ImagesList(container_engine="docker").commands[0]
    cmd.stdout = "my-image\tlatest\tabc123def456\n"
    with pytest.raises(ValueError, match="zip"):
        ImagesList.parse(cmd)


def test_images_list_parse_apple_container() -> None:
    """Test that Apple Container list output headers are normalized."""
    stdout = "NAME                TAG       DIGEST\nmy-image            latest    sha256:abc123"
    cmd = Command(
        identity="images",
        command="container image list",
        post_process=ImagesList.parse,
    )
    cmd.stdout = stdout
    ImagesList.parse(cmd)
    assert isinstance(cmd.details, list)
    assert len(cmd.details) == 1
    assert cmd.details[0]["repository"] == "my-image"
    assert cmd.details[0]["tag"] == "latest"
    assert cmd.details[0]["image_id"] == "sha256:abc123"
