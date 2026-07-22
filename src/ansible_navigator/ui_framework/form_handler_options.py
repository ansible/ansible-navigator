"""Get one line of text input."""

from __future__ import annotations

import curses

from curses import ascii as curses_ascii
from typing import TYPE_CHECKING
from typing import Any

from .curses_defs import CursesLine
from .curses_defs import CursesLinePart
from .curses_window import CursesWindow


if TYPE_CHECKING:
    from ansible_navigator.action_runner import Window
    from ansible_navigator.ui_framework.field_text import FieldText
    from ansible_navigator.ui_framework.ui_config import UIConfig


class FormHandlerOptions(CursesWindow):
    """Handle form checkbox field."""

    def __init__(self, screen: Window, ui_config: UIConfig) -> None:
        """Initialize the handler for either form checkboxes or radio buttons.

        Args:
            screen: A curses window
            ui_config: The current user interface configuration
        """
        super().__init__(ui_config=ui_config)
        self._screen = screen

    def populate(self, form_field: FieldText, active: int) -> None:
        """Populate the window with the checkboxes.

        Args:
            form_field: Field from a form
            active: Track active checkbox/option
        """
        options = getattr(form_field, "options", [])
        for idx, option in enumerate(options):
            option_code = option.ansi_code(form_field)
            color = 8 if option.disabled else 0
            decoration = curses.A_STANDOUT if idx == active else 0
            clp_option_code = CursesLinePart(0, option_code, color, 0)
            if self._ui_config.color is False:
                text = (
                    f"[{option.text.capitalize()}]" if idx == active else option.text + "  "
                )  # clear the [], for else
            else:
                text = option.text
            clp_text = CursesLinePart(len(option_code) + 1, text, color, decoration)
            self._add_line(
                window=self.win,
                lineno=idx,
                line=CursesLine((clp_option_code, clp_text)),
            )

    def _handle_key_input(
        self,
        char: int,
        form_field: Any,
        active: int,
    ) -> tuple[bool, int]:
        """Process a single key input for checkbox/radio fields.

        Args:
            char: The character input from the user
            form_field: Field from a form
            active: Track active checkbox/option

        Returns:
            Tuple of (should_break, new_active)
        """
        if char in (curses_ascii.SO, curses.KEY_DOWN):
            return False, active + 1

        if char in (curses_ascii.DLE, curses.KEY_UP):
            return False, active - 1

        if char == curses.KEY_RESIZE:
            return True, active

        if char == curses_ascii.TAB:
            if active == len(form_field.options) - 1:
                return True, active
            return False, active + 1

        if char == curses_ascii.SP:
            if not form_field.options[active].disabled:
                form_field.options[active].checked = not form_field.options[active].checked
                if form_field.__class__.__name__ == "FieldRadio":
                    for ffo_idx, option in enumerate(form_field.options):
                        if ffo_idx != active:
                            option.checked = False
            return False, active

        if char in [curses_ascii.NL, curses_ascii.CR]:
            return True, active

        return False, active

    def handle(self, idx: int, form_fields: list[FieldText]) -> tuple[FieldText, int]:
        """Handle the check box field.

        Args:
            form_fields: List of fields
            idx: Index to retrieve specific field

        Returns:
            Field from form and characters

        Raises:
            RuntimeError: if there is a runtime error.
        """
        form_field = form_fields[idx]
        active = 0

        if not hasattr(form_field, "options"):
            raise RuntimeError
        while True:
            active = active % len(form_field.options)
            self.populate(form_field, active)

            char = self.win.getch()

            should_break, active = self._handle_key_input(char, form_field, active)
            if should_break:
                break

        return form_field, char
