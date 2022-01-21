"""Unit tests for the inventory action.
"""
import curses

from ansible_navigator.actions.inventory import color_menu
from ansible_navigator.actions.inventory import content_heading
from ansible_navigator.actions.inventory import filter_content_keys
from ansible_navigator.ui_framework.curses_defs import CursesLinePart


def test_color_menu_true():
    """test color menu for a val set to the default"""
    assert color_menu(0, "__name", {}) == (10, 0)
    assert color_menu(0, "__taxonomy", {}) == (11, 0)
    assert color_menu(0, "description", {}) == (12, 0)
    assert color_menu(0, "__type", {"__type": ""}) == (12, 0)
    assert color_menu(0, "__type", {"__type": "group"}) == (11, 0)
    assert color_menu(0, "", {"__name": True}) == (14, 0)


def test_content_heading_true():
    """test menu generation for a defaulted value"""
    curses.initscr()
    curses.start_color()
    line_length = 100
    inventory_hostname = "host01"
    ansible_platform = "test"
    obj = {
        "__name": "testhost",
        "__taxonomy": "all",
        "__type": "group",
        "inventory_hostname": inventory_hostname,
        "ansible_platform": ansible_platform,
    }
    heading = content_heading(obj, line_length)
    assert len(heading) == 1
    assert len(heading[0]) == 1
    assert isinstance(heading[0][0], CursesLinePart)
    assert len(heading[0][0].string) == line_length + 1
    assert f"[{inventory_hostname}] {ansible_platform}" in heading[0][0].string
    assert heading[0][0].color == curses.color_pair(curses.COLOR_BLACK)
    assert heading[0][0].column == 0


def test_filter_content_keys() -> None:
    """test filtering keys"""
    obj = {"__key": "value", "key": "value"}
    ret = {"key": "value"}
    assert filter_content_keys(obj) == ret
