"""Tests related to a missing ``/dev/mqueue/`` directory when using ``podman``."""

from unittest.mock import patch

import pytest


@pytest.mark.parametrize("exists,", [True, False], ids=["exists-True", "exists-False"])
@pytest.mark.parametrize("is_dir", [True, False], ids=["is_dir-True", "is_dir-False"])
@pytest.mark.parametrize("ee_support", [True, False], ids=["ee_support-True", "ee_support-False"])
@pytest.mark.parametrize("engine", ["podman", "docker"], ids=["engine-podman", "engine-docker"])
def test_posix_message_queue_ee(exists, is_dir, ee_support, engine, generate_config):
    """Confirm error messages related to missing ``/dev/mqueue/`` and ``podman``.

    Test using all possible combinations of container_engine, ee_support, directory exists
    and is a directory.

    :param exists: The return value to set for ``pathlib.Path.exists``
    :param is_dir: The return value to set for ``pathlib.Path.is_dir``
    :param ee_support: The value to set for ``--ee``
    :param engine: The value to set for ``--ce``
    :param generate_config: The configuration generator fixture
    """
    mqueue_msg = (
        "Execution environment support while using podman requires a '/dev/mqueue/' directory."
    )
    with patch("pathlib.Path.exists", return_value=exists):
        with patch("pathlib.Path.is_dir", return_value=is_dir):
            response = generate_config(params=["--ce", engine, "--ee", str(ee_support)])
            if ee_support is False or engine == "docker" or (exists is True and is_dir is True):
                assert mqueue_msg not in [exit_msg.message for exit_msg in response.exit_messages]
            else:
                assert mqueue_msg in [exit_msg.message for exit_msg in response.exit_messages]
