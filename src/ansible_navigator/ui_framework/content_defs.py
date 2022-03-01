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
    """The base class for all content dataclasses presented in the UI."""

    def asdict(
        self,
        serf: SerializationFormat,
        view: ContentView,
    ) -> DictT:
        """Convert thy self into a dictionary.

        :param serf: The serialization format
        :param view: The content view
        :returns: A dictionary created from self
        """
        if (view, serf) == (ContentView.FULL, SerializationFormat.JSON):
            return self.serialize_json_full()
        if (view, serf) == (ContentView.FULL, SerializationFormat.YAML):
            return self.serialize_yaml_full()
        if (view, serf) == (ContentView.NORMAL, SerializationFormat.JSON):
            return self.serialize_json_normal()
        if (view, serf) == (ContentView.NORMAL, SerializationFormat.YAML):
            return self.serialize_yaml_normal()
        return asdict(self)

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
