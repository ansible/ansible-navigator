""" load libyaml or pyyaml ldumper """
# pylint: disable=unused-import
import re

from typing import NamedTuple
from typing import Union
from typing import Any

import yaml  # noqa: F401

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper  # type: ignore # noqa: F401

try:
    from yaml import CLoader as Loader
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import Loader  # type: ignore # noqa: F401
    from yaml import SafeLoader  # type: ignore # noqa: F401


class YamlStyle(NamedTuple):
    """the params for yaml dump"""

    default_flow_style: bool = False
    explicit_start: bool = True
    sort_keys: bool = True


def human_dump(obj: Any, filename: str = None, fmode: str = "w") -> Union[str, None]:
    """Consistant dumping of object across the application"""
    dumper = HumanDumper
    if filename is not None:
        with open(filename, fmode) as outfile:
            yaml.dump(
                obj,
                outfile,
                Dumper=dumper,
                **YamlStyle()._asdict(),
            )
        return None
    return yaml.dump(obj, Dumper=dumper, **YamlStyle()._asdict())


class HumanDumper(Dumper):
    # pylint: disable=too-many-ancestors
    """for block scalar for multiline"""

    def represent_scalar(self, tag, value, style=None):
        """Uses a block scalar for a nicer human representation of multiline strings."""
        if style is None and _is_multiline_string(value):
            style = "|"

            # Remove leading or trailing newline and convert tabs to spaces
            # which can cause havoc on yaml blocks
            value = value.strip().expandtabs()

            # Replace some whitespace chars
            value = re.sub(r"[\r]", "", value)

        return super().represent_scalar(tag, value, style)


# from http://stackoverflow.com/a/15423007/115478
def _is_multiline_string(value):
    for character in "\u000a\u000d\u001c\u001d\u001e\u0085\u2028\u2029":
        if character in value:
            return True

    return False
