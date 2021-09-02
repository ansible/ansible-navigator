import json
import os

from typing import Any
from typing import Dict
from typing import FrozenSet
from typing import List
from typing import NamedTuple
from typing import Tuple
from typing import TypeVar


from .compiler import Compiler
from .fchainmap import FChainMap
from .reg import _Reg
from .reg import make_reg
from .rules import _Rule
from .rules import Rule
from .utils import uniquely_constructed


T = TypeVar("T")


@uniquely_constructed
class Grammar(NamedTuple):
    scope_name: str
    repository: FChainMap[str, _Rule]
    patterns: Tuple[_Rule, ...]

    @classmethod
    def make(cls, data: Dict[str, Any]) -> "Grammar":
        scope_name = data["scopeName"]
        if "repository" in data:
            # this looks odd, but it's so we can have a self-referential
            # immutable-after-construction chain map
            repository_dct: Dict[str, _Rule] = {}
            repository = FChainMap(repository_dct)
            for k, dct in data["repository"].items():
                repository_dct[k] = Rule.make(dct, repository)
        else:
            repository = FChainMap()
        patterns = tuple(Rule.make(d, repository) for d in data["patterns"])
        return cls(scope_name=scope_name, repository=repository, patterns=patterns)


class Grammars:
    def __init__(self, *directories: str) -> None:
        self._scope_to_files = {
            os.path.splitext(filename)[0]: os.path.join(directory, filename)
            for directory in directories
            if os.path.exists(directory)
            for filename in sorted(os.listdir(directory))
            if filename.endswith(".json")
        }

        unknown_grammar = {"scopeName": "source.unknown", "patterns": []}
        self._raw = {"source.unknown": unknown_grammar}
        self._file_types: List[Tuple[FrozenSet[str], str]] = []
        self._first_line: List[Tuple[_Reg, str]] = []
        self._parsed: Dict[str, Grammar] = {}
        self._compiled: Dict[str, Compiler] = {}

    def _raw_for_scope(self, scope: str) -> Dict[str, Any]:
        try:
            return self._raw[scope]
        except KeyError:
            pass

        grammar_path = self._scope_to_files.pop(scope)
        with open(grammar_path, encoding="UTF-8") as f:
            ret = self._raw[scope] = json.load(f)

        file_types = frozenset(ret.get("fileTypes", ()))
        first_line = make_reg(ret.get("firstLineMatch", "$impossible^"))

        self._file_types.append((file_types, scope))
        self._first_line.append((first_line, scope))

        return ret

    def grammar_for_scope(self, scope: str) -> Grammar:
        try:
            return self._parsed[scope]
        except KeyError:
            pass

        raw = self._raw_for_scope(scope)
        ret = self._parsed[scope] = Grammar.make(raw)
        return ret

    def compiler_for_scope(self, scope: str) -> Compiler:
        try:
            return self._compiled[scope]
        except KeyError:
            pass

        grammar = self.grammar_for_scope(scope)
        ret = self._compiled[scope] = Compiler(grammar, self)
        return ret

    def blank_compiler(self) -> Compiler:
        return self.compiler_for_scope("source.unknown")

    def compiler_for_file(self, filename: str, first_line: str) -> Compiler:
        # No file support needed today
        # for tag in tags_from_filename(filename) - {"text"}:
        #     try:
        #         # TODO: this doesn't always match even if we detect it
        #         return self.compiler_for_scope(f"source.{tag}")
        #     except KeyError:
        #         pass

        # didn't find it in the fast path, need to read all the json
        for k in tuple(self._scope_to_files):
            self._raw_for_scope(k)

        _, _, ext = os.path.basename(filename).rpartition(".")
        for extensions, scope in self._file_types:
            if ext in extensions:
                return self.compiler_for_scope(scope)

        for reg, scope in self._first_line:
            if reg.match(first_line, 0, first_line=True, boundary=True):
                return self.compiler_for_scope(scope)

        return self.compiler_for_scope("source.unknown")
