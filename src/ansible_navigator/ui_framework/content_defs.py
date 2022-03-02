"""Definitions of UI content objects."""

from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict
from typing import Generic
from typing import TypeVar

from ..utils.serialize import SerializationFormat


class ContentView(Enum):
    """The content view."""

    FULL = "full"
    NORMAL = "normal"


DictValueT = TypeVar("DictValueT")
DictT = Dict[str, DictValueT]


@dataclass
class ContentBase(Generic[DictValueT]):
    r"""The base class for all content dataclasses presented in the UI.

    It should be noted, that while the return type is defined as ``DictValueT``
    for the serialization functions below, mypy will not catch in incorrect
    definition of ``DictValueT`` at this time.  This is because of how ``asdict()``
    is typed:

    @overload
    def asdict(obj: Any) -> dict[str, Any]: ...
    @overload
    def asdict(obj: Any, \*, dict_factory: Callable[[list[tuple[str, Any]]], _T]) -> _T: ...

    Which result in mypy believing the outcome of asdict is dict[str, Any] and letting it silently
    pass through an incorrect ``DictValueT``. ``Mypy`` identifies this as a known issue:
    https://mypy.readthedocs.io/en/stable/additional_features.html#caveats-known-issues
    """

    def asdict(
        self,
        content_view: ContentView,
        serialization_format: SerializationFormat,
    ) -> DictT:
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

    def serialize_json_full(self) -> DictT:
        """Provide dictionary for ``JSON`` with all attributes.

        :returns: A dictionary created from self
        """
        return asdict(self)

    def serialize_json_normal(self) -> DictT:
        """Provide dictionary for ``JSON`` with curated attributes.

        :returns: A dictionary created from self
        """
        return asdict(self)

    def serialize_yaml_full(self) -> DictT:
        """Provide dictionary for ``YAML`` with all attributes.

        :returns: A dictionary created from self
        """
        return asdict(self)

    def serialize_yaml_normal(self) -> DictT:
        """Provide dictionary for ``JSON`` with curated attributes.

        :returns: A dictionary created from self
        """
        return asdict(self)
