"""ANSI color codes and functions for terminal output."""

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
