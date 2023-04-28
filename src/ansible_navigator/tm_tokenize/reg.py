from __future__ import annotations

import functools
import re

from re import Match
from typing import TYPE_CHECKING
from typing import Optional

import onigurumacffi

from .region import Region


if TYPE_CHECKING:
    from ._types import Protocol  # noqa: F401
    from .compiler import Compiler
    from .region import Regions
    from .rules import CompiledRegsetRule
    from .rules import CompiledRule  # noqa: F401
    from .rules import _Rule  # noqa: F401
    from .state import State

_BACKREF_RE = re.compile(r"((?<!\\)(?:\\\\)*)\\([0-9]+)")


_FLAGS = {
    # (first_line, boundary)  # noqa: E800
    (False, False): (
        onigurumacffi.OnigSearchOption.NOT_END_STRING
        | onigurumacffi.OnigSearchOption.NOT_BEGIN_STRING
        | onigurumacffi.OnigSearchOption.NOT_BEGIN_POSITION
    ),
    (False, True): (
        onigurumacffi.OnigSearchOption.NOT_END_STRING
        | onigurumacffi.OnigSearchOption.NOT_BEGIN_STRING
    ),
    (True, False): (
        onigurumacffi.OnigSearchOption.NOT_END_STRING
        | onigurumacffi.OnigSearchOption.NOT_BEGIN_POSITION
    ),
    (True, True): onigurumacffi.OnigSearchOption.NOT_END_STRING,
}


class _Reg:
    def __init__(self, s: str) -> None:
        self._pattern = s
        self._reg = onigurumacffi.compile(self._pattern)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._pattern!r})"

    def search(self, line: str, pos: int, first_line: bool, boundary: bool) -> Match[str] | None:
        return self._reg.search(line, pos, flags=_FLAGS[first_line, boundary])

    def match(self, line: str, pos: int, first_line: bool, boundary: bool) -> Match[str] | None:
        return self._reg.match(line, pos, flags=_FLAGS[first_line, boundary])


class _RegSet:
    def __init__(self, *s: str) -> None:
        self._patterns = s
        self._set = onigurumacffi.compile_regset(*self._patterns)

    def __repr__(self) -> str:
        args = ", ".join(repr(s) for s in self._patterns)
        return f"{type(self).__name__}({args})"

    def search(
        self,
        line: str,
        pos: int,
        first_line: bool,
        boundary: bool,
    ) -> tuple[int, Match[str] | None]:
        return self._set.search(line, pos, flags=_FLAGS[first_line, boundary])


def do_regset(
    idx: int,
    match: Match[str] | None,
    rule: CompiledRegsetRule,
    compiler: Compiler,
    state: State,
    pos: int,
) -> tuple[State, int, bool, Regions] | None:
    if match is None:
        return None

    ret = []
    if match.start() > pos:
        ret.append(Region(pos, match.start(), state.cur.scope))

    target_rule = compiler.compile_rule(rule.u_rules[idx])
    state, boundary, regions = target_rule.start(compiler, match, state)
    ret.extend(regions)

    return state, match.end(), boundary, tuple(ret)


def expand_escaped(match: Match[str], s: str) -> str:
    return _BACKREF_RE.sub(lambda m: f"{m[1]}{re.escape(match[int(m[2])])}", s)


make_reg = functools.cache(_Reg)
make_regset = functools.cache(_RegSet)
ERR_REG = make_reg("$ ^")
