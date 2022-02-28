"""Definitions of UI content objects."""

from dataclasses import dataclass
from enum import Enum
from typing import Callable
from typing import Optional

from ..utils.serialize_defs import SerializationFormat


class ContentView(Enum):
    """The content view."""

    FULL = "full"
    NORMAL = "normal"


@dataclass
class ContentBase:
    """The base class for all content dataclasses presented in the UI."""

    def serialization_dict_factory(
        self,
        serf: SerializationFormat,
        view: ContentView,
    ) -> Optional[Callable]:
        """Provide the factory to be used to convert self into a dictionary.

        :param serf: The serialization format
        :param view: The content view
        :returns: The factory
        """
        if (view, serf) == (ContentView.FULL, SerializationFormat.JSON):
            return self.serialize_json_full()
        if (view, serf) == (ContentView.FULL, SerializationFormat.YAML):
            return self.serialize_yaml_full()
        if (view, serf) == (ContentView.NORMAL, SerializationFormat.JSON):
            return self.serialize_json_normal()
        if (view, serf) == (ContentView.NORMAL, SerializationFormat.YAML):
            return self.serialize_yaml_normal()
        return None

    # pylint: disable=no-self-use
    def serialize_json_full(self) -> Optional[Callable]:
        """Provide dictionary factory for ``JSON`` with all attributes.

        :returns: The function used for conversion to a dictionary or nothing
        """
        return None

    def serialize_json_normal(self) -> Optional[Callable]:
        """Provide dictionary factory for ``JSON`` with curated attributes.

        :returns: The function used for conversion to a dictionary or nothing
        """
        return None

    def serialize_yaml_full(self) -> Optional[Callable]:
        """Provide dictionary factory for ``YAML`` with all attributes.

        :returns: The function used for conversion to a dictionary or nothing
        """
        return None

    def serialize_yaml_normal(self) -> Optional[Callable]:
        """Provide dictionary factory for ``JSON`` with curated attributes.

        :returns: The function used for conversion to a dictionary or nothing
        """
        return None

    # pylint: enable=no-self-use
