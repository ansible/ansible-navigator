"""Tests related to a missing ``/dev/mqueue`` directory when using ``podman``.
"""
from pathlib import Path


def test_posix_message_queue(monkeypatch, generate_config):
    """Check for error messages related to missing ``/dev/mqueue`` and ``podman``.

    :param monkeypatch: The monkeypatch fixture
    :param generate_config: The configuration generator fixture
    """

    def exists(_arg):
        """Return false when checking for a file or directory path.

        :param arg: The file or directory path to look for
        :returns: False, indicating it does not exist
        """
        return False

    monkeypatch.setattr(Path, "exists", exists)
    response = generate_config(params=["--ce", "podman"])
    exit_msg = (
        "Execution environment support while using podman requires a '/dev/mqueue' directory."
    )
    assert exit_msg in [exit_msg.message for exit_msg in response.exit_messages]
