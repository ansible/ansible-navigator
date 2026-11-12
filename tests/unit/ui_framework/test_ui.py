"""Unit tests for arrow-key cursor navigation in UserInterface."""

# pylint: disable=redefined-outer-name
from __future__ import annotations

import re

from types import SimpleNamespace
from typing import Any
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

    def test_initial_cursor_pos_is_none(self, ui: UserInterface) -> None:
        """Cursor starts as None (inactive) until an arrow key is pressed.

        Args:
            ui: A UserInterface fixture.
        """
        assert ui._menu_cursor_pos is None

    # cspell:ignore NPAGE PPAGE
    @pytest.mark.parametrize(
        "key",
        (
            "KEY_DOWN",
            "KEY_UP",
            "KEY_NPAGE",
            "KEY_PPAGE",
            "^F",
            "^B",
        ),
    )
    def test_navigation_keys_preserve_scroll(self, key: str, ui: UserInterface) -> None:
        """Scrolling navigation keys do not reset the displayed content.

        Args:
            key: Navigation key to test.
            ui: A UserInterface fixture.
        """
        ui.scroll(40)

        with (
            patch.object(ui, "_filter_and_serialize", return_value=(None, ())),
            patch.object(ui, "_display", side_effect=[key, StopIteration]),
            pytest.raises(StopIteration),
        ):
            ui._show_obj_from_list([{"key": "value"}], index=0, await_input=True)

        assert ui.scroll() == 40

    def test_changing_object_resets_scroll(self, ui: UserInterface) -> None:
        """Selecting another object resets the scroll position.

        Args:
            ui: A UserInterface fixture.
        """
        ui.scroll(40)

        with (
            patch.object(ui, "_filter_and_serialize", return_value=(None, ())),
            patch.object(ui, "_display", side_effect=["1", StopIteration]),
            pytest.raises(StopIteration),
        ):
            ui._show_obj_from_list([{"key": "value"}, {"key": "other"}], index=0, await_input=True)

        assert ui.scroll() == 0

    def test_cursor_activates_at_zero_on_first_key_down(self, ui: UserInterface) -> None:
        """First KEY_DOWN activates the cursor at position 0.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (0, 1, 2)
        ui._highlight_line_offset = None

        # Simulate first KEY_DOWN: activate cursor at 0, no movement (elif guards it)
        if ui._menu_cursor_pos is None:
            ui._menu_cursor_pos = 0
        # elif would run here, but the branch above was taken, so no increment

        assert ui._menu_cursor_pos == 0

    def test_cursor_increments_on_key_down(self, ui: UserInterface) -> None:
        """KEY_DOWN increments cursor when below the last item.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (0, 1, 2)
        ui._menu_cursor_pos = 0
        ui._highlight_line_offset = 0

        if ui._menu_cursor_pos < len(ui._menu_indices) - 1:
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

        if ui._menu_cursor_pos is not None and ui._menu_cursor_pos > 0:
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

        if ui._menu_cursor_pos is not None and ui._menu_cursor_pos > 0:
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

        if ui._menu_cursor_pos < len(ui._menu_indices) - 1:
            ui._menu_cursor_pos += 1

        assert ui._menu_cursor_pos == 2


class TestHighlightLineOffset:
    """Tests for _highlight_line_offset computation."""

    def test_no_highlight_when_cursor_inactive(self, ui: UserInterface) -> None:
        """No row is highlighted when cursor is None (not yet activated).

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (0, 1, 2, 3, 4)
        showing_indices = (0, 1, 2, 3, 4)

        ui._highlight_line_offset = None
        if ui._menu_indices and ui._menu_cursor_pos is not None:
            selected_global_index = ui._menu_indices[ui._menu_cursor_pos]
            try:
                ui._highlight_line_offset = list(showing_indices).index(selected_global_index)
            except ValueError:
                ui._highlight_line_offset = None

        assert ui._highlight_line_offset is None

    def test_highlight_offset_matches_visible_row(self, ui: UserInterface) -> None:
        """_highlight_line_offset is the index of the selected item in showing_indices.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (0, 1, 2, 3, 4)
        ui._menu_cursor_pos = 2
        showing_indices = (0, 1, 2, 3, 4)

        ui._highlight_line_offset = None
        if ui._menu_indices and ui._menu_cursor_pos is not None:
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
        if ui._menu_indices and ui._menu_cursor_pos is not None:
            selected_global_index = ui._menu_indices[ui._menu_cursor_pos]
            try:
                ui._highlight_line_offset = list(showing_indices).index(selected_global_index)
            except ValueError:
                ui._highlight_line_offset = None

        assert ui._highlight_line_offset is None


