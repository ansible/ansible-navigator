"""Utilities related to the merging of dictionaries."""

from __future__ import annotations

from typing import Any


class DictMergeError(Exception):
    """Custom exception for a dict merge error."""


Mergeable = bool | dict[Any, Any] | list[Any] | str | None


def _merge_dicts(
    left: dict[Any, Any],
    right: dict[Any, Any],
) -> dict[Any, Any]:
    """Merge right dict into left dict recursively.

    Args:
        left: Dict to be merged into.
        right: Dict to be merged from.

    Returns:
        The merged dict.
    """
    for key, value in right.items():
        if key in left:
            left[key] = in_place_list_replace(left[key], value)
        else:
            left[key] = value
    return left


def in_place_list_replace(left: Mergeable, right: Mergeable) -> Mergeable:
    """Merge right into left in place and returns merged result.

    If left is a primitive, right will be used
    If left key is a list or tuple right will be used.
    If left and right have a common key, they will be dict merged
    If left is missing a key from right, the key from right will be added

    Args:
        left: Dict to be merged into
        right: Dict to be merged from

    Raises:
        DictMergeError: If merging cannot be done

    Returns:
        Merged dict
    """
    key = None
    try:
        if left is None or isinstance(left, (str | int | float | bool, tuple | list)):
            left = right
        elif isinstance(left, dict):
            if isinstance(right, dict):
                left = _merge_dicts(left, right)
            else:
                msg = f"Cannot merge non-dict '{right}' into dict '{left}'"
                raise DictMergeError(msg)
        else:
            msg = f"Not implemented '{right}' into '{left}'"
            raise DictMergeError(msg)
    except TypeError as exc:
        msg = f"TypeError '{exc}' in key '{key}' when merging '{right}' into '{left}'"
        raise DictMergeError(msg) from exc
    return left
