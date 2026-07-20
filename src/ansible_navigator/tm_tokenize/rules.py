from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import NamedTuple

from ._types import Protocol
from .fchainmap import FChainMap
from .reg import ERR_REG
from .reg import _Reg
from .reg import _RegSet
from .reg import do_regset
from .reg import expand_escaped
from .reg import make_reg
from .region import Region
from .region import Regions
from .state import State
from .tokenize import tokenize
from .utils import uniquely_constructed


if TYPE_CHECKING:
    from re import Match

    from .compiler import Compiler
    from .region import Scope

Captures = tuple[tuple[int, "_Rule"], ...]  # declared later


def _split_name(s: str | None) -> tuple[str, ...]:
    if s is None:
        return ()
    return tuple(s.split())


class CompiledRule(Protocol):
    @property
    def name(self) -> tuple[str, ...]: ...

    def start(
        self,
        compiler: Compiler,
        match: Match[str],
        state: State,
    ) -> tuple[State, bool, Regions]: ...

    def search(
        self,
        compiler: Compiler,
        state: State,
        line: str,
        pos: int,
        first_line: bool,
        boundary: bool,
    ) -> tuple[State, int, bool, Regions] | None: ...


class Entry(NamedTuple):
    scope: tuple[str, ...]
    rule: CompiledRule
    start: tuple[str, int]
    reg: _Reg = ERR_REG
    boundary: bool = False


class _Rule(Protocol):
    """hack for recursive types python/mypy#731."""

    @property
    def name(self) -> tuple[str, ...]: ...

    @property
    def match(self) -> str | None: ...

    @property
    def begin(self) -> str | None: ...

    @property
    def end(self) -> str | None: ...

    @property
    def while_(self) -> str | None: ...

    @property
    def content_name(self) -> tuple[str, ...]: ...

    @property
    def captures(self) -> Captures: ...

    @property
    def begin_captures(self) -> Captures: ...

    @property
    def end_captures(self) -> Captures: ...

    @property
    def while_captures(self) -> Captures: ...

    @property
    def include(self) -> str | None: ...

    @property
    def patterns(self) -> tuple[_Rule, ...]: ...

    @property
    def repository(self) -> FChainMap[str, _Rule]: ...


class CompiledRegsetRule(CompiledRule, Protocol):
    @property
    def regset(self) -> _RegSet: ...

    @property
    def u_rules(self) -> tuple[_Rule, ...]: ...


@uniquely_constructed
class EndRule(NamedTuple):
    name: tuple[str, ...]
    content_name: tuple[str, ...]
    begin_captures: Captures
    end_captures: Captures
    end: str
    regset: _RegSet
    u_rules: tuple[_Rule, ...]

    def start(
        self,
        compiler: Compiler,
        match: Match[str],
        state: State,
    ) -> tuple[State, bool, Regions]:
        scope = state.cur.scope + self.name
        next_scope = scope + self.content_name

        boundary = match.end() == len(match.string)
        reg = make_reg(expand_escaped(match, self.end))
        start = (match.string, match.start())
        state = state.push(Entry(next_scope, self, start, reg, boundary))
        regions = _captures(compiler, scope, match, self.begin_captures)
        return state, True, regions

    def _end_ret(
        self,
        compiler: Compiler,
        state: State,
        pos: int,
        m: Match[str],
    ) -> tuple[State, int, bool, Regions]:
        ret = []
        if m.start() > pos:
            ret.append(Region(pos, m.start(), state.cur.scope))
        ret.extend(_captures(compiler, state.cur.scope, m, self.end_captures))
        # this is probably a bug in the grammar, but it pushed and popped at
        # the same position.
        # we'll advance the highlighter by one position to get past the loop
        # this appears to be what vs code does as well
        if state.entries[-1].start == (m.string, m.end()):
            ret.append(Region(m.end(), m.end() + 1, state.cur.scope))
            end = m.end() + 1
        else:
            end = m.end()
        return state.pop(), end, False, tuple(ret)

    def search(
        self,
        compiler: Compiler,
        state: State,
        line: str,
        pos: int,
        first_line: bool,
        boundary: bool,
    ) -> tuple[State, int, bool, Regions] | None:
        end_match = state.cur.reg.search(line, pos, first_line, boundary)
        if end_match is not None and end_match.start() == pos:
            return self._end_ret(compiler, state, pos, end_match)
        if end_match is None:
            idx, match = self.regset.search(line, pos, first_line, boundary)
            return do_regset(idx, match, self, compiler, state, pos)
        idx, match = self.regset.search(line, pos, first_line, boundary)
        if match is None or end_match.start() <= match.start():
            return self._end_ret(compiler, state, pos, end_match)
        return do_regset(idx, match, self, compiler, state, pos)


