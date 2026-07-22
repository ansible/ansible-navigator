"""Simple utils for working with forms."""

from __future__ import annotations

import copy
import shutil
import textwrap

from functools import partial
from typing import Any

from ansible_navigator.utils.definitions import ExitMessage
from ansible_navigator.utils.definitions import ExitMessages
from ansible_navigator.utils.definitions import ExitPrefix
from ansible_navigator.utils.functions import console_width

from .colorize import ansi_to_curses
from .curses_defs import CursesLines
from .field_checks import FieldChecks
from .field_curses_information import FieldCursesInformation
from .field_information import FieldInformation
from .field_option import FieldOption
from .field_radio import FieldRadio
from .field_text import FieldText
from .field_working import FieldWorking
from .form import Form
from .form import FormType
from .ui_constants import Color
from .validators import FieldValidators


def _build_text_field(field: dict[str, Any]) -> FieldText:
    """Build a FieldText from a field dictionary.

    Args:
        field: Field dictionary from form data

    Returns:
        Constructed FieldText instance
    """
    field_params: dict[str, Any] = {"name": field["name"]}
    field_params["prompt"] = field["prompt"]
    field_params["validator"] = getattr(FieldValidators, field["validator"]["name"])

    choices = field["validator"].get("choices")
    if choices:
        field_params["validator"] = partial(field_params["validator"], choices=choices)

    default = field.get("default")
    if default:
        field_params["default"] = default

    frm_field_text = FieldText(**field_params)

    pre_populate = field.get("pre_populate")
    if pre_populate:
        frm_field_text.pre_populate(pre_populate)

    return frm_field_text


def _build_checks_field(field: dict[str, Any]) -> FieldChecks:
    """Build a FieldChecks from a field dictionary.

    Args:
        field: Field dictionary from form data

    Returns:
        Constructed FieldChecks instance
    """
    field_params: dict[str, Any] = {"name": field["name"]}
    field_params["prompt"] = field["prompt"]
    field_params["options"] = [FieldOption(**option) for option in field["options"]]

    max_selected = field.get("max_selected")
    if max_selected:
        field_params["max_selected"] = max_selected

    min_selected = field.get("min_selected")
    if min_selected:
        field_params["min_selected"] = min_selected

    return FieldChecks(**field_params)


def _build_radio_field(field: dict[str, Any]) -> FieldRadio:
    """Build a FieldRadio from a field dictionary.

    Args:
        field: Field dictionary from form data

    Returns:
        Constructed FieldRadio instance
    """
    field_params: dict[str, Any] = {"name": field["name"]}
    field_params["prompt"] = field["prompt"]
    field_params["options"] = [FieldOption(**option) for option in field["options"]]
    return FieldRadio(**field_params)


def dict_to_form(form_data: dict[str, Any]) -> Form:
    """Convert a python dict to a form.

    Args:
        form_data: Form data

    Returns:
        Object containing fields from form
    """
    if form_data.get("type") == "notification":
        form = Form(type_=FormType.NOTIFICATION)
    elif form_data.get("type") == "working":
        form = Form(type_=FormType.WORKING)
    else:
        form = Form(type_=FormType.FORM)

    form._dict = form_data  # noqa: SLF001
    form.title = form_data["title"]
    form.title_color = form_data.get("title_color", 0)

    for field in form_data["fields"]:
        if field["type"] == "text_input":
            form.fields.append(_build_text_field(field))

        elif field["type"] == "checkbox":
            form.fields.append(_build_checks_field(field))

        elif field["type"] == "radio":
            form.fields.append(_build_radio_field(field))

        elif field["type"] == "information":
            frm_field_info = FieldInformation(name=field["name"], information=field["information"])
            form.fields.append(frm_field_info)

        elif field["type"] == "working":
            frm_field_working = FieldWorking(name=field["name"], messages=field["messages"])
            form.fields.append(frm_field_working)

    return form


