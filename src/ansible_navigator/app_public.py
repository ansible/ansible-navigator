"""A carrier for app internals.

This will be shared with other actions and is immutable.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING
from typing import NamedTuple

from .steps import Steps


if TYPE_CHECKING:
    from .configuration_subsystem.definitions import ApplicationConfiguration


class AppPublic(NamedTuple):
    """A carrier class for app internals.

    This will be shared with other actions and is immutable.
    """

    # Quoted due to https://github.com/sphinx-doc/sphinx/issues/10400
    args: ApplicationConfiguration
    name: str
    rerun: Callable[[], None]
    stdout: list[str]
    steps: Steps
    update: Callable[..., None]
    write_artifact: Callable[..., None]
