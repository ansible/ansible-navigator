"""unit tests for image puller"""

import shlex
import uuid

from typing import NamedTuple

import pytest

from ansible_navigator.configuration_subsystem import Constants
from ansible_navigator.image_manager import ImagePuller
from ...defaults import DEFAULT_CONTAINER_IMAGE
from ...defaults import SMALL_TEST_IMAGE


class TstPullPolicy(NamedTuple):
    """test object"""

    pull_policy: str
    pull_required: bool


def id_from_data(value):
    """return the name from the test data object"""
    return f" {value.pull_policy} "


# Note, these tests assume our default is not a :latest
data_do_have = [
    TstPullPolicy(pull_policy="always", pull_required=True),
    TstPullPolicy(pull_policy="missing", pull_required=False),
    TstPullPolicy(pull_policy="never", pull_required=False),
    TstPullPolicy(pull_policy="tag", pull_required=False),
]


@pytest.mark.parametrize("data", data_do_have, ids=id_from_data)
def test_do_have(valid_container_engine, data):
    """test using an image local"""
    image_puller = ImagePuller(
        container_engine=valid_container_engine,
        image=DEFAULT_CONTAINER_IMAGE,
        arguments=Constants.NOT_SET,
        pull_policy=data.pull_policy,
    )
    image_puller.assess()
    assert image_puller.assessment.pull_required == data.pull_required


# Note, these tests assume the image is a :latest
data_do_have_but_latest = [
    TstPullPolicy(pull_policy="always", pull_required=True),
    TstPullPolicy(pull_policy="missing", pull_required=False),
    TstPullPolicy(pull_policy="never", pull_required=False),
    TstPullPolicy(pull_policy="tag", pull_required=True),
]


@pytest.mark.parametrize("data", data_do_have_but_latest, ids=id_from_data)
def test_do_have_but_latest(valid_container_engine, data):
    """test using an image local"""
    image_puller = ImagePuller(
        container_engine=valid_container_engine,
        image=SMALL_TEST_IMAGE,
        arguments=Constants.NOT_SET,
        pull_policy=data.pull_policy,
    )
    image_puller.assess()
    assert image_puller.assessment.pull_required == data.pull_required


data_missing_locally = [
    TstPullPolicy(pull_policy="always", pull_required=True),
    TstPullPolicy(pull_policy="missing", pull_required=True),
    TstPullPolicy(pull_policy="never", pull_required=False),
    TstPullPolicy(pull_policy="tag", pull_required=True),
]


@pytest.mark.parametrize("data", data_missing_locally, ids=id_from_data)
def test_missing_locally(valid_container_engine, data):
    """test using an image not local"""
    uuid_str = str(uuid.uuid4())
    image_puller = ImagePuller(
        container_engine=valid_container_engine,
        image=uuid_str,
        arguments=Constants.NOT_SET,
        pull_policy=data.pull_policy,
    )
    image_puller.assess()
    assert image_puller.assessment.pull_required == data.pull_required


# order here is critical
# use missing to trigger the initial pull
data_will_have = [
    TstPullPolicy(pull_policy="missing", pull_required=True),
    TstPullPolicy(pull_policy="always", pull_required=True),
    TstPullPolicy(pull_policy="never", pull_required=False),
    TstPullPolicy(pull_policy="tag", pull_required=True),
]


@pytest.mark.parametrize("data", data_will_have, ids=id_from_data)
def test_will_have(valid_container_engine, pullable_image, data):
    """test using an image not local"""
    image_puller = ImagePuller(
        container_engine=valid_container_engine,
        image=pullable_image,
        arguments=Constants.NOT_SET,
        pull_policy=data.pull_policy,
    )
    image_puller.assess()
    assert image_puller.assessment.pull_required == data.pull_required
    image_puller.pull_stdout()
    assert image_puller.assessment.pull_required is False


data_image_tag = [
    ("foo", "latest"),
    ("foo:bar", "bar"),
    ("registry.redhat.io:443/ansible-automation-platform-21/ee-supported-rhel8", "latest"),
    ("registry.redhat.io:443/ansible-automation-platform-21/ee-supported-rhel8:latest", "latest"),
]


@pytest.mark.parametrize(
    "image, expected_tag",
    data_image_tag,
    ids=[
        "simple image name, no tag specified",
        "simple image name, with tag",
        "complex image URL, with port but no tag",
        "complex image URL, with port and tag",
    ],
)
def test_tag_parsing(image, expected_tag):
    """test that we parse image tags in a reasonable way"""
    image_puller = ImagePuller(
        container_engine="podman",
        image=image,
        arguments=Constants.NOT_SET,
        pull_policy="tag",
    )
    image_puller._extract_tag()  # pylint: disable=protected-access
    assert image_puller._image_tag == expected_tag  # pylint: disable=protected-access


def test_pull_with_args():
    """Ensure command is generated with additional arguments."""
    image_puller = ImagePuller(
        container_engine="podman",
        image="my_image",
        arguments=["--tls-verify false"],
        pull_policy="tag",
    )
    result = image_puller._generate_pull_command()  # pylint: disable=protected-access
    expected_list = ["podman", "pull", "--tls-verify", "false", "my_image"]
    assert result == expected_list
    expected_string = "podman pull --tls-verify false my_image"
    assert result == shlex.split(expected_string)
