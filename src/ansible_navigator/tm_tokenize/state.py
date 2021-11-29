from typing import NamedTuple
from typing import Tuple


from .rules import TmRuleEntry
from .rules import WhileRule

class State(NamedTuple):
    entries: Tuple[TmRuleEntry, ...]
    while_stack: Tuple[Tuple[WhileRule, int], ...]

    @classmethod
    def root(cls, entry: TmRuleEntry) -> "State":
        return cls((entry,), ())

    @property
    def cur(self) -> TmRuleEntry:
        return self.entries[-1]

    def push(self, entry: TmRuleEntry) -> "State":
        return self._replace(entries=(*self.entries, entry))

    def pop(self) -> "State":
        return self._replace(entries=self.entries[:-1])

    def push_while(self, rule: WhileRule, entry: TmRuleEntry) -> "State":
        entries = (*self.entries, entry)
        while_stack = (*self.while_stack, (rule, len(entries)))
        return self._replace(entries=entries, while_stack=while_stack)

    def pop_while(self) -> "State":
        entries, while_stack = self.entries[:-1], self.while_stack[:-1]
        return self._replace(entries=entries, while_stack=while_stack)
