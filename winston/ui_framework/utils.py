""" some ui specific utils
"""
import re
from math import floor

from typing import List


def convert_percentages(dicts: List, keys: List, pbar_width: int) -> List:
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
    for idx, entry in enumerate(dicts):
        for key in [k for k in entry.keys() if k in keys]:
            value = entry[key]
            if re.match(r"^\d{1,3}%$", str(value)):
                numx = floor(pbar_width / 100 * int(value[0:-1]))
                entry["_" + key] = value
                entry[key] = "{value} {numx}".format(
                    value=value.rjust(4), numx=("\u2587" * numx).ljust(pbar_width)
                )
        dicts[idx] = entry
    return dicts


def distribute(available, weights):
    """distrubute some available fairly
    across a list of numbers

    :param available: the total
    :type available: int
    :param weights: numbers
    :type weights: list of int
    """
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


def sacrifice(available, weights):
    """if available > total
    reduce last until it match next biggest
    """
    total = sum(weights)
    if available < total:
        second_largest = max(weights[0:-1])
        sum_but_last = sum(weights[0:-1])
        if sum_but_last > available:
            weights[-1] = second_largest
        else:
            weights[-1] = available - sum_but_last
    return distribute(available, weights)
