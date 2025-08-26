"""Unit tests for image puller."""

import os
import shlex
import subprocess
import uuid

from typing import NamedTuple

import pytest

from ansible_navigator.configuration_subsystem import Constants
from ansible_navigator.image_manager import ImagePuller


class TstPullPolicy(NamedTuple):
    """Test object."""

    pull_policy: str
    pull_required: bool


# Note, these tests assume our default is a :latest
data_do_have = [
    pytest.param(TstPullPolicy(pull_policy="always", pull_required=True), id="always"),
    pytest.param(TstPullPolicy(pull_policy="missing", pull_required=False), id="missing"),
    pytest.param(TstPullPolicy(pull_policy="never", pull_required=False), id="never"),
    pytest.param(TstPullPolicy(pull_policy="tag", pull_required=True), id="tag"),
]


@pytest.mark.parametrize("data", data_do_have)
def test_do_have(
    valid_container_engine: str,
    default_ee_image_name: str,
    data: TstPullPolicy,
) -> None:
    """Test using an image local.

    Args:
        valid_container_engine: Container engine identifier
        default_ee_image_name: Default image name
        data: Test object
    """
    image_puller = ImagePuller(
        container_engine=valid_container_engine,
        image=default_ee_image_name,
        arguments=Constants.NOT_SET,
        pull_policy=data.pull_policy,
    )
    image_puller.assess()
    assert image_puller.assessment.pull_required == data.pull_required


# Note, these tests assume the image is a :latest
data_do_have_but_latest = [
    pytest.param(TstPullPolicy(pull_policy="always", pull_required=True), id="always"),
    pytest.param(TstPullPolicy(pull_policy="missing", pull_required=False), id="missing"),
    pytest.param(TstPullPolicy(pull_policy="never", pull_required=False), id="never"),
    pytest.param(TstPullPolicy(pull_policy="tag", pull_required=True), id="tag"),
]


@pytest.mark.parametrize("data", data_do_have_but_latest)
def test_do_have_but_latest(
    valid_container_engine: str,
    small_image_name: str,
    data: TstPullPolicy,
) -> None:
    """Test using an image local.

    Args:
        valid_container_engine: Container engine identifier
        small_image_name: Small image name
        data: Test object
    """
    image_puller = ImagePuller(
        container_engine=valid_container_engine,
        image=small_image_name,
        arguments=Constants.NOT_SET,
        pull_policy=data.pull_policy,
    )
    image_puller.assess()
    assert image_puller.assessment.pull_required == data.pull_required


data_missing_locally = [
    pytest.param(TstPullPolicy(pull_policy="always", pull_required=True), id="always"),
    pytest.param(TstPullPolicy(pull_policy="missing", pull_required=True), id="missing"),
    pytest.param(TstPullPolicy(pull_policy="never", pull_required=False), id="never"),
    pytest.param(TstPullPolicy(pull_policy="tag", pull_required=True), id="tag"),
]


@pytest.mark.parametrize("data", data_missing_locally)
def test_missing_locally(valid_container_engine: str, data: TstPullPolicy) -> None:
    """Test using an image not local.

    Args:
        valid_container_engine: Container engine identifier
        data: Test object
    """
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


@pytest.mark.parametrize(
    "data",
    (
        pytest.param(TstPullPolicy(pull_policy="missing", pull_required=True), id="0"),
        pytest.param(TstPullPolicy(pull_policy="always", pull_required=True), id="1"),
        pytest.param(TstPullPolicy(pull_policy="never", pull_required=False), id="2"),
        pytest.param(TstPullPolicy(pull_policy="tag", pull_required=True), id="3"),
    ),
)
def test_will_have(valid_container_engine: str, pullable_image: str, data: TstPullPolicy) -> None:
    """Test using an image not local.

    Args:
        valid_container_engine: Container engine identifier
        pullable_image: Container image
        data: Test object
    """
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


@pytest.mark.parametrize(
    ("image", "expected_tag"),
    (
        pytest.param("foo", "latest", id="simple-image-name:no-tag-specified"),
        pytest.param("foo:bar", "bar", id="simple-image-name:with-tag"),
        pytest.param(
            "registry.redhat.io:443/ansible-automation-platform-21/ee-supported-rhel8",
            "latest",
            id="complex-image-URL:with-port-but-no-tag",
        ),
        pytest.param(
            "registry.redhat.io:443/ansible-automation-platform-21/ee-supported-rhel8:latest",
            "latest",
            id="complex-image-URL:with-port-and-tag",
        ),
    ),
)
def test_tag_parsing(image: str, expected_tag: str) -> None:
    """Test that we parse image tags in a reasonable way.

    Args:
        image: Test image
        expected_tag: Expected tag for assertion
    """
    image_puller = ImagePuller(
        container_engine="podman",
        image=image,
        arguments=Constants.NOT_SET,
        pull_policy="tag",
    )
    image_puller._extract_tag()
    assert image_puller._image_tag == expected_tag


def test_pull_with_args() -> None:
    """Ensure command is generated with additional arguments."""
    image_puller = ImagePuller(
        container_engine="podman",
        image="my_image",
        arguments=["--tls-verify false"],
        pull_policy="tag",
    )
    result = image_puller._generate_pull_command()
    expected_string = "podman pull --tls-verify false my_image"
    assert result == expected_string
    expected_list = ["podman", "pull", "-q", "--tls-verify", "false", "my_image"]
    assert shlex.split(result) == expected_list


def test_pull_with_env_arg() -> None:
    """Ensure the expansion of env variable in the arguments."""
    image_puller = ImagePuller(
        container_engine="podman",
        image="my_image",
        arguments=["--authfile", "${XDG_RUNTIME_DIR}/containers/auth.json"],
        pull_policy="tag",
    )
    result = image_puller._generate_pull_command()
    cmd_to_run = f"echo {result}"
    proc = subprocess.run(
        cmd_to_run,
        check=True,
        shell=True,
        env=os.environ,
        capture_output=True,
        text=True,
    )
    assert "XDG_RUNTIME_DIR" not in proc.stdout
    assert "containers/auth.json" in proc.stdout
