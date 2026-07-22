"""Tests for pure helper functions in colorize module."""

from __future__ import annotations

import pytest

from ansible_navigator.ui_framework.colorize import _rgb_to_ansi_16
from ansible_navigator.ui_framework.colorize import _rgb_to_ansi_256


class TestRgbToAnsi256:
    """Tests for _rgb_to_ansi_256."""

    def test_black(self) -> None:
        """Pure black (0,0,0) maps to color 16."""
        assert _rgb_to_ansi_256(0, 0, 0) == 16

    def test_white(self) -> None:
        """Pure white (255,255,255) maps to color 231."""
        assert _rgb_to_ansi_256(255, 255, 255) == 231

    def test_mid_grey_grayscale(self) -> None:
        """A mid-grey value falls in the grayscale ramp (232-255)."""
        result = _rgb_to_ansi_256(128, 128, 128)
        assert 232 <= result <= 255

    def test_pure_red(self) -> None:
        """Pure red (255,0,0) maps to 196 in the 6x6x6 cube."""
        assert _rgb_to_ansi_256(255, 0, 0) == 196

    def test_pure_green(self) -> None:
        """Pure green (0,255,0) maps to 46 in the 6x6x6 cube."""
        assert _rgb_to_ansi_256(0, 255, 0) == 46

    def test_pure_blue(self) -> None:
        """Pure blue (0,0,255) maps to 21 in the 6x6x6 cube."""
        assert _rgb_to_ansi_256(0, 0, 255) == 21

    @pytest.mark.parametrize(
        ("red", "green", "blue"),
        (
            (0, 0, 0),
            (128, 128, 128),
            (255, 255, 255),
        ),
    )
    def test_grayscale_values_are_in_range(
        self,
        red: int,
        green: int,
        blue: int,
    ) -> None:
        """Equal RGB values should map to the grayscale range or boundary colors.

        Args:
            red: Red component.
            green: Green component.
            blue: Blue component.
        """
        result = _rgb_to_ansi_256(red, green, blue)
        assert 16 <= result <= 255


class TestRgbToAnsi16:
    """Tests for _rgb_to_ansi_16."""

    def test_black(self) -> None:
        """Pure black (0,0,0) maps to 30 (ANSI black foreground)."""
        assert _rgb_to_ansi_16(0, 0, 0) == 30

    def test_white(self) -> None:
        """Pure white (255,255,255) maps to 7 (standard white foreground)."""
        assert _rgb_to_ansi_16(255, 255, 255) == 7

    def test_returns_int(self) -> None:
        """Return type is always int."""
        result = _rgb_to_ansi_16(100, 150, 200)
        assert isinstance(result, int)
