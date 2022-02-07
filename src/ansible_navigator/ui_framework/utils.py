"""some UI specific utils
"""
import functools
import re

from math import floor
from typing import List


def convert_percentage(data_dict: dict, keys: List, progress_bar_width: int) -> None:
    """convert a string % to a little progress bar
    not recursive
    80% = 80%|XXXXXXXX  |

    :param data_dict: The dictionary to update
    :param keys: The keys to convert in each dictionary
    :param progress_bar_width: The width of the progress bar
    """
    for key in keys:
        value = data_dict.get(key)
        if value and is_percent(str(value)):
            if value == "100%":
                data_dict[key] = "COMPLETE".center(progress_bar_width, " ")
            else:
                chars_in_progress_bar = floor(progress_bar_width / 100 * int(value[0:-1]))
                data_dict["_" + key] = value
                data_dict[key] = ("\u2587" * chars_in_progress_bar).ljust(progress_bar_width)


@functools.lru_cache(maxsize=None)
def is_percent(string):
    """is a string a percent?"""
    if string.endswith("%"):
        if re.match(r"^\d{1,3}%$", string):
            return True
    return False


def distribute(available, weights):
    """distribute some available fairly
    across a list of numbers

    :param available: the total
    :type available: int
    :param weights: numbers
    :type weights: List[int]
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
