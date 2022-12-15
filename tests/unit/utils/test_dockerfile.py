"""Tests related to the retrieval of image names from the packaged dockerfile."""

import pytest

from ansible_navigator.utils.packaged_data import ImageEntry
from ansible_navigator.utils.packaged_data import retrieve_content


@pytest.fixture(scope="module", name="contents")
def _contents() -> str:
    """Return the contents of the dockerfile.

    :returns: The contents of the dockerfile.
    """
    return retrieve_content(filename="images_dockerfile")


def test_count(contents: str):
    """Verify the number of images in the dockerfile.

    :param contents: The contents of the dockerfile.
    """
    assert len(ImageEntry.__members__) == len(
        [line for line in contents.splitlines() if line.startswith("FROM")]
    )


def test_format(contents: str):
    """Verify the format of each FROM line.

    :param contents: The contents of the dockerfile.
    """
    from_lines = (line for line in contents.splitlines() if line.startswith("FROM"))
    for line in from_lines:
        assert len(line.split()) == 4


@pytest.mark.parametrize("image", ImageEntry)
def test_get(image: ImageEntry):
    """Verify the image name can be retrieved.

    :param image: The image to retrieve.
    """
    name = image.get(app_name="ansible_navigator")
    assert isinstance(name, str)
