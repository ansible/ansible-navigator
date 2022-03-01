"""Tests for TypeStep class."""

from ansible_navigator.steps import TypedStep

# Test variables

# Select a test index for @property index test
TEST_INDEX = 1

# TypedStep object for all tests
TypedStepTest = TypedStep(name="test_menu", step_type="menu")

# TypedStep objects contained in test_value list for @value.setter test
TypedStep1 = TypedStep(name="test_element_one", step_type="menu")
TypedStep2 = TypedStep(name="test_element_two", step_type="menu")
test_value_list = [TypedStep1, TypedStep2]


def test_property_changed():
    """Test for TypedStep @property changed() and setter."""
    assert TypedStepTest.changed is False
    TypedStepTest.changed = True
    assert TypedStepTest.changed is True


def test_property_index():
    """Test for TypedStep @property index() and setter."""
    assert TypedStepTest.index is None
    TypedStepTest.index = TEST_INDEX
    assert TypedStepTest.index == TEST_INDEX


def test_property_value():
    """Test for TypedStep @property value() and setter."""
    TypedStepTest.value = test_value_list
    assert TypedStepTest.value == test_value_list


def test_property_selected():
    """Test for TypedStep @property selected()."""
    assert TypedStepTest.selected == TypedStep2