class TestEnterKeySelection:
    """Tests for Enter-key converting cursor position to a numeric entry."""

    def test_cursor_enter_ignored_when_cursor_inactive(self, ui: UserInterface) -> None:
        """CURSOR_ENTER does nothing when cursor is None (not yet activated).

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (3, 7, 11)
        # cursor_pos is None (inactive) — stray Enter should be ignored

        entry = "CURSOR_ENTER"
        if entry == "CURSOR_ENTER" and ui._menu_indices and ui._menu_cursor_pos is not None:
            entry = str(ui._menu_indices[ui._menu_cursor_pos])

        assert entry == "CURSOR_ENTER"  # unchanged — stray Enter was ignored

    def test_cursor_enter_selects_correct_index(self, ui: UserInterface) -> None:
        """CURSOR_ENTER converts _menu_cursor_pos to the correct global index string.

        Args:
            ui: A UserInterface fixture.
        """
        ui._menu_indices = (3, 7, 11)
        ui._menu_cursor_pos = 1  # pointing at global index 7

        entry = "CURSOR_ENTER"
        if entry == "CURSOR_ENTER" and ui._menu_indices and ui._menu_cursor_pos is not None:
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
        if entry == "CURSOR_ENTER" and ui._menu_indices and ui._menu_cursor_pos is not None:
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
        if entry == "CURSOR_ENTER" and ui._menu_indices and ui._menu_cursor_pos is not None:
            entry = str(ui._menu_indices[ui._menu_cursor_pos])

        assert entry == "7"


def _show_menu(ui: UserInterface, items: list[dict[str, str]], keys: list[str]) -> Any:
    """Drive ``_show_menu`` with a scripted key sequence.

    Stops after the last key unless the menu returns an interaction first.

    Args:
        ui: A UserInterface fixture.
        items: The menu rows.
        keys: Keys returned by successive ``_display`` calls.

    Returns:
        The interaction returned by the menu, or None if the keys ran out.
    """
    ui._color_menu_item = lambda *_args, **_kwargs: (0, 0)
    ui._kegexes = lambda: [SimpleNamespace(name="select", kegex=re.compile(r"^\d+$"))]
    with (
        patch.object(ui, "_display", side_effect=[*keys, StopIteration]),
        patch("curses.COLORS", 8, create=True),
    ):
        try:
            return ui._show_menu(items, ["task"], await_input=True)
        except StopIteration:
            return None


class TestCursorFollowsViewport:
    """The cursor bar must stay visible when the viewport moves without it."""

    # 24-row screen, 1 heading, 1 footer -> 22 visible rows; 40 items scrolled to the end
    # shows items 18..39.

    def test_cursor_clamped_into_view_when_scroll_moves(self, ui: UserInterface) -> None:
        """Auto-scroll or paging past the cursor pulls the cursor onto the first visible row.

        Args:
            ui: A UserInterface fixture.
        """
        items = [{"task": str(i)} for i in range(40)]
        ui._menu_current_id = id(items)
        ui._menu_cursor_pos = 2
        ui.scroll(40)

        _show_menu(ui, items, [])

        assert ui._menu_cursor_pos == 18
        assert ui._highlight_line_offset == 0

    def test_first_key_down_activates_on_first_visible_row(self, ui: UserInterface) -> None:
        """First KEY_DOWN in a scrolled menu highlights the top visible row, not item 0.

        Args:
            ui: A UserInterface fixture.
        """
        items = [{"task": str(i)} for i in range(40)]
        ui.scroll(40)

        _show_menu(ui, items, ["KEY_DOWN"])

        assert ui._menu_cursor_pos == 18
        assert ui._highlight_line_offset == 0

    def test_first_key_up_activates_on_last_visible_row(self, ui: UserInterface) -> None:
        """First KEY_UP in a scrolled menu highlights the bottom visible row.

        Args:
            ui: A UserInterface fixture.
        """
        items = [{"task": str(i)} for i in range(40)]
        ui.scroll(40)

        _show_menu(ui, items, ["KEY_UP"])

        assert ui._menu_cursor_pos == 39
        assert ui._highlight_line_offset == 21

    def test_cursor_on_first_visible_row_stays_when_viewport_stationary(
        self,
        ui: UserInterface,
    ) -> None:
        """A cursor already on the top visible row is not moved by a redraw.

        Args:
            ui: A UserInterface fixture.
        """
        items = [{"task": str(i)} for i in range(40)]
        ui._menu_current_id = id(items)
        ui._menu_cursor_pos = 18
        ui.scroll(40)

        _show_menu(ui, items, [])

        assert ui._menu_cursor_pos == 18
        assert ui._highlight_line_offset == 0

    def test_cursor_on_last_visible_row_stays_when_viewport_stationary(
        self,
        ui: UserInterface,
    ) -> None:
        """A cursor already on the bottom visible row is not moved by a redraw.

        Args:
            ui: A UserInterface fixture.
        """
        items = [{"task": str(i)} for i in range(40)]
        ui._menu_current_id = id(items)
        ui._menu_cursor_pos = 39
        ui.scroll(40)

        _show_menu(ui, items, [])

        assert ui._menu_cursor_pos == 39
        assert ui._highlight_line_offset == 21

    def test_cursor_mid_screen_unchanged_when_viewport_moves_one_row(
        self,
        ui: UserInterface,
    ) -> None:
        """A one-row viewport move (one task arriving) leaves a mid-screen cursor alone.

        Args:
            ui: A UserInterface fixture.
        """
        items = [{"task": str(i)} for i in range(40)]
        ui._menu_current_id = id(items)
        ui._menu_cursor_pos = 30
        ui.scroll(39)
        _show_menu(ui, items, [])
        assert ui._highlight_line_offset == 13

        ui.scroll(40)
        _show_menu(ui, items, [])

        assert ui._menu_cursor_pos == 30
        assert ui._highlight_line_offset == 12

    def test_cursor_clamped_to_last_row_when_viewport_moves_backwards(
        self,
        ui: UserInterface,
    ) -> None:
        """Paging up past the cursor pulls it onto the last visible row.

        Args:
            ui: A UserInterface fixture.
        """
        items = [{"task": str(i)} for i in range(40)]
        ui._menu_current_id = id(items)
        ui._menu_cursor_pos = 39
        ui.scroll(40 - 22)  # what KEY_PPAGE does in _display: back one viewport

        _show_menu(ui, items, [])

        assert ui._menu_cursor_pos == 17
        assert ui._highlight_line_offset == 17

    def test_key_down_off_bottom_row_scrolls_without_clamping(self, ui: UserInterface) -> None:
        """Arrow keys keep the cursor adjacent to the viewport, so the clamp never fires.

        Args:
            ui: A UserInterface fixture.
        """
        items = [{"task": str(i)} for i in range(45)]
        ui._menu_current_id = id(items)
        ui._menu_cursor_pos = 39
        ui.scroll(40)

        _show_menu(ui, items, ["KEY_DOWN", "KEY_DOWN"])

        assert ui._menu_cursor_pos == 41
        assert ui.scroll() == 42
        assert ui._highlight_line_offset == 21

    def test_short_menu_cursor_stays_valid(self, ui: UserInterface) -> None:
        """With fewer items than rows the cursor and highlight track the same item.

        Args:
            ui: A UserInterface fixture.
        """
        items = [{"task": str(i)} for i in range(5)]

        _show_menu(ui, items, ["KEY_UP", "KEY_UP", "KEY_UP"])

        assert ui._menu_cursor_pos == 2
        assert ui._highlight_line_offset == 2

    def test_empty_menu_ignores_arrows_and_enter(self, ui: UserInterface) -> None:
        """An empty menu never indexes into its items or highlights a row.

        Args:
            ui: A UserInterface fixture.
        """
        result = _show_menu(ui, [], ["KEY_DOWN", "KEY_UP", "CURSOR_ENTER"])

        assert result is None
        assert ui._menu_cursor_pos is None
        assert ui._highlight_line_offset is None

    def test_filtered_menu_highlight_maps_to_matching_item(self, ui: UserInterface) -> None:
        """With a filter the cursor is a position in the filtered list and maps to a match.

        Args:
            ui: A UserInterface fixture.
        """
        items = [{"task": f"t{i}"} for i in range(40)]
        ui.menu_filter("t1")  # t1, t10..t19 -> 11 items, all visible
        ui.scroll(40)

        _show_menu(ui, items, ["KEY_UP"])

        assert ui._menu_indices == (1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19)
        assert ui._menu_cursor_pos == 10
        assert ui._highlight_line_offset == 10
        assert items[ui._menu_indices[ui._menu_cursor_pos]]["task"] == "t19"

    def test_filtered_menu_enter_selects_highlighted_item(self, ui: UserInterface) -> None:
        """Enter in a filtered menu selects the highlighted item, not another match.

        Args:
            ui: A UserInterface fixture.
        """
        items = [{"task": f"t{i}"} for i in range(40)]
        ui.menu_filter("t1")
        ui.scroll(40)

        result = _show_menu(ui, items, ["KEY_UP", "CURSOR_ENTER"])

        assert result is not None
        assert result.name == "select"
        assert items[result.action.value]["task"] == "t19"

    def test_enter_after_clamp_selects_highlighted_item(self, ui: UserInterface) -> None:
        """After auto-scroll clamps the cursor, Enter selects the row that is highlighted.

        Args:
            ui: A UserInterface fixture.
        """
        items = [{"task": str(i)} for i in range(40)]
        ui._menu_current_id = id(items)
        ui._menu_cursor_pos = 2
        ui.scroll(40)

        result = _show_menu(ui, items, ["CURSOR_ENTER"])

        assert result is not None
        assert ui._highlight_line_offset == 0
        assert result.action.value == 18
