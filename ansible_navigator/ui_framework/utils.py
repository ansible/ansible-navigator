""" some ui specific utils
"""
import functools
import re
from math import floor

from typing import List


def convert_percentage(dyct: dict, keys: List, pbar_width: int) -> None:
    """convert a string % to a little progress bar
    not recursive
    80% = 80%|XXXXXXXX  |

    :pararm dicts: a list fo dictionaries
    :type dicts: list of dictionaries
    :param keys: The keys to convert in each dictionary
    :type keys: list of str
    :param pbar_width: The width of the progress bar
    :type pbar_width: int
    """
    for key in keys:
        value = dyct.get(key)
        if value and is_percent(str(value)):
            if value == "100%":
                dyct[key] = "COMPLETE".center(pbar_width, " ")
            else:
                numx = floor(pbar_width / 100 * int(value[0:-1]))
                dyct["_" + key] = value
                dyct[key] = ("\u2587" * numx).ljust(pbar_width)


@functools.lru_cache(maxsize=None)
def is_percent(string):
    """is a string a percent?"""
    if string.endswith("%"):
        if re.match(r"^\d{1,3}%$", string):
            return True
    return False


def distribute(available, weights):
    """distrubute some available fairly
    across a list of numbers

    :param available: the total
    :type available: int
    :param weights: numbers
    :type weights: list of int
    """
    total = sum(weights)
    if available < total:
        while available != total:
            maxv = max(weights)
            maxvs = [i for i, j in enumerate(weights) if j == maxv]
            for idx in maxvs:
                weights[idx] -= 1
                if sum(weights) == available:
                    return weights

    distributed_amounts = []
    total_weights = sum(weights)
    for weight in weights:
        weight = float(weight)
        pcent = weight / total_weights
        distributed_amount = round(pcent * available)
        distributed_amounts.append(distributed_amount)
        total_weights -= weight
        available -= distributed_amount
    return distributed_amounts
