"""Tests related to a missing ``/dev/mqueue/`` directory when using ``podman``."""

import pathlib

from typing import Callable

import pytest


@pytest.mark.parametrize("is_dir", [True, False], ids=["is_dir-True", "is_dir-False"])
@pytest.mark.parametrize("ee_support", [True, False], ids=["ee_support-True", "ee_support-False"])
@pytest.mark.parametrize("engine", ["podman", "docker"], ids=["engine-podman", "engine-docker"])
def test_posix_message_queue_ee(
    monkeypatch: pytest.MonkeyPatch,
    is_dir: bool,
    ee_support: bool,
    engine: str,
    generate_config: Callable,
):
    """Confirm error messages related to missing ``/dev/mqueue/`` and ``podman``.

    Test using all possible combinations of container_engine, ee_support, and ``is_dir``.

    :param monkeypatch: Fixture for patching
    :param is_dir: The return value to set for ``pathlib.Path.is_dir``
    :param ee_support: The value to set for ``--ee``
    :param engine: The value to set for ``--ce``
    :param generate_config: The configuration generator fixture
    """
    message_queue_msg = (
        "Execution environment support while using podman requires a '/dev/mqueue/' directory."
    )
    unpatched_is_dir = pathlib.Path.is_dir

    def mock_is_dir(path):
        """Override the result for ``Path('/dev/mqueue/')`` to ``is_dir``.

        :param path: The provided path to check
        :returns: ``is_dir`` if the path is ``/dev/mqueue/``, else the real result
        """
        if path == pathlib.Path("/dev/mqueue/"):
            return is_dir
        return unpatched_is_dir(path)

    monkeypatch.setattr("pathlib.Path.is_dir", mock_is_dir)
    response = generate_config(params=["--ce", engine, "--ee", str(ee_support)])
    should_error = ee_support and engine == "podman" and not is_dir
    message_queue_msg_exists = any(
        exit_msg.message == message_queue_msg for exit_msg in response.exit_messages
    )
    assert should_error == message_queue_msg_exists
