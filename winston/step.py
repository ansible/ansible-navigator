""" A step
"""


class Step:

    # pylint: disable=too-many-instance-attributes
    """One step in the flow of things"""

    def __init__(self, name, tipe, func):
        self._index = None
        self._index_changed = False
        self._value = []
        self._value_changed = False
        self.name = name
        self.type = tipe
        self.func = func
        self.previous = None
        self.next = None
        self.columns = []

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
        try:
            return self._value[self._index % len(self._value)]
        except AttributeError as _exc:
            return None

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
