"""Definitions of UI content objects."""

from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict
from typing import Generic
from typing import TypeVar

from ..utils.compatibility import TypeAlias
from ..utils.serialize import SerializationFormat


class ContentView(Enum):
    """The content view."""

    FULL = "full"
    NORMAL = "normal"


T = TypeVar("T")  # pylint:disable=invalid-name # https://github.com/PyCQA/pylint/pull/5221
DictType: TypeAlias = Dict[str, T]


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
        else:
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
