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


def _id_from_scenario(param: BaseScenario) -> str:
    """Generate id from a BaseScenario instance.

    Args:
        param: A BaseScenario instance

    Returns:
        The id string
    """
    if hasattr(param, "name"):
        return param.name
    if hasattr(param, "comment"):
        return param.comment
    return ""


def _id_from_tuple(param: tuple[Any, ...]) -> str:
    """Generate id from a tuple.

    Args:
        param: A tuple of values

    Returns:
        The id string
    """
    if hasattr(param, "name"):
        return param.name
    args = [str(part.value) if isinstance(part, Enum) else str(part) for part in param]
    return "-".join(args)


def id_func(param: Any) -> str:
    """Generate id for tests.

    Args:
        param: the parametrized data

    Returns:
        Returns a string.
    """
    if isinstance(param, str):
        result = param
    elif hasattr(param, "value") and isinstance(param.value, str):
        result = str(param.value)
    elif isinstance(param, BaseScenario):
        result = _id_from_scenario(param)
    elif isinstance(param, tuple):
        result = _id_from_tuple(param)
    else:
        result = "0"
    return result.lower().replace(" ", "-")
