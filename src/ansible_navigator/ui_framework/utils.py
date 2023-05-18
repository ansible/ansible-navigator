"""Some UI specific utils."""
from __future__ import annotations

import functools
import re

from dataclasses import is_dataclass
from math import floor
from typing import Any

from ansible_navigator.content_defs import ContentBase


def convert_percentage(
    content: dict[str, Any] | ContentBase,
    columns: list[str],
    progress_bar_width: int,
) -> None:
    """Convert an attribute or value to a progress bar formatted for the TUI in place.

    :param content: The content for which the progress bar will be generated
    :param columns: The menu columns, only make progress bars for columns
    :param progress_bar_width: The target width of the progress bar
    """
    for column in columns:
        value = content.get(column)
        if value and is_percent(str(value)):
            new_value = _string_to_progress(value, progress_bar_width)
            if isinstance(content, dict):
                content["_" + column] = value
                content[column] = new_value
            elif is_dataclass(content):
                setattr(content, f"_{column}", value)
                setattr(content, column, new_value)


def _string_to_progress(value: str, progress_bar_width: int) -> str:
    """Convert a string to a progress bar or text string indicating complete.

    :param value: The percent string
    :param progress_bar_width: The target width of the progress bar
    :returns: The resulting progress bar or text string
    """
    if value == "100%":
        return "Complete".center(progress_bar_width, " ")
    chars_in_progress_bar = floor(progress_bar_width / 100 * int(value[0:-1]))
    return ("\u2587" * chars_in_progress_bar).ljust(progress_bar_width)


@functools.cache
def is_percent(string):
    """Determine if a string is a percentage.

    :param string: The string to check
    :returns: Boolean of comparison
    """
    if string.endswith("%") and re.match(r"^\d{1,3}%$", string):
        return True
    return False


def distribute(available, weights):
    """Distribute some available fairly across a list of numbers.

    :param available: the total
    :type available: int
    :param weights: numbers
    :type weights: List[int]
    :returns: List of distributed amounts available
    """
    total = sum(weights)
    if available < total:
        while available != total:
            max_value = max(weights)
            max_values = [i for i, j in enumerate(weights) if j == max_value]
            for idx in max_values:
                weights[idx] -= 1
                if sum(weights) == available:
                    return weights

    distributed_amounts = []
    total_weights = sum(weights)
    for weight in weights:
        weight = float(weight)
        percent_of_total = weight / total_weights
        distributed_amount = round(percent_of_total * available)
        distributed_amounts.append(distributed_amount)
        total_weights -= weight
        available -= distributed_amount
    return distributed_amounts
