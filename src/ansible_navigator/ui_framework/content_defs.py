"""Definitions of UI content objects."""

from dataclasses import dataclass
from enum import Enum
from typing import Callable
from typing import Optional

from ..utils.serialize import SerializationFormat


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
            return self._serialize_json_full()
        if (view, serf) == (ContentView.FULL, SerializationFormat.YAML):
            return self._serialize_yaml_full()
        if (view, serf) == (ContentView.NORMAL, SerializationFormat.JSON):
            return self._serialize_json_normal()
        if (view, serf) == (ContentView.NORMAL, SerializationFormat.YAML):
            return self._serialize_yaml_normal()
        return None

    def _serialize_json_full(self):
        return self._default_dict_factory()

    def _serialize_json_normal(self):
        return self._default_dict_factory()

    def _serialize_yaml_full(self):
        return self._default_dict_factory()

    def _serialize_yaml_normal(self):
        return self._default_dict_factory()

    @staticmethod
    def _default_dict_factory():
        return None
