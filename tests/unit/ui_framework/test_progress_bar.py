"""Test for the conversion of percent string to progress bars."""
from dataclasses import dataclass

from ansible_navigator.content_defs import ContentBase
from ansible_navigator.ui_framework.utils import convert_percentage


def test_dictionary_running() -> None:
    """Test the conversion of a string within a dictionary to a progress bar when not complete."""
    test_data = {"progress": "30%", "other": "test value"}
    convert_percentage(content=test_data, columns=["progress"], progress_bar_width=10)
    expected = {"progress": "▇▇▇       ", "other": "test value", "_progress": "30%"}
    assert test_data == expected


def test_dictionary_complete() -> None:
    """Test the conversion of a string within a dictionary to a progress bar when complete."""
    test_data = {"progress": "100%", "other": "test value"}
    convert_percentage(content=test_data, columns=["progress"], progress_bar_width=10)
    expected = {"progress": " COMPLETE ", "other": "test value", "_progress": "100%"}
    assert test_data == expected


@dataclass
class ContentTest(ContentBase):
    """Test data for string conversion to a progress bar."""

    progress: str
    _progress: str = ""
    other: str = "test_value"

    def get(self, attribute: str):
        """Allow this dataclass to be treated like a dictionary.

        This is a work around until the UI fully supports dataclasses
        at which time this can be removed.

        Default is intentionally not implemented as a safeguard to enure
        this is not more work than necessary to remove in the future
        and will only return attributes in existence.

        :param attribute: The attribute to get
        :returns: The gotten attribute
        """
        return getattr(self, attribute)


def test_dataclass_running() -> None:
    """Test the conversion of a string within a dataclass to a progress bar when not complete."""
    test_data = ContentTest(progress="30%")
    convert_percentage(content=test_data, columns=["progress"], progress_bar_width=10)
    assert test_data.progress == "▇▇▇       "
    assert test_data._progress == "30%"  # pylint: disable=protected-access
    assert test_data.other == "test_value"


def test_dataclass_complete() -> None:
    """Test the conversion of a string within a dataclass to a progress bar when not complete."""
    test_data = ContentTest(progress="100%")
    convert_percentage(content=test_data, columns=["progress"], progress_bar_width=10)
    assert test_data.progress == " COMPLETE "
    assert test_data._progress == "100%"  # pylint: disable=protected-access
    assert test_data.other == "test_value"
