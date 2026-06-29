"""Tests for the definitions module."""

from __future__ import annotations

import logging

from ansible_navigator.utils.definitions import Color
from ansible_navigator.utils.definitions import Decoration
from ansible_navigator.utils.definitions import ExitMessage
from ansible_navigator.utils.definitions import ExitMessages
from ansible_navigator.utils.definitions import ExitPrefix
from ansible_navigator.utils.definitions import LogMessage


class TestExitPrefix:
    """Tests for the ExitPrefix enum."""

    def test_error_value(self) -> None:
        """Test ERROR prefix value."""
        assert ExitPrefix.ERROR.value == "Error"

    def test_hint_value(self) -> None:
        """Test HINT prefix value."""
        assert ExitPrefix.HINT.value == "Hint"

    def test_note_value(self) -> None:
        """Test NOTE prefix value."""
        assert ExitPrefix.NOTE.value == "Note"

    def test_warning_value(self) -> None:
        """Test WARNING prefix value."""
        assert ExitPrefix.WARNING.value == "Warning"

    def test_str_format(self) -> None:
        """Test string formatting includes aligned prefix."""
        result = str(ExitPrefix.ERROR)
        assert "Error:" in result

    def test_longest_formatted(self) -> None:
        """Test longest_formatted returns an integer."""
        result = ExitPrefix.longest_formatted()
        assert isinstance(result, int)
        assert result > 0


class TestExitMessage:
    """Tests for the ExitMessage dataclass."""

    def test_default_prefix(self) -> None:
        """Test default prefix is ERROR."""
        msg = ExitMessage(message="test")
        assert msg.prefix == ExitPrefix.ERROR

    def test_color_property(self) -> None:
        """Test color property returns a color string."""
        msg = ExitMessage(message="test", prefix=ExitPrefix.ERROR)
        assert msg.color == Color.RED

    def test_color_hint(self) -> None:
        """Test hint color."""
        msg = ExitMessage(message="test", prefix=ExitPrefix.HINT)
        assert msg.color == Color.CYAN

    def test_color_note(self) -> None:
        """Test note color."""
        msg = ExitMessage(message="test", prefix=ExitPrefix.NOTE)
        assert msg.color == Color.GREEN

    def test_color_warning(self) -> None:
        """Test warning color."""
        msg = ExitMessage(message="test", prefix=ExitPrefix.WARNING)
        assert msg.color == Color.YELLOW

    def test_level_error(self) -> None:
        """Test level for error messages."""
        msg = ExitMessage(message="test", prefix=ExitPrefix.ERROR)
        assert msg.level == logging.ERROR

    def test_level_hint(self) -> None:
        """Test level for hint messages."""
        msg = ExitMessage(message="test", prefix=ExitPrefix.HINT)
        assert msg.level == logging.INFO

    def test_level_warning(self) -> None:
        """Test level for warning messages."""
        msg = ExitMessage(message="test", prefix=ExitPrefix.WARNING)
        assert msg.level == logging.WARNING

    def test_to_lines_with_color(self) -> None:
        """Test to_lines with color enabled."""
        msg = ExitMessage(message="test error")
        lines = msg.to_lines(color=True, width=80, with_prefix=True)
        assert len(lines) >= 1
        assert Color.RED in lines[0]
        assert "test error" in lines[0]

    def test_to_lines_without_color(self) -> None:
        """Test to_lines without color."""
        msg = ExitMessage(message="test error")
        lines = msg.to_lines(color=False, width=80, with_prefix=True)
        assert len(lines) >= 1
        assert Color.RED not in lines[0]

    def test_to_lines_without_prefix(self) -> None:
        """Test to_lines without prefix."""
        msg = ExitMessage(message="test error")
        lines = msg.to_lines(color=False, width=80, with_prefix=False)
        assert len(lines) >= 1


class TestExitMessages:
    """Tests for the ExitMessages container."""

    def test_empty_messages(self) -> None:
        """Test with no messages."""
        msgs = ExitMessages()
        result = msgs.to_strings(color=False, width=80)
        assert not result

    def test_single_message(self) -> None:
        """Test with a single message."""
        msgs = ExitMessages(messages=[ExitMessage(message="error1")])
        result = msgs.to_strings(color=False, width=80)
        assert len(result) >= 1
        assert "error1" in result[0]

    def test_multiple_same_prefix(self) -> None:
        """Test with multiple messages of same prefix."""
        msgs = ExitMessages(
            messages=[
                ExitMessage(message="err1"),
                ExitMessage(message="err2"),
            ]
        )
        result = msgs.to_strings(color=False, width=80)
        assert len(result) >= 2

    def test_different_prefixes_with_separator(self) -> None:
        """Test messages with different prefixes get separator."""
        msgs = ExitMessages(
            messages=[
                ExitMessage(message="error", prefix=ExitPrefix.ERROR),
                ExitMessage(message="note", prefix=ExitPrefix.NOTE),
            ]
        )
        result = msgs.to_strings(color=False, width=80)
        assert "" in result

    def test_hint_follows_without_break(self) -> None:
        """Test hint after error doesn't get blank line separator."""
        msgs = ExitMessages(
            messages=[
                ExitMessage(message="error", prefix=ExitPrefix.ERROR),
                ExitMessage(message="try this", prefix=ExitPrefix.HINT),
            ]
        )
        result = msgs.to_strings(color=False, width=80)
        assert "" not in result


class TestLogMessage:
    """Tests for the LogMessage NamedTuple."""

    def test_creation(self) -> None:
        """Test creating a log message."""
        msg = LogMessage(level=logging.INFO, message="test")
        assert msg.level == logging.INFO
        assert msg.message == "test"


class TestColor:
    """Tests for Color constants."""

    def test_has_red(self) -> None:
        """Test RED color exists."""
        assert Color.RED == "\033[31m"

    def test_has_end(self) -> None:
        """Test END color exists."""
        assert Color.END == "\033[0m"


class TestDecoration:
    """Tests for Decoration constants."""

    def test_has_bold(self) -> None:
        """Test BOLD exists."""
        assert Decoration.BOLD == "\033[1m"
