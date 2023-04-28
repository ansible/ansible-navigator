from __future__ import annotations

from typing import TYPE_CHECKING
from typing import NamedTuple


if TYPE_CHECKING:
    from .rules import Entry
    from .rules import WhileRule


class State(NamedTuple):
    entries: tuple[Entry, ...]
    while_stack: tuple[tuple[WhileRule, int], ...]

    @classmethod
    def root(cls, entry: Entry) -> State:
        return cls((entry,), ())

    @property
    def cur(self) -> Entry:
        return self.entries[-1]

    def push(self, entry: Entry) -> State:
        return self._replace(entries=(*self.entries, entry))

    def pop(self) -> State:
        return self._replace(entries=self.entries[:-1])

    def push_while(self, rule: WhileRule, entry: Entry) -> State:
        entries = (*self.entries, entry)
        while_stack = (*self.while_stack, (rule, len(entries)))
        return self._replace(entries=entries, while_stack=while_stack)

    def pop_while(self) -> State:
        entries, while_stack = self.entries[:-1], self.while_stack[:-1]
        return self._replace(entries=entries, while_stack=while_stack)
