"""Constants with default values used throughout the tests."""

from enum import Enum
from pathlib import Path
from typing import Any

from ansible_navigator.utils.functions import expand_path


FIXTURES_DIR = expand_path(Path(__file__).parent / "fixtures")
FIXTURES_COLLECTION_DIR = expand_path(Path(__file__).parent / "fixtures" / "common" / "collections")
FIXTURES_COLLECTION_PATH = FIXTURES_COLLECTION_DIR


class BaseScenario:
    """Used as container for test data."""

    name: str


def id_func(param: Any) -> str:
    """Generate id for tests.

    :param param: the parametrized data
    :return: Returns a string.
    """
    result = ""
    auto_id_counter = 0
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
        result = str(auto_id_counter)
        auto_id_counter += 1
    result = result.lower().replace(" ", "-")
    return result
