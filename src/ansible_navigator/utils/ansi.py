"""ANSI color codes and functions for terminal output."""


class Color:
    """Color constants."""

    GREY = "\033[90m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    END = "\033[0m"


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
