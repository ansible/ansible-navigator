# cspell:ignore A_INVIS
"""Tokenize and color text."""

import colorsys
import curses
import functools
import json
import logging
import os
import re

from itertools import chain
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from ..tm_tokenize.grammars import Grammars
from ..tm_tokenize.region import Regions
from ..tm_tokenize.tokenize import tokenize
from .curses_defs import CursesLine
from .curses_defs import CursesLinePart
from .curses_defs import CursesLines
from .curses_defs import RgbTuple
from .curses_defs import SimpleLinePart


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
    """A storage mechanism for the schema (theme)."""

    def __init__(self, schema: Dict[str, Union[str, List, Dict]]):
        """Initialize the ColorSchema class.

        :param schema: The color scheme, theme to use
        """
        self._logger = logging.getLogger(__name__)
        self._schema = schema

    @functools.lru_cache(maxsize=None)
    def get_color(self, scope: str) -> Optional[RgbTuple]:
        """Get a color from the schema, from most specific to least.

        :param scope: The scope, aka format
        :returns: The color in RGB format or nothing
        """
        for name in reversed(scope):
            for parts in range(0, len(name.split("."))):
                prop = name.split()[-1].rsplit(".", parts)[0]
                color = next(
                    (
                        token_color
                        for token_color in self._schema["tokenColors"]
                        if (
                            isinstance(token_color, dict)
                            and prop in scope_to_list(token_color.get("scope", []))
                        )
                    ),
                    None,
                )
                if color:
                    foreground = color.get("settings", {}).get("foreground", None)
                    # Without decoration support, continue resolving to a until we find a
                    # foreground color or ultimately return None. This currently completely
                    # ignores font styles.
                    # e.g. color={'scope': 'strong', 'settings': {'fontStyle': 'bold'}}
                    if foreground is not None:
                        return hex_to_rgb(foreground)
                    self._logger.debug("Color resolution continued: %s", color)
        return None


class Colorize:
    """Functionality for coloring."""

    def __init__(self, grammar_dir: str, theme_path: str):
        """Initialize the colorizer.

        :param grammar_dir: The directory in which the grammars reside
        :param theme_path: The path to the currently configured color theme
        """
        self._logger = logging.getLogger(__name__)
        self._schema: ColorSchema
        self._grammars = Grammars(grammar_dir)
        self._theme_path = theme_path
        self._load()

    def _load(self):
        """Load the color scheme from the file system."""
        with open(os.path.join(self._theme_path), encoding="utf-8") as fh:
            self._schema = ColorSchema(json.load(fh))

    @staticmethod
    @functools.lru_cache(maxsize=100)
    def render_ansi(doc: str) -> CursesLines:
        """Convert ansi colored text into curses lines.

        :param doc: The text to convert
        :returns: Lines ready to present using the TUI
        """
        lines = tuple(ansi_to_curses(line) for line in doc.splitlines())
        return CursesLines(lines)

    @functools.lru_cache(maxsize=100)
    def render(self, doc: str, scope: str) -> List[List[SimpleLinePart]]:
        """Render text lines into lines of columns and colors.

        :param doc: The string to split, tokenize and color
        :param scope: The scope, aka the format of the string
        :returns: A list of lines, each a list of dicts
        """
        try:
            compiler = self._grammars.compiler_for_scope(scope)
        except KeyError:
            compiler = None

        if compiler and scope != "no_color":
            state = compiler.root_state
            lines = []
            for line_idx, line in enumerate(doc.splitlines()):
                line += "\n"
                first_line = line_idx == 0
                try:
                    state, regions = tokenize(compiler, state, line, first_line)
                except Exception as exc:  # pylint: disable=broad-except
                    self._logger.critical(
                        (
                            "An unexpected error occurred within the tokenization"
                            " subsystem.  Please log an issue with the following:"
                        ),
                    )
                    self._logger.critical(
                        "  Err: '%s', Scope: '%s', Line follows....",
                        str(exc),
                        scope,
                    )
                    self._logger.critical("  '%s'", line)
                    self._logger.critical("  The current content will be rendered without color")
                    break
                else:
                    lines.append((regions, line))
            else:
                return columns_and_colors(lines, self._schema)

        res = [
            [SimpleLinePart(column=0, chars=doc_line, color=None)] for doc_line in doc.splitlines()
        ]
        return res


