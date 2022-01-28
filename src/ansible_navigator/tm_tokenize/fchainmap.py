from typing import Generic
from typing import TypeVar

from ._types import Protocol


TKey = TypeVar("TKey", contravariant=True)
TValue = TypeVar("TValue", covariant=True)


class Indexable(Generic[TKey, TValue], Protocol):
    def __getitem__(self, key: TKey) -> TValue:
        ...


class FChainMap(Generic[TKey, TValue]):
    def __init__(self, *mappings: Indexable[TKey, TValue]) -> None:
        """Initialize the FChainMap.

        :param mappings: A tuple of mappings, each corresponding to a repository entry of a
            ``tm_language`` file
        """
        self._mappings = mappings

    def __getitem__(self, key: TKey) -> TValue:
        for mapping in reversed(self._mappings):
            try:
                return mapping[key]
            except KeyError:
                pass
        else:
            raise KeyError(key)
