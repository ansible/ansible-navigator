from __future__ import annotations

from re import Match  # noqa: F401
from typing import TypeVar


T = TypeVar("T")


def uniquely_constructed(t: T) -> T:
    """avoid tuple.__hash__ for "singleton" constructed objects"""
    t.__hash__ = object.__hash__  # type: ignore[assignment]
    return t
