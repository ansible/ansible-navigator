""" parse pip freeze
"""
import re


def _parse_pip(*args, **_kwargs):
    """Convert the list of pip pkgs"""
    result = {}
    for line in args[0]:
        parts = re.split("==|@", line)
        if len(parts) == 2:
            result[parts[0].strip()] = parts[1].strip()
    return result


def _parse_galaxy(*args, **_kwargs):
    result = {}
    for line in args[0][2:]:
        parts = line.split()
        if len(parts) == 2 and parts[1][0].isdigit():
            result[parts[0].strip()] = parts[1].strip()
    return result


class FilterModule:
    # pylint: disable=too-few-public-methods
    """pip_parse"""

    @staticmethod
    def filters():
        """a mapping of filter names to functions"""
        return {"parse_pip": _parse_pip, "parse_galaxy": _parse_galaxy}
