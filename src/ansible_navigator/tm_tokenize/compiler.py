from __future__ import annotations

import functools

from typing import TYPE_CHECKING

from .fchainmap import FChainMap
from .reg import make_regset
from .rules import EndRule
from .rules import Entry
from .rules import MatchRule
from .rules import PatternRule
from .rules import WhileRule
from .state import State


if TYPE_CHECKING:
    from .grammars import Grammar
    from .grammars import Grammars
    from .rules import Captures
    from .rules import CompiledRule
    from .rules import _Rule


class Compiler:
    def __init__(self, grammar: Grammar, grammars: Grammars) -> None:
        """Initialize the grammar compiler.

        :param grammar: The grammar to compile, a text mate language file
        :param grammars: All previously compiled grammars
        """
        self._root_scope = grammar.scope_name
        self._grammars = grammars
        self._rule_to_grammar: dict[_Rule, Grammar] = {}
        self._c_rules: dict[_Rule, CompiledRule] = {}
        root = self._compile_root(grammar)
        self.root_state = State.root(Entry(root.name, root, ("", 0)))

    def _visit_rule(self, grammar: Grammar, rule: _Rule) -> _Rule:
        self._rule_to_grammar[rule] = grammar
        return rule

    @functools.cache
    def _include(
        self,
        grammar: Grammar,
        repository: FChainMap[str, _Rule],
        s: str,
    ) -> tuple[list[str], tuple[_Rule, ...]]:
        if s == "$self":
            return self._patterns(grammar, grammar.patterns)
        elif s == "$base":
            grammar = self._grammars.grammar_for_scope(self._root_scope)
            return self._include(grammar, grammar.repository, "$self")
        elif s.startswith("#"):
            return self._patterns(grammar, (repository[s[1:]],))
        elif "#" not in s:
            grammar = self._grammars.grammar_for_scope(s)
            return self._include(grammar, grammar.repository, "$self")
        else:
            scope, _, s = s.partition("#")
            grammar = self._grammars.grammar_for_scope(scope)
            return self._include(grammar, grammar.repository, f"#{s}")

    @functools.cache
    def _patterns(
        self,
        grammar: Grammar,
        rules: tuple[_Rule, ...],
    ) -> tuple[list[str], tuple[_Rule, ...]]:
        ret_regs = []
        ret_rules: list[_Rule] = []
        for rule in rules:
            if rule.include is not None:
                tmp_regs, tmp_rules = self._include(grammar, rule.repository, rule.include)
                ret_regs.extend(tmp_regs)
                ret_rules.extend(tmp_rules)
            elif rule.match is None and rule.begin is None and rule.patterns:
                tmp_regs, tmp_rules = self._patterns(grammar, rule.patterns)
                ret_regs.extend(tmp_regs)
                ret_rules.extend(tmp_rules)
            elif rule.match is not None:
                ret_regs.append(rule.match)
                ret_rules.append(self._visit_rule(grammar, rule))
            elif rule.begin is not None:
                ret_regs.append(rule.begin)
                ret_rules.append(self._visit_rule(grammar, rule))
            else:
                msg = f"unreachable {rule}"
                raise AssertionError(msg)
        return ret_regs, tuple(ret_rules)

    def _captures_ref(self, grammar: Grammar, captures: Captures) -> Captures:
        return tuple((n, self._visit_rule(grammar, r)) for n, r in captures)

    def _compile_root(self, grammar: Grammar) -> PatternRule:
        regs, rules = self._patterns(grammar, grammar.patterns)
        return PatternRule((grammar.scope_name,), make_regset(*regs), rules)

    def _compile_rule(self, grammar: Grammar, rule: _Rule) -> CompiledRule:
        assert rule.include is None, rule
        if rule.match is not None:
            captures_ref = self._captures_ref(grammar, rule.captures)
            return MatchRule(rule.name, captures_ref)
        elif rule.begin is not None and rule.end is not None:
            regs, rules = self._patterns(grammar, rule.patterns)
            return EndRule(
                rule.name,
                rule.content_name,
                self._captures_ref(grammar, rule.begin_captures),
                self._captures_ref(grammar, rule.end_captures),
                rule.end,
                make_regset(*regs),
                rules,
            )
        elif rule.begin is not None and rule.while_ is not None:
            regs, rules = self._patterns(grammar, rule.patterns)
            return WhileRule(
                rule.name,
                rule.content_name,
                self._captures_ref(grammar, rule.begin_captures),
                self._captures_ref(grammar, rule.while_captures),
                rule.while_,
                make_regset(*regs),
                rules,
            )
        else:
            regs, rules = self._patterns(grammar, rule.patterns)
            return PatternRule(rule.name, make_regset(*regs), rules)

    def compile_rule(self, rule: _Rule) -> CompiledRule:
        try:
            return self._c_rules[rule]
        except KeyError:
            pass

        grammar = self._rule_to_grammar[rule]
        ret = self._c_rules[rule] = self._compile_rule(grammar, rule)
        return ret
