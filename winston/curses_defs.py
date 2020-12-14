""" commonly used defs
"""

from typing import NamedTuple
from typing import Tuple


class CursesLinePart(NamedTuple):
    """One chuck of a line of text"""

    column: int
    string: str
    color: int
    decoration: int


CursesLine = Tuple[CursesLinePart, ...]
CursesLines = Tuple[CursesLine, ...]
