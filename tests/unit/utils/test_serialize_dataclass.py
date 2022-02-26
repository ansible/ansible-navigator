"""Tests for serializing a dataclass."""
from dataclasses import dataclass

from ansible_navigator.ui_framework.content_defs import ContentBase
from ansible_navigator.ui_framework.content_defs import ContentView
from ansible_navigator.utils.serialize import SerializationFormat
from ansible_navigator.utils.serialize import _content_to_dict
from ansible_navigator.utils.serialize import serialize


@dataclass
class ContentTest(ContentBase):
    """Test content."""

    attr_01: bool = False
    attr_02: int = 2
    attr_03: str = "three"


def test_content_to_dict_default():
    """Test the conversion of the dataclass to a dict."""
    content = ContentTest()
    dict_factory = content.serialization_dict_factory(
        serf=SerializationFormat.JSON,
        view=ContentView.NORMAL,
    )
    result = _content_to_dict(content=content, dict_factory=dict_factory)
    assert result == {"attr_01": False, "attr_02": 2, "attr_03": "three"}


def test_content_to_json():
    """Test the conversion of the data class to json."""
    content = ContentTest()
    result = serialize(content=content, serf=SerializationFormat.JSON, view=ContentView.NORMAL)
    expected = '{\n    "attr_01": false,\n    "attr_02": 2,\n    "attr_03": "three"\n}'
    assert result == expected


def test_content_to_yaml():
    """Test the conversion of the data class to yaml."""
    content = ContentTest()
    result = serialize(content=content, serf=SerializationFormat.YAML, view=ContentView.NORMAL)
    expected = "---\nattr_01: false\nattr_02: 2\nattr_03: three\n"
    assert result == expected


if __name__ == "__main__":
    test_content_to_yaml()
