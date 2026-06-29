"""Tests for the steps module."""

from __future__ import annotations

import pytest

from ansible_navigator.steps import Step
from ansible_navigator.steps import Steps
from ansible_navigator.steps import StepType
from ansible_navigator.steps import TypedStep


class TestStep:
    """Tests for the Step class."""

    def test_constructor_defaults(self) -> None:
        """Test Step constructor with defaults."""
        step = Step(name="test", step_type="menu", value=[])
        assert step.name == "test"
        assert step.type == "menu"
        assert step.value == []
        assert step.columns == []
        assert step.index is None
        assert step.select_func is None
        assert step.show_func is None
        assert step.next is None
        assert step.previous is None

    def test_changed_false_initially(self) -> None:
        """Test changed is False initially."""
        step = Step(name="test", step_type="menu", value=[])
        assert step.changed is False

    def test_changed_after_index_set(self) -> None:
        """Test changed is True after index changes."""
        step = Step(name="test", step_type="menu", value=[{"a": "1"}])
        step.index = 0
        assert step.changed is True

    def test_changed_after_value_set(self) -> None:
        """Test changed is True after value changes."""
        step = Step(name="test", step_type="menu", value=[])
        step.value = [{"a": "1"}]
        assert step.changed is True

    def test_changed_setter(self) -> None:
        """Test changed setter resets both flags."""
        step = Step(name="test", step_type="menu", value=[{"a": "1"}])
        step.index = 0
        step.changed = False
        assert step.changed is False

    def test_changed_setter_type_error(self) -> None:
        """Test changed setter with invalid type."""
        step = Step(name="test", step_type="menu", value=[])
        with pytest.raises(TypeError):
            step.changed = "not a bool"  # type: ignore[assignment]

    def test_index_setter(self) -> None:
        """Test index setter."""
        step = Step(name="test", step_type="menu", value=[{"a": "1"}])
        step.index = 0
        assert step.index == 0

    def test_index_setter_none(self) -> None:
        """Test index setter with None."""
        step = Step(name="test", step_type="menu", value=[{"a": "1"}], index=0)
        step.index = None
        assert step.index is None

    def test_index_setter_type_error(self) -> None:
        """Test index setter with invalid type."""
        step = Step(name="test", step_type="menu", value=[])
        with pytest.raises(TypeError):
            step.index = "bad"  # type: ignore[assignment]

    def test_value_setter(self) -> None:
        """Test value setter."""
        step = Step(name="test", step_type="menu", value=[])
        new_val = [{"a": "1"}]
        step.value = new_val
        assert step.value == new_val

    def test_value_setter_type_error(self) -> None:
        """Test value setter with invalid type."""
        step = Step(name="test", step_type="menu", value=[])
        with pytest.raises(TypeError):
            step.value = "not a list"  # type: ignore[assignment]

    def test_selected_none_index(self) -> None:
        """Test selected returns None when index is None."""
        step = Step(name="test", step_type="menu", value=[{"a": "1"}])
        assert step.selected is None

    def test_selected_empty_value(self) -> None:
        """Test selected returns None when value is empty."""
        step = Step(name="test", step_type="menu", value=[], index=0)
        assert step.selected is None

    def test_selected_valid(self) -> None:
        """Test selected returns correct item."""
        data = [{"a": "1"}, {"b": "2"}]
        step = Step(name="test", step_type="menu", value=data, index=1)
        assert step.selected == {"b": "2"}

    def test_selected_wrap_around(self) -> None:
        """Test selected wraps around via modulo."""
        data = [{"a": "1"}, {"b": "2"}]
        step = Step(name="test", step_type="menu", value=data, index=3)
        assert step.selected == {"b": "2"}

    def test_value_check_valid(self) -> None:
        """Test _value_check with valid type."""
        Step._value_check(42, int)

    def test_value_check_invalid(self) -> None:
        """Test _value_check with invalid type raises TypeError."""
        with pytest.raises(TypeError, match="wanted"):
            Step._value_check("string", int)

    def test_value_check_tuple_types(self) -> None:
        """Test _value_check with tuple of types."""
        Step._value_check(None, (int, type(None)))


class TestStepType:
    """Tests for the StepType enum."""

    def test_menu_value(self) -> None:
        """Test MENU value."""
        assert StepType.MENU.value == "menu"

    def test_content_value(self) -> None:
        """Test CONTENT value."""
        assert StepType.CONTENT.value == "content"


class TestTypedStep:
    """Tests for the TypedStep dataclass."""

    def test_changed_false_initially(self) -> None:
        """Test changed is False initially."""
        step = TypedStep[str](name="test", step_type=StepType.MENU)
        assert step.changed is False

    def test_changed_after_index(self) -> None:
        """Test changed after index set."""
        step = TypedStep[str](name="test", step_type=StepType.MENU)
        step.index = 0
        assert step.changed is True

    def test_changed_setter(self) -> None:
        """Test changed setter resets flags."""
        step = TypedStep[str](name="test", step_type=StepType.MENU)
        step.index = 0
        step.changed = False
        assert step.changed is False

    def test_index_tracks_changes(self) -> None:
        """Test index tracks whether it changed."""
        step = TypedStep[str](name="test", step_type=StepType.MENU)
        step.index = 0
        assert step._index_changed is True
        step.index = 0
        assert step._index_changed is False

    def test_selected_none_index(self) -> None:
        """Test selected with None index."""
        step = TypedStep[str](name="test", step_type=StepType.MENU, _value=["a", "b"])
        assert step.selected is None

    def test_selected_empty_value(self) -> None:
        """Test selected with empty value."""
        step = TypedStep[str](name="test", step_type=StepType.MENU, _index=0)
        assert step.selected is None

    def test_selected_valid(self) -> None:
        """Test selected with valid index."""
        step = TypedStep[str](name="test", step_type=StepType.MENU, _value=["a", "b"], _index=1)
        assert step.selected == "b"

    def test_selected_wrap_around(self) -> None:
        """Test selected wraps via modulo."""
        step = TypedStep[str](name="test", step_type=StepType.MENU, _value=["a", "b"], _index=3)
        assert step.selected == "b"

    def test_value_setter_tracks_changes(self) -> None:
        """Test value setter tracks changes."""
        step = TypedStep[str](name="test", step_type=StepType.MENU)
        step.value = ["a", "b"]
        assert step._value_changed is True
        assert step.value == ["a", "b"]

    def test_value_no_change(self) -> None:
        """Test value setter when value doesn't change."""
        step = TypedStep[str](name="test", step_type=StepType.MENU, _value=["a"])
        step.value = ["a"]
        assert step._value_changed is False


class TestSteps:
    """Tests for the Steps deque."""

    def test_back_one_returns_item(self) -> None:
        """Test back_one returns the popped item."""
        steps = Steps([1, 2, 3])
        assert steps.back_one() == 3
        assert len(steps) == 2

    def test_back_one_empty(self) -> None:
        """Test back_one returns None when empty."""
        steps = Steps()
        assert steps.back_one() is None

    def test_current(self) -> None:
        """Test current returns last item."""
        steps = Steps([1, 2, 3])
        assert steps.current == 3

    def test_previous(self) -> None:
        """Test previous returns second-to-last item."""
        steps = Steps([1, 2, 3])
        assert steps.previous == 2
