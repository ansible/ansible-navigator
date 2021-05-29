""" Tokenize and color text
"""

import json
import logging
import os
import re

import colorsys
import curses
import functools

from itertools import chain

from .curses_defs import CursesLine
from .curses_defs import CursesLinePart

from ..tm_tokenize.grammars import Grammars
from ..tm_tokenize.tokenize import tokenize


CURSES_STYLES = {
    0: None,
    1: getattr(curses, "A_BOLD", None),
    2: getattr(curses, "A_DIM", None),
    3: getattr(curses, "A_ITALIC", None),
    4: getattr(curses, "A_UNDERLINE", None),
    5: getattr(curses, "A_BLINK", None),
    6: getattr(curses, "A_BLINK", None),
    7: getattr(curses, "A_REVERSE", None),
    8: getattr(curses, "A_INVIS", None),
}


class ColorSchema:
    """Simple holer for the schema (theme)"""

    # pylint: disable=too-few-public-methods

    def __init__(self, schema):
        """start

        :param schema: The color scheme, theme to use
        :type schema: dict
        """
        self._schema = schema

    @functools.lru_cache(maxsize=None)
    def get_color(self, scope):
        """Get a color from the schema, from most specific to least

        :param scope: The scope, aka format
        :type scope: str
        :return: the color in rgb format or None
        :rtype: tuple or None
        """
        for name in reversed(scope):
            for parts in range(0, len(name.split("."))):
                prop = name.split()[-1].rsplit(".", parts)[0]
                color = next(
                    (tc for tc in self._schema["tokenColors"] if prop in to_list(tc["scope"])), None
                )
                if color:
                    foreground = color.get("settings", {}).get("foreground", None)
                    return hex_to_rgb(foreground)
        return None


class Colorize:
    """Functionality for coloring"""

    # pylint: disable=too-few-public-methods
    def __init__(self, grammar_dir: str, theme_path: str):
        self._logger = logging.getLogger(__name__)
        self._schema = None
        self._grammars = Grammars(grammar_dir)
        self._theme_path = theme_path
        self._load()

    def _load(self):
        with open(os.path.join(self._theme_path)) as data_file:
            self._schema = ColorSchema(json.load(data_file))

    @functools.lru_cache(maxsize=100)
    def render(self, doc, scope):
        """render some text into columns and colors

        :param doc: The thing to tokenize and color
        :type doc: str
        :param scope: The scope, aka the format of the string
        :type scope: str
        :return: A list of lines, each a list of dicts
        :rtype: list
        """
        if scope == "source.ansi":
            return [ansi_to_curses(l) for l in doc.splitlines()]  # noqa: E741
        try:
            compiler = self._grammars.compiler_for_scope(scope)
        except KeyError:
            compiler = None

        if compiler and scope != "no_color":
            state = compiler.root_state
            lines = []
            for line_idx, line in enumerate(doc.splitlines()):
                first_line = line_idx == 0
                try:
                    state, regions = tokenize(compiler, state, line, first_line)
                except Exception as exc:  # pylint: disable=broad-except
                    self._logger.critical(
                        (
                            "An unexpected error occured within the tokenization"
                            " subsystem.  Please log an issue with the following:"
                        )
                    )
                    self._logger.critical(
                        "  Err: '%s', Scope: '%s', Line follows....", str(exc), scope
                    )
                    self._logger.critical("  '%s'", line)
                    self._logger.critical("  The current content will be rendered without color")
                    break
                else:
                    lines.append((regions, line))
            else:
                return columns_and_colors(lines, self._schema)

        res = [[{"column": 0, "chars": doc_line, "color": None}] for doc_line in doc.splitlines()]
        return res


def to_list(thing):
    """convert something to a list if necessary

    :param thing: Maybe a list?
    :type thing: str or list
    :return: listified thing
    :rtype: list
    """
    if not isinstance(thing, list):
        return [thing]
    return thing


