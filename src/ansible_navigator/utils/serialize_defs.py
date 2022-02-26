"""Defintions related to content serialization."""

from enum import Enum


class SerializationFormat(Enum):
    """The serialization format."""

    YAML = "yaml"
    JSON = "json"
