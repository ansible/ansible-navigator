"""Conditional imports related to python versions."""

# pylint: disable=unused-import

import sys

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    # https://mypy.readthedocs.io/en/stable/common_issues.html#variables-vs-type-aliases
    from typing import TypeAlias


import importlib.metadata as importlib_metadata


if sys.version_info < (3, 11):
    from importlib.abc import Traversable
else:
    from importlib.resources.abc import Traversable
