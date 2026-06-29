"""Conditional imports related to python versions."""

import importlib.metadata as importlib_metadata

from importlib.resources.abc import Traversable

# https://mypy.readthedocs.io/en/stable/common_issues.html#variables-vs-type-aliases
from typing import TypeAlias


__all__ = ["Traversable", "TypeAlias", "importlib_metadata"]
