"""Unit tests for the ``config`` action."""

import curses

from copy import deepcopy

import pytest

from ansible_navigator.actions.config import Action as action
from ansible_navigator.actions.config import color_menu
from ansible_navigator.actions.config import content_heading
from ansible_navigator.actions.config import filter_content_keys
from ansible_navigator.cli import NavigatorConfiguration
from ansible_navigator.ui_framework.curses_defs import CursesLinePart


def test_config_color_menu_true() -> None:
    """Test color menu for a val set to the default."""
    entry = {"default": True}
    assert color_menu(0, "", entry) == (2, 0)


def test_config_color_menu_false() -> None:
    """Test color menu for a val not set to default."""
    entry = {"default": False}
    assert color_menu(0, "", entry) == (3, 0)


def test_config_content_heading_true() -> None:
    """Test menu generation for a defaulted value."""
    curses.initscr()
    curses.start_color()
    line_length = 100
    default_value = "default_value"
    obj = {
        "default": True,
        "current_value": default_value,
        "default_value": default_value,
        "name": "Test option",
    }
    heading = content_heading(obj, line_length)
    assert heading
    assert len(heading) == 1
    assert len(heading[0]) == 1
    assert isinstance(heading[0][0], CursesLinePart)
    assert len(heading[0][0].string) == line_length + 1
    assert f"Test option (current/default: {default_value})" in heading[0][0].string
    assert heading[0][0].color == curses.COLOR_GREEN
    assert heading[0][0].column == 0


def test_config_content_heading_false() -> None:
    """Test menu generation for a value not default."""
    curses.initscr()
    curses.start_color()
    line_length = 100
    current_value = "current_value"
    default_value = "default_value"
    obj = {
        "default": False,
        "current_value": current_value,
        "default_value": default_value,
        "name": "Test option",
    }
    heading = content_heading(obj, line_length)
    assert heading
    assert len(heading) == 1
    assert len(heading[0]) == 1
    assert isinstance(heading[0][0], CursesLinePart)
    assert len(heading[0][0].string) == line_length + 1
    assert (
        f"Test option (current: {current_value})  (default: {default_value})"
        in heading[0][0].string
    )
    assert heading[0][0].color == curses.COLOR_YELLOW
    assert heading[0][0].column == 0


def test_config_filter_content_keys() -> None:
    """Test filtering keys."""
    obj = {"__key": "value", "key": "value"}
    ret = {"key": "value"}
    assert filter_content_keys(obj) == ret


@pytest.mark.parametrize(
    ("list_output", "dump_output", "expected_config"),
    (
        pytest.param(
            """GALAXY_SERVERS:""",
            "",
            [],
        ),
        pytest.param(
            "{}",
            "\n\nSOME_VAR(default) = some_value",
            [],
        ),
    ),
    ids=[
        "output_with_galaxy_server",
        "empty_output_with_some_var_dump",
    ],
)
def test_parse_and_merge(
    list_output: str,
    dump_output: str,
    expected_config: list[str],
) -> None:
    """Test _parse_and_merge method of config class."""
    args = deepcopy(NavigatorConfiguration)
    run_action = action(args=args)
    run_action._parse_and_merge(list_output, dump_output)

    assert run_action._config == expected_config

    if "GALAXY_SERVERS" in list_output:
        assert not any(config.get("option") == "GALAXY_SERVERS" for config in run_action._config)
