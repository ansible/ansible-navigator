"""Tests for the ansi module."""

from __future__ import annotations

import pytest

from ansible_navigator.utils.ansi import blank_line
from ansible_navigator.utils.ansi import changed
from ansible_navigator.utils.ansi import failed
from ansible_navigator.utils.ansi import info
from ansible_navigator.utils.ansi import prompt_enter
from ansible_navigator.utils.ansi import prompt_yn
from ansible_navigator.utils.ansi import subtle
from ansible_navigator.utils.ansi import success
from ansible_navigator.utils.ansi import warning
from ansible_navigator.utils.ansi import working
from ansible_navigator.utils.definitions import Color


def test_changed_with_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test changed output with color enabled."""
    changed(color=True, message="something changed")
    captured = capsys.readouterr()
    assert Color.YELLOW in captured.out
    assert "something changed" in captured.out
    assert Color.END in captured.out


def test_changed_without_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test changed output without color."""
    changed(color=False, message="something changed")
    captured = capsys.readouterr()
    assert captured.out.strip() == "something changed"
    assert Color.YELLOW not in captured.out


def test_failed_with_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test failed output with color enabled."""
    failed(color=True, message="it failed")
    captured = capsys.readouterr()
    assert Color.RED in captured.out
    assert "it failed" in captured.out


def test_failed_without_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test failed output without color."""
    failed(color=False, message="it failed")
    assert capsys.readouterr().out.strip() == "it failed"


def test_info_with_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test info output with color enabled."""
    info(color=True, message="some info")
    captured = capsys.readouterr()
    assert Color.CYAN in captured.out
    assert "some info" in captured.out


def test_info_without_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test info output without color."""
    info(color=False, message="some info")
    assert capsys.readouterr().out.strip() == "some info"


def test_subtle_with_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test subtle output with color enabled."""
    subtle(color=True, message="subtle msg")
    captured = capsys.readouterr()
    assert Color.GREY in captured.out
    assert "subtle msg" in captured.out


def test_subtle_without_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test subtle output without color."""
    subtle(color=False, message="subtle msg")
    assert capsys.readouterr().out.strip() == "subtle msg"


def test_success_with_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test success output with color enabled."""
    success(color=True, message="it worked")
    captured = capsys.readouterr()
    assert Color.GREEN in captured.out
    assert "it worked" in captured.out


def test_success_without_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test success output without color."""
    success(color=False, message="it worked")
    assert capsys.readouterr().out.strip() == "it worked"


def test_warning_with_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test warning output with color enabled."""
    warning(color=True, message="be careful")
    captured = capsys.readouterr()
    assert Color.YELLOW in captured.out
    assert "be careful" in captured.out


def test_warning_without_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test warning output without color."""
    warning(color=False, message="be careful")
    assert capsys.readouterr().out.strip() == "be careful"


def test_working_with_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test working output with color enabled."""
    working(color=True, message="processing")
    captured = capsys.readouterr()
    assert Color.GREY in captured.out
    assert "processing" in captured.out


def test_working_without_color(capsys: pytest.CaptureFixture[str]) -> None:
    """Test working output without color."""
    working(color=False, message="processing")
    assert capsys.readouterr().out.strip() == "processing"


def test_blank_line(capsys: pytest.CaptureFixture[str]) -> None:
    """Test blank line output."""
    blank_line()
    assert capsys.readouterr().out == "\n"


def test_prompt_enter(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test prompt_enter with normal input."""
    monkeypatch.setattr("builtins.input", lambda _: "")
    prompt_enter()


def test_prompt_enter_keyboard_interrupt(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test prompt_enter exits on KeyboardInterrupt."""

    def raise_keyboard_interrupt(_: str) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", raise_keyboard_interrupt)
    with pytest.raises(SystemExit) as exc_info:
        prompt_enter()
    assert exc_info.value.code == 0


def test_prompt_yn_yes(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test prompt_yn returns True for 'y'."""
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert prompt_yn("Continue?") is True


def test_prompt_yn_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test prompt_yn returns True for empty input (default yes)."""
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert prompt_yn("Continue?") is True


def test_prompt_yn_no(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test prompt_yn returns False for 'n'."""
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert prompt_yn("Continue?") is False


def test_prompt_yn_keyboard_interrupt(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test prompt_yn exits on KeyboardInterrupt."""

    def raise_keyboard_interrupt(_: str) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", raise_keyboard_interrupt)
    with pytest.raises(SystemExit) as exc_info:
        prompt_yn("Continue?")
    assert exc_info.value.code == 0
