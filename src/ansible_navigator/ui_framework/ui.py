# cspell:ignore KEY_NPAGE, KEY_PPAGE
"""The main UI renderer."""
from __future__ import annotations

import curses
import logging
import re

from collections.abc import Mapping
from collections.abc import Sequence
from curses import ascii as curses_ascii
from functools import cache
from math import ceil
from math import floor
from re import Match
from re import Pattern
from typing import Any
from typing import Callable
from typing import NamedTuple
from typing import Protocol

from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.content_defs import ContentType
from ansible_navigator.content_defs import ContentTypeSequence
from ansible_navigator.content_defs import ContentView
from ansible_navigator.utils.functions import templar
from ansible_navigator.utils.serialize import serialize

from .colorize import Colorize
from .colorize import rgb_to_ansi
from .curses_defs import CursesLine
from .curses_defs import CursesLinePart
from .curses_defs import CursesLines
from .curses_defs import RgbTuple
from .curses_defs import SimpleLinePart
from .curses_window import CursesWindow
from .curses_window import Window
from .field_text import FieldText
from .form import Form
from .form_handler_text import FormHandlerText
from .form_utils import warning_notification
from .menu_builder import MenuBuilder
from .ui_config import UIConfig
from .ui_constants import Decoration


STANDARD_KEYS = {
    "^b/PgUp": "page up",
    "^f/PgDn": "page down",
    "\u2191\u2193": "scroll",
    "esc": "back",
}
END_KEYS = {":help": "help"}


class Action(NamedTuple):
    """the user's input."""

    value: str | int
    match: Match


class Content(NamedTuple):
    """what's on the screen, when showing content."""

    showing: Any


class Menu(NamedTuple):
    """details about the currently showing menu."""

    current: ContentTypeSequence
    columns: list[str]


class ContentFormatCallable(Protocol):
    """Protocol definition for the Ui.content_format callable."""

    def __call__(
        self,
        value: ContentFormat | None = None,
        default: bool = False,
    ) -> ContentFormat:
        """Refer to and keep in sync with UserInterface.content_format.

        :param value: The value refers to the UI content format
        :param default: The default UI content format
        """


class ShowCallable(Protocol):
    """Protocol definition for the Ui.show callable."""

    # pylint: disable=too-many-arguments
    def __call__(
        self,
        obj: ContentType,
        content_format: ContentFormat | None = None,
        index: int | None = None,
        columns: list | None = None,
        await_input: bool = True,
        filter_content_keys: Callable = lambda x: x,
        color_menu_item: Callable = lambda *args, **kwargs: (0, 0),
        content_heading: Callable = lambda *args, **kwargs: None,
    ) -> Interaction:
        """Refer to and keep in sync with UserInterface.show.

        :param obj: The inbound object
        :param content_format: Refers to the content format
        :param index: The indices of objects
        :param columns: Refers to the menu column
        :param await_input: Should we wait for user input?
        :param filter_content_keys: The filter content keys
        :param color_menu_item: To color the menu item
        :param content_heading: Refers to the content heading
        """


class Ui(NamedTuple):
    """select functions that can be called from an action."""

    clear: Callable
    menu_filter: Callable
    scroll: Callable
    show: ShowCallable
    show_form: Callable[[Form], Form]
    update_status: Callable
    content_format: ContentFormatCallable


class Interaction(NamedTuple):
    """wrapper for what is sent back to the calling app."""

    name: str
    action: Action
    ui: Ui
    content: Content | None = None
    menu: Menu | None = None


