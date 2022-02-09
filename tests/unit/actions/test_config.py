"""Unit tests for the ``config`` action.
"""
import curses

from ansible_navigator.actions.config import color_menu
from ansible_navigator.actions.config import content_heading
from ansible_navigator.actions.config import filter_content_keys
from ansible_navigator.ui_framework.curses_defs import CursesLinePart


def test_color_menu_true():
    """test color menu for a val set to the default"""
    entry = {"__default": True}
    assert color_menu(0, "", entry) == (2, 0)


def test_color_menu_false():
    """test color menu for a val not set to default"""
    entry = {"__default": False}
    assert color_menu(0, "", entry) == (3, 0)


def test_content_heading_true():
    """test menu generation for a defaulted value"""
    curses.initscr()
    curses.start_color()
    line_length = 100
    default = "default_value"
    obj = {
        "__default": True,
        "__current_value": default,
        "default": default,
        "option": "test_option",
    }
    heading = content_heading(obj, line_length)
    assert len(heading) == 1
    assert len(heading[0]) == 1
    assert isinstance(heading[0][0], CursesLinePart)
    assert len(heading[0][0].string) == line_length + 1
    assert f"test option (current/default: {default})" in heading[0][0].string
    assert heading[0][0].color == curses.COLOR_GREEN
    assert heading[0][0].column == 0


def test_content_heading_false() -> None:
    """test menu generation for a value not default"""
    curses.initscr()
    curses.start_color()
    line_length = 100
    current = "current_value"
    default = "default_value"
    obj = {
        "__default": False,
        "__current_value": current,
        "default": default,
        "option": "test_option",
    }
    heading = content_heading(obj, line_length)
    assert heading
    assert len(heading) == 1
    assert len(heading[0]) == 1
    assert isinstance(heading[0][0], CursesLinePart)
    assert len(heading[0][0].string) == line_length + 1
    assert f"test option (current: {current})  (default: {default})" in heading[0][0].string
    assert heading[0][0].color == curses.COLOR_YELLOW
    assert heading[0][0].column == 0


def test_filter_content_keys() -> None:
    """test filtering keys"""
    obj = {"__key": "value", "key": "value"}
    ret = {"key": "value"}
    assert filter_content_keys(obj) == ret
