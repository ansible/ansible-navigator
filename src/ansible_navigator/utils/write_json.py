"""Utilities for writing files with specific permissions."""
from __future__ import annotations

import json
import os

from functools import partial


def opener(path: str, flags: int, mode: int) -> int:
    """Open a file with the given path and flags.

    :param path: The path of the file to open.
    :param flags: The flags to use when opening the file.
    :param mode: The mode to use when opening the file.
    :return: The file descriptor of the opened file.
    """
    return os.open(path=path, flags=flags, mode=mode)


def write_with_permissions(path: str, mode: int, content: object) -> None:
    """Write a file with the given name.

    :param content: The content we want to write in the file.
    :param mode: The mode to use when writing the file.
    :param path: The path of the file to write.
    """
    # Without this, the created file will have 0o777 - 0o022 (default umask) = 0o755 permissions
    oldmask = os.umask(0)

    opener_func = partial(opener, mode=mode)
    with open(path, "w", encoding="utf-8", opener=opener_func) as f:
        f.write(json.dumps(content, indent=4, sort_keys=True))
    os.umask(oldmask)
