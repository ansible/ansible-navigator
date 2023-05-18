"""Utilities for working with dictionaries using paths."""
from __future__ import annotations

import copy
import operator

from collections.abc import MutableMapping
from enum import Enum
from functools import reduce


class MergeBehaviors(Enum):
    """The merge behaviors."""

    LIST_LIST_EXTEND = "append list to list"
    LIST_LIST_REPLACE = "replace list with list"
    LIST_APPEND = "append to list"
    LIST_REPLACE = "replace list"
    LIST_SORT = "sort resulting list"
    LIST_UNIQUE = "only unique values in resulting list"
    DICT_DICT_UPDATE = "update left dict with right dict"
    DICT_DICT_REPLACE = "replace left dict with right dict"


def get_with_path(content: MutableMapping, path: str):
    """Get a value from a path in a dictionary.

    :param content: The content of the settings file
    :param path: The path to the value
    :return: The value at the path
    """
    return reduce(operator.getitem, path.split("."), content)


def check_path(content: MutableMapping, path: str):
    """Check if a path exists in a dictionary.

    :param content: The content of the settings file
    :param path: The path to the value
    :return: Whether the path exists
    """
    try:
        get_with_path(content, path)
        return True
    except (KeyError, TypeError):
        return False


def delete_with_path(content: MutableMapping, path: str):
    """Delete a value from a path in a dictionary.

    :param content: The content of the settings file
    :param path: The path to the value
    """
    parts = path.split(".")
    del reduce(operator.getitem, parts[:-1], content)[parts[-1]]


def ascendants_from_path(path: str):
    """Get the ascendants of a path.

    :param path: The path to the value
    :return: The ascendants of the path
    """
    parts = path.split(".")
    return [path.rsplit(".", i)[0] for i in range(len(parts))]


def descendants_to_path(path: str):
    """Get the descendants to a path.

    :param path: The path to the value
    :return: The descendants to the path
    """
    parts = path.split(".")
    return [path.rsplit(".", i)[0] for i in reversed(range(len(parts)))]


def remove_and_delete_empty_ascendants(content: MutableMapping, path: str):
    """Remove and delete empty ascendants.

    :param content: The content of the settings file
    :param path: The path to the value
    """
    ascendants = ascendants_from_path(path)
    delete_with_path(content, ascendants.pop(0))
    while ascendants:
        ascendant = ascendants.pop(0)
        branch_value = get_with_path(content, ascendant)
        if branch_value == {}:
            delete_with_path(content, ascendant)
        else:
            break


def place_at_path(
    behaviors: tuple[MergeBehaviors, ...],
    content: dict,
    path: str,
    value: bool | int | list | float | str | list | dict,
) -> dict:
    """Place a value at a path in a dictionary.

    :param behaviors: The merge behaviors
    :param content: The content of the settings file
    :param path: The path to the value
    :param value: The value to place
    :raises ValueError: If something can't be done
    :return: The updated content
    """
    if (
        MergeBehaviors.DICT_DICT_REPLACE in behaviors
        and MergeBehaviors.DICT_DICT_UPDATE in behaviors
    ):
        msg = "Can't use both DICT_DICT_REPLACE and DICT_DICT_UPDATE behaviors"
        raise ValueError(msg)
    if (
        MergeBehaviors.LIST_LIST_EXTEND in behaviors
        and MergeBehaviors.LIST_LIST_REPLACE in behaviors
    ):
        msg = "Can't use both LIST_LIST_EXTEND and LIST_LIST_REPLACE behaviors"
        raise ValueError(msg)

    copied_content = copy.deepcopy(content)
    nested = copied_content
    if path in ("", None):
        if isinstance(value, dict):
            if MergeBehaviors.DICT_DICT_REPLACE in behaviors:
                return value
            if MergeBehaviors.DICT_DICT_UPDATE in behaviors:
                return {**nested, **value}
        msg = "Cannot place non dict at root of dict"
        raise ValueError(msg)

    for part in path.split("."):
        if part == path.rsplit(".", maxsplit=1)[-1]:
            if isinstance(nested.get(part), list):
                if isinstance(value, list):
                    if MergeBehaviors.LIST_LIST_EXTEND in behaviors:
                        nested[part].extend(value)
                    elif MergeBehaviors.LIST_LIST_REPLACE in behaviors:
                        nested[part] = value
                    else:
                        msg = "No behavior specified for LIST_LIST"
                        raise ValueError(msg)
                else:
                    if MergeBehaviors.LIST_APPEND in behaviors:
                        nested[part].append(value)
                    elif MergeBehaviors.LIST_REPLACE in behaviors:
                        nested[part] = value
                        continue
                    else:
                        msg = "No behavior specified for LIST_*"
                        raise ValueError(msg)

                if MergeBehaviors.LIST_UNIQUE in behaviors:
                    nested[part] = list(dict.fromkeys(nested[part]))
                if MergeBehaviors.LIST_SORT in behaviors:
                    nested[part].sort()
                continue

            if isinstance(nested.get(part), dict) and isinstance(value, dict):
                if MergeBehaviors.DICT_DICT_UPDATE in behaviors:
                    nested[part].update(value)
                elif MergeBehaviors.DICT_DICT_REPLACE in behaviors:
                    nested[part] = value
                else:
                    msg = "No behavior specified for DICT_DICT"
                    raise ValueError(msg)
                continue

            nested[part] = value
        elif part not in nested:
            nested[part] = {}
        nested = nested[part]
    return copied_content


def move_to_path(
    behaviors: tuple[MergeBehaviors, ...],
    content: dict,
    new_path: str,
    old_path: str,
) -> dict:
    """Move a value to a path in a dictionary.

    :param behaviors: The merge behaviors
    :param content: The content of the settings file
    :param old_path: The path to the value
    :param new_path: The path to the value
    :return: The updated content
    """
    copied_content = copy.deepcopy(content)
    if new_path == old_path:
        return copied_content

    value = get_with_path(content=copied_content, path=old_path)
    delete_with_path(content=copied_content, path=old_path)
    updated_content = place_at_path(
        content=copied_content,
        path=new_path,
        value=value,
        behaviors=behaviors,
    )
    return updated_content
