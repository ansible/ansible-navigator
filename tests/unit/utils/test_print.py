"""Tests for the print utility module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import NamedTuple

from ansible_navigator.utils.print import color_bits
from ansible_navigator.utils.print import color_lines


if TYPE_CHECKING:
    import pytest


class MockLinePart(NamedTuple):
    """A mock for SimpleLinePart."""

    color: tuple[int, int, int] | None
    chars: str


class TestColorBits:
    """Tests for the color_bits function."""

    def test_truecolor(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test COLORTERM=truecolor returns 24."""
        monkeypatch.setenv("COLORTERM", "truecolor")
        assert color_bits() == 24

    def test_24bit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test COLORTERM=24bit returns 24."""
        monkeypatch.setenv("COLORTERM", "24bit")
        assert color_bits() == 24

    def test_256color_term(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test TERM=xterm-256color returns 8."""
        monkeypatch.delenv("COLORTERM", raising=False)
        monkeypatch.setenv("TERM", "xterm-256color")
        assert color_bits() == 8

    def test_16color_term(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test TERM=xterm-16color returns 4."""
        monkeypatch.delenv("COLORTERM", raising=False)
        monkeypatch.setenv("TERM", "xterm-16color")
        assert color_bits() == 4

    def test_no_env_vars(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test fallback with no color env vars returns 4."""
        monkeypatch.delenv("COLORTERM", raising=False)
        monkeypatch.delenv("TERM", raising=False)
        assert color_bits() == 4

    def test_plain_term(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test TERM=xterm (no color suffix) returns 4."""
        monkeypatch.delenv("COLORTERM", raising=False)
        monkeypatch.setenv("TERM", "xterm")
        assert color_bits() == 4


class TestColorLines:
    """Tests for the color_lines function."""

    def test_24bit_with_color(self) -> None:
        """Test 24-bit color output."""
        tokenized = [[MockLinePart(color=(255, 0, 0), chars="red")]]
        result = color_lines(24, tokenized)
        assert "\033[38;2;255;0;0m" in result
        assert "red" in result

    def test_24bit_none_color(self) -> None:
        """Test 24-bit with None color defaults to white."""
        tokenized = [[MockLinePart(color=None, chars="text")]]
        result = color_lines(24, tokenized)
        assert "\033[38;2;255;255;255m" in result
        assert "text" in result

    def test_8bit_none_color(self) -> None:
        """Test 8-bit with None color uses ansi_color 1."""
        tokenized = [[MockLinePart(color=None, chars="text")]]
        result = color_lines(8, tokenized)
        assert "\033[38;5;1m" in result

    def test_multiple_parts(self) -> None:
        """Test multiple parts in a line."""
        tokenized = [
            [
                MockLinePart(color=(255, 0, 0), chars="red"),
                MockLinePart(color=(0, 255, 0), chars="green"),
            ]
        ]
        result = color_lines(24, tokenized)
        assert "red" in result
        assert "green" in result

    def test_empty_input(self) -> None:
        """Test empty input."""
        result = color_lines(24, [])
        assert result == ""

    def test_multiple_lines(self) -> None:
        """Test multiple lines."""
        tokenized = [
            [MockLinePart(color=(255, 0, 0), chars="line1")],
            [MockLinePart(color=(0, 0, 255), chars="line2")],
        ]
        result = color_lines(24, tokenized)
        assert "line1" in result
        assert "line2" in result