def form_to_dict(form: Form, key_on_name: bool = False) -> dict[str, Any]:
    """Populate the original _dict of the form with the results.

    Args:
        form: Holding place for form fields
        key_on_name: Bool used to filter via name

    Returns:
        form as type dict
    """
    res = form._dict  # noqa: SLF001
    res["cancelled"] = form.cancelled
    res["submitted"] = form.submitted
    for field_idx, field in enumerate(form.fields):
        if isinstance(field, FieldText):
            res["fields"][field_idx]["response"] = copy.copy(field.response)
            res["fields"][field_idx]["value"] = copy.copy(field.value)
        elif isinstance(field, FieldChecks | FieldRadio):
            for option_idx, option in enumerate(field.options):
                res_field_options = res["fields"][field_idx]["options"]
                res_field_options[option_idx]["checked"] = option.checked
            res["fields"][field_idx]["checked"] = [
                option.name for option in field.options if option.checked
            ]

    if key_on_name:
        res["fields"] = _rekey_fields_by_name(res)
    return res


def _rekey_fields_by_name(res: dict[str, Any]) -> dict[str, Any]:
    """Rekey the fields list into a dict keyed by field name.

    Args:
        res: The form result dictionary containing a "fields" list

    Returns:
        Dictionary of fields keyed by name
    """
    fields: dict[str, Any] = {}
    for field in res["fields"]:
        fields[field["name"]] = field
        if "options" in field:
            options = {}
            for option in field["options"]:
                options[option["name"]] = option
            fields[field["name"]]["options"] = options
    return fields


def break_long_lines(messages: list[str]) -> list[str]:
    """Break lines such that the form width !> 80%.

    Args:
        messages: Lines of the form

    Returns:
        Resulting messages split if needed
    """
    width = int(shutil.get_terminal_size().columns * 0.8)
    result = []
    for message in messages:
        lns = textwrap.wrap(message, width)
        result.extend(lns)
    return result


def nonblocking_notification(messages: list[str]) -> Form:
    """Generate a std nonblocking notification.

    Args:
        messages: List of messages to display

    Returns:
        Form to display as type dict
    """
    messages = break_long_lines(messages)
    form = {
        "title": "Working on it...",
        "title_color": 2,
        "fields": [{"name": "message", "messages": messages, "type": "working"}],
        "type": "working",
    }
    return dict_to_form(form)


def settings_notification(color: bool, messages: list[ExitMessage]) -> Form:
    """Generate a warning notification for settings errors.

    Args:
        messages: List of messages to display
        color: Bool to reflect if color is transferred or not

    Returns:
        The form to display
    """
    # Take the initial warning if there is one
    if messages[0].prefix is ExitPrefix.WARNING:
        title = messages.pop(0).to_lines(color=False, width=console_width(), with_prefix=True)[0]
    else:
        title = "Warning"

    formatted = ExitMessages(messages).to_strings(color=color, width=console_width())
    formatted_curses = CursesLines(
        tuple(ansi_to_curses(line) for line in formatted),
    )
    form = Form(
        FormType.NOTIFICATION,
        title=title,
        title_color=Color.YELLOW,
        fields=[
            FieldCursesInformation(
                name="settings_warning",
                information=formatted_curses,
            ),
        ],
    )
    return form


def warning_notification(messages: list[str]) -> Form:
    """Generate a std warning notification.

    Args:
        messages: List of warning messages to be displayed

    Returns:
        Form to display as type dict
    """
    messages = break_long_lines(messages)
    form = {
        "title": "WARNING",
        "title_color": 3,
        "fields": [{"name": "info", "information": messages, "type": "information"}],
        "type": "notification",
    }
    return dict_to_form(form)


def error_notification(messages: list[str]) -> Form:
    """Generate a std error notification.

    Args:
        messages: List of error messages to display

    Returns:
        Form to display as type dict
    """
    messages = break_long_lines(messages)
    form = {
        "title": "ERROR",
        "title_color": 1,
        "fields": [{"name": "info", "information": messages, "type": "information"}],
        "type": "notification",
    }
    return dict_to_form(form)


def success_notification(messages: list[str]) -> Form:
    """Generate a std success notification.

    Args:
        messages: List of success messages to display

    Returns:
        Form to display as type dict
    """
    messages = break_long_lines(messages)
    form = {
        "title": "SUCCESS",
        "title_color": 2,
        "fields": [{"name": "info", "information": messages, "type": "information"}],
        "type": "notification",
    }
    return dict_to_form(form)
