"""Tests for serializing a dataclass."""
from dataclasses import dataclass
from functools import partial
from typing import Callable
from typing import Iterable
from typing import NamedTuple
from typing import Optional
from typing import Tuple

import pytest

from ansible_navigator.ui_framework.content_defs import ContentBase
from ansible_navigator.ui_framework.content_defs import ContentView
from ansible_navigator.utils.serialize import SerializationFormat
from ansible_navigator.utils.serialize import _content_to_dict
from ansible_navigator.utils.serialize import serialize


class ParametrizeView(NamedTuple):
    """Keyword arguments for parametrization of view."""

    argnames: str = "view"
    argvalues: Iterable = (ContentView.NORMAL, ContentView.FULL)
    ids: Callable = str


class ParametrizeFormat(NamedTuple):
    """Keyword arguments for parametrization of format."""

    argnames: str = "serf_tuple"
    argvalues: Iterable = (("j", SerializationFormat.JSON), ("y", SerializationFormat.YAML))
    ids: Callable = str


@dataclass
class ContentTestSimple(ContentBase):
    """Test content, no dictionary factory overrides."""

    attr_01: bool = False
    attr_02: int = 2
    attr_03: str = "three"


def custom_dict_factory(kv_pairs, suffix: str):
    """Create a dictionary with suffixed values from a list of key-value pairs.

    :param kv_pairs: The key-value pairs provided by ``dataclasses.asdict()``
    :param suffix: The suffix to append to values
    :returns: The dictionary with suffixed values
    """
    return {name: f"{str(value)}_{suffix}" for name, value in kv_pairs}


@dataclass
class ContentTestOverride(ContentTestSimple):
    """Test content, with dictionary factory overrides."""

    def serialize_json_full(self) -> Optional[Callable]:
        """Provide dictionary factory for ``JSON`` with all attributes.

        :returns: The function used for conversion to a dictionary or nothing
        """
        return partial(custom_dict_factory, suffix=f"_j_{ContentView.FULL!s}")

    def serialize_json_normal(self) -> Optional[Callable]:
        """Provide dictionary factory for ``JSON`` with curated attributes.

        :returns: The function used for conversion to a dictionary or nothing
        """
        return partial(custom_dict_factory, suffix=f"_j_{ContentView.NORMAL!s}")

    def serialize_yaml_full(self) -> Optional[Callable]:
        """Provide dictionary factory for ``YAML`` with all attributes.

        :returns: The function used for conversion to a dictionary or nothing
        """
        return partial(custom_dict_factory, suffix=f"_y_{ContentView.FULL!s}")

    def serialize_yaml_normal(self) -> Optional[Callable]:
        """Provide dictionary factory for ``JSON`` with curated attributes.

        :returns: The function used for conversion to a dictionary or nothing
        """
        return partial(custom_dict_factory, suffix=f"_y_{ContentView.NORMAL!s}")


@pytest.mark.parametrize(**ParametrizeView()._asdict())
class Test:
    """The dataclass serialization test class."""

    @staticmethod
    @pytest.mark.parametrize(**ParametrizeFormat()._asdict())
    def test_content_to_dict(view: ContentView, serf_tuple: Tuple[str, SerializationFormat]):
        """Test the conversion of the dataclass to a dict.

        :param view: The content view
        :param serf_tuple: The suffix, serialization format
        """
        content = ContentTestSimple()
        dict_factory = content.serialization_dict_factory(
            serf=serf_tuple[1],
            view=view,
        )
        result = _content_to_dict(content=content, dict_factory=dict_factory)
        assert result == {"attr_01": False, "attr_02": 2, "attr_03": "three"}

    @staticmethod
    def test_content_to_json(view: ContentView):
        """Test the conversion of the dataclass to json.

        :param view: The content view
        """
        content = ContentTestSimple()
        result = serialize(content=content, serf=SerializationFormat.JSON, view=view)
        expected = '{\n    "attr_01": false,\n    "attr_02": 2,\n    "attr_03": "three"\n}'
        assert result == expected

    @staticmethod
    def test_content_to_yaml(view: ContentView):
        """Test the conversion of the dataclass to yaml.

        :param view: The content view
        """
        content = ContentTestSimple()
        result = serialize(content=content, serf=SerializationFormat.YAML, view=view)
        expected = "---\nattr_01: false\nattr_02: 2\nattr_03: three\n"
        assert result == expected

    @staticmethod
    @pytest.mark.parametrize(**ParametrizeFormat()._asdict())
    def test_content_to_dict_override(
        view: ContentView,
        serf_tuple: Tuple[str, SerializationFormat],
    ):
        """Test the conversion of the dataclass with overrides to a ``dict``.

        :param view: The content view
        :param serf_tuple: The suffix, serialization format
        """
        content = ContentTestOverride()
        dict_factory = content.serialization_dict_factory(
            serf=serf_tuple[1],
            view=view,
        )
        result = _content_to_dict(content=content, dict_factory=dict_factory)
        for _key, value in result.items():
            assert value.endswith(f"_{serf_tuple[0]}_{str(view)}")

    @staticmethod
    def test_content_to_json_override(view: ContentView):
        """Test the conversion of the dataclass with overrides to ``JSON``.

        :param view: The content view
        """
        content = ContentTestOverride()
        result = serialize(content=content, serf=SerializationFormat.JSON, view=view)
        result_template = (
            '{{\n    "attr_01": "False__j_{view}",\n'
            '    "attr_02": "2__j_{view}",\n'
            '    "attr_03": "three__j_{view}"\n}}'
        )
        assert result == result_template.format(view=view)

    @staticmethod
    def test_content_to_yaml_override(view: ContentView):
        """Test the conversion of the dataclass with overrides to ``YAML``.

        :param view: The content view
        """
        content = ContentTestOverride()
        result = serialize(content=content, serf=SerializationFormat.YAML, view=view)
        result_template = (
            "---\nattr_01: False__y_{view}\nattr_02: 2__y_{view}\nattr_03: three__y_{view}\n"
        )
        assert result == result_template.format(view=view)
