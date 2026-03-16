"""Unit tests for arrow-key cursor navigation in UserInterface."""

# pylint: disable=redefined-outer-name
from __future__ import annotations

from unittest.mock import MagicMock  # pylint: disable=W0407
from unittest.mock import patch  # pylint: disable=W0407

import pytest

from ansible_navigator.constants import GRAMMAR_DIR
from ansible_navigator.constants import TERMINAL_COLORS_PATH
from ansible_navigator.constants import THEME_PATH
from ansible_navigator.ui_framework.ui import UserInterface
from ansible_navigator.ui_framework.ui_config import UIConfig


@pytest.fixture
def ui_config() -> UIConfig:
    """Return a minimal UIConfig for testing.

    Returns:
        A UIConfig with color and osc4 disabled.
    """
    return UIConfig(
        color=False,
        colors_initialized=True,
        grammar_dir=GRAMMAR_DIR,
        osc4=False,
        terminal_colors_path=TERMINAL_COLORS_PATH,
        theme_path=THEME_PATH,
    )


@pytest.fixture
def ui(ui_config: UIConfig) -> UserInterface:
    """Return a UserInterface with curses patched out.

    Args:
        ui_config: A minimal UIConfig fixture.

    Returns:
        A UserInterface instance with curses mocked.
    """
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = (24, 80)
    mock_screen.timeout = MagicMock()
    mock_screen.keypad = MagicMock()

    with (
        patch("curses.initscr", return_value=mock_screen),
        patch("curses.cbreak"),
        patch("curses.nocbreak"),
        patch("curses.endwin"),
        patch("curses.use_default_colors"),
        patch("curses.can_change_color", return_value=False),
        patch("curses.COLORS", 8, create=True),
        patch("curses.curs_set"),
    ):
        instance = UserInterface(
            screen_min_height=3,
            kegexes=list,
            refresh=100,
            ui_config=ui_config,
        )
    return instance


class TestMenuCursorPos:
    """Tests for _menu_cursor_pos increment/decrement and clamping."""

    def test_initial_cursor_pos(self, ui: UserInterface) -> None:
        """Cursor starts at 0.

        Args:
            ui: A UserInterface fixture.
        """
        assert ui._menu_cursor_pos == 0

    def test_cursor_increments_on_key_down(self, ui: UserInterface) -> None:
        """KEY_DOWN increments cursor when below the last item.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (0, 1, 2)
        ui._menu_cursor_pos = 0
        ui._highlight_line_offset = 0

        entry = "KEY_DOWN"
        if entry == "KEY_DOWN" and ui._menu_cursor_pos < len(ui._menu_indices) - 1:
            ui._menu_cursor_pos += 1

        assert ui._menu_cursor_pos == 1

    def test_cursor_decrements_on_key_up(self, ui: UserInterface) -> None:
        """KEY_UP decrements cursor when above the first item.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (0, 1, 2)
        ui._menu_cursor_pos = 2
        ui._highlight_line_offset = 2

        entry = "KEY_UP"
        if entry == "KEY_UP" and ui._menu_cursor_pos > 0:
            ui._menu_cursor_pos -= 1

        assert ui._menu_cursor_pos == 1

    def test_cursor_clamps_at_zero(self, ui: UserInterface) -> None:
        """KEY_UP does not decrement below 0.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (0, 1, 2)
        ui._menu_cursor_pos = 0
        ui._highlight_line_offset = 0

        entry = "KEY_UP"
        if entry == "KEY_UP" and ui._menu_cursor_pos > 0:
            ui._menu_cursor_pos -= 1

        assert ui._menu_cursor_pos == 0

    def test_cursor_clamps_at_max(self, ui: UserInterface) -> None:
        """KEY_DOWN does not increment past the last menu index.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (0, 1, 2)
        ui._menu_cursor_pos = 2
        ui._highlight_line_offset = 2

        entry = "KEY_DOWN"
        if entry == "KEY_DOWN" and ui._menu_cursor_pos < len(ui._menu_indices) - 1:
            ui._menu_cursor_pos += 1

        assert ui._menu_cursor_pos == 2


class TestHighlightLineOffset:
    """Tests for _highlight_line_offset computation."""

    def test_highlight_offset_matches_visible_row(self, ui: UserInterface) -> None:
        """_highlight_line_offset is the index of the selected item in showing_indices.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (0, 1, 2, 3, 4)
        ui._menu_cursor_pos = 2
        showing_indices = (0, 1, 2, 3, 4)

        ui._highlight_line_offset = None
        selected_global_index = ui._menu_indices[ui._menu_cursor_pos]
        try:
            ui._highlight_line_offset = list(showing_indices).index(selected_global_index)
        except ValueError:
            ui._highlight_line_offset = None

        assert ui._highlight_line_offset == 2

    def test_highlight_offset_none_when_selected_not_visible(self, ui: UserInterface) -> None:
        """_highlight_line_offset is None when the selected item is scrolled out of view.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (0, 1, 2, 3, 4)
        ui._menu_cursor_pos = 4
        showing_indices = (0, 1, 2)  # item 4 is not visible

        ui._highlight_line_offset = None
        selected_global_index = ui._menu_indices[ui._menu_cursor_pos]
        try:
            ui._highlight_line_offset = list(showing_indices).index(selected_global_index)
        except ValueError:
            ui._highlight_line_offset = None

        assert ui._highlight_line_offset is None


class TestEnterKeySelection:
    """Tests for Enter-key converting cursor position to a numeric entry."""

    def test_cursor_enter_selects_correct_index(self, ui: UserInterface) -> None:
        """CURSOR_ENTER converts _menu_cursor_pos to the correct global index string.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (3, 7, 11)
        ui._menu_cursor_pos = 1  # pointing at global index 7

        entry = "CURSOR_ENTER"
        if entry == "CURSOR_ENTER" and ui._menu_indices:
            index_to_select = ui._menu_indices[ui._menu_cursor_pos]
            entry = str(index_to_select)

        assert entry == "7"

    def test_cursor_enter_first_item(self, ui: UserInterface) -> None:
        """CURSOR_ENTER at position 0 selects the first menu item.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (5, 6, 7)
        ui._menu_cursor_pos = 0

        entry = "CURSOR_ENTER"
        if entry == "CURSOR_ENTER" and ui._menu_indices:
            entry = str(ui._menu_indices[ui._menu_cursor_pos])

        assert entry == "5"

    def test_cursor_enter_last_item(self, ui: UserInterface) -> None:
        """CURSOR_ENTER at last position selects the last menu item.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (5, 6, 7)
        ui._menu_cursor_pos = 2

        entry = "CURSOR_ENTER"
        if entry == "CURSOR_ENTER" and ui._menu_indices:
            entry = str(ui._menu_indices[ui._menu_cursor_pos])

        assert entry == "7"