def hex_to_rgb(value):
    """Convert a hex value to RGB

    :param value: the hex color
    :type value: string
    :returns: rgb tuple
    :rtype: tuple
    """
    if value:
        value = value.lstrip("#")
        lenv = len(value)
        return tuple(int(value[i : i + lenv // 3], 16) for i in range(0, lenv, lenv // 3))
    return None


def hex_to_rgb_curses(value):
    """Convert a hex color to RGB scaled to 1000
    b/c that's what curses needs

    :param value: a rgb color
    :type value: tuple
    :return: The colors scaled to 1000
    :rtype: tuple
    """
    scale = lambda x: int(x * 1000 / 255)  # noqa: E731
    red, green, blue = hex_to_rgb(value)
    return (scale(red), scale(green), scale(blue))


def rgb_to_ansi(red: int, green: int, blue: int, colors: int) -> int:
    """Convert an RGB color to an terminal color

    :param red: the red component
    :type red: int
    :param green: the green component
    :type green: int
    :param blue: the blue component
    :type blue: int
    :param colors: The number of color supported by the termina
    :type colors: int
    """
    # https://github.com/Qix-/color-convert/blob/master/conversions.js
    if colors == 256:
        if red == green and green == blue:
            if red < 8:
                ansi = 16
            if red > 248:
                ansi = 231
            ansi = round(((red - 8) / 247) * 24) + 232
        else:
            ansi = (
                16
                + (36 * round(red / 255 * 5))
                + (6 * round(green / 255 * 5))
                + round(blue / 255 * 5)
            )
    elif colors == 16:
        value = colorsys.rgb_to_hsv(red, green, blue)[2]
        value = round(value / 50)
        if value == 0:
            ansi = 30
        else:
            ansi = (round(blue / 255) << 2) | (round(green / 255) << 1) | round(red / 255)
            if value == 2:
                ansi += 8
    else:  # colors == 8, sorry
        ansi = (round(blue / 255) << 2) | (round(green / 255) << 1) | round(red / 255)
    return ansi


def columns_and_colors(lines, schema):
    """Convert to colors and columns

    :param lines: A list of regions (line parts) and the line
    :type lines: list of lines, each a ([regions], line)
    :param scheam: An instance of the ColorSchema
    :type schema: ColorSchema
    """
    result = []

    for line in lines:
        column = 0
        char_dicts = [{"chars": c, "color": None} for c in line[1]]

        for region in line[0]:
            color = schema.get_color(region.scope)
            if color:
                for idx in range(region.start, region.end):
                    char_dicts[idx]["color"] = color

        if char_dicts:
            grouped = [char_dicts.pop(0)]
            while char_dicts:
                entry = char_dicts.pop(0)
                if entry["color"] == grouped[-1]["color"]:
                    grouped[-1]["chars"] += entry["chars"]
                else:
                    grouped.append(entry)
            result.append(grouped)
        else:
            result.append([{"chars": line[1], "color": None}])

    for line in result:
        column = 0
        for chunk in line:
            chunk["column"] = column
            column += len(chunk["chars"])

    return result


def ansi_to_curses(line: str) -> CursesLine:

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-locals
    """Convert ansible color codes to curses colors

    :param line: A string with ansi colors
    :type line: string
    :return: A list of str tuples [(x, s, c), (x, s, c)...]
    :rtype: list
    """
    printable = []
    ansi_regex = re.compile(r"(\x1b\[[\d;]*m)")
    color_regex = re.compile(
        r"""(?x)
            \x1b\[                              # Control Sequence Introducer
            (?P<fg_action>(38;5|39);)?          # optional FG color action
            (?P<_bg_action>(48;5|49);)?         # optional BG color action
            (?P<one>\d+)                        # required, one number
            (;(?P<two>\d+))?                    # optional 2nd number
            m
        """
    )
    parts = ansi_regex.split(line)
    colno = 0
    color = 0
    style = 0
    while parts:
        part = parts.pop(0)
        if part:
            match = color_regex.match(part)
            if match:
                cap = match.groupdict()
                one = cap["one"]
                two = cap["two"]
                if cap["fg_action"] == "39;":
                    pass  # default color
                elif one == "0" and two is None:
                    pass  # default color
                elif cap["fg_action"] == "38;5;":
                    color = int(one)
                    if two:
                        style = CURSES_STYLES.get(int(two), None) or 0
                elif not cap["fg_action"]:
                    ansi_16 = list(chain(range(30, 38), range(90, 98)))
                    if two is None:
                        color = ansi_16.index(int(one)) if int(one) in ansi_16 else int(one)
                    else:
                        color = ansi_16.index(int(two)) if int(two) in ansi_16 else int(two)
                        style = CURSES_STYLES.get(int(one), None) or 0
            else:
                curses_line = CursesLinePart(
                    column=colno, string=part, color=color, decoration=style
                )
                printable.append(curses_line)
                colno += len(part)
                color = 0
                style = 0
    return tuple(printable)
