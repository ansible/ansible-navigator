"""Utilities related to the merging of dictionaries."""
from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional
from typing import Union


class DictMergeError(Exception):
    """Custom exception for a dict merge error."""


Mergeable = Optional[
    Union[
        bool,
        Dict,
        List,
        str,
    ]
]


def in_place_list_replace(left: Mergeable, right: Mergeable):
    """Merge right into left in place and returns merged result.

    If left is a primitive, right will be used
    If left key is a list or tuple right will be used.
    If left and right have a common key, they will be dict merged
    If left is missing a key from right, the key from right will be added

    :param left: Dict to be merged into
    :param right: Dict to be merged from
    :raises DictMergeError: If merging cannot be done
    :return: Merged dict
    """
    key = None
    try:
        if left is None or isinstance(left, (str, int, float, bool)):
            # Border case for first run or if a is a primitive
            left = right
        elif isinstance(left, (tuple, list)):
            left = right
        elif isinstance(left, dict):
            if isinstance(right, dict):
                for key in right:
                    if key in left:
                        left[key] = in_place_list_replace(left[key], right[key])
                    else:
                        left[key] = right[key]
            else:
                raise DictMergeError(f"Cannot merge non-dict '{right}' into dict '{left}'")
        else:
            raise DictMergeError(f"Not implemented '{right}' into '{left}'")
    except TypeError as exc:
        raise DictMergeError(
            f"TypeError '{exc}' in key '{key}' when merging '{right}' into '{left}'",
        ) from exc
    return left
