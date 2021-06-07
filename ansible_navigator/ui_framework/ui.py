""" the main ui renderer
"""

# pylint: disable=too-many-lines
import curses
import json
import logging

import re

from collections.abc import Mapping

from curses import ascii as curses_ascii

from functools import lru_cache
from math import ceil
from math import floor
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Match
from typing import NamedTuple
from typing import Pattern
from typing import Tuple
from typing import Union

from .colorize import Colorize
from .colorize import rgb_to_ansi

from .curses_defs import CursesLine
from .curses_defs import CursesLinePart
from .curses_defs import CursesLines

from .curses_window import CursesWindow
from .curses_window import Window

from .field_text import FieldText
from .form import Form
from .form_handler_text import FormHandlerText
from .form_utils import warning_notification
from .menu_builder import MenuBuilder

from .ui_config import UIConfig
from ..utils import templar


from ..yaml import human_dump

STND_KEYS = {"^f/PgUp": "page up", "^b/PgDn": "page down", "\u2191\u2193": "scroll", "esc": "back"}
END_KEYS = {":help": "help"}

# pylint: disable=inherit-non-class
# pylint: disable=too-few-public-methods


class Action(NamedTuple):
    """the user's input"""

    value: Union[str, int]
    match: Match


class Content(NamedTuple):
    """what's on the screen, when showing content"""

    showing: Any


class Menu(NamedTuple):
    """details about the currently showing menu"""

    current: List
    columns: List


class Ui(NamedTuple):
    """select functions that can be called from an action"""

    clear: Callable
    menu_filter: Callable
    scroll: Callable
    show: Callable
    update_status: Callable
    xform: Callable


class Interaction(NamedTuple):
    """wrapper for what is sent bak to the calling app"""

    name: str
    action: Action
    ui: Ui
    content: Union[Content, None] = None
    menu: Union[Menu, None] = None


