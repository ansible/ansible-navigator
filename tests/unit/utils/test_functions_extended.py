"""Tests for additional functions in the functions module."""

from __future__ import annotations

import shutil

from typing import TYPE_CHECKING
from unittest.mock import patch  # pylint: disable=preferred-module

import pytest

from ansible_navigator.utils.functions import check_for_ansible
from ansible_navigator.utils.functions import check_playbook_type
from ansible_navigator.utils.functions import clear_screen
from ansible_navigator.utils.functions import console_width
from ansible_navigator.utils.functions import dispatch
from ansible_navigator.utils.functions import divmod_int
from ansible_navigator.utils.functions import escape_moustaches
from ansible_navigator.utils.functions import is_jinja
from ansible_navigator.utils.functions import pascal_to_snake
from ansible_navigator.utils.functions import remove_ansi
from ansible_navigator.utils.functions import remove_dbl_un
from ansible_navigator.utils.functions import shlex_join
from ansible_navigator.utils.functions import str2bool
from ansible_navigator.utils.functions import templar
from ansible_navigator.utils.functions import time_stamp_for_file
from ansible_navigator.utils.functions import timestamp_to_iso
from ansible_navigator.utils.functions import to_list


if TYPE_CHECKING:
    from pathlib import Path


def test_check_for_ansible_found(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test check_for_ansible when ansible-playbook is found."""
    monkeypatch.setattr(shutil, "which", lambda _: "/usr/bin/ansible-playbook")
    messages, exit_messages = check_for_ansible()
    assert len(messages) == 1
    assert not exit_messages
    assert "found at" in messages[0].message


def test_check_for_ansible_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test check_for_ansible when ansible-playbook is not found."""
    monkeypatch.setattr(shutil, "which", lambda _: None)
    messages, exit_messages = check_for_ansible()
    assert not messages
    assert len(exit_messages) == 1
    assert "could not be found" in exit_messages[0].message


def test_check_playbook_type_file(tmp_path: Path) -> None:
    """Test check_playbook_type with an existing file."""
    playbook = tmp_path / "playbook.yml"
    playbook.write_text("---")
    assert check_playbook_type(str(playbook)) == "file"


def test_check_playbook_type_missing() -> None:
    """Test check_playbook_type with a missing file."""
    assert check_playbook_type("/nonexistent/playbook.yml") == "missing"


def test_check_playbook_type_fqcn() -> None:
    """Test check_playbook_type with an FQCN playbook."""
    assert check_playbook_type("namespace.collection.playbook") == "fqcn"


def test_clear_screen_vscode(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test clear_screen prints blank lines in vscode terminal."""
    monkeypatch.setenv("TERM_PROGRAM", "vscode")
    fake_size = type("TermSize", (), {"lines": 5, "columns": 80})()
    with patch(
        "ansible_navigator.utils.functions.shutil.get_terminal_size", return_value=fake_size
    ):
        clear_screen()
    captured = capsys.readouterr()
    assert captured.out.count("\n") == 5


def test_clear_screen_normal(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test clear_screen does nothing in normal terminal."""
    monkeypatch.setenv("TERM_PROGRAM", "xterm")
    clear_screen()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_console_width_small() -> None:
    """Test console_width with small terminal."""
    fake_size = type("TermSize", (), {"columns": 60})()
    with patch(
        "ansible_navigator.utils.functions.shutil.get_terminal_size", return_value=fake_size
    ):
        assert console_width() == 60


def test_console_width_medium() -> None:
    """Test console_width with medium terminal."""
    fake_size = type("TermSize", (), {"columns": 120})()
    with patch(
        "ansible_navigator.utils.functions.shutil.get_terminal_size", return_value=fake_size
    ):
        result = console_width()
    assert 80 <= result <= 120


def test_console_width_large() -> None:
    """Test console_width with large terminal."""
    fake_size = type("TermSize", (), {"columns": 200})()
    with patch(
        "ansible_navigator.utils.functions.shutil.get_terminal_size", return_value=fake_size
    ):
        assert console_width() == 132


def test_dispatch_string() -> None:
    """Test dispatch with string replacement."""
    result = dispatch("hello world", (("hello", "hi"),))
    assert result == "hi world"


def test_dispatch_list() -> None:
    """Test dispatch with list."""
    result = dispatch(["hello", "world"], (("hello", "hi"),))
    assert result == ["hi", "world"]


def test_dispatch_dict() -> None:
    """Test dispatch with dict."""
    result = dispatch({"key": "hello"}, (("hello", "hi"),))
    assert result == {"key": "hi"}


def test_dispatch_nested() -> None:
    """Test dispatch with nested structure."""
    result = dispatch({"a": ["hello"]}, (("hello", "hi"),))
    assert result == {"a": ["hi"]}


def test_dispatch_non_string() -> None:
    """Test dispatch with non-string value."""
    result = dispatch(42, (("hello", "hi"),))
    assert result == 42


def test_escape_moustaches() -> None:
    """Test escape_moustaches replaces braces."""
    result = escape_moustaches({"key": "{{ value }}"})
    assert "U+007B" in str(result)
    assert "{" not in result["key"]


def test_escape_moustaches_nested() -> None:
    """Test escape_moustaches with nested dict."""
    result = escape_moustaches({"a": {"b": "{test}"}})
    assert "U+007B" in str(result)


def test_is_jinja_true() -> None:
    """Test is_jinja with jinja template."""
    assert is_jinja("{{ variable }}") is True


def test_is_jinja_false() -> None:
    """Test is_jinja with plain string."""
    assert is_jinja("no jinja here") is False


def test_is_jinja_incomplete() -> None:
    """Test is_jinja with incomplete template."""
    assert is_jinja("{{ incomplete") is False


def test_pascal_to_snake_string() -> None:
    """Test pascal_to_snake with a plain string (no conversion)."""
    assert pascal_to_snake("hello") == "hello"


def test_pascal_to_snake_dict() -> None:
    """Test pascal_to_snake with dict keys."""
    result = pascal_to_snake({"MyKey": "value", "AnotherKey": "val2"})
    assert result == {"my_key": "value", "another_key": "val2"}


def test_pascal_to_snake_list() -> None:
    """Test pascal_to_snake with list of dicts."""
    result = pascal_to_snake([{"MyKey": "value"}])
    assert result == [{"my_key": "value"}]


def test_pascal_to_snake_nested() -> None:
    """Test pascal_to_snake with nested dicts."""
    result = pascal_to_snake({"OuterKey": {"InnerKey": "value"}})
    assert result == {"outer_key": {"inner_key": "value"}}


def test_remove_ansi() -> None:
    """Test remove_ansi strips ANSI codes."""
    ansi_string = "\033[31mred text\033[0m"
    assert remove_ansi(ansi_string) == "red text"


def test_remove_ansi_no_codes() -> None:
    """Test remove_ansi with no ANSI codes."""
    assert remove_ansi("plain text") == "plain text"


def test_remove_ansi_complex() -> None:
    """Test remove_ansi with complex ANSI sequences."""
    ansi_string = "\033[38;2;255;0;0mcolored\033[m"
    assert remove_ansi(ansi_string) == "colored"


def test_remove_dbl_un_with_prefix() -> None:
    """Test remove_dbl_un with __ prefix."""
    assert remove_dbl_un("__name") == "name"


def test_remove_dbl_un_without_prefix() -> None:
    """Test remove_dbl_un without __ prefix."""
    assert remove_dbl_un("name") == "name"


def test_remove_dbl_un_single_underscore() -> None:
    """Test remove_dbl_un with single underscore."""
    assert remove_dbl_un("_name") == "_name"


def test_str2bool_true_values() -> None:
    """Test str2bool with truthy strings."""
    assert str2bool("yes") is True
    assert str2bool("true") is True
    assert str2bool("YES") is True
    assert str2bool("True") is True
    assert str2bool(True) is True


def test_str2bool_false_values() -> None:
    """Test str2bool with falsy strings."""
    assert str2bool("no") is False
    assert str2bool("false") is False
    assert str2bool("NO") is False
    assert str2bool(False) is False


def test_str2bool_invalid() -> None:
    """Test str2bool with invalid value."""
    with pytest.raises(ValueError, match="maybe"):
        str2bool("maybe")


def test_str2bool_int() -> None:
    """Test str2bool with non-bool non-string."""
    with pytest.raises(ValueError, match="42"):
        str2bool(42)


def test_templar_simple() -> None:
    """Test templar with simple template."""
    errors, result = templar("Hello {{ name }}", {"name": "world"})
    assert not errors
    assert result == "Hello world"


def test_templar_error() -> None:
    """Test templar with undefined variable."""
    errors, _result = templar("{{ undefined_var }}", {})
    assert len(errors) > 0


def test_templar_with_moustaches_in_vars() -> None:
    """Test templar with braces in template vars."""
    errors, result = templar("{{ name }}", {"name": "test", "other": "{{ jinja }}"})
    assert not errors
    assert result == "test"


def test_timestamp_to_iso_local() -> None:
    """Test timestamp_to_iso with local timezone."""
    result = timestamp_to_iso(0, "local")
    assert result is not None
    assert "T" in result


def test_timestamp_to_iso_utc() -> None:
    """Test timestamp_to_iso with UTC timezone."""
    result = timestamp_to_iso(0, "UTC")
    assert result is not None
    assert "1970" in result


def test_timestamp_to_iso_invalid_tz() -> None:
    """Test timestamp_to_iso with invalid timezone."""
    result = timestamp_to_iso(0, "Invalid/Zone")
    assert result is None


def test_time_stamp_for_file_exists(tmp_path: Path) -> None:
    """Test time_stamp_for_file with existing file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    modified, iso_stamp = time_stamp_for_file(str(test_file), "UTC")
    assert modified is not None
    assert iso_stamp is not None


def test_time_stamp_for_file_missing() -> None:
    """Test time_stamp_for_file with missing file."""
    modified, iso_stamp = time_stamp_for_file("/nonexistent/file", "UTC")
    assert modified is None
    assert iso_stamp is None


def test_to_list_string() -> None:
    """Test to_list with a string."""
    assert to_list("hello") == ["hello"]


def test_to_list_list() -> None:
    """Test to_list with a list."""
    assert to_list([1, 2, 3]) == [1, 2, 3]


def test_to_list_tuple() -> None:
    """Test to_list with a tuple."""
    assert to_list(("a",)) == ["a"]


def test_to_list_set() -> None:
    """Test to_list with a set."""
    result = to_list({1})
    assert result == [1]


def test_to_list_none() -> None:
    """Test to_list with None."""
    assert not to_list(None)


def test_divmod_int() -> None:
    """Test divmod_int returns integers."""
    q, r = divmod_int(10.0, 3.0)
    assert q == 3
    assert r == 1
    assert isinstance(q, int)
    assert isinstance(r, int)


def test_shlex_join() -> None:
    """Test shlex_join concatenates tokens."""
    result = shlex_join(["echo", "hello world"])
    assert result == "echo 'hello world'"
