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


def test_podman_user_root_default() -> None:
    """Test that podman sets --user=root by default."""
    base = Base(
        container_engine="podman",
        execution_environment=True,
    )

    opts = base._runner_args.get("container_options") or []

    assert "--user=root" in opts


@pytest.mark.parametrize(
    "user_option",
    (
        "--user=myuser",
        "--user",
        "-u",
        "-u=myuser",
    ),
)
def test_podman_user_override(user_option: str) -> None:
    """Test that podman respects user-provided --user or -u options.

    Args:
        user_option: The user option to test
    """
    base = Base(
        container_engine="podman",
        execution_environment=True,
        container_options=[user_option],
    )

    opts = base._runner_args.get("container_options") or []

    assert "--user=root" not in opts
    assert user_option in opts


def test_podman_user_override_with_other_options() -> None:
    """Test that podman respects --user when mixed with other options."""
    base = Base(
        container_engine="podman",
        execution_environment=True,
        container_options=["--volume=/tmp:/tmp", "--user=custom", "--env=TEST=1"],
    )

    opts = base._runner_args.get("container_options") or []

    assert "--user=root" not in opts
    assert "--user=custom" in opts
    assert "--volume=/tmp:/tmp" in opts
    assert "--env=TEST=1" in opts


def test_docker_no_user_root() -> None:
    """Test that docker does not set --user=root."""
    base = Base(
        container_engine="docker",
        execution_environment=True,
    )

    opts = base._runner_args.get("container_options") or []

    assert "--user=root" not in opts


def test_podman_other_u_flags_dont_match() -> None:
    """Test that other flags starting with -u don't prevent --user=root."""
    base = Base(
        container_engine="podman",
        execution_environment=True,
        container_options=["--ulimit=nofile:1024", "-unknown"],
    )

    opts = base._runner_args.get("container_options") or []

    # --user=root should be added because neither --ulimit nor -unknown are user flags
    assert "--user=root" in opts
    assert "--ulimit=nofile:1024" in opts
    assert "-unknown" in opts


def test_podman_user_space_separated() -> None:
    """Test that space-separated user flags are detected (as separate list items)."""
    # When passed as --container-options="-u myuser", the parser may split into ["-u", "myuser"]
    base = Base(
        container_engine="podman",
        execution_environment=True,
        container_options=["-u", "myuser"],  # Space-separated, two list items
    )

    opts = base._runner_args.get("container_options") or []

    assert "--user=root" not in opts
    assert "-u" in opts
    assert "myuser" in opts


def test_podman_user_long_space_separated() -> None:
    """Test that space-separated --user flags are detected (as separate list items)."""
    base = Base(
        container_engine="podman",
        execution_environment=True,
        container_options=["--user", "myuser"],  # Space-separated, two list items
    )

    opts = base._runner_args.get("container_options") or []

    assert "--user=root" not in opts
    assert "--user" in opts
    assert "myuser" in opts


def test_podman_user_quoted_with_space() -> None:
    """Test detection when user passes quoted string with space (edge case)."""
    # Edge case: if someone passes --co "-u myuser" as a single quoted argument
    base = Base(
        container_engine="podman",
        execution_environment=True,
        container_options=["-u myuser"],  # Single item with space inside
    )

    opts = base._runner_args.get("container_options") or []

    assert "--user=root" not in opts
    assert "-u myuser" in opts
