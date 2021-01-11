import copy
from functools import partial
from typing import Dict


from .field_checks import FieldChecks
from .field_option import FieldOption
from .field_radio import FieldRadio
from .field_text import FieldText
from .field_validators import FieldValidators
from .form import Form


def dict_to_form(form_data: Dict) -> Form:
    """convert a python dict to a form"""
    form = Form()
    form._dict = form_data  # pylint: disable=protected-access
    form.title = form_data["title"]
    for field in form_data["fields"]:
        field_params = {"name": field["name"], "prompt": field["prompt"]}
        if field["type"] == "text_input":
            field_params["validator"] = getattr(FieldValidators, field["validator"]["name"])

            if choices := field["validator"].get("choices"):
                field_params["validator"] = partial(field_params["validator"], choices=choices)

            if default := field.get("default"):
                field_params["default"] = default

            frm_field_text = FieldText(**field_params)

            if pre_populate := field.get("pre_populate"):
                frm_field_text.pre_populate(pre_populate)

            form.fields.append(frm_field_text)

        elif field["type"] in ["checkbox", "radio"]:
            field_params["options"] = [FieldOption(**option) for option in field["options"]]
            if field["type"] == "checkbox":
                if max_selected := field.get("max_selected"):
                    field_params["max_selected"] = max_selected
                if min_selected := field.get("min_selected"):
                    field_params["min_selected"] = min_selected
                frm_field_checks = FieldChecks(**field_params)
                form.fields.append(frm_field_checks)

            elif field["type"] == "radio":
                frm_field_radio = FieldRadio(**field_params)
                form.fields.append(frm_field_radio)
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
