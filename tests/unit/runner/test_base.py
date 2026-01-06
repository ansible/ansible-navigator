"""Unit tests for the Base runner class."""

import sys

import pytest

from ansible_navigator.runner.base import Base


macos_docker_ssh_opts = [
    "--volume=/run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock:ro",
    "--env=SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock",
]


@pytest.mark.parametrize(
    ("platform", "container_engine"),
    (
        ("darwin", "docker"),
        ("darwin", "podman"),
        ("linux", "docker"),
        ("linux", "podman"),
    ),
)
def test_ssh_agent_options_mac_docker(
    monkeypatch: pytest.MonkeyPatch, platform: str, container_engine: str
) -> None:
    """Test that SSH agent options are correctly set for different platforms and container engines.

    Args:
        monkeypatch: The monkeypatch fixture
        platform: The platform string
        container_engine: The container engine to use
    """
    monkeypatch.setattr(sys, "platform", platform)

    base = Base(
        container_engine=container_engine,
        execution_environment=True,
    )

    opts = base._runner_args.get("container_options") or []

    for expected_opt in macos_docker_ssh_opts:
        if platform == "darwin" and container_engine == "docker":
            assert expected_opt in opts
        else:
            assert expected_opt not in opts


def test_ssh_agent_options_order(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that custom container options are appended after SSH agent options on macOS with Docker.

    Args:
        monkeypatch: The monkeypatch fixture
    """
    monkeypatch.setattr(sys, "platform", "darwin")

    base = Base(
        container_engine="docker",
        execution_environment=True,
        container_options=["--test"],
    )

    opts = base._runner_args.get("container_options") or []

    assert "--test" in opts
    # Assert that SSH agent fix options are set first to allow overriding them.
    assert opts[2] == "--test"
