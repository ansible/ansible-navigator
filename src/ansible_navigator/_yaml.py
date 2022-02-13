"""A wrapper for pyyaml."""
# pylint: disable=unused-import
import re

from typing import Any
from typing import NamedTuple
from typing import Union

import yaml  # noqa: F401


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


class YamlStyle(NamedTuple):
    """The parameters for yaml dump."""

    default_flow_style: bool = False
    explicit_start: bool = True
    allow_unicode: bool = True


def human_dump(obj: Any, filename: str = None, file_mode: str = "w") -> Union[str, None]:
    """Serialize an object to yaml.

    This allows for the consistent representation across the application.

    :param obj: The object to serialize
    :param filename: The filename of the file in which the obj should be written
    :param file_mode: The mode to use for file writing
    :return: Either the serialized obj or None if written to a file
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
        style: Union[str, None] = None,
    ) -> yaml.nodes.ScalarNode:
        """Represent all multiline strings as block scalars to improve readability for humans.

        :param tag: A custom tag
        :param value: The value to represent
        :param style: The style to use
        :return: The serialized multiline string, result of the super scalar
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
    :return: A boolean indicating if the string is multiline
    """
    for character in "\u000a\u000d\u001c\u001d\u001e\u0085\u2028\u2029":
        if character in value:
            return True

    return False
