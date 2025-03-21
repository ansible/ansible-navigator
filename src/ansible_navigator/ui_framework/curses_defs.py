"""Commonly used definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple
from typing import NewType


class CursesLinePart(NamedTuple):
    """One chunk of a line of text.

    Args:
        column: the column at which the text should start
        string: the text to be displayed
        color: An integer representing a color, not a
            curses.color_pair(n)
        decoration: A curses decoration
    """

    column: int
    string: str
    color: int
    decoration: int


CursesLine = NewType("CursesLine", tuple[CursesLinePart, ...])
"""One line of text ready for curses."""

CursesLines = NewType("CursesLines", tuple[CursesLine, ...])
"""One or more lines of text ready for curses."""


RgbTuple = tuple[int, int, int]


@dataclass
class SimpleLinePart:
    """Definition of one part of one line having a common color."""

    #: One group of characters sharing the same color
    chars: str
    #: The column where the characters start, the sum of all previous characters in the line
    column: int
    #: The color for these characters
    color: RgbTuple | None
    #: The style for these characters
    style: str | None
