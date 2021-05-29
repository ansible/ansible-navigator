""" commonly used defs
"""

from typing import NamedTuple
from typing import Tuple


class CursesLinePart(NamedTuple):
    # pylint: disable=inherit-non-class
    # pylint: disable=too-few-public-methods
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


CursesLine = Tuple[CursesLinePart, ...]
CursesLines = Tuple[CursesLine, ...]
