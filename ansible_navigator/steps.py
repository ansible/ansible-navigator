""" steps here
"""
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union
from collections import deque


class Step:

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    """One step in the flow of things"""

    def __init__(
        self,
        name: str,
        tipe: str,
        value: List[Dict[str, str]],
        columns: Union[List[str], None] = None,
        index: Union[int, None] = None,
        select_func: Union[Callable[[], "Step"], None] = None,
        show_func: Union[Callable[[], None], None] = None,
    ) -> None:
        self._index = index
        self._index_changed = False
        self._value = value or []
        self._value_changed = False
        self.columns = columns or []
        self.name = name
        self.next = None
        self.previous = None
        self.select_func = select_func
        self.show_func = show_func
        self.type = tipe

    @property
    def changed(self) -> bool:
        """return if this has changed

        :return: if this has changed
        :rtype: bool
        """
        return self._index_changed or self._value_changed

    @changed.setter
    def changed(self, value: bool) -> None:
        """set the changed value

        :param value: The value to set
        :type value: something that can be booled
        """
        self._value_check(value, bool)
        self._index_changed = value
        self._value_changed = value

    @property
    def index(self) -> Union[int, None]:
        """return the index

        :return: index
        :rtype: should be int
        """
        return self._index

    @index.setter
    def index(self, index: int) -> None:
        """set the index

        :param index: the index
        :type index: intable index
        """
        self._value_check(index, (int, type(None)))
        self._index_changed = self._index != index
        self._index = index

    @property
    def selected(self) -> Union[None, Dict[str, Any]]:
        """return the selected item

        :return: the selected item
        :rtype: obj
        """
        if self._index is None or not self._value:
            return None
        return self._value[self._index % len(self._value)]

    @property
    def value(self) -> List[Dict[str, Any]]:
        """return the value

        :return: the value
        :rtype: list
        """
        return self._value

    @value.setter
    def value(self, value: List[Dict[str, Any]]) -> None:
        """set the value and changed is needed

        :param value: list
        :type value: list
        """
        self._value_check(value, list)
        self._value_changed = self._value != value
        self._value = value

    @staticmethod
    def _value_check(value: Any, want: Union[type, Tuple[type, ...]]) -> None:
        """check some expect type against a value"""
        if not isinstance(value, want):
            raise ValueError("wanted {want}, got {value}".format(want=want, value=type(value)))


class Steps(deque):  # type: ignore

    """a custom deque"""

    def back_one(self) -> Any:
        """convenience method"""
        if self:
            return self.pop()
        return None

    @property
    def current(self) -> Any:
        """return the current step"""
        return self[-1]

    @property
    def previous(self) -> Any:
        """return the previous step"""
        return self[-2]
