"""commonly used definitions
"""

from dataclasses import dataclass
from typing import NamedTuple
from typing import NewType
from typing import Optional
from typing import Tuple


class CursesLinePart(NamedTuple):
    """One chunk of a line of text

    :param column: the column at which the text should start
    :param string: the text to be displayed
    :param color: An integer representing a color, not a curses.color_pair(n)
    :param decoration: A curses decoration
    """

    column: int
    string: str
    color: int
    decoration: int


CursesLine = NewType("CursesLine", Tuple[CursesLinePart, ...])
"""One line of text ready for curses."""

CursesLines = NewType("CursesLines", Tuple[CursesLine, ...])
"""One or more lines of text ready for curses."""


RgbTuple = Tuple[int, int, int]


@dataclass
class SimpleLinePart:
    """Definition of one part of one line having a common color."""

    #: One group of characters sharing the same color
    chars: str
    #: The column where the characters start, the sum of all previous characters in the line
    column: int
    #: The color for these characters
    color: Optional[RgbTuple]
