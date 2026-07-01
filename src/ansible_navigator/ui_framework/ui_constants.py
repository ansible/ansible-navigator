"""Constants for use with the user interface."""

from __future__ import annotations

import curses

from enum import IntEnum


class Color(IntEnum):
    """Constants for the 16 basic ANSI colors.

    Attributes:
        BLACK: Color index 0.
        RED: Color index 1.
        GREEN: Color index 2.
        YELLOW: Color index 3.
        BLUE: Color index 4.
        MAGENTA: Color index 5.
        CYAN: Color index 6.
        WHITE: Color index 7.
        GREY: Color index 8.
        BRIGHT_RED: Color index 9.
        BRIGHT_GREEN: Color index 10.
        BRIGHT_YELLOW: Color index 11.
        BRIGHT_BLUE: Color index 12.
        BRIGHT_MAGENTA: Color index 13.
        BRIGHT_CYAN: Color index 14.
        BRIGHT_WHITE: Color index 15.
    """

    BLACK = curses.COLOR_BLACK
    RED = curses.COLOR_RED
    GREEN = curses.COLOR_GREEN
    YELLOW = curses.COLOR_YELLOW
    BLUE = curses.COLOR_BLUE
    MAGENTA = curses.COLOR_MAGENTA
    CYAN = curses.COLOR_CYAN
    WHITE = curses.COLOR_WHITE
    GREY = BLACK + 8
    BRIGHT_RED = RED + 8
    BRIGHT_GREEN = GREEN + 8
    BRIGHT_YELLOW = YELLOW + 8
    BRIGHT_BLUE = BLUE + 8
    BRIGHT_MAGENTA = MAGENTA + 8
    BRIGHT_CYAN = CYAN + 8
    BRIGHT_WHITE = WHITE + 8


class Decoration(IntEnum):
    """Constants for text decoration.

    These are rarely used within the interface.

    Attributes:
        BOLD: Bold text attribute.
        ITALIC: Italic text attribute.
        NORMAL: Normal text attribute.
        UNDERLINE: Underline text attribute.
    """

    BOLD = curses.A_BOLD
    # Fix for missing curses.A_ITALIC on macOS
    ITALIC = getattr(curses, "A_ITALIC", curses.A_BOLD)
    NORMAL = curses.A_NORMAL
    UNDERLINE = curses.A_UNDERLINE

    @classmethod
    def get_best(cls, name: str | None) -> int:
        """Return the default value for a missing value.

        Args:
            name: The name of the value

        Returns:
            The match or default value
        """
        if isinstance(name, str):
            try:
                return cls[name.upper()]
            except KeyError:
                return cls.NORMAL
        return cls.NORMAL
