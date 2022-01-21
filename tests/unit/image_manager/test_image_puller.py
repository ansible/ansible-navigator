"""unit tests for image puller"""

import uuid

from typing import NamedTuple

import pytest

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
        pull_policy=data.pull_policy,
    )
    image_puller.assess()
    assert image_puller.assessment.pull_required == data.pull_required


data_dont_have = [
    TstPullPolicy(pull_policy="always", pull_required=True),
    TstPullPolicy(pull_policy="missing", pull_required=True),
    TstPullPolicy(pull_policy="never", pull_required=False),
    TstPullPolicy(pull_policy="tag", pull_required=True),
]


@pytest.mark.parametrize("data", data_dont_have, ids=id_from_data)
def test_dont_have(valid_container_engine, data):
    """test using an image not local"""
    uuid_str = str(uuid.uuid4())
    image_puller = ImagePuller(
        container_engine=valid_container_engine, image=uuid_str, pull_policy=data.pull_policy
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
        pull_policy=data.pull_policy,
    )
    image_puller.assess()
    assert image_puller.assessment.pull_required == data.pull_required
    image_puller.pull_stdout()
    assert image_puller.assessment.pull_required is False
