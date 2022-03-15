"""Tests for serializing a dataclass."""
from dataclasses import asdict
from dataclasses import dataclass
from functools import partial
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import NamedTuple
from typing import Tuple
from typing import Union

import pytest

from ansible_navigator.content_defs import ContentBase
from ansible_navigator.content_defs import ContentView
from ansible_navigator.utils.serialize import SerializationFormat
from ansible_navigator.utils.serialize import serialize


class ParametrizeView(NamedTuple):
    """Keyword arguments for parametrization of view."""

    argnames: str = "content_view"
    argvalues: Iterable = (ContentView.NORMAL, ContentView.FULL)
    ids: Callable = str


class ParametrizeFormat(NamedTuple):
    """Keyword arguments for parametrization of format."""

    argnames: str = "serialization_tuple"
    argvalues: Iterable = (("j", SerializationFormat.JSON), ("y", SerializationFormat.YAML))
    ids: Callable = str


SimpleDictValueT = Union[bool, str, int]


@dataclass
class ContentTestSimple(ContentBase[SimpleDictValueT]):
    """Test content, no dictionary factory overrides."""

    attr_01: bool = False
    attr_02: int = 2
    attr_03: str = "three"


OverrideDictValueT = str
OverrideDictReturn = Dict[str, OverrideDictValueT]
OverrideAllValuesT = Union[bool, int, str]


@dataclass
class ContentTestOverride(ContentBase[OverrideDictValueT]):
    """Test content, with dictionary factory overrides."""

    attr_01: bool = False
    attr_02: int = 2
    attr_03: str = "three"

    def serialize_json_full(self) -> OverrideDictReturn:
        """Provide dictionary factory for ``JSON`` with all attributes.

        :returns: The function used for conversion to a dictionary or nothing
        """
        return self._asdict(suffix=f"_j_{ContentView.FULL!s}")

    def serialize_json_normal(self) -> OverrideDictReturn:
        """Provide dictionary factory for ``JSON`` with curated attributes.

        :returns: The function used for conversion to a dictionary or nothing
        """
        return self._asdict(suffix=f"_j_{ContentView.NORMAL!s}")

    def serialize_yaml_full(self) -> OverrideDictReturn:
        """Provide dictionary factory for ``YAML`` with all attributes.

        :returns: The function used for conversion to a dictionary or nothing
        """
        return self._asdict(suffix=f"_y_{ContentView.FULL!s}")

    def serialize_yaml_normal(self) -> OverrideDictReturn:
        """Provide dictionary factory for ``JSON`` with curated attributes.

        :returns: The function used for conversion to a dictionary or nothing
        """
        return self._asdict(suffix=f"_y_{ContentView.NORMAL!s}")

    def _asdict(self, suffix) -> OverrideDictReturn:
        return asdict(self, dict_factory=partial(self._custom_dict_factory, suffix=suffix))

    @staticmethod
    def _custom_dict_factory(
        kv_pairs: List[Tuple[str, OverrideAllValuesT]],
        suffix: str,
    ) -> OverrideDictReturn:
        """Create a dictionary with suffixed values from a list of key-value pairs.

        :param kv_pairs: The key-value pairs provided by ``dataclasses.asdict()``
        :param suffix: The suffix to append to values
        :returns: The dictionary with suffixed values
        """
        return {name: f"{str(value)}_{suffix}" for name, value in kv_pairs}


parametrize_content_views = pytest.mark.parametrize(**ParametrizeView()._asdict())
parametrize_serialization_format = pytest.mark.parametrize(**ParametrizeFormat()._asdict())


@parametrize_serialization_format
@parametrize_content_views
def test_content_to_dict(
    content_view: ContentView,
    serialization_tuple: Tuple[str, SerializationFormat],
):
    """Test the conversion of the dataclass to a dict.

    :param content_view: The content view
    :param serialization_tuple: The suffix, serialization format
    """
    content = ContentTestSimple()
    content_as_dict = content.asdict(
        serialization_format=serialization_tuple[1],
        content_view=content_view,
    )
    assert content_as_dict == {"attr_01": False, "attr_02": 2, "attr_03": "three"}


@parametrize_content_views
def test_content_to_json(content_view: ContentView):
    """Test the conversion of the dataclass to json.

    :param content_view: The content view
    """
    content = ContentTestSimple()
    content_serialized = serialize(
        content=content,
        content_view=content_view,
        serialization_format=SerializationFormat.JSON,
    )
    expected = '{\n    "attr_01": false,\n    "attr_02": 2,\n    "attr_03": "three"\n}'
    assert content_serialized == expected


@parametrize_content_views
def test_content_to_yaml(content_view: ContentView):
    """Test the conversion of the dataclass to yaml.

    :param content_view: The content view
    """
    content = ContentTestSimple()
    content_serialized = serialize(
        content=content,
        content_view=content_view,
        serialization_format=SerializationFormat.YAML,
    )
    expected = "---\nattr_01: false\nattr_02: 2\nattr_03: three\n"
    assert content_serialized == expected


@parametrize_serialization_format
@parametrize_content_views
def test_content_to_dict_override(
    subtests: Any,
    content_view: ContentView,
    serialization_tuple: Tuple[str, SerializationFormat],
):
    """Test the conversion of the dataclass with overrides to a ``dict``.

    :param subtests: The pytest subtest fixture
    :param content_view: The content view
    :param serialization_tuple: The suffix, serialization format
    """
    content = ContentTestOverride()
    content_as_dict = content.asdict(
        content_view=content_view,
        serialization_format=serialization_tuple[1],
    )
    for key, value in content_as_dict.items():
        with subtests.test(msg=key, value=value):
            assert value.endswith(f"_{serialization_tuple[0]}_{str(content_view)}")


@parametrize_content_views
def test_content_to_json_override(content_view: ContentView):
    """Test the conversion of the dataclass with overrides to ``JSON``.

    :param content_view: The content view
    """
    content = ContentTestOverride()
    content_serialized = serialize(
        content=content,
        content_view=content_view,
        serialization_format=SerializationFormat.JSON,
    )
    expected_template = (
        '{{\n    "attr_01": "False__j_{view}",\n'
        '    "attr_02": "2__j_{view}",\n'
        '    "attr_03": "three__j_{view}"\n}}'
    )
    assert content_serialized == expected_template.format(view=content_view)


@parametrize_content_views
def test_content_to_yaml_override(content_view: ContentView):
    """Test the conversion of the dataclass with overrides to ``YAML``.

    :param content_view: The content view
    """
    content = ContentTestOverride()
    content_serialized = serialize(
        content=content,
        content_view=content_view,
        serialization_format=SerializationFormat.YAML,
    )
    expected_template = (
        "---\nattr_01: False__y_{view}\nattr_02: 2__y_{view}\nattr_03: three__y_{view}\n"
    )
    assert content_serialized == expected_template.format(view=content_view)
