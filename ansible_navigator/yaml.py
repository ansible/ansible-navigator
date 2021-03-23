""" load libyaml or pyyaml ldumper """
# pylint: disable=unused-import
import re
import yaml

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper  # type: ignore

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader  # type: ignore


class HumanDumper(Dumper):

    def represent_scalar(self, tag, value, style=None):
        """ Uses a block scalar for a nicer human representation of multiline strings. """
        if style is None and _is_multiline_string(value):
            style = '|'

            # Remove leading or trailing newline and convert tabs to spaces
            # which can cause havoc on yaml blocks
            value = value.strip().expandtabs()

            # Replace some whitespace chars
            value = re.sub(r'[\r]', '', value)

        return super().represent_scalar(tag, value, style)


# from http://stackoverflow.com/a/15423007/115478
def _is_multiline_string(value):
    for c in u"\u000a\u000d\u001c\u001d\u001e\u0085\u2028\u2029":
        if c in value:
            return True

    return False
