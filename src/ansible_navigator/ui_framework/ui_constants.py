"""Constants for use with the user interface."""
from __future__ import annotations

import curses

from enum import IntEnum


class Color(IntEnum):
    """Constants for the 16 basic ANSI colors."""

    BLACK = curses.COLOR_BLACK
    """0"""
    RED = curses.COLOR_RED
    """1"""
    GREEN = curses.COLOR_GREEN
    """2"""
    YELLOW = curses.COLOR_YELLOW
    """3"""
    BLUE = curses.COLOR_BLUE
    """4"""
    MAGENTA = curses.COLOR_MAGENTA
    """5"""
    CYAN = curses.COLOR_CYAN
    """6"""
    WHITE = curses.COLOR_WHITE
    """7"""
    GREY = BLACK + 8
    """8"""
    BRIGHT_RED = RED + 8
    """9"""
    BRIGHT_GREEN = GREEN + 8
    """10"""
    BRIGHT_YELLOW = YELLOW + 8
    """11"""
    BRIGHT_BLUE = BLUE + 8
    """12"""
    BRIGHT_MAGENTA = MAGENTA + 8
    """13"""
    BRIGHT_CYAN = CYAN + 8
    """14"""
    BRIGHT_WHITE = WHITE + 8
    """15"""


class Decoration(IntEnum):
    """Constants for text decoration.

    These are rarely used within the interface.
    """

    BOLD = curses.A_BOLD
    """2097152"""
    # Fix for missing curses.A_ITALIC on macOS
    ITALIC = getattr(curses, "A_ITALIC", curses.A_BOLD)
    """2147483648"""
    NORMAL = curses.A_NORMAL
    """0"""
    UNDERLINE = curses.A_UNDERLINE
    """131072"""

    @classmethod
    def get_best(cls, name: str | None) -> int:
        """Return the default value for a missing value.

        :param name: The name of the value
        :return: The match or default value
        """
        if isinstance(name, str):
            try:
                return cls[name.upper()]
            except KeyError:
                return cls.NORMAL
        return cls.NORMAL
