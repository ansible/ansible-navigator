import curses
import re

from argparse import Namespace

from ansible_navigator.app_public import AppPublic

from ansible_navigator.actions.config import Action
from ansible_navigator.actions.config import color_menu
from ansible_navigator.actions.config import content_heading
from ansible_navigator.actions.config import filter_content_keys

from ansible_navigator.ui_framework.curses_defs import CursesLinePart

from ansible_navigator.ui_framework.ui import Action as Ui_action
from ansible_navigator.ui_framework.ui import Interaction
from ansible_navigator.ui_framework.ui import Ui

from ansible_navigator.steps import Steps


def test_color_menu_true():
    entry = {"__default": True}
    assert color_menu(0, "", entry) == 2


def test_color_menu_false():
    entry = {"__default": False}
    assert color_menu(0, "", entry) == 3


def test_content_heading_true():
    curses.initscr()
    curses.start_color()
    line_length = 100
    default = "dval"
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
    assert heading[0][0].color == curses.color_pair(curses.COLOR_GREEN)
    assert heading[0][0].column == 0


def test_content_heading_false():
    curses.initscr()
    curses.start_color()
    line_length = 100
    current = "cval"
    default = "dval"
    obj = {
        "__default": False,
        "__current_value": current,
        "default": default,
        "option": "test_option",
    }
    heading = content_heading(obj, line_length)
    assert len(heading) == 1
    assert len(heading[0]) == 1
    assert isinstance(heading[0][0], CursesLinePart)
    assert len(heading[0][0].string) == line_length + 1
    assert f"test option (current: {current})  (default: {default})" in heading[0][0].string
    assert heading[0][0].color == curses.color_pair(curses.COLOR_YELLOW)
    assert heading[0][0].column == 0


def test_filter_content_keys():
    obj = {"__key": "value", "key": "value"}
    ret = {"key": "value"}
    assert filter_content_keys(obj) == ret


def callable_pass():
    pass


def test_run():
    args = Namespace(
        container_engine=None,
        execution_environment=None,
        ee_image=None,
        navigator_mode="stdout",
        cmdline="",
    )
    steps = Steps()
    action = Action(args=args)
    app = AppPublic(
        args=args,
        name="test_app",
        rerun=callable_pass,
        stdout=[],
        steps=steps,
        update=callable_pass,
        write_artifact=callable_pass,
    )

    ui = Ui(
        clear=callable_pass,
        menu_filter=callable_pass,
        scroll=callable_pass,
        show=callable_pass,
        update_status=callable_pass,
        xform=callable_pass,
    )
    ui_action = Ui_action(match=re.match(Action.KEGEX, "config"), value="config")
    interaction = Interaction(name="test", ui=ui, action=ui_action)
    result = action.run(interaction=interaction, app=app)
    assert result is None
