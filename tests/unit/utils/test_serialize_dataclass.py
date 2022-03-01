"""Tests for serializing a dataclass."""
from dataclasses import asdict
from dataclasses import dataclass
from functools import partial
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import NamedTuple
from typing import Tuple
from typing import Union

import pytest

from ansible_navigator.ui_framework.content_defs import ContentBase
from ansible_navigator.ui_framework.content_defs import ContentView
from ansible_navigator.utils.serialize import SerializationFormat
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
        result = content.asdict(
            serf=serf_tuple[1],
            view=view,
        )
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
        result = content.asdict(
            serf=serf_tuple[1],
            view=view,
        )
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
