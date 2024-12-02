"""Conditional imports related to python versions."""

import importlib.metadata as importlib_metadata
import sys


# https://mypy.readthedocs.io/en/stable/common_issues.html#variables-vs-type-aliases
from typing import TypeAlias


if sys.version_info < (3, 11):
    from importlib.abc import Traversable
else:
    from importlib.resources.abc import Traversable


__all__ = ["Traversable", "TypeAlias", "importlib_metadata"]