@uniquely_constructed
class MatchRule(NamedTuple):
    name: tuple[str, ...]
    captures: Captures

    def start(
        self,
        compiler: Compiler,
        match: Match[str],
        state: State,
    ) -> tuple[State, bool, Regions]:
        scope = state.cur.scope + self.name
        return state, False, _captures(compiler, scope, match, self.captures)

    def search(
        self,
        _compiler: Compiler,
        _state: State,
        _line: str,
        _pos: int,
        _first_line: bool,
        _boundary: bool,
    ) -> tuple[State, int, bool, Regions] | None:
        msg = f"unreachable {self}"
        raise AssertionError(msg)


@uniquely_constructed
class PatternRule(NamedTuple):
    name: tuple[str, ...]
    regset: _RegSet
    u_rules: tuple[_Rule, ...]

    def start(
        self,
        _compiler: Compiler,
        _match: Match[str],
        _state: State,
    ) -> tuple[State, bool, Regions]:
        msg = f"unreachable {self}"
        raise AssertionError(msg)

    def search(
        self,
        compiler: Compiler,
        state: State,
        line: str,
        pos: int,
        first_line: bool,
        boundary: bool,
    ) -> tuple[State, int, bool, Regions] | None:
        idx, match = self.regset.search(line, pos, first_line, boundary)
        return do_regset(idx, match, self, compiler, state, pos)


@uniquely_constructed
class Rule(NamedTuple):
    name: tuple[str, ...]
    match: str | None
    begin: str | None
    end: str | None
    while_: str | None
    content_name: tuple[str, ...]
    captures: Captures
    begin_captures: Captures
    end_captures: Captures
    while_captures: Captures
    include: str | None
    patterns: tuple[_Rule, ...]
    repository: FChainMap[str, _Rule]

    @classmethod
    def _parse_captures_key(
        cls,
        dct: dict[str, Any],
        key: str,
        repository: FChainMap[str, _Rule],
    ) -> Captures:
        """Parse a captures key from the grammar dict.

        Args:
            dct: The grammar dictionary.
            key: The captures key name.
            repository: The rule repository.

        Returns:
            The parsed captures tuple.
        """
        if key in dct:
            return tuple(
                (int(k), Rule.make(v, repository))
                for k, v in sorted(dct[key].items(), key=lambda x: int(x[0]))
            )
        return ()

    @classmethod
    def make(cls, dct: dict[str, Any], parent_repository: FChainMap[str, _Rule]) -> _Rule:
        if "repository" in dct:
            repository_dct: dict[str, _Rule] = {}
            repository = FChainMap(parent_repository, repository_dct)
            for k, sub_dct in dct["repository"].items():
                repository_dct[k] = Rule.make(sub_dct, repository)
        else:
            repository = parent_repository

        name = _split_name(dct.get("name"))
        match = dct.get("match")
        begin = dct.get("begin")
        end = dct.get("end")
        while_ = dct.get("while")
        content_name = _split_name(dct.get("contentName"))

        captures = cls._parse_captures_key(dct, "captures", repository)
        begin_captures = cls._parse_captures_key(dct, "beginCaptures", repository)
        end_captures = cls._parse_captures_key(dct, "endCaptures", repository)
        while_captures = cls._parse_captures_key(dct, "whileCaptures", repository)

        if begin is not None and end is None and while_ is None:
            end = "$impossible^"

        if begin and end and captures:
            begin_captures = end_captures = captures
            captures = ()
        elif begin and while_ and captures:
            begin_captures = while_captures = captures
            captures = ()

        include = dct.get("include")

        if "patterns" in dct:
            patterns = tuple(Rule.make(d, repository) for d in dct["patterns"])
        else:
            patterns = ()

        return cls(
            name=name,
            match=match,
            begin=begin,
            end=end,
            while_=while_,
            content_name=content_name,
            captures=captures,
            begin_captures=begin_captures,
            end_captures=end_captures,
            while_captures=while_captures,
            include=include,
            patterns=patterns,
            repository=repository,
        )


