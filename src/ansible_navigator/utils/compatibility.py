"""Conditional imports related to python versions."""

import sys


# pylint: disable=unused-import

# https://mypy.readthedocs.io/en/stable/common_issues.html#variables-vs-type-aliases
if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias
