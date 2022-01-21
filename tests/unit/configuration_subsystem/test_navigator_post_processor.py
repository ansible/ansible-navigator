"""Tests for the navigator config post-processor."""

import pytest

from ansible_navigator.configuration_subsystem.navigator_post_processor import (
    VolumeMount,
)
from ansible_navigator.configuration_subsystem.navigator_post_processor import (
    VolumeMountOption,
)


@pytest.mark.parametrize(
    ("volmount", "expected"),
    (
        (VolumeMount("test_option", "/foo", "/bar"), "/foo:/bar"),
        (VolumeMount("test_option", "/foo", "/bar", [VolumeMountOption.z]), "/foo:/bar:z"),
        (
            VolumeMount("test_option", "/foo", "/bar", [VolumeMountOption.z, VolumeMountOption.Z]),
            "/foo:/bar:z,Z",
        ),
        (VolumeMount("test_option", "/foo", "/bar", []), "/foo:/bar"),
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