class UserInterface(CursesWindow):
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-arguments

    """The main UI class"""

    def __init__(
        self,
        screen_miny: int,
        kegexes: Callable[..., Any],
        refresh: int,
        ui_config: UIConfig,
        pbar_width: int = 8,
        status_width=12,
    ) -> None:
        """init

        :param screen_miny: The minimum screen height
        :type screen_miny: int
        :param pbar_width: The width of the progress bar
        :type pbar_width: int
        :param words_to_color: Words that get colored (regex, color_int)
        :type words_to_color: list
        """
        super().__init__(ui_config=ui_config)
        self._color_menu_item: Callable[[int, str, Dict[str, Any]], Tuple[int, int]]
        self._colorizer = Colorize(
            grammar_dir=self._ui_config.grammar_dir, theme_path=self._ui_config.theme_path
        )
        self._content_heading: Callable[[Any, int], Union[CursesLines, None]]
        self._default_colors = None
        self._default_pairs = None
        self._default_obj_serialization = "source.yaml"
        self._filter_content_keys: Callable[[Dict[Any, Any]], Dict[Any, Any]]
        self._hide_keys = True
        self._kegexes = kegexes
        self._logger = logging.getLogger(__name__)
        self._menu_filter: Union[Pattern, None] = None
        self._menu_indicies: Tuple[int, ...] = tuple()

        self._pbar_width = pbar_width
        self._status_width = status_width
        self._prefix_color = 8
        self._refresh = [refresh]
        self._rgb_to_curses_color_idx: Dict[str, int] = {}
        self._screen_miny = screen_miny
        self._scroll = 0
        self._xform = self._default_obj_serialization
        self._status = ""
        self._status_color = 0
        self._screen: Window = curses.initscr()
        self._screen.timeout(refresh)
        self._one_line_input = FormHandlerText(screen=self._screen, ui_config=self._ui_config)

    def clear(self) -> None:
        """clear the screen"""
        self._screen.clear()
        self._screen.refresh()

    def disable_refresh(self) -> None:
        """Disable the screen refresh"""
        self._refresh.append(self._refresh[-1])
        self._refresh.append(-1)
        self._screen.timeout(-1)

    def restore_refresh(self) -> None:
        """Restore the screen refresh
        to the previous value
        """
        self._refresh.pop()
        self._screen.timeout(self._refresh.pop())

    def update_status(self, status: str = "", status_color: int = 0) -> None:
        """update the status"""
        self._status = status
        self._status_color = status_color

    def menu_filter(self, value: Union[str, None] = "") -> Union[Pattern, None]:
        """Set or return the menu filter

        :param args[0]: None or the menu_filter to set
        :type args[0]: None or str(regex)
        :return: the current menu filter
        :rtype: None or Pattern
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

    def scroll(self, value: Union[int, None] = None) -> int:
        """Set or return the current scroll

        :param value: the value to set the scroll to
        :type value: int
        :return: the current scroll
        :rtype: int
        """
        if value is not None:
            if not isinstance(value, int):
                raise TypeError
            self._scroll = value
        return self._scroll

    def xform(self, value: Union[str, None] = None, default: bool = False) -> str:
        """Set or return the current xform

        :param value: the value to set the xform to
        :type value: str or None
        :return: the current xform
        :rtype: str
        """
        if value is not None:
            self._xform = value
            if default:
                self._default_obj_serialization = value
        return self._xform

    @property
    def _ui(self) -> Ui:
        """Limit the callables the actions can access

        :return: A tuple of avialble functions
        :rtype: Ui
        """
        res = Ui(
            clear=self.clear,
            menu_filter=self.menu_filter,
            scroll=self.scroll,
            show=self.show,
            update_status=self.update_status,
            xform=self.xform,
        )
        return res

    def _footer(self, key_dict: dict) -> CursesLine:
        """build a footer from the key dict
        spread the columns out evenly

        :param key_dict: the keys and their description
        :type key_dict: dict
        :return: The footer line
        :rtype: CursesLine
        """
        colws = [len("{k}: {v}".format(k=str(k), v=str(v))) for k, v in key_dict.items()]
        if self._status:
            status_width = self._pbar_width
        else:
            status_width = 0
        gap = floor((self._screen_w - status_width - sum(colws)) / len(key_dict))
        adj_colws = [c + gap for c in colws]
        col_starts = [0]
        for idx, colw in enumerate(adj_colws):
            col_starts.append(colw + col_starts[idx])
        footer = []
        for idx, key in enumerate(key_dict):
            left = key[0 : adj_colws[idx]]
            right = " {v}".format(v=key_dict[key])
            right = right[0 : adj_colws[idx] - len(key)]
            footer.append(
                CursesLinePart(
                    column=col_starts[idx],
                    string=left,
                    color=0,
                    decoration=curses.A_REVERSE,
                )
            )
            footer.append(
                CursesLinePart(
                    column=col_starts[idx] + len(left),
                    string=right,
                    color=0,
                    decoration=0,
                )
            )
        if self._status:
            # place the status to the far right -1 for the scrollbar
            # center place the uneven extra on the right, so flip it twice
            status = self._status[0 : self._status_width - 1]  # max
            status = status[::-1]  # reverse
            status = status.center(self._status_width)  # pad
            status = status[::-1]  # reverse
            status = status.upper()  # upper
            footer.append(
                CursesLinePart(
                    column=self._screen_w - self._status_width - 1,
                    string=status,
                    color=self._status_color,
                    decoration=curses.A_REVERSE,
                )
            )
        return tuple(footer)

    def _scroll_bar(
        self, viewport_h: int, len_heading: int, menu_size: int, body_start: int, body_stop: int
    ) -> None:
        """Add a scroll bar if the lines > viewport

        :param footer_height: The height of the footer
        :type footer_height: int
        :param_len_heading: the height of the heading
        :type len_heading: int
        :param len_lines: the number of lines in the content
        :type len_lines: int
        :param body_start: where we are in the body
        :type body_start: int
        :param body_stop: the end of the body
        :type body_stop: int
        """
        start_scroll_bar = body_start / menu_size * viewport_h
        stop_scroll_bar = body_stop / menu_size * viewport_h
        len_scroll_bar = ceil(stop_scroll_bar - start_scroll_bar)
        color = self._prefix_color
        for idx in range(int(start_scroll_bar), int(start_scroll_bar + len_scroll_bar)):
            lineno = idx + len_heading
            line_part = CursesLinePart(
                column=self._screen_w - 1, string="\u2592", color=color, decoration=0
            )
            self._add_line(
                window=self._screen,
                lineno=min(lineno, viewport_h + len_heading),
                line=tuple([line_part]),
            )

    def _get_input_line(self) -> str:
        """get one line of input from the user

        :return: the lines
        :rtype: str
        """
        self.disable_refresh()
        form_field = FieldText(name="one_line", prompt="")
        clp = CursesLinePart(column=0, string=":", color=0, decoration=0)
        input_at = self._screen_h - 1  # screen y is zero based
        self._add_line(window=self._screen, lineno=input_at, line=tuple([clp]))
        self._screen.refresh()
        self._one_line_input.win = curses.newwin(1, self._screen_w, input_at, 1)
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
        line_numbers: Tuple[int, ...],
        heading: Union[CursesLines, None],
        indent_heading: int,
        key_dict: dict,
        await_input: bool,
        count: int,
    ) -> str:
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-nested-blocks
        """show something on the screen

        :param lines: The lines to show
        :type lines: CursesLines
        :param heading: the headers to show
        :type heading: CursesLines or None
        :param key_dict: any suplimental key to show
        :type key_dict: dict
        :param await_input: Should we wait for a key
        :type await_input: bool
        :return: the key pressed
        :rtype: str
        """
        heading = heading or ()
        heading_len = len(heading)
        footer = self._footer(dict(**STND_KEYS, **key_dict, **END_KEYS))
        footer_at = self._screen_h - 1  # screen is 0 based index
        footer_len = 1

        viewport_h = self._screen_h - len(heading) - footer_len
        self.scroll(max(self.scroll(), viewport_h))

        index_width = len(str(count))

        keypad = set(str(x) for x in range(0, 10))
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
                prefix = "{idx}\u2502".format(idx=str(line_index).rjust(index_width))
                self._add_line(
                    window=self._screen, lineno=idx + len(heading), line=line, prefix=prefix
                )

            # Add the scroll bar
            if count > viewport_h:
                self._scroll_bar(
                    viewport_h=viewport_h,
                    len_heading=len(heading),
                    menu_size=count,
                    body_start=self._scroll - viewport_h,
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
                    self._scroll - viewport_h + self._screen_h - heading_len - footer_len,
                    len(lines),
                )
                self.scroll(new_scroll)
                return_value = key
            elif key in keypad or key in other_valid_keys:
                return_value = key
            elif key == "KEY_DOWN":
                self.scroll(max(min(self.scroll() + 1, count), viewport_h))
                return_value = key
            elif key == "KEY_UP":
                self.scroll(max(self.scroll() - 1, viewport_h))
                return_value = key
            elif key in ["^F", "KEY_NPAGE"]:
                self.scroll(max(min(self.scroll() + viewport_h, count), viewport_h))
                return_value = key
            elif key in ["^B", "KEY_PPAGE"]:
                self.scroll(max(self.scroll() - viewport_h, viewport_h))
                return_value = key
            elif key == ":":
                colon_entry = self._get_input_line()
                if colon_entry is None:
                    continue
                return_value = colon_entry

            if return_value is not None:
                return return_value

    def _template_match_action(
        self, entry: str, current: Any
    ) -> Union[Tuple[str, Action], Tuple[None, None]]:
        """attempt to template & match the user input against the regexes
        provided by each action

        :param entry: the user input
        :param current: the content on the screen
        :return: The name and matching action or not
        :rtype: str, Action or None, None
        """
        if not entry.startswith("{{"):  # don't match pure template
            if "{{" in entry and "}}" in entry:
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
        msgs.append("[HINT] Try ':help' for a list of available commands.")
        self._show_form(warning_notification(msgs))
        return None, None

    def _serialize_color(self, obj: Any) -> CursesLines:
        """Serialize, if neccesary and color an obj

        :param obj: the object to color
        :type obj: Any
        :return: The generated lines
        :rtype: CursesLines
        """

        if self.xform() == "source.ansi":
            return self._colorizer.render(doc=obj, scope=self.xform())
        if self.xform() == "source.yaml":
            string = human_dump(obj)
        elif self.xform() == "source.json":
            string = json.dumps(obj, indent=4, sort_keys=True)
        else:
            string = obj

        scope = "no_color"
        if self._ui_config.color:
            scope = self.xform()

        rendered = self._colorizer.render(doc=string, scope=scope)
        return self._color_lines_for_term(rendered)

    def _color_lines_for_term(self, lines: List) -> CursesLines:
        """Give a list of dicts from tokenized lines
        transform them into lines for curses
        add colors as needed, maintain a mapping of rgb colors
        to curses colors in self._rgb_to_curses_color_idx

        :params lines: the lines to transform
        :type lines: list of lists of dicts
            Lines[LinePart[{"color": rgb, "chars": text, "column": n},...]]
        :return: the lines ready for curses
        :type: CursesLines
        """
        if curses.COLORS > 16 and self._term_osc4_supprt:
            unique_colors = list(
                set(chars["color"] for line in lines for chars in line if chars["color"])
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
                        curses_colors_idx, int(red * scale), int(green * scale), int(blue * scale)
                    )
                    self._logger.debug(
                        "Added color: %s:%s",
                        curses_colors_idx,
                        curses.color_content(curses_colors_idx),
                    )
                    curses.init_pair(curses_colors_idx, curses_colors_idx, -1)
        colored_lines = self._colored_lines(lines)
        return colored_lines

    def _colored_lines(self, lines: List[List[Dict]]) -> CursesLines:
        """color each of the lines

        :params lines: the lines to transform
        :type lines: list of lists of dicts
            Lines[LinePart[{"color": rgb, "chars": text, "column": n},...]]
        :return: all the lines
        :rtype: CursesLines
        """
        return tuple(self._colored_line(line) for line in lines)

    def _colored_line(self, line: List[Dict]) -> CursesLine:
        """color one line

        :param line: the line to transform
        :type line: lists of dicts
            LinePart[{"color": rgb, "chars": text, "column": n},...]
        :return one colored line:
        :rtype: CursesLine
        """
        return tuple(self._colored_line_part(line_part) for line_part in line)

    def _colored_line_part(self, lp_dict: Dict) -> CursesLinePart:
        """color one linepart

        :param lp_dict: a dict describing the line part
        :type lp_dict: dict {"color": rgb, "chars": text, "column": n}
        :return: the colored line part
        :rtype: CursesLinePart
        """
        if lp_dict["color"]:
            if self._term_osc4_supprt and curses.COLORS > 16:
                color = self._rgb_to_curses_color_idx[lp_dict["color"]]
            else:
                red, green, blue = lp_dict["color"]
                color = rgb_to_ansi(red, green, blue, curses.COLORS)
        else:
            color = 0
        return CursesLinePart(
            column=lp_dict["column"],
            string=lp_dict["chars"],
            color=color,
            decoration=0,
        )

    def _filter_and_serialize(self, obj: Any) -> Tuple[Union[CursesLines, None], CursesLines]:
        """filter an obj and serialize

        :param obj: the obj to serialize
        :type obj: Any
        :return: the serialize lines ready for display
        :rtype: CursesLines
        """
        heading = self._content_heading(obj, self._screen_w)
        filtered_obj = (
            self._filter_content_keys(obj) if self._hide_keys and isinstance(obj, dict) else obj
        )
        lines = self._serialize_color(filtered_obj)
        return heading, lines

    def _show_form(self, obj: Form) -> Form:
        res = obj.present(screen=self._screen, ui_config=self._ui_config)
        return res

    def _show_obj_from_list(self, objs: List[Any], index: int, await_input: bool) -> Interaction:
        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        """Show an object on the display

        :param objs: A list of one or more object
        :type objs: A list of Any
        :param await_input: Should we wait for user input before returning
        :type await_input: bool
        :return: interaction with the user
        :rtype: Interaction
        """
        heading, lines = self._filter_and_serialize(objs[index])
        while True:
            if heading is not None:
                heading_len = len(heading)
            else:
                heading_len = 0
            footer_len = 1

            if self.scroll() == 0:
                last_line_idx = min(len(lines) - 1, self._screen_h - heading_len - footer_len - 1)
            else:
                last_line_idx = min(len(lines) - 1, self._scroll - 1)

            first_line_idx = max(0, last_line_idx - (self._screen_h - 1 - heading_len - footer_len))

            if len(objs) > 1:
                key_dict = {"-": "previous", "+": "next", "[0-9]": "goto"}
            else:
                key_dict = {}

            line_numbers = tuple(range(first_line_idx, last_line_idx + 1))

            entry = self._display(
                lines=lines[first_line_idx : last_line_idx + 1],
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
                # only the heading knows about the screen_w and screen_h
                heading = self._content_heading(objs[index], self._screen_w)
                continue

            if entry == "_":
                self._hide_keys = not self._hide_keys
                heading, lines = self._filter_and_serialize(objs[index])
                continue

            # get the less or more, wrap, incase we jumped out of the menu indices
            if entry == "-":
                less = list(reversed([i for i in self._menu_indicies if i - index < 0]))
                more = list(reversed([i for i in self._menu_indicies if i - index > 0]))

                ordered_indicies = less + more
                if ordered_indicies:
                    index = ordered_indicies[0]
                    self.scroll(0)
                    entry = "KEY_F(5)"
                continue

            if entry == "+":
                more = [i for i in self._menu_indicies if i - index > 0]
                less = [i for i in self._menu_indicies if i - index < 0]

                ordered_indicies = more + less
                if ordered_indicies:
                    index = ordered_indicies[0]
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

                filtered = (
                    self._filter_content_keys(current)
                    if self._hide_keys and isinstance(current, dict)
                    else current
                )
                content = Content(showing=filtered)
                return Interaction(name=name, action=action, content=content, ui=self._ui)

    def _obj_match_filter(self, obj: Dict, columns: List) -> bool:
        """Check a dict's columns against a regex

        :param obj: The dict to check
        :type obj: dict
        :param columns: The dicts keys to check
        :type columns: list
        :return: True if a mtch else False
        :rtype: bool
        """
        for key in columns:
            if self._search_value(self.menu_filter(), obj[key]):
                return True
        return False

    @staticmethod
    @lru_cache(maxsize=None)
    def _search_value(regex: Pattern, value: str) -> Union[Match, None]:
        """check a str against a regex
        lru_cache enabled because this is hit during resize

        :param regex: the compiled regex
        :type regex: Pattern
        :param value: the string to check
        :type value: str
        :return: the match if made
        :rtype: Match or None
        """
        return regex.search(str(value))

    def _get_heading_menu_items(
        self, current: List, columns: List, indicies
    ) -> Tuple[CursesLines, CursesLines]:
        """build the menu

        :param current: A dict
        :type current: dict
        :param columns: The keys from the dic to use as columns
        :type columns: list
        :param distribute: method for width deficit
        :type distribute: str
        :return: The heading and menu items
        :rtype: CursesLines, CursesLines
        """
        menu_builder = MenuBuilder(
            pbar_width=self._pbar_width,
            screen_w=self._screen_w,
            number_colors=curses.COLORS,
            color_menu_item=self._color_menu_item,
            ui_config=self._ui_config,
        )
        menu_heading, menu_items = menu_builder.build(current, columns, indicies)
        return menu_heading, menu_items

    def _show_menu(self, current: List, columns: List, await_input: bool) -> Interaction:
        """Show a menu on the screen

        :param current: A dict
        :type current: dict
        :param columns: The keys from the dic to use as columns
        :type columns: list
        :param await_input: Should we wait for user input?
        :type await_input: bool
        :return: interaction with the user
        :rtype: Interaction
        """

        while True:

            if self.scroll() == 0:
                last_line_idx = min(len(current) - 1, self._screen_h - 3)
            else:
                last_line_idx = min(len(current) - 1, self._scroll - 1)

            first_line_idx = max(0, last_line_idx - (self._screen_h - 3))

            if self.menu_filter():
                self._menu_indicies = tuple(
                    idx for idx, mi in enumerate(current) if self._obj_match_filter(mi, columns)
                )
                line_numbers = tuple(range(last_line_idx - first_line_idx + 1))
                self._scroll = min(len(self._menu_indicies), self._scroll)
            else:
                self._menu_indicies = tuple(range(len(current)))
                line_numbers = self._menu_indicies[first_line_idx : last_line_idx + 1]

            showing_idxs = self._menu_indicies[first_line_idx : last_line_idx + 1]
            menu_heading, menu_lines = self._get_heading_menu_items(current, columns, showing_idxs)

            entry = self._display(
                lines=menu_lines,
                line_numbers=line_numbers,
                count=len(self._menu_indicies),
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
                        index = self._menu_indicies[int(entry) % len(self._menu_indicies)]
                        action = action._replace(value=index)
                    else:
                        continue
                menu = Menu(current=current, columns=columns)
                return Interaction(name=name, action=action, menu=menu, ui=self._ui)

    def show(
        self,
        obj: Union[List, Dict, str, bool, int, float],
        xform: str = "",
        index: int = None,
        columns: List = None,
        await_input: bool = True,
        filter_content_keys: Callable = lambda x: x,
        color_menu_item: Callable = lambda *args, **kwargs: (0, 0),
        content_heading: Callable = lambda *args, **kwargs: None,
    ) -> Union[Interaction, Form]:
        """Show something on the screen

        :param obj: The inbound object
        :type obj: anything
        :param xform: Set the xform
        :type xform: str
        :param index: When obj is a list, show this entry
        :type index: int
        :param columns: When obj is a list of dicts, use these keys for menu columns
        :type columns: list
        :param wait_input: Should we wait for user input?
        :type wait_input: bool
        :return: interaction with the user
        :rtype: Interaction
        """
        self._color_menu_item = color_menu_item
        self._content_heading = content_heading
        self._filter_content_keys = filter_content_keys
        columns = columns or []
        self.xform(xform or self._default_obj_serialization)

        if isinstance(obj, Form):
            form_result = self._show_form(obj)
            return form_result

        if index is not None and isinstance(obj, list):
            result = self._show_obj_from_list(obj, index, await_input)
        elif columns and isinstance(obj, list):
            result = self._show_menu(obj, columns, await_input)
        else:
            result = self._show_obj_from_list([obj], 0, await_input)
        return result