def scope_to_list(scope: Union[str, List]) -> List:
    """Convert a token scope to a list if necessary.

    A scope in a theme should always be a string or list,
    but just in case return an empty list if not

    :param scope: The scope
    :returns: Scope as list
    """
    if isinstance(scope, list):
        return scope
    if isinstance(scope, str):
        return [scope]
    return []


def hex_to_rgb(value: str) -> RgbTuple:
    """Convert a hex value to RGB tuple.

    :param value: The hex color
    :returns: RGB tuple
    """
    value = value.lstrip("#")
    value_length = len(value)
    red, green, blue = (
        int(value[i : i + value_length // 3], 16) for i in range(0, value_length, value_length // 3)
    )
    return red, green, blue


def scale_for_curses(rgb_value: int) -> int:
    """Scale a single RGB value for curses.

    :param rgb_value: One RGB value
    :returns: The value scaled for curses
    """
    curses_ceiling = 1000
    rgb_ceiling = 255
    return int(rgb_value * curses_ceiling / rgb_ceiling)


def hex_to_rgb_curses(value: str) -> RgbTuple:
    """Convert a hex color to RGB scaled for curses.

    :param value: an RGB color
    :returns: The colors scaled to 1000
    """
    red, green, blue = hex_to_rgb(value)
    return (scale_for_curses(red), scale_for_curses(green), scale_for_curses(blue))


def rgb_to_ansi(red: int, green: int, blue: int, colors: int) -> int:
    """Convert an RGB color to an ansi color.

    :param red: The red component
    :param green: The green component
    :param blue: The blue component
    :param colors: The number of color supported by the terminal
    :returns: A color suitable for the terminal
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


def columns_and_colors(
    lines: List[Tuple[Regions, str]],
    schema: ColorSchema,
) -> List[List[SimpleLinePart]]:
    """Convert to colors and columns.

    :param lines: Lines of text and their regions
    :param schema: An instance of the ColorSchema
    :returns: Lines of text, each broken into sections
    """
    results: List[List[SimpleLinePart]] = []

    for line in lines:
        # Break the into 1 character parts, temporarily set the column to 0
        line_parts = [
            SimpleLinePart(chars=character, color=None, column=0) for character in line[1]
        ]

        # Replace the color with the RgbTuple
        for region in line[0]:
            color = schema.get_color(region.scope)
            if color:
                for idx in range(region.start, region.end):
                    line_parts[idx].color = color

        # Compress the line, grouping characters of like color
        if line_parts:
            grouped = [line_parts.pop(0)]
            while line_parts:
                entry = line_parts.pop(0)
                if entry.color == grouped[-1].color:
                    grouped[-1].chars += entry.chars
                else:
                    grouped.append(entry)
            results.append(grouped)
        else:
            results.append([SimpleLinePart(chars=line[1], color=None, column=0)])

    # Update the column in each line part, based on the total of the preceding text lengths
    for result in results:
        column = 0
        for line_part in result:
            line_part.column = column
            column += len(line_part.chars)

    return results


def ansi_to_curses(line: str) -> CursesLine:
    """Convert ansible color codes to curses colors.

    :param line: A string with ansi colors
    :returns: A line ready for presentation in the TUI
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
        """,
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
                    column=colno,
                    string=part,
                    color=color,
                    decoration=style,
                )
                printable.append(curses_line)
                colno += len(part)
                color = 0
                style = 0
    return CursesLine(tuple(printable))
