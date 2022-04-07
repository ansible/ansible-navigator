"""ANSI color codes and functions for terminal output."""
import os
import sys

from sys import stdout

from .definitions import Color


IS_TTY = stdout.isatty()
COLOR = "NO_COLOR" not in os.environ and IS_TTY


def changed(color: bool, message: str):
    """Output changed information to the console.

    :param color: Whether to color the message
    :param message: The message to output
    """
    if color:
        print(f"\r{Color.YELLOW}{message}{Color.END}\033[K")
    else:
        print(message)


def failed(color: bool, message: str):
    """Output failure information to the console.

    :param color: Whether to color the message
    :param message: The message to output
    """
    if color:
        print(f"\r{Color.RED}{message}{Color.END}\033[K")
    else:
        print(message)


def info(color: bool, message: str):
    """Output info information to the console.

    :param color: Whether to color the message
    :param message: The message to output
    """
    if color:
        print(f"{Color.CYAN}{message}{Color.END}")
    else:
        print(message)


def subtle(color: bool, message: str):
    """Output subtle information to the console.

    :param color: Whether to color the message
    :param message: The message to output
    """
    if color:
        print(f"{Color.GREY}{message}{Color.END}")
    else:
        print(message)


def prompt_enter():
    """Output prompt information to the console."""
    try:
        input("Press Enter to continue: ")
    except KeyboardInterrupt:
        sys.exit(0)


def prompt_yn(message: str) -> bool:
    """Output prompt information to the console.

    :param message: The message to output
    :return: Whether the user answered yes
    """
    try:
        reply = None
        while reply not in ("", "y", "n"):
            reply = input(f"{message} (Y/n): ").lower()
        return reply in ("", "y")
    except KeyboardInterrupt:
        sys.exit(0)


def success(color: bool, message: str):
    """Output success information to the console.

    :param color: Whether to color the message
    :param message: The message to output
    """
    if color:
        print(f"\r{Color.GREEN}{message}{Color.END}\033[K")
    else:
        print(message)


def warning(color: bool, message: str):
    """Output warning information to the console.

    :param color: Whether to color the message
    :param message: The message to output
    """
    if color:
        print(f"{Color.YELLOW}{message}{Color.END}")
    else:
        print(message)


def working(color: bool, message: str):
    """Output working information to the console.

    :param color: Whether to color the message
    :param message: The message to output
    """
    if color:
        print(f"{Color.GREY}{message}{Color.END}", end="", flush=True)
    else:
        print(message)


def blank_line():
    """Output a blank line to the console."""
    print()
