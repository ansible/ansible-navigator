"""the form and presenter of the form to the user
"""
import curses

from curses import ascii as curses_ascii
from typing import TYPE_CHECKING
from typing import List
from typing import Optional
from typing import Tuple

from .curses_defs import CursesLine
from .curses_defs import CursesLinePart
from .curses_defs import CursesLines
from .curses_window import CursesWindow
from .field_button import FieldButton
from .field_checks import FieldChecks
from .field_information import FieldInformation
from .field_radio import FieldRadio
from .field_text import FieldText
from .field_working import FieldWorking
from .form_defs import FormType
from .form_handler_text import FormHandlerText
from .sentinels import unknown


if TYPE_CHECKING:
    from .form import Form  # pylint: disable=cyclic-import


# the maximum form size
MAX_FORM_HEIGHT = 1024
MAX_FORM_WIDTH = 1024
LEFT_PAD_RATIO = 2 / 5
TOP_PAD_RATIO = 2 / 5
BUTTON_SPACE = 10


class FormPresenter(CursesWindow):
    """present the form to the user"""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, form, screen, ui_config):
        """Initialize the form presenter.

        :param form: The form to present to the user
        :param screen: A curses window
        :param ui_config: The current user interface configuration
        """
        super().__init__(ui_config=ui_config)
        self._form = form
        self._screen = screen
        self._line_number: int = 0
        self._prompt_end: int = 0
        self._input_start: int = 0
        self._form_width: int = 0
        self._form_height: int = 0
        self._pad_left: int = 0
        self._pad_top: int = 0
        self._separator = ": "

    @property
    def _field_win_start(self):
        return self._input_start + self._pad_left

    @property
    def _field_win_width(self):
        return self._screen_width - self._field_win_start

    def _dimensions(self):
        self._prompt_end = max([len(form_field.full_prompt) for form_field in self._form.fields])
        self._input_start = self._prompt_end + len(self._separator)

        widths = []
        for field in self._form.fields:
            if hasattr(field, "value") and field.value is not unknown:
                widths.append(len(str(field.value)) + self._input_start)
            if hasattr(field, "options"):
                widths.extend((len(option.text) + self._input_start for option in field.options))
            if hasattr(field, "information"):
                widths.append(max([len(info) for info in field.information]))
            if hasattr(field, "messages"):
                widths.append(max([len(msg) for msg in field.messages]))
            widths.append(len(field.validator(hint=True)) + self._input_start)

        if self._form.type is FormType.FORM:
            self._form_width = max(widths) + BUTTON_SPACE
        elif self._form.type in (FormType.NOTIFICATION, FormType.WORKING):
            self._form_width = max(widths)

        height = 2  # title + horizontal line
        for field in self._form.fields:
            if isinstance(field, FieldInformation):
                height += len(field.information)
            if isinstance(field, (FieldWorking)):
                height += len(field.messages)
            elif isinstance(field, FieldText):
                height += 1
            elif isinstance(field, (FieldChecks, FieldRadio)):
                height += len(field.options)
        height += 2  # horizontal line + buttons
        self._form_height = height

        self._pad_top = max(int((self._screen_height - self._form_height) * TOP_PAD_RATIO), 0)
        self._pad_left = max(int((self._screen_width - self._form_width) * LEFT_PAD_RATIO), 0)

    def _generate_form(self) -> Tuple[Tuple[int, CursesLine], ...]:
        lines = []
        lines.append((self._line_number, self._generate_title()))
        self._line_number += 1
        lines.append((self._line_number, self._generate_horizontal_line()))
        self._line_number += 1

        body_fields = [
            field for field in self._form.fields if field.name not in ["submit", "cancel"]
        ]
        for form_field in body_fields:

            # pylint: disable=not-an-iterable
            # https://github.com/PyCQA/pylint/issues/2296
            if isinstance(form_field, FieldInformation):
                information_lines = self._generate_information(form_field)
                for line in information_lines:
                    lines.append((self._line_number, line))
                    self._line_number += 1

            elif isinstance(form_field, FieldWorking):
                message_lines = self._generate_messages(form_field)
                for line in message_lines:
                    lines.append((self._line_number, line))
                    self._line_number += 1
            # pylint: enable=not-an-iterable

            elif isinstance(form_field, FieldText):
                prompt = self._generate_prompt(form_field)
                line = CursesLine((tuple(prompt + [self._generate_field_text(form_field)])))
                lines.append((self._line_number, line))
                self._line_number += 1

            elif isinstance(form_field, (FieldChecks, FieldRadio)):
                prompt = self._generate_prompt(form_field)
                option_lines = self._generate_field_options(form_field)
                # although option_lines[0] is a CursesLine, only it's first line part is needed
                # because the prompt needs to be prepended to it
                first_option_line_part = option_lines[0][0]
                line = CursesLine((tuple(prompt + [first_option_line_part])))
                lines.append((self._line_number, line))
                self._line_number += 1

                for option_line in option_lines[1:]:
                    lines.append((self._line_number, CursesLine((option_line))))
                    self._line_number += 1

            error = self._generate_error(form_field)
            if error:
                lines.append((self._line_number, error))
                self._line_number += 1

        lines.append((self._line_number, self._generate_horizontal_line()))
        self._line_number += 1
        lines.append((self._line_number, self._generate_buttons()))
        return tuple(lines)

    def _generate_buttons(self) -> CursesLine:
        line_parts = []
        far_right = self._form_width
        footer_fields = [field for field in self._form.fields if field.name in ["submit", "cancel"]]
        for form_field in reversed(footer_fields):
            string = f" {form_field.text} "  # room for []
            far_right -= len(string)
            window = curses.newwin(1, len(string), self._line_number, far_right + self._pad_left)
            window.keypad(True)
            form_field.win = window
            form_validity_state = [
                f.valid for f in self._form.fields if not isinstance(f, FieldButton)
            ]
            form_field.conditional_validation(form_validity_state)
            if form_field.disabled is True:
                color = 8
            else:
                color = form_field.color
            line_part = CursesLinePart(far_right, string, color, 0)
            line_parts.append(line_part)
            far_right -= 1
        return CursesLine(tuple(line_parts))

    def _generate_error(self, form_field) -> Optional[CursesLine]:
        if form_field.current_error:
            line_part = CursesLinePart(self._input_start, form_field.current_error, 9, 0)
            return CursesLine((line_part,))
        return None

    def _generate_field_options(self, form_field) -> CursesLines:
        window = curses.newwin(
            len(form_field.options),
            self._field_win_width,
            self._line_number,
            self._field_win_start,
        )
        window.keypad(True)
        form_field.win = window
        lines = []
        for option in form_field.options:
            option_code = option.ansi_code(form_field)
            color = 8 if option.disabled else 0
            text = f"{option_code} {str(option.text)}"
            line_part = CursesLinePart(self._input_start, text, color, 0)
            lines.append(CursesLine((line_part,)))
        return CursesLines(tuple(lines))

    def _generate_field_text(self, form_field) -> CursesLinePart:
        window = curses.newwin(1, self._field_win_width, self._line_number, self._field_win_start)
        window.keypad(True)
        form_field.win = window

        if form_field.value is unknown:
            text = form_field.validator(hint=True)
            color = 8
        else:
            text = str(form_field.value)
            color = 0
        return CursesLinePart(self._input_start, text, color, 0)

    def _generate_horizontal_line(self) -> CursesLine:
        line_part = CursesLinePart(0, "\u2500" * self._form_width, 8, 0)
        return CursesLine((line_part,))

    @staticmethod
    def _generate_information(form_field) -> CursesLines:
        lines = tuple(
            CursesLine((CursesLinePart(0, line, 0, 0),)) for line in form_field.information
        )
        return CursesLines(lines)

    @staticmethod
    def _generate_messages(form_field) -> CursesLines:
        lines = tuple(CursesLine((CursesLinePart(0, line, 0, 0),)) for line in form_field.messages)
        return CursesLines(lines)

    def _generate_prompt(self, form_field) -> List[CursesLinePart]:
        prompt_start = self._prompt_end - len(form_field.full_prompt)
        if form_field.valid is True:
            color = 10
        else:
            color = 0

        cl_prompt = CursesLinePart(prompt_start, form_field.prompt, color, 0)
        cl_default = CursesLinePart(
            prompt_start + len(form_field.prompt),
            str(form_field.formatted_default),
            4,
            0,
        )
        cl_separator = CursesLinePart(self._prompt_end, self._separator, color, 0)
        return [cl_prompt, cl_default, cl_separator]

    def _generate_title(self) -> CursesLine:
        line_part = CursesLinePart(0, self._form.title.upper(), self._form.title_color, 0)
        return CursesLine((line_part,))

    def present(self) -> "Form":
        """present the form to the user"""
        self._screen.clear()
        self._screen.refresh()
        idx = 0
        pad = curses.newpad(MAX_FORM_HEIGHT, MAX_FORM_WIDTH)
        shared_input_line_cache: List[str] = []
        for form_field in self._form.fields:
            form_field.window_handler = form_field.window_handler(
                screen=self._screen,
                ui_config=self._ui_config,
            )
            if isinstance(form_field.window_handler, FormHandlerText):
                form_field.window_handler.input_line_cache = shared_input_line_cache

        while True:
            self._dimensions()
            self._line_number = self._pad_top

            pad.clear()
            for line in self._generate_form():
                self._add_line(pad, *line)
            pad.refresh(0, 0, 0, self._pad_left, self._screen_height - 1, self._screen_width - 1)

            idx = idx % len(self._form.fields)
            form_field = self._form.fields[idx]

            form_field.window_handler.win = form_field.win
            win_response = form_field.window_handler.handle(idx, self._form.fields)

            response, char = win_response

            if char == curses.KEY_RESIZE:
                self._screen.clear()
                self._screen.refresh()

            elif char == 112065:
                # non-blocking form
                break

            elif isinstance(form_field, FieldButton):
                if form_field.pressed:
                    break
                idx += 1
            else:
                if char == curses_ascii.TAB:
                    form_field.conditional_validation(response)
                    idx += 1
                else:
                    form_field.validate(response)
                    if form_field.valid is True:
                        idx += 1

        return self._form
