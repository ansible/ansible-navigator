"""Definitions of UI content objects."""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import Union


if TYPE_CHECKING:
    from .utils.compatibility import TypeAlias


class ContentView(Enum):
    """The content view."""

    FULL = "full"
    NORMAL = "normal"


T = TypeVar("T")
DictType: TypeAlias = dict[str, T]


class SerializationFormat(Enum):
    """The serialization format."""

    YAML = "YAML"
    JSON = "JSON"


@dataclass
class ContentBase(Generic[T]):
    r"""The base class for all content dataclasses presented in the UI.

    It should be noted, that while the return type is defined as ``T``
    for the serialization functions below, mypy will not catch in incorrect
    definition of ``T`` at this time.  This is because of how ``asdict()``
    is typed:

    @overload
    def asdict(obj: Any) -> dict[str, Any]: ...
    @overload
    def asdict(obj: Any, \*, dict_factory: Callable[[list[tuple[str, Any]]], _T]) -> _T: ...

    Which result in mypy believing the outcome of asdict is dict[str, Any] and letting it silently
    pass through an incorrect ``T``. ``Mypy`` identifies this as a known issue:
    https://mypy.readthedocs.io/en/stable/additional_features.html#caveats-known-issues
    """

    def asdict(
        self,
        content_view: ContentView,
        serialization_format: SerializationFormat,
    ) -> DictType:
        """Convert thy self into a dictionary.

        :param content_view: The content view
        :param serialization_format: The serialization format
        :returns: A dictionary created from self
        """
        converter_map = {
            (ContentView.FULL, SerializationFormat.JSON): self.serialize_json_full,
            (ContentView.FULL, SerializationFormat.YAML): self.serialize_yaml_full,
            (ContentView.NORMAL, SerializationFormat.JSON): self.serialize_json_normal,
            (ContentView.NORMAL, SerializationFormat.YAML): self.serialize_yaml_normal,
        }

        try:
            dump_self_as_dict = converter_map[content_view, serialization_format]
        except KeyError:
            return asdict(self)
        return dump_self_as_dict()

    def serialize_json_full(self) -> DictType:
        """Provide dictionary for ``JSON`` with all attributes.

        :returns: A dictionary created from self
        """
        return asdict(self)

    def serialize_json_normal(self) -> DictType:
        """Provide dictionary for ``JSON`` with curated attributes.

        :returns: A dictionary created from self
        """
        return asdict(self)

    def serialize_yaml_full(self) -> DictType:
        """Provide dictionary for ``YAML`` with all attributes.

        :returns: A dictionary created from self
        """
        return asdict(self)

    def serialize_yaml_normal(self) -> DictType:
        """Provide dictionary for ``JSON`` with curated attributes.

        :returns: A dictionary created from self
        """
        return asdict(self)

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

    def items(self):
        """Allow this dataclass to be treated like a dictionary.

        This is a work around until the UI fully supports dataclasses
        at which time this can be removed.

        :returns: Tuples of attribute value pairs
        """
        return asdict(self).items()


ContentTypeSingle = Union[bool, float, int, str, dict[str, Any], ContentBase]
ContentTypeSequence = Union[list[Any], Sequence[ContentBase]]
ContentType = Union[ContentTypeSingle, ContentTypeSequence]


@dataclass(frozen=True)
class CFormat:
    """A single instance for a content format."""

    scope: str
    """The scope, used for tokenization"""
    file_extension: str
    """The file extension, with a ."""
    serialization: SerializationFormat | None
    """If needed the serialization format"""


class ContentFormat(Enum):
    """All content formats."""

    ANSI = CFormat(scope="source.ansi", file_extension=".ansi", serialization=None)
    JSON = CFormat(
        scope="source.json",
        file_extension=".json",
        serialization=SerializationFormat.JSON,
    )
    LOG = CFormat(scope="text.log", file_extension=".log", serialization=None)
    MARKDOWN = CFormat(scope="text.html.markdown", file_extension=".md", serialization=None)
    TXT = CFormat(scope="source.txt", file_extension=".txt", serialization=None)
    YAML = CFormat(
        scope="source.yaml",
        file_extension=".yml",
        serialization=SerializationFormat.YAML,
    )
    # YAML as string, already serialized
    YAML_TXT = CFormat(
        scope="source.yaml",
        file_extension=".yml",
        serialization=None,
    )
