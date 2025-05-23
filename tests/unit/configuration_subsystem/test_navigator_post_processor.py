"""Tests for the navigator config post-processor."""

import pytest

from ansible_navigator.configuration_subsystem.definitions import Constants
from ansible_navigator.configuration_subsystem.definitions import VolumeMount


@pytest.mark.parametrize(
    ("volmount", "expected"),
    (
        (
            VolumeMount(
                fs_destination="/bar",
                fs_source="/tmp",
                options_string="",
                settings_entry="test_option",
                source=Constants.USER_CLI,
            ),
            "/tmp:/bar",
        ),
        (
            VolumeMount(
                settings_entry="test_option",
                fs_source="/tmp",
                fs_destination="/bar",
                options_string="z",
                source=Constants.USER_CLI,
            ),
            "/tmp:/bar:z",
        ),
        (
            VolumeMount(
                settings_entry="test_option",
                fs_source="/tmp",
                fs_destination="/bar",
                options_string="z,Z",
                source=Constants.USER_CLI,
            ),
            "/tmp:/bar:z,Z",
        ),
        (
            VolumeMount(
                settings_entry="test_option",
                fs_source="/tmp",
                fs_destination="/bar",
                options_string="",
                source=Constants.USER_CLI,
            ),
            "/tmp:/bar",
        ),
    ),
    ids=(
        "normal",
        "mount-relabel",
        "mount-list",
        "mount-empty-list",
    ),
)
def test_navigator_volume_mount_to_string(volmount: VolumeMount, expected: str) -> None:
    """Make sure volume mount ``to_string`` is sane.

    Args:
        volmount: The volume mount to test
        expected: The expected string resulting from the conversion of
            the mount to a string
    """
    assert volmount.to_string() == expected
