"""Abstractions for common serialization formats."""

import json
import re

from enum import Enum
from pathlib import Path
from typing import IO
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import NamedTuple
from typing import Optional
from typing import Union

import yaml


class SerializationFormat(Enum):
    """The serialization format."""

    YAML = "yaml"
    JSON = "json"


if TYPE_CHECKING:
    from ..ui_framework import ContentBase
    from ..ui_framework import ContentView


# pylint: disable=unused-import
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper  # type: ignore[misc] # noqa: F401

try:
    from yaml import CLoader as Loader
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import Loader  # type: ignore[misc] # noqa: F401
    from yaml import SafeLoader  # type: ignore[misc] # noqa: F401
# pylint: enable=unused-import


def serialize(
    content_view: "ContentView",
    content: "ContentBase",
    serialization_format: SerializationFormat,
    file_mode: str = "w",
    filename: Optional[Path] = None,
) -> Optional[str]:
    """Serialize a dataclass based on format and view.

    :param content_view: The content view
    :param content: The content dataclass to serialize
    :param serialization_format: The serialization format
    :param file_mode: The mode for the file operation
    :param filename: A filename to write to
    :returns: The serialized content
    """
    content_as_dict = content.asdict(
        content_view=content_view,
        serialization_format=serialization_format,
    )
    if serialization_format == SerializationFormat.YAML:
        if filename is None:
            return yaml_dumps(obj=content_as_dict)
        return yaml_dump(obj=content_as_dict, filename=filename, file_mode=file_mode)
    if serialization_format == SerializationFormat.JSON:
        if filename is None:
            return json_dumps(content_as_dict)
        return _json_dump(dumpable=content_as_dict, filename=filename, file_mode=file_mode)
    return None


class JsonParams(NamedTuple):
    """The parameters for json dump and dumps."""

    indent: int = 4
    sort_keys: bool = True
    ensure_ascii: bool = False


def _json_dump(dumpable: Dict, filename: Path, file_mode: str):
    """Create a file handle and dump json.

    :param dumpable: The object to dump
    :param filename: The file name for the file
    :param file_mode: The file mode for the operation
    """
    with filename.open(mode=file_mode, encoding="utf-8") as file_handle:
        json_dump(dumpable=dumpable, file_handle=file_handle)


def json_dump(dumpable: Any, file_handle: IO, params: NamedTuple = JsonParams()) -> None:
    """Serialize and write the dumpable to a file.

    :param dumpable: The object to serialize
    :param file_handle: The file handle to write to
    :param params: Parameters to override the defaults
    """
    json.dump(dumpable, file_handle, **params._asdict())


def json_dumps(dumpable: Any, params: NamedTuple = JsonParams()) -> str:
    """Serialize the dumpable to json.

    :param dumpable: The object to serialize
    :param params: Parameters to override the defaults
    :returns: The object serialized
    """
    string = json.dumps(dumpable, **params._asdict())
    return string


class YamlStyle(NamedTuple):
    """The parameters for yaml dump."""

    default_flow_style: bool = False
    explicit_start: bool = True
    allow_unicode: bool = True


def human_dump(
    obj: Any,
    filename: Optional[Union[Path, str]] = None,
    file_mode: str = "w",
) -> Optional[str]:
    """Serialize an object to yaml.

    This allows for the consistent representation across the application.

    :param obj: The object to serialize
    :param filename: The filename of the file in which the obj should be written
    :param file_mode: The mode to use for file writing
    :returns: Either the serialized obj or None if written to a file
    """
    dumper = HumanDumper
    if filename is not None:
        with open(filename, file_mode, encoding="utf-8") as fh:
            yaml.dump(
                obj,
                fh,
                Dumper=dumper,
                **YamlStyle()._asdict(),
            )
        return None
    return yaml.dump(obj, Dumper=dumper, **YamlStyle()._asdict())


yaml_dump = human_dump
yaml_dumps = human_dump


class HumanDumper(Dumper):
    # pylint: disable=too-many-ancestors
    """An instance of a pyyaml Dumper.

    This deviates from the base to dump a multiline string in a human readable format
    and disables the use of anchors and aliases.
    """

    def ignore_aliases(self, _data: Any) -> bool:
        """Disable the use of anchors and aliases in the given data.

        :param _data: The data used to make the determination
        :returns: True, indicating aliases and anchors should not be used
        """
        return True

    def represent_scalar(
        self,
        tag: str,
        value: str,
        style: Optional[str] = None,
    ) -> yaml.nodes.ScalarNode:
        """Represent all multiline strings as block scalars to improve readability for humans.

        :param tag: A custom tag
        :param value: The value to represent
        :param style: The style to use
        :returns: The serialized multiline string, result of the super scalar
        """
        if style is None and _is_multiline_string(value):
            style = "|"

            # Remove leading or trailing newline and convert tabs to spaces
            # which can cause havoc on yaml blocks
            value = value.strip().expandtabs()

            # Replace some whitespace chars
            value = re.sub(r"[\r]", "", value)

        return super().represent_scalar(tag, value, style)


def _is_multiline_string(value: str):
    """Determine if a string is multiline.

    .. note::

       Inspired by http://stackoverflow.com/a/15423007/115478.

    :param value: The value to check
    :returns: A boolean indicating if the string is multiline
    """
    for character in "\u000a\u000d\u001c\u001d\u001e\u0085\u2028\u2029":
        if character in value:
            return True

    return False
