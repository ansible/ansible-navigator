"""Print pretty colors."""
from __future__ import annotations

import logging
import math
import os

from sys import stdout

from ansible_navigator.constants import GRAMMAR_DIR
from ansible_navigator.constants import THEME_PATH
from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.content_defs import ContentType
from ansible_navigator.content_defs import ContentView
from ansible_navigator.ui_framework.colorize import Colorize
from ansible_navigator.ui_framework.colorize import rgb_to_ansi
from ansible_navigator.ui_framework.curses_defs import SimpleLinePart
from ansible_navigator.utils.serialize import serialize


logger = logging.getLogger(__name__)


def color_bits() -> int:
    """Determine to number of color bit the terminal can support.

    :returns: The number of color bits
    """
    color_term = os.environ.get("COLORTERM", "").strip().lower()
    if color_term in ("truecolor", "24bit"):
        return 24
    term = os.environ.get("TERM", "").strip().lower()
    _term_name, _hyphen, colors = term.rpartition("-")
    colors = colors.replace("color", "")
    try:
        return int(math.log2(int(colors)))
    except (ValueError, TypeError):
        return 4


def color_lines(term_color_bits, tokenized) -> str:
    """Transform tokenized lines to ANSI lines.

    :param term_color_bits: The number of color bits the terminal supports
    :param tokenized: The tokenized content
    :returns: The ANSI string
    """
    lines = []
    for line in tokenized:
        printable = ""
        for line_part in line:
            color = line_part.color
            if color is not None:
                red, green, blue = color
            if term_color_bits == 24:
                if color is None:
                    ansi_code = "\033[38;2;255;255;255m"
                else:
                    ansi_code = f"\033[38;2;{red};{green};{blue}m"
            else:
                if color is None:
                    ansi_color = 1
                else:
                    number_of_colors = 2**term_color_bits
                    ansi_color = rgb_to_ansi(red, green, blue, number_of_colors)
                ansi_code = f"\033[38;5;{ansi_color}m"
            printable += f"{ansi_code}{line_part.chars}\033[1m"
        lines.append(printable)
    return "".join(lines)


def tokenize(
    content_format: ContentFormat,
    serialized: str,
) -> list[list[SimpleLinePart]]:
    """Serialize and tokenize an object.

    :param content_format: The format type
    :param serialized: The serialized content
    :returns: A list of list of line parts
    """
    colorizer = Colorize(
        grammar_dir=GRAMMAR_DIR,
        theme_path=THEME_PATH,
    )

    tokenized = colorizer.render(doc=serialized, scope=content_format.value.scope)
    return tokenized


def print_to_stdout(
    content: ContentType,
    content_format: ContentFormat,
    use_color: bool,
) -> None:
    """Print some colored output to stdout.

    :param content: The content to print out.
    :param content_format: The content_format
    :param use_color: Indicates if color should be used
    """
    serialization_format = content_format.value.serialization
    if serialization_format:
        serialized = serialize(
            content=content,
            content_view=ContentView.NORMAL,
            serialization_format=serialization_format,
        )
        output = serialized
    else:
        output = str(content)

    if use_color and not stdout.isatty():
        logger.debug("Color requested, but device is not a TTY")
        use_color = False

    if use_color:
        tokenized = tokenize(
            content_format=content_format,
            serialized=output,
        )
        terminal_color_bits = color_bits()
        output = color_lines(terminal_color_bits, tokenized)

    print(output)
