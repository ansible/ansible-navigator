"""Step abstractions for actions."""
from collections import deque
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import TypeVar
from typing import Union


class Step:
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    """One step in the flow of things.

    The ``TypedStep`` below should be used for all new actions.
    """

    def __init__(
        self,
        name: str,
        step_type: str,
        value: List[Dict[str, str]],
        columns: Optional[List[str]] = None,
        index: Optional[int] = None,
        select_func: Optional[Callable[[], "Step"]] = None,
        show_func: Optional[Callable[[], None]] = None,
    ) -> None:
        """Initialize the instance of a step.

        :param name: The name of the step
        :param step_type: The type of step
        :param value: The data corresponding to the step
        :param columns: The columns to show when the data is presented as a menu
        :param index: The currently selected entry in the data
        :param select_func: The function to be called when the user selects an entry
        :param show_func: The function to call prior to an entry being shown to the user
        """
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
        self.type = step_type

    @property
    def changed(self) -> bool:
        """Return if this has changed.

        :returns: Boolean if index or value has changed
        """
        return self._index_changed or self._value_changed

    @changed.setter
    def changed(self, value: bool) -> None:
        """Set the changed value.

        :param value: The value to set
        :type value: bool
        """
        self._value_check(value, bool)
        self._index_changed = value
        self._value_changed = value

    @property
    def index(self) -> Optional[int]:
        """Return the index.

        :returns: Index (should be ``int``)
        """
        return self._index

    @index.setter
    def index(self, index: int) -> None:
        """Set the index.

        :param index: The index
        :type index: int
        """
        self._value_check(index, (int, type(None)))
        self._index_changed = self._index != index
        self._index = index

    @property
    def selected(self) -> Optional[Dict[str, Any]]:
        """Return the selected item.

        :returns: The selected item.
        """
        if self._index is None or not self._value:
            return None
        return self._value[self._index % len(self._value)]

    @property
    def value(self) -> List[Dict[str, Any]]:
        """Return the value.

        :returns: The value
        """
        return self._value

    @value.setter
    def value(self, value: List[Dict[str, Any]]) -> None:
        """Set the value and changed is needed.

        :param value: List of dicts
        :type value: list
        """
        self._value_check(value, list)
        self._value_changed = self._value != value
        self._value = value

    @staticmethod
    def _value_check(value: Any, want: Union[type, Tuple[type, ...]]) -> None:
        """Check some expected type against a value's type.

        :param value: Some value for comparison
        :param want: The desired type for value
        :raises ValueError: If value type doesn't match wanted type
        """
        if not isinstance(value, want):
            raise ValueError(f"wanted {want}, got {type(value)}")


class StepType(Enum):
    """Type of step, either menu or content."""

    MENU = "menu"
    CONTENT = "content"


T = TypeVar("T")  # pylint: disable=invalid-name


@dataclass
class TypedStep(Generic[T]):
    # pylint: disable=too-many-instance-attributes
    """One step in the flow of things.

    This should be used for new actions following the pattern of a
    ``TypedDict`` for the user interface as seen in settings.
    """

    name: str
    step_type: StepType
    _index_changed: bool = False
    _index: Optional[int] = None
    _value_changed: bool = False
    _value: Sequence[T] = field(default_factory=list)
    columns: Optional[List[str]] = None
    select_func: Optional[Callable[[], "TypedStep"]] = None
    show_func: Optional[Callable[[], None]] = None

    @property
    def changed(self) -> bool:
        """Return the changed flag.

        :returns: Indication of change
        """
        return self._index_changed or self._value_changed

    @changed.setter
    def changed(self, value: bool) -> None:
        """Set the changed value.

        :param value: Indication of change
        """
        self._index_changed = value
        self._value_changed = value

    @property
    def index(self) -> Optional[int]:
        """Return the index.

        :returns: The index
        """
        return self._index

    @index.setter
    def index(self, index: int) -> None:
        """Set the index.

        :param index: The index
        """
        self._index_changed = self.index != index
        self._index = index

    @property
    def selected(self) -> Optional[T]:
        """Return the selected item.

        :returns: The selected item
        """
        if self._index is None or not self._value:
            return None
        return self._value[self._index % len(self._value)]

    @property
    def value(self) -> Sequence[T]:
        """Return the value.

        :returns: The value
        """
        return self._value

    @value.setter
    def value(self, value: Sequence[T]) -> None:
        """Set the value and value changed if needed.

        :param value: The value for this instance
        """
        self._value_changed = self._value != value
        self._value = value


class Steps(deque):
    """A custom deque."""

    def back_one(self) -> Any:
        """Pop one step off the dequeue to move backwards.

        :returns: The dequeue after pop() or None if no steps are left
        """
        if self:
            return self.pop()
        return None

    @property
    def current(self) -> Any:
        """Return the current step.

        :returns: The TypedStep (or Step) currently accessed
        """
        return self[-1]

    @property
    def previous(self) -> Any:
        """Return the previous step.

        :returns: The TypedStep (or Step) previously accessed
        """
        return self[-2]
