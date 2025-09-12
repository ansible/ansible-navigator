from typing import Generic
from typing import TypeVar

from ._types import Protocol


TKey_contra = TypeVar("TKey_contra", contravariant=True)
TValue_co = TypeVar("TValue_co", covariant=True)


class Indexable(Generic[TKey_contra, TValue_co], Protocol):  # noqa: PYI059
    def __getitem__(self, key: TKey_contra) -> TValue_co:
        """Get the value associated with the given key.

        Args:
            key: The key to retrieve the value for.
        """


class FChainMap(Generic[TKey_contra, TValue_co]):
    def __init__(self, *mappings: Indexable[TKey_contra, TValue_co]) -> None:
        """Initialize the FChainMap.

        Args:
            *mappings: A tuple of mappings, each corresponding to a
                repository entry of a ``tm_language`` file
        """
        self._mappings = mappings

    def __getitem__(self, key: TKey_contra) -> TValue_co:
        """Get the value associated with the given key.

        Args:
            key: The key to retrieve the value for.

        Returns:
            The value associated with the key.

        Raises:
            KeyError: If the key is not found in any of the mappings.
        """
        for mapping in reversed(self._mappings):
            try:
                return mapping[key]
            except KeyError:
                pass
        raise KeyError(key)
