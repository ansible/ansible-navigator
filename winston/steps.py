""" steps here
"""
from typing import Union
from collections import deque


class Step:

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    """One step in the flow of things"""

    def __init__(
        self,
        columns=None,
        index=None,
        name=None,
        select_func=None,
        show_func=None,
        tipe=None,
        value=None,
    ):
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
    def changed(self):
        """return if this has changed

        :return: if this has changed
        :rtype: bool
        """
        return self._index_changed or self._value_changed

    @changed.setter
    def changed(self, value):
        """set the changed value

        :param value: The value to set
        :type value: something that can be booled
        """
        self._value_check(value, bool)
        self._index_changed = value
        self._value_changed = value

    @property
    def index(self):
        """return the index

        :return: index
        :rtype: should be int
        """
        return self._index

    @index.setter
    def index(self, index):
        """set the index

        :param index: the index
        :type index: intable index
        """
        self._value_check(index, (int, type(None)))
        self._index_changed = self._index != index
        self._index = index

    @property
    def selected(self):
        """return the selected item

        :return: the selected item
        :rtype: obj
        """
        if self.index is None or not self._value:
            return None
        return self._value[self._index % len(self._value)]

    @property
    def value(self):
        """return the value

        :return: the value
        :rtype: list
        """
        return self._value

    @value.setter
    def value(self, value):
        """set the value and changed is needed

        :param value: list
        :type value: list
        """
        self._value_check(value, list)
        self._value_changed = self._value != value
        self._value = value

    @staticmethod
    def _value_check(value, want):
        """check some expect type against a value"""
        if not isinstance(value, want):
            raise ValueError("wanted {want}, got {value}".format(want=want, value=type(value)))


class Steps(deque):
    """a custom deque"""

    def back_one(self) -> Union[Step, None]:
        """convenience method"""
        if self:
            return self.pop()
        return None

    @property
    def current(self):
        """return the current step"""
        return self[-1]

    @property
    def previous(self) -> Step:
        """return the previous step"""
        return self[-2]
