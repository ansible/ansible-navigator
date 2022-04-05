"""ANSI color codes and functions for terminal output."""
import os

from sys import stdout


IS_TTY = stdout.isatty()
COLOR = "NO_COLOR" not in os.environ and IS_TTY

from .definitions import Color


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


def prompt_yn(message: str):
    """Output prompt information to the console.

    :param message: The message to output
    :return: Whether the user answered yes
    """
    reply = None
    while reply not in ("", "y", "n"):
        reply = input(f"{message} (Y/n): ").lower()
    return reply in ("", "y")


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
