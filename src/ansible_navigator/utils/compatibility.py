"""Conditional imports related to python versions."""

# pylint: disable=unused-import

import sys

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    # https://mypy.readthedocs.io/en/stable/common_issues.html#variables-vs-type-aliases
    if sys.version_info >= (3, 10):
        from typing import TypeAlias
    else:
        from typing_extensions import TypeAlias


if sys.version_info < (3, 9):
    from backports import zoneinfo
else:
    import zoneinfo


if sys.version_info < (3, 9):
    import importlib_resources

    from importlib_resources.abc import Traversable
else:
    import importlib.resources as importlib_resources

    from importlib.abc import Traversable


if sys.version_info < (3, 10):
    from importlib_metadata import packages_distributions
else:
    from importlib.metadata import packages_distributions
