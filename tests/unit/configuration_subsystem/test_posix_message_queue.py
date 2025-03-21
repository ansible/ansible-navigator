"""Tests related to a missing ``/dev/mqueue/`` directory when using ``podman``."""

import pathlib

from collections.abc import Callable
from typing import Any

import pytest


@pytest.mark.parametrize("is_dir", (True, False), ids=["is_dir", "no_is_dir"])
@pytest.mark.parametrize("ee_support", (True, False), ids=["ee", "no-ee"])
@pytest.mark.parametrize("engine", ("podman", "docker"), ids=["podman", "docker"])
@pytest.mark.parametrize("platform", ("linux", "darwin"), ids=["linux", "darwin"])
def test_posix_message_queue_ee(
    monkeypatch: pytest.MonkeyPatch,
    is_dir: bool,
    ee_support: bool,
    engine: str,
    platform: str,
    generate_config: Callable[..., Any],
) -> None:
    """Confirm error messages related to missing ``/dev/mqueue/`` and ``podman``.

    Test using all possible combinations of container_engine, ee_support, and ``is_dir``.

    Args:
        monkeypatch: Fixture for patching
        is_dir: The return value to set for ``pathlib.Path.is_dir``
        ee_support: The value to set for ``--ee``
        engine: The value to set for ``--ce``
        platform: The system platform to mock
        generate_config: The configuration generator fixture
    """
    message_queue_msg = (
        "Execution environment support while using podman requires a '/dev/mqueue/' directory."
    )
    unpatched_is_dir = pathlib.Path.is_dir

    def mock_is_dir(path: pathlib.Path) -> bool:
        """Override the result for ``Path('/dev/mqueue/')`` to ``is_dir``.

        Args:
            path: The provided path to check

        Returns:
            ``is_dir`` if the path is ``/dev/mqueue/``, else the real
            result
        """
        if path == pathlib.Path("/dev/mqueue/"):
            return is_dir
        return unpatched_is_dir(path)

    monkeypatch.setattr("pathlib.Path.is_dir", mock_is_dir)
    monkeypatch.setattr("sys.platform", platform)

    response = generate_config(params=["--ce", engine, "--ee", str(ee_support)])
    should_error = ee_support and engine == "podman" and not is_dir and platform != "darwin"
    message_queue_msg_exists = any(
        exit_msg.message == message_queue_msg for exit_msg in response.exit_messages
    )
    assert should_error == message_queue_msg_exists
