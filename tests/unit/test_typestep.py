"""Tests for TypeStep class."""

from dataclasses import dataclass

from ansible_navigator.steps import TypedStep


# Test dataclass

@dataclass
class TSTestClass:
    """A dataclass for testing TypedStep @property and @setter functions.

    :attr attr_1: Test integer
    :attr attr_2: Test string
    """

    attr_1: int
    attr_2: str


# Select a test index for @property index test
TEST_INDEX = 5

# Dataclass objects contained in value attr for @value.setter test
value_1 = TSTestClass(attr_1=1, attr_2="test element 1")
value_2 = TSTestClass(attr_1=3, attr_2="test element 2")

# TypedStep object for all tests
TypedStepTest1 = TypedStep[TSTestClass](name="test_menu", step_type="menu")


def test_property_setters():
    """Test for TypedStep @properties and setters."""
    # Test @changed.setter
    assert TypedStepTest1.changed is False
    TypedStepTest1.changed = True
    assert TypedStepTest1.changed is True

    # Reset
    TypedStepTest1.changed = False
    assert TypedStepTest1.changed is False

    # Test @value.setter and @changed
    TypedStepTest1.value = [value_1, value_2]
    assert TypedStepTest1.value == [value_1, value_2]
    assert TypedStepTest1.changed is True

    # Reset
    TypedStepTest1.changed = False
    assert TypedStepTest1.changed is False

    # Test @index and @index.setter and changed
    TypedStepTest1.index = TEST_INDEX
    assert TypedStepTest1.index == TEST_INDEX
    assert TypedStepTest1.changed is True


def test_property_selected():
    """Test for TypedStep @property selected()."""
    assert TypedStepTest1.selected == value_2
