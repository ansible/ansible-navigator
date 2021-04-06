""" config tests
"""
import curses
import re
import sys
import tempfile

from argparse import Namespace

from typing import Any
from typing import List
from typing import Tuple

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


# some common funcs for the tests


def callable_pass():
    """a do nothing callable"""


def run_action_stdout(name: str, cmdline: List) -> Tuple[Any, str, str]:
    """run the action"""
    args = Namespace(
        container_engine=None,
        execution_environment=None,
        ee_image=None,
        mode="stdout",
        cmdline=cmdline,
    )
    action = Action(args=args)
    steps = Steps()
    app = AppPublic(
        args=args,
        name="test_app",
        rerun=callable_pass,
        stdout=[],
        steps=steps,
        update=callable_pass,
        write_artifact=callable_pass,
    )

    user_interface = Ui(
        clear=callable_pass,
        menu_filter=callable_pass,
        scroll=callable_pass,
        show=callable_pass,
        update_status=callable_pass,
        xform=callable_pass,
    )
    match = re.match(Action.KEGEX, name)
    if not match:
        raise ValueError

    ui_action = Ui_action(match=match, value=name)
    interaction = Interaction(name="test", ui=user_interface, action=ui_action)

    # preserve current stdin, stdout, stderr
    __stdin__ = sys.stdin
    __stdout__ = sys.stdout
    __stderr__ = sys.stderr

    # pytest psuedo stdin doesn't fileno(), use original
    sys.stdin = sys.__stdin__

    # set stderr and stdout to fds
    sys.stdout = tempfile.TemporaryFile()  # type: ignore
    sys.stderr = tempfile.TemporaryFile()  # type: ignore

    # run the action
    result = action.run(interaction=interaction, app=app)

    # restore stdin
    sys.stdin = __stdin__

    # read and restore stdout
    sys.stdout.seek(0)
    stdout = sys.stdout.read().decode()  # type: ignore
    sys.stdout = __stdout__

    # read and restore stderr
    sys.stderr.seek(0)
    stderr = sys.stderr.read().decode()  # type: ignore
    sys.stderr = __stderr__

    return result, stdout, stderr


# individual tests to follow


def test_color_menu_true():
    """test color menu for a val set to the default"""
    entry = {"__default": True}
    assert color_menu(0, "", entry) == 2


def test_color_menu_false():
    """test color menu for a val not set to default"""
    entry = {"__default": False}
    assert color_menu(0, "", entry) == 3


def test_content_heading_true():
    """test menu generation for a defaulted value"""
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


def test_content_heading_false() -> None:
    """test menu generation for a value not default"""
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
    assert heading
    assert len(heading) == 1
    assert len(heading[0]) == 1
    assert isinstance(heading[0][0], CursesLinePart)
    assert len(heading[0][0].string) == line_length + 1
    assert f"test option (current: {current})  (default: {default})" in heading[0][0].string
    assert heading[0][0].color == curses.color_pair(curses.COLOR_YELLOW)
    assert heading[0][0].column == 0


def test_filter_content_keys() -> None:
    """test filtering keys"""
    obj = {"__key": "value", "key": "value"}
    ret = {"key": "value"}
    assert filter_content_keys(obj) == ret


def test_run_stdout_dump() -> None:
    """test config dump to stdout"""
    result, stdout, _stderr = run_action_stdout("config", ["dump"])
    assert result is None
    assert "ACTION_WARNING" in stdout
    # TODO: handle DECRECATION WARNINGS
    # assert stderr == ""


def test_run_stdout_list() -> None:
    """test config list to stdout"""
    result, stdout, _stderr = run_action_stdout("config", ["list"])
    assert result is None
    assert "ACTION_WARNING" in stdout
    # TODO: handle DECRECATION WARNINGS
    # assert stderr == ""
