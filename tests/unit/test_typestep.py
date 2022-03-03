"""Tests for TypeStep class."""

from dataclasses import dataclass

import pytest

from ansible_navigator.steps import StepType
from ansible_navigator.steps import TypedStep


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


@pytest.fixture(name="test_step")
def _test_step():
    """Instantiate and set default attribute values for TypedStep test object.

    :returns: Test fixture
    """
    test_step = TypedStep[TSTestClass](name="test", step_type=StepType.MENU)
    test_step.value = [value_1, value_2]
    test_step.value = [value_1, value_2]  # produce it "unchanged"
    test_step.index = 0
    test_step.index = 0  # produce it "unchanged"
    return test_step


def test_fixture(test_step):
    """Base test fixture test for the other tests.

    :param test_step: Test fixture
    """
    assert not test_step.changed
    assert test_step.index == 0
    assert test_step.value == [value_1, value_2]
    assert test_step.selected == value_1


def test_index(test_step):
    """Testing @property index and index.setter.

    :param test_step: Test fixture
    """
    test_step.index = 1
    assert test_step.index == 1
    assert test_step.changed
    test_step.index = 1
    assert test_step.index == 1
    assert not test_step.changed
    test_step.index = 2
    assert test_step.index == 2
    assert test_step.changed


def test_selected(test_step):
    """Testing @property selected.

    :param test_step: Test fixture
    """
    test_step.index = 1
    assert test_step.selected == value_2
    test_step.index = 2
    assert test_step.selected == value_1


def test_value(test_step):
    """Testing @property value and value.setter.

    :param test_step: Test fixture
    """
    assert not test_step.changed
    test_step.value = [value_2, value_2]
    assert test_step.value == [value_2, value_2]
    assert test_step.changed
    test_step.value = [value_2, value_2]
    assert test_step.value == [value_2, value_2]
    assert not test_step.changed
