"""Object definitions related to utils."""

from __future__ import annotations

import logging
import textwrap

from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import NamedTuple


GOLDEN_RATIO = 1.61803398875


class Color:
    """Color constants."""

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GREY = "\033[90m"  # Bright black?
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    END = "\033[0m"


class Decoration:
    """Decoration constants."""

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    REVERSED = "\033[7m"
    END = "\033[0m"


class ExitPrefix(Enum):
    """An exit message prefix."""

    ERROR = "Error"
    HINT = "Hint"
    NOTE = "Note"
    WARNING = "Warning"

    @classmethod
    def _longest_name(cls):
        """Return the longest exit message prefix.

        :returns: The longest exit message prefix
        """
        return max(len(member.value) for member in cls)

    @classmethod
    def longest_formatted(cls):
        """Return the longest exit message prefix.

        :returns: The longest exit message prefix
        """
        return max(len(str(member)) for member in cls)

    def __str__(self):
        """Return the exit message prefix as a string.

        :returns: The exit message prefix as a string
        """
        return f"{' ' * (self._longest_name() - len(self.name))}{self.name.capitalize()}: "


@dataclass
class ExitMessage:
    """An object to hold a message to present when exiting."""

    #: The message that will be presented
    message: str
    #: The prefix for the message, used for formatting
    prefix: ExitPrefix = ExitPrefix.ERROR

    @property
    def color(self):
        """Return a color for the prefix.

        :returns: The color for the prefix
        """
        color_mapping = {
            ExitPrefix.ERROR: Color.RED,
            ExitPrefix.HINT: Color.CYAN,
            ExitPrefix.NOTE: Color.GREEN,
            ExitPrefix.WARNING: Color.YELLOW,
        }
        return color_mapping[self.prefix]

    @property
    def level(self):
        """Return a log level.

        :returns: The log level
        """
        mapping = {
            ExitPrefix.ERROR: logging.ERROR,
            ExitPrefix.HINT: logging.INFO,
            ExitPrefix.NOTE: logging.INFO,
            ExitPrefix.WARNING: logging.WARNING,
        }
        return mapping[self.prefix]

    def to_lines(self, color: bool, width: int, with_prefix: bool) -> list[str]:
        """Output exit message to the console.

        :param color: Whether to color the message
        :param width: Constrain message to width
        :param with_prefix: Whether to prefix the message
        :returns: The exit message as a string
        """
        prefix_length = ExitPrefix.longest_formatted()
        indent = " " * prefix_length

        message = textwrap.fill(
            self.message,
            width=width,
            break_on_hyphens=False,
            initial_indent=str(self.prefix) if with_prefix else indent,
            subsequent_indent=indent,
        )
        lines = message.splitlines()

        start_color = self.color if color else ""
        end_color = Color.END if color else ""

        printable = [f"{start_color}{line}{end_color}" for line in lines]
        return printable


@dataclass
class ExitMessages:
    """A mechanism to store multiple exit messages."""

    messages: list[ExitMessage] = field(default_factory=list)

    def to_strings(self, color: bool, width: int) -> list[str]:
        """Output exit messages to the console.

        :param color: Whether to color the message
        :param width: Constrain messages to width
        :returns: The exit messages as a list of strings
        """
        printable = []
        new_section = True
        for idx, message in enumerate(self.messages):
            # Print the prefix if the next is different or a new section
            if new_section:
                # Use prefix, starting a new section
                with_prefix = True
            else:
                try:
                    # Prefix if previous is different
                    with_prefix = self.messages[idx - 1].prefix != message.prefix
                except IndexError:
                    # Last message
                    with_prefix = True
            printable.extend(message.to_lines(color=color, with_prefix=with_prefix, width=width))

            try:
                next_prefix = self.messages[idx + 1].prefix

                # Never break before a hint
                if next_prefix is ExitPrefix.HINT:
                    new_section = False
                    continue

                # Keep like items together
                if message.prefix is next_prefix:
                    new_section = False
                    continue

                # Start a new section
                printable.append("")
                new_section = True

            except IndexError:
                pass

        return printable


class LogMessage(NamedTuple):
    """An object to hold a message destined for the logger."""

    level: int
    message: str
