"""A couple singleton sentinels for convenience to avoid the use of None."""
from __future__ import annotations

from typing import Any


class Singleton(type):
    """One of a kind."""

    _instances: dict[Any, Singleton] = {}

    def __call__(cls, *args, **kwargs):
        """Determine if the instance is one of a kind.

        :param *args: Arbitrary arguments
        :param **kwargs: Dict of Keyword Args
        :returns: The type
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Unknown(metaclass=Singleton):
    """Something that should eventually be known."""

    def __repr__(self):
        """Return the type of the object.

        :returns: The type of the object.
        """
        return type(self).__name__


unknown = Unknown()


class Nonexistent(metaclass=Singleton):
    """Something that does not exist."""

    def __repr__(self):
        """Return the type of the object.

        :returns: The type of the object
        """
        return type(self).__name__


nonexistent = Nonexistent()