class UserInterface(CursesWindow):
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    """The main UI class."""

    def __init__(
        self,
        screen_min_height: int,
        kegexes: Callable[..., Any],
        refresh: int,
        ui_config: UIConfig,
        progress_bar_width: int = 8,
        status_width=12,
    ) -> None:
        """Initialize the user interface.

        :param screen_min_height: The minimum screen height
        :param kegexes: A callable producing a list of action regular expressions to match against
        :param refresh: The screen refresh time is ms
        :param ui_config: The current UI configuration
        :param progress_bar_width: The width of the progress bar
        :param status_width: The width of the status indicator
        """
        super().__init__(ui_config=ui_config)
        self._color_menu_item: Callable[[int, str, dict[str, Any]], tuple[int, int]]
        self._colorizer = Colorize(
            grammar_dir=self._ui_config.grammar_dir,
            theme_path=self._ui_config.theme_path,
        )
        self._content_heading: Callable[[Any, int], CursesLines | None]
        self._default_colors = None
        self._default_pairs = None
        self._default_content_format = ContentFormat.YAML
        self._filter_content_keys: Callable[[Any], dict[Any, Any]]
        self._hide_keys = True
        self._kegexes = kegexes
        self._logger = logging.getLogger(__name__)
        self._menu_filter: Pattern | None = None
        self._menu_indices: tuple[int, ...] = tuple()

        self._progress_bar_width = progress_bar_width
        self._status_width = status_width
        self._prefix_color = 8
        self._refresh = [refresh]
        self._rgb_to_curses_color_idx: dict[RgbTuple, int] = {}
        self._screen_min_height = screen_min_height
        self._scroll = 0
        self._content_format = self._default_content_format
        self._status = ""
        self._status_color = 0
        self._screen: Window = curses.initscr()
        self._screen.timeout(refresh)
        self._one_line_input = FormHandlerText(screen=self._screen, ui_config=self._ui_config)

    def clear(self) -> None:
        """Clear the screen."""
        self._screen.clear()
        self._screen.refresh()

    def disable_refresh(self) -> None:
        """Disable the screen refresh."""
        self._refresh.append(self._refresh[-1])
        self._refresh.append(-1)
        self._screen.timeout(-1)

    def restore_refresh(self) -> None:
        """Restore the screen refresh to the previous value."""
        self._refresh.pop()
        self._screen.timeout(self._refresh.pop())

    def update_status(self, status: str = "", status_color: int = 0) -> None:
        """Update the status.

        :param status: The string of status information
        :param status_color: The color of status
        """
        self._status = status
        self._status_color = status_color

    def menu_filter(self, value: str | None = "") -> Pattern | None:
        """Set or return the menu filter.

        :param value: None or the menu_filter regex to set
        :returns: the current menu filter
        """
        if value != "":
            if value is None:
                self._menu_filter = None
            else:
                try:
                    self._menu_filter = re.compile(value)
                except re.error as exc:
                    self._menu_filter = None
                    self._logger.error("Regex for menu filter was invalid: %s", value)
                    self._logger.exception(exc)
        return self._menu_filter

    def scroll(self, value: int | None = None) -> int:
        """Set or return the current scroll.

        :param value: the value to set the scroll to
        :raises TypeError: raise exception here
        :returns: the current scroll
        """
        if value is not None:
            if not isinstance(value, int):
                raise TypeError
            self._scroll = value
        return self._scroll

    def content_format(
        self,
        value: ContentFormat | None = None,
        default: bool = False,
    ) -> ContentFormat:
        """Set or return the current content format.

        :param value: The value to set the content format to
        :param default: The default content format
        :returns: The current content format
        """
        if value is not None:
            self._content_format = value
            if default:
                self._default_content_format = value
        return self._content_format

    @property
    def _ui(self) -> Ui:
        """Limit the callables the actions can access.

        :returns: A tuple of available functions
        """
        res = Ui(
            clear=self.clear,
            menu_filter=self.menu_filter,
            scroll=self.scroll,
            show=self.show,
            show_form=self.show_form,
            update_status=self.update_status,
            content_format=self.content_format,
        )
        return res

    def _footer(self, key_dict: dict) -> CursesLine:
        """Build a footer from the key dict spread the columns out evenly.

        :param key_dict: the keys and their description
        :returns: The footer line
        """
        column_widths = [len(f"{k!s}: {v!s}") for k, v in key_dict.items()]
        status_width = self._progress_bar_width if self._status else 0
        gap = floor((self._screen_width - status_width - sum(column_widths)) / len(key_dict))
        adjusted_column_widths = [c + gap for c in column_widths]
        col_starts = [0]
        for idx, column_width in enumerate(adjusted_column_widths):
            col_starts.append(column_width + col_starts[idx])
        footer = []
        for idx, key in enumerate(key_dict):
            left = key[0 : adjusted_column_widths[idx]]
            right = f" {key_dict[key]}"
            right = right[0 : adjusted_column_widths[idx] - len(key)]
            footer.append(
                CursesLinePart(
                    column=col_starts[idx],
                    string=left,
                    color=0,
                    decoration=curses.A_BOLD,
                ),
            )
            footer.append(
                CursesLinePart(
                    column=col_starts[idx] + len(left),
                    string=right,
                    color=0,
                    decoration=0,
                ),
            )
        if self._status:
            # place the status to the far right -1 for the scrollbar
            # center place the uneven extra on the right, so flip it twice
            status = self._status.capitalize()
            status = status[0 : self._status_width - 1]  # max
            status = status[::-1]  # reverse
            status = status.center(self._status_width)  # pad
            status = status[::-1]  # reverse
            footer.append(
                CursesLinePart(
                    column=self._screen_width - self._status_width - 1,
                    string=status,
                    color=self._status_color,
                    decoration=curses.A_REVERSE,
                ),
            )
        return CursesLine(tuple(footer))

    def _scroll_bar(
        self,
        viewport_height: int,
        len_heading: int,
        menu_size: int,
        body_start: int,
        body_stop: int,
    ) -> None:
        """Add a scroll bar if the length of the content is longer than the viewport height.

        :param viewport_height: The height of the viewport
        :param len_heading: The height of the heading
        :param menu_size: The number of lines in the content
        :param body_start: Where we are in the body
        :param body_stop: The end of the body
        """
        start_scroll_bar = body_start / menu_size * viewport_height
        stop_scroll_bar = body_stop / menu_size * viewport_height
        len_scroll_bar = ceil(stop_scroll_bar - start_scroll_bar)
        color = self._prefix_color
        for idx in range(int(start_scroll_bar), int(start_scroll_bar + len_scroll_bar)):
            lineno = idx + len_heading
            line_part = CursesLinePart(
                column=self._screen_width - 1,
                string="\u2592",
                color=color,
                decoration=0,
            )
            self._add_line(
                window=self._screen,
                lineno=min(lineno, viewport_height + len_heading),
                line=CursesLine(
                    ((line_part,)),
                ),
            )

    def _get_input_line(self) -> str:
        """Get one line of input from the user.

        :returns: the lines
        """
        self.disable_refresh()
        form_field = FieldText(name="one_line", prompt="")
        line_part = CursesLinePart(column=0, string=":", color=0, decoration=0)
        input_at = self._screen_height - 1  # screen y is zero based
        self._add_line(
            window=self._screen,
            lineno=input_at,
            line=CursesLine(
                ((line_part,)),
            ),
        )
        self._screen.refresh()
        self._one_line_input.win = curses.newwin(1, self._screen_width, input_at, 1)
        self._one_line_input.win.keypad(True)
        while True:
            user_input, char = self._one_line_input.handle(0, [form_field])
            if char == curses_ascii.ESC:
                break
            if char in (curses.KEY_ENTER, 10, 13):
                break
            if char == curses.KEY_RESIZE:
                break
        self.restore_refresh()
        self._curs_set(0)
        return user_input

    def _display(
        self,
        lines: CursesLines,
        line_numbers: tuple[int, ...],
        heading: CursesLines | None,
        indent_heading: int,
        key_dict: dict,
        await_input: bool,
        count: int,
    ) -> str:
        # pylint: disable=too-many-locals
        """Show something on the screen.

        :param lines: The lines to show
        :param line_numbers: The number of lines to show
        :param heading: The headers to show
        :param indent_heading: The indentation of heading
        :param key_dict: any supplemental key to show
        :param await_input: Should we wait for a key
        :param count: The count to show
        :returns: the key pressed
        """
        heading = heading or CursesLines(tuple())
        heading_len = len(heading)
        footer = self._footer({**STANDARD_KEYS, **key_dict, **END_KEYS})
        footer_at = self._screen_height - 1  # screen is 0 based index
        footer_len = 1

        viewport_height = self._screen_height - len(heading) - footer_len
        self.scroll(max(self.scroll(), viewport_height))

        index_width = len(str(count))

        keypad = {str(x) for x in range(0, 10)}
        other_valid_keys = ["+", "-", "_", "KEY_F(5)", "^[", "\x1b"]

        while True:
            self._screen.erase()
            prefix = " " * (index_width + len("|")) if indent_heading else None

            # Add the heading
            for idx, line in enumerate(heading):
                self._add_line(window=self._screen, lineno=idx, line=line, prefix=prefix)

            # Add the content
            for idx, line in enumerate(lines):
                line_index = line_numbers[idx]
                line_index_str = str(line_index).rjust(index_width)
                prefix = f"{line_index_str}\u2502"
                self._add_line(
                    window=self._screen,
                    lineno=idx + len(heading),
                    line=line,
                    prefix=prefix,
                )

            # Add the scroll bar
            if count > viewport_height:
                self._scroll_bar(
                    viewport_height=viewport_height,
                    len_heading=len(heading),
                    menu_size=count,
                    body_start=self._scroll - viewport_height,
                    body_stop=self._scroll,
                )

            # Add the footer after the rest of the screen has been drawn
            self._add_line(window=self._screen, lineno=footer_at, line=footer)

            self._screen.refresh()

            if await_input:
                char = self._screen.getch()
                key = "KEY_F(5)" if char == -1 else curses.keyname(char).decode()
            else:
                key = "KEY_F(5)"

            return_value = None
            if key == "KEY_RESIZE":
                new_scroll = min(
                    self._scroll - viewport_height + self._screen_height - heading_len - footer_len,
                    len(lines),
                )
                self.scroll(new_scroll)
                return_value = key
            elif key in keypad or key in other_valid_keys:
                return_value = key
            elif key == "KEY_DOWN":
                self.scroll(max(min(self.scroll() + 1, count), viewport_height))
                return_value = key
            elif key == "KEY_UP":
                self.scroll(max(self.scroll() - 1, viewport_height))
                return_value = key
            elif key in ["^F", "KEY_NPAGE"]:
                self.scroll(max(min(self.scroll() + viewport_height, count), viewport_height))
                return_value = key
            elif key in ["^B", "KEY_PPAGE"]:
                self.scroll(max(self.scroll() - viewport_height, viewport_height))
                return_value = key
            elif key == ":":
                colon_entry = self._get_input_line()
                if colon_entry is None:
                    continue
                return_value = colon_entry

            if return_value is not None:
                return return_value

    def _template_match_action(
        self,
        entry: str,
        current: Any,
    ) -> tuple[str, Action] | tuple[None, None]:
        """Attempt to template & match the user input against the kegexes.

        :param entry: the user input
        :param current: the content on the screen
        :returns: The name of the action and the action to call or nothing if no match found
        """
        if (
            not entry.startswith("{{") and "{{" in entry and "}}" in entry
        ):  # don't match pure template
            if isinstance(current, Mapping):
                template_vars = current
                type_msgs = []
            else:
                template_vars = {"this": current}
                type_msgs = ["Current content passed for templating is not a dictionary."]
                type_msgs.append("[HINT] Use 'this' to reference it (e.g. {{ this[0] }}")
            errors, entry = templar(entry, template_vars)
            if errors:
                msgs = ["Errors encountered while templating input"] + errors
                msgs.extend(type_msgs)
                self._show_form(warning_notification(msgs))
                return None, None
        for kegex in self._kegexes():
            match = kegex.kegex.match(entry)
            if match:
                return kegex.name, Action(match=match, value=entry)

        msgs = [f"Could not find a match for ':{entry}'"]
        msgs.append("[Hint] Try ':help' for a list of available commands.")
        self._show_form(warning_notification(msgs))
        return None, None

    def _serialize_color(self, obj: Any) -> CursesLines:
        """Serialize, if necessary and color an obj.

        :param obj: the object to color
        :returns: The generated lines
        """
        if self.content_format() is ContentFormat.ANSI:
            return self._colorizer.render_ansi(doc=obj)

        content_view = ContentView.NORMAL if self._hide_keys else ContentView.FULL
        current_format = self.content_format()
        if current_format.value.serialization:
            string = serialize(
                content_view=content_view,
                content=obj,
                serialization_format=current_format.value.serialization,
            )
        else:
            string = obj

        scope = "no_color"
        if self._ui_config.color:
            scope = self.content_format().value.scope

        rendered = self._colorizer.render(doc=string, scope=scope)
        self._cache_init_colors(rendered)
        return self._color_decorate_lines(rendered)

    def _cache_init_colors(self, lines: list):
        """Cache and init the unique colors for future use.

        Maintain a mapping of RGB colors
        to curses colors in self._rgb_to_curses_color_idx

        :param lines: The from which colors will be cached and initialized
        """
        if curses.COLORS > 16 and self._term_osc4_support:
            unique_colors = list(
                {chars.color for line in lines for chars in line if chars.color},
            )
            # start custom colors at 16
            for color in unique_colors:
                scale = 1000 / 255
                red, green, blue = color
                if color not in self._rgb_to_curses_color_idx:
                    if not self._rgb_to_curses_color_idx:
                        curses_colors_idx = 16
                    else:
                        curses_colors_idx = max(self._rgb_to_curses_color_idx.values()) + 1

                    self._rgb_to_curses_color_idx[color] = curses_colors_idx
                    curses.init_color(
                        curses_colors_idx,
                        int(red * scale),
                        int(green * scale),
                        int(blue * scale),
                    )
                    self._logger.debug(
                        "Added color: %s:%s",
                        curses_colors_idx,
                        curses.color_content(curses_colors_idx),
                    )
                    curses.init_pair(curses_colors_idx, curses_colors_idx, -1)

    def _color_decorate_lines(self, lines: list[list[SimpleLinePart]]) -> CursesLines:
        """Color and decorate each of the lines.

        :param lines: The lines to transform
        :returns: All lines colored
        """
        return CursesLines(tuple(self._color_decorate_line(line) for line in lines))

    def _color_decorate_line(self, line: list[SimpleLinePart]) -> CursesLine:
        """Color and decorate one line.

        :param line: The line to color
        :returns: One line colored
        """
        return CursesLine(tuple(self._color_decorate_line_part(line_part) for line_part in line))

    def _color_decorate_line_part(self, line_part: SimpleLinePart) -> CursesLinePart:
        """Color and decorate one line part.

        :param line_part: One line part
        :returns: One line part colored
        """
        if line_part.color:
            if self._term_osc4_support and curses.COLORS > 16:
                color = self._rgb_to_curses_color_idx[line_part.color]
            else:
                red, green, blue = line_part.color
                color = rgb_to_ansi(red, green, blue, curses.COLORS)
        else:
            color = 0

        decoration = Decoration.get_best(line_part.style)
        return CursesLinePart(
            column=line_part.column,
            string=line_part.chars,
            color=color,
            decoration=decoration,
        )

    def _filter_and_serialize(self, obj: Any) -> tuple[CursesLines | None, CursesLines]:
        """Filter an obj and serialize.

        :param obj: the obj to serialize
        :returns: the serialize lines ready for display
        """
        heading = self._content_heading(obj, self._screen_width)
        filtered_obj = self._filter_content_keys(obj) if self._hide_keys else obj
        lines = self._serialize_color(filtered_obj)
        return heading, lines

    def _show_form(self, obj: Form) -> Form:
        """Show a form on the display.

        :param obj: The form to show
        :returns: The form
        """
        res = obj.present(screen=self._screen, ui_config=self._ui_config)
        return res

    def _show_obj_from_list(
        self,
        objs: ContentTypeSequence,
        index: int,
        await_input: bool,
    ) -> Interaction:
        # pylint: disable=too-many-locals
        """Show an object on the display.

        :param objs: A list of one or more object
        :param index: The index associated with an object
        :param await_input: Should we wait for user input before returning
        :returns: interaction with the user
        """
        heading, lines = self._filter_and_serialize(objs[index])
        while True:
            heading_len = len(heading) if heading is not None else 0
            footer_len = 1

            if self.scroll() == 0:
                last_line_idx = min(
                    len(lines) - 1,
                    self._screen_height - heading_len - footer_len - 1,
                )
            else:
                last_line_idx = min(len(lines) - 1, self._scroll - 1)

            first_line_idx = max(
                0,
                last_line_idx - (self._screen_height - 1 - heading_len - footer_len),
            )

            key_dict = {"-": "previous", "+": "next", "[0-9]": "goto"} if len(objs) > 1 else {}

            line_numbers = tuple(range(first_line_idx, last_line_idx + 1))

            entry = self._display(
                lines=CursesLines(lines[first_line_idx : last_line_idx + 1]),
                line_numbers=line_numbers,
                heading=heading,
                indent_heading=False,
                key_dict=key_dict,
                await_input=await_input,
                count=len(lines),
            )
            if entry in ["KEY_DOWN", "KEY_UP", "KEY_NPAGE", "KEY_PPAGE", "^F", "^B"]:
                continue

            if entry == "KEY_RESIZE":
                # only the heading knows about the screen width and height
                heading = self._content_heading(objs[index], self._screen_width)
                continue

            if entry == "_":
                self._hide_keys = not self._hide_keys
                heading, lines = self._filter_and_serialize(objs[index])
                continue

            # get the less or more, wrap, in case we jumped out of the menu indices
            if entry == "-":
                less = list(reversed([i for i in self._menu_indices if i - index < 0]))
                more = list(reversed([i for i in self._menu_indices if i - index > 0]))

                ordered_indices = less + more
                if ordered_indices:
                    index = ordered_indices[0]
                    self.scroll(0)
                    entry = "KEY_F(5)"
                continue

            if entry == "+":
                more = [i for i in self._menu_indices if i - index > 0]
                less = [i for i in self._menu_indices if i - index < 0]

                ordered_indices = more + less
                if ordered_indices:
                    index = ordered_indices[0]
                    self.scroll(0)
                    entry = "KEY_F(5)"
                continue

            if entry.isnumeric():
                index = int(entry) % len(objs)
                self.scroll(0)
                entry = "KEY_F(5)"
                continue

            current = objs[index % len(objs)]

            name, action = self._template_match_action(entry, current)
            if name and action:
                if name == "refresh":
                    action = action._replace(value=index)

                filtered = self._filter_content_keys(current) if self._hide_keys else current
                content = Content(showing=filtered)
                return Interaction(name=name, action=action, content=content, ui=self._ui)

    def _obj_match_filter(self, obj: dict, columns: list) -> bool:
        """Check columns in a dictionary against a regex.

        :param obj: The dict to check
        :param columns: The dicts keys to check
        :returns: True if a match else False
        """
        return any(self._search_value(self.menu_filter(), obj.get(key)) for key in columns)

    @staticmethod
    @cache
    def _search_value(regex: Pattern, value: str) -> Match | None:
        """Check a str against a regex.

        :param regex: the compiled regex
        :param value: the string to check
        :returns: the match if made
        """
        return regex.search(str(value))

    def _get_heading_menu_items(
        self,
        current: Sequence[Any],
        columns: list,
        indices,
    ) -> tuple[CursesLines, CursesLines]:
        """Build the menu.

        :param current: A dict
        :param columns: The keys from the dictionary to use as columns
        :param indices: The indices associated with items
        :returns: The heading and menu items
        """
        menu_builder = MenuBuilder(
            progress_bar_width=self._progress_bar_width,
            screen_width=self._screen_width,
            number_colors=curses.COLORS,
            color_menu_item=self._color_menu_item,
            ui_config=self._ui_config,
        )
        menu_heading, menu_items = menu_builder.build(current, columns, indices)
        return menu_heading, menu_items

    def _show_menu(self, current: Sequence[Any], columns: list, await_input: bool) -> Interaction:
        """Show a menu on the screen.

        :param current: A dict
        :param columns: The keys from the dictionary to use as columns
        :param await_input: Should we wait for user input?
        :returns: Interaction with the user
        """
        while True:
            if self.scroll() == 0:
                last_line_idx = min(len(current) - 1, self._screen_height - 3)
            else:
                last_line_idx = min(len(current) - 1, self._scroll - 1)

            first_line_idx = max(0, last_line_idx - (self._screen_height - 3))

            if self.menu_filter():
                self._menu_indices = tuple(
                    idx for idx, mi in enumerate(current) if self._obj_match_filter(mi, columns)
                )
                line_numbers = tuple(range(last_line_idx - first_line_idx + 1))
                self._scroll = min(len(self._menu_indices), self._scroll)
            else:
                self._menu_indices = tuple(range(len(current)))
                line_numbers = self._menu_indices[first_line_idx : last_line_idx + 1]

            showing_indices = self._menu_indices[first_line_idx : last_line_idx + 1]
            menu_heading, menu_lines = self._get_heading_menu_items(
                current,
                columns,
                showing_indices,
            )

            entry = self._display(
                lines=menu_lines,
                line_numbers=line_numbers,
                count=len(self._menu_indices),
                heading=menu_heading,
                indent_heading=True,
                key_dict={"[0-9]": "goto"},
                await_input=await_input,
            )

            if entry in ["KEY_RESIZE", "KEY_DOWN", "KEY_UP", "KEY_NPAGE", "KEY_PPAGE", "^F", "^B"]:
                continue

            name, action = self._template_match_action(entry, current)
            if name and action:
                if name == "select":
                    if current:
                        index = self._menu_indices[int(entry) % len(self._menu_indices)]
                        action = action._replace(value=index)
                    else:
                        continue
                menu = Menu(current=current, columns=columns)
                return Interaction(name=name, action=action, menu=menu, ui=self._ui)

    def show(
        self,
        obj: ContentType,
        content_format: ContentFormat | None = None,
        index: int | None = None,
        columns: list | None = None,
        await_input: bool = True,
        filter_content_keys: Callable = lambda x: x,
        color_menu_item: Callable = lambda *args, **kwargs: (0, 0),
        content_heading: Callable = lambda *args, **kwargs: None,
    ) -> Interaction:
        """Show something on the screen.

        :param obj: The inbound object
        :param content_format: Set the content format
        :param index: When obj is a list, show this entry
        :param columns: When obj is a list of dicts, use these keys for menu columns
        :param await_input: Should we wait for user input?
        :param filter_content_keys: To show the filter content keys
        :param color_menu_item: To show the colored menu item
        :param content_heading: Show the content heading
        :returns: interaction with the user
        """
        self._color_menu_item = color_menu_item
        self._content_heading = content_heading
        self._filter_content_keys = filter_content_keys
        columns = columns or []
        self.content_format(content_format or self._default_content_format)

        if index is not None and isinstance(obj, (list, tuple)):
            result = self._show_obj_from_list(obj, index, await_input)
        elif columns and isinstance(obj, (list, tuple)):
            result = self._show_menu(obj, columns, await_input)
        else:
            result = self._show_obj_from_list([obj], 0, await_input)
        return result

    def show_form(self, form: Form) -> Form:
        """Show a form on using the user interface.

        :param form: The form to show
        :returns: The form populated with the response
        """
        form_result = self._show_form(form)
        return form_result
