""" simple utils for working with forms
"""
import copy
import shutil
import textwrap

from functools import partial
from typing import Dict
from typing import List


from .field_checks import FieldChecks
from .field_information import FieldInformation
from .field_option import FieldOption
from .field_radio import FieldRadio
from .field_text import FieldText
from .field_working import FieldWorking
from .validators import FieldValidators
from .form import Form
from .form import FormType


def dict_to_form(form_data: Dict) -> Form:
    # pylint: disable=too-many-branches
    """convert a python dict to a form"""
    if form_data.get("type") == "notification":
        form = Form(type=FormType.NOTIFICATION)
    elif form_data.get("type") == "working":
        form = Form(type=FormType.WORKING)
    else:
        form = Form(type=FormType.FORM)

    form._dict = form_data  # pylint: disable=protected-access
    form.title = form_data["title"]
    form.title_color = form_data.get("title_color", 0)

    for field in form_data["fields"]:
        field_params = {"name": field["name"]}
        if field["type"] == "text_input":
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

            form.fields.append(frm_field_text)

        elif field["type"] in ["checkbox", "radio"]:
            field_params["prompt"] = field["prompt"]
            field_params["options"] = [FieldOption(**option) for option in field["options"]]
            if field["type"] == "checkbox":
                max_selected = field.get("max_selected")
                if max_selected:
                    field_params["max_selected"] = max_selected

                min_selected = field.get("min_selected")
                if min_selected:
                    field_params["min_selected"] = min_selected
                frm_field_checks = FieldChecks(**field_params)
                form.fields.append(frm_field_checks)

            elif field["type"] == "radio":
                frm_field_radio = FieldRadio(**field_params)
                form.fields.append(frm_field_radio)

        elif field["type"] == "information":
            frm_field_info = FieldInformation(name=field["name"], information=field["information"])
            form.fields.append(frm_field_info)

        elif field["type"] == "working":
            frm_field_working = FieldWorking(name=field["name"], messages=field["messages"])
            form.fields.append(frm_field_working)

    return form


def form_to_dict(form: Form, key_on_name: bool = False) -> Dict:
    """populate the original _dict of the form
    with the results
    """
    res = form._dict  # pylint: disable=protected-access
    res["cancelled"] = form.cancelled
    res["submitted"] = form.submitted
    for idx, field in enumerate(form.fields):
        if isinstance(field, FieldText):
            res["fields"][idx]["response"] = copy.copy(field.response)
            res["fields"][idx]["value"] = copy.copy(field.value)
        elif isinstance(field, (FieldChecks, FieldRadio)):
            for oidx, option in enumerate(field.options):
                res["fields"][idx]["options"][oidx]["checked"] = option.checked
            res["fields"][idx]["checked"] = [
                option.name for option in field.options if option.checked
            ]

    if key_on_name:
        fields = {}
        for field in res["fields"]:
            fields[field["name"]] = field
            if "options" in field:
                options = {}
                for option in field["options"]:
                    options[option["name"]] = option
                fields[field["name"]]["options"] = options
        res["fields"] = fields
    return res


def break_long_lines(messages):
    """break lines such that the form widt !> 80%"""
    width = int(shutil.get_terminal_size().columns * 0.8)
    result = []
    for message in messages:
        lns = textwrap.wrap(message, width)
        result.extend(lns)
    return result


def nonblocking_notification(messages: List[str]) -> Form:
    """generate a std nonblocking notification"""
    messages = break_long_lines(messages)
    form = {
        "title": "Working on it...",
        "title_color": 2,
        "fields": [{"name": "message", "messages": messages, "type": "working"}],
        "type": "working",
    }
    return dict_to_form(form)


def warning_notification(messages: List[str]) -> Form:
    """generate a std warning notification"""
    messages = break_long_lines(messages)
    form = {
        "title": "WARNING",
        "title_color": 3,
        "fields": [{"name": "info", "information": messages, "type": "information"}],
        "type": "notification",
    }
    return dict_to_form(form)
