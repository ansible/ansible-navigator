"""Tests for the navigator config post-processor."""

import pytest

from ansible_navigator.configuration_subsystem.definitions import Constants
from ansible_navigator.configuration_subsystem.definitions import VolumeMount
from ansible_navigator.configuration_subsystem.definitions import VolumeMountOption


@pytest.mark.parametrize(
    ("volmount", "expected"),
    (
        (
            VolumeMount(
                settings_entry="test_option",
                fs_source="/foo",
                fs_destination="/bar",
                source=Constants.USER_CLI,
            ),
            "/foo:/bar",
        ),
        (
            VolumeMount(
                settings_entry="test_option",
                fs_source="/foo",
                fs_destination="/bar",
                options=[VolumeMountOption.z],
                source=Constants.USER_CLI,
            ),
            "/foo:/bar:z",
        ),
        (
            VolumeMount(
                settings_entry="test_option",
                fs_source="/foo",
                fs_destination="/bar",
                options=[VolumeMountOption.z, VolumeMountOption.Z],
                source=Constants.USER_CLI,
            ),
            "/foo:/bar:z,Z",
        ),
        (
            VolumeMount(
                settings_entry="test_option",
                fs_source="/foo",
                fs_destination="/bar",
                options=[],
                source=Constants.USER_CLI,
            ),
            "/foo:/bar",
        ),
    ),
    ids=(
        "normal mount",
        "mount with relabel option",
        "mount with a list of options",
        "mount with empty list of options",
    ),
)
def test_navigator_volume_mount_to_string(volmount, expected):
    """Make sure volume mount ``to_string`` is sane.

    :param volmount: The volume mount to test
    :param expected: The expected string resulting from the conversion of the mount to a string
    """
    assert volmount.to_string() == expected
