from __future__ import annotations

from typing import TYPE_CHECKING

from .region import Region
from .region import Regions
from .state import State


if TYPE_CHECKING:
    from .compiler import Compiler


def tokenize(
    compiler: Compiler,
    state: State,
    line: str,
    first_line: bool,
) -> tuple[State, Regions]:
    """tokenize a string into it's parts"""
    ret: list[Region] = []
    pos = 0
    boundary = state.cur.boundary

    # TODO: this is still a little wasteful
    while_stack = []
    for while_rule, idx in state.while_stack:
        while_stack.append((while_rule, idx))
        while_state = State(state.entries[:idx], tuple(while_stack))

        while_res = while_rule.continues(compiler, while_state, line, pos, first_line, boundary)
        if while_res is None:
            state = while_state.pop_while()
            break
        pos, boundary, regions = while_res
        ret.extend(regions)

    search_res = state.cur.rule.search(compiler, state, line, pos, first_line, boundary)
    while search_res is not None:
        state, pos, boundary, regions = search_res
        ret.extend(regions)

        search_res = state.cur.rule.search(compiler, state, line, pos, first_line, boundary)

    if pos < len(line):
        ret.append(Region(pos, len(line), state.cur.scope))

    return state, tuple(ret)
