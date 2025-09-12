"""Conditional imports related to python versions."""

import importlib.metadata as importlib_metadata


# https://mypy.readthedocs.io/en/stable/common_issues.html#variables-vs-type-aliases
from typing import TypeAlias


try:
    from importlib.resources.abc import Traversable
except ImportError:
    # pylint: disable-next=deprecated-class
    from importlib.abc import Traversable


__all__ = ["Traversable", "TypeAlias", "importlib_metadata"]
