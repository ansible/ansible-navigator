from __future__ import annotations

from typing import NamedTuple
from typing import Tuple


Scope = tuple[str, ...]

Regions = tuple["Region", ...]


class Region(NamedTuple):
    start: int
    end: int
    scope: Scope
