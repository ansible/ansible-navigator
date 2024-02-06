"""Constants with default values used throughout the tests."""

import os

from enum import Enum
from pathlib import Path
from typing import Any


FIXTURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "fixtures"))
FIXTURES_COLLECTION_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "fixtures", "common", "collections"),
)
FIXTURES_COLLECTION_PATH = Path(FIXTURES_COLLECTION_DIR)


class BaseScenario:
    """Used as container for test data."""

    name: str


_AUTO_ID_COUNTER = 0


def id_func(param: Any) -> str:
    """Generate id for tests.

    :param param: the parametrized data
    :return: Returns a string.
    """
    result = ""
    global _AUTO_ID_COUNTER
    if isinstance(param, str):
        result = param
    elif hasattr(param, "value") and isinstance(param.value, str):  # covers for Enums too
        result = str(param.value)
    elif isinstance(param, BaseScenario):
        if hasattr(param, "name"):
            result = param.name
        elif hasattr(param, "comment"):
            result = param.comment
    elif isinstance(param, tuple):
        if hasattr(param, "name"):
            result = param.name
        else:
            args = []
            for _, part in enumerate(param):
                if isinstance(part, Enum):
                    args.append(str(part.value))
                else:
                    args.append(str(part))
            result = "-".join(args)
    else:
        result = str(_AUTO_ID_COUNTER)
        _AUTO_ID_COUNTER += 1
    result = result.lower().replace(" ", "-")
    return result