@uniquely_constructed
class WhileRule(NamedTuple):
    name: tuple[str, ...]
    content_name: tuple[str, ...]
    begin_captures: Captures
    while_captures: Captures
    while_: str
    regset: _RegSet
    u_rules: tuple[_Rule, ...]

    def start(
        self,
        compiler: Compiler,
        match: Match[str],
        state: State,
    ) -> tuple[State, bool, Regions]:
        scope = state.cur.scope + self.name
        next_scope = scope + self.content_name

        boundary = match.end() == len(match.string)
        reg = make_reg(expand_escaped(match, self.while_))
        start = (match.string, match.start())
        entry = Entry(next_scope, self, start, reg, boundary)
        state = state.push_while(self, entry)
        regions = _captures(compiler, scope, match, self.begin_captures)
        return state, True, regions

    def continues(
        self,
        compiler: Compiler,
        state: State,
        line: str,
        pos: int,
        first_line: bool,
        boundary: bool,
    ) -> tuple[int, bool, Regions] | None:
        match = state.cur.reg.match(line, pos, first_line, boundary)
        if match is None:
            return None

        ret = _captures(compiler, state.cur.scope, match, self.while_captures)
        return match.end(), True, ret

    def search(
        self,
        compiler: Compiler,
        state: State,
        line: str,
        pos: int,
        first_line: bool,
        boundary: bool,
    ) -> tuple[State, int, bool, Regions] | None:
        idx, match = self.regset.search(line, pos, first_line, boundary)
        return do_regset(idx, match, self, compiler, state, pos)


def _backtrack_capture(
    compiler: Compiler,
    ret: list[Region],
    start: int,
    end: int,
    group_s: str,
    rule: CompiledRule,
) -> None:
    """Handle a capture group that starts before the current position.

    Args:
        compiler: The grammar compiler.
        ret: The regions list to splice into.
        start: The start of the capture group.
        end: The end of the capture group.
        group_s: The captured string.
        rule: The compiled rule for the capture.
    """
    j = len(ret) - 1
    while j > 0 and start < ret[j - 1].end:
        j -= 1

    oldtok = ret[j]
    newtok = []
    if start > oldtok.start:
        newtok.append(oldtok._replace(end=start))

    newtok.extend(_inner_capture_parse(compiler, start, group_s, oldtok.scope, rule))

    if end < oldtok.end:
        newtok.append(oldtok._replace(start=end))
    ret[j : j + 1] = newtok


def _captures(
    compiler: Compiler,
    scope: Scope,
    match: Match[str],
    captures: Captures,
) -> Regions:
    ret: list[Region] = []
    pos, pos_end = match.span()
    for i, u_rule in captures:
        try:
            group_s = match[i]
        except IndexError:
            continue
        if not group_s:
            continue

        rule = compiler.compile_rule(u_rule)
        start, end = match.span(i)
        if start < pos:
            _backtrack_capture(compiler, ret, start, end, match[i], rule)
        else:
            if start > pos:
                ret.append(Region(pos, start, scope))
            ret.extend(_inner_capture_parse(compiler, start, match[i], scope, rule))
            pos = end

    if pos < pos_end:
        ret.append(Region(pos, pos_end, scope))
    return tuple(ret)


def _inner_capture_parse(
    compiler: Compiler,
    start: int,
    s: str,
    scope: Scope,
    rule: CompiledRule,
) -> Regions:
    state = State.root(Entry(scope + rule.name, rule, (s, 0)))
    _, regions = tokenize(compiler, state, s, first_line=False)
    return tuple(r._replace(start=r.start + start, end=r.end + start) for r in regions)
