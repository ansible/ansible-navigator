"""Predefined form field validators."""

from __future__ import annotations

import os

from collections.abc import Iterable
from random import randrange
from typing import Any
from typing import NamedTuple
from urllib.parse import urlparse

from .form_defs import FieldValidationStates
from .sentinels import Unknown
from .sentinels import unknown


class Validation(NamedTuple):
    """The response from a validation."""

    value: Any
    error_msg: str


class FieldValidators:
    """A box in which field validators are put."""

    @staticmethod
    def http(text: str = "", hint: bool = False) -> Validation | str:
        """Validate http or https.

        :param text: The text to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        msg = "Please enter a valid URL"
        if hint:
            return msg
        if text:
            result = urlparse(text)
            if result.scheme in ["http", "https"] and result.hostname:
                msg = ""
        return Validation(value=text, error_msg=msg)

    @staticmethod
    def masked_or_none(text="", hint: bool = False) -> Validation | str:
        """Validate a masked field or None.

        :param text: The text to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        if hint:
            return "Please provide a value (optional)"
        value = "*" * randrange(15, 20) if text else ""
        return Validation(value=value, error_msg="")

    @staticmethod
    def none(
        text: FieldValidationStates | str = "",
        hint: bool = False,
    ) -> Validation | str:
        """Validate nothing about this field.

        :param text: The text to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        if hint:
            return "Please provide a value (optional)"
        return Validation(value=text, error_msg="")

    @staticmethod
    def null(text="", hint: bool = False) -> Validation | str:
        """No validation, no message.

        :param text: The text to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        if hint:
            return ""
        return Validation(value=text, error_msg="")

    @staticmethod
    def one_of(choices: list = [], text: str = "", hint: bool = False) -> Validation | str:
        """Validate that some text is one of choices.

        :param choices: The list of choices
        :param text: The text to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        choices_str = f"{', '.join(choices[:-1])} or {choices[-1]}" if choices else ""
        msg = f"Please enter {choices_str}"
        value = text
        if hint:
            return msg
        try:
            value = choices[[c.lower() for c in choices].index(text.lower())]
            msg = ""
        except ValueError:
            pass
        return Validation(value=value, error_msg=msg)

    @staticmethod
    def some_of_or_none(
        choices: Unknown | list = unknown,
        min_selected: Unknown | int = unknown,
        max_selected: Unknown | int = unknown,
        hint: bool = False,
    ) -> Validation | str:
        """Validate a checkbox set.

        :param choices: The list of choices
        :param min_selected: The minimum number of choices that must be selected
        :param max_selected: The maximum number of choices that can be selected
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        :raises TypeError: If the types are not as expected
        """
        if min_selected == max_selected:
            word = "entry" if min_selected == 1 else "entries"
            msg = f"Please select {min_selected!s} {word}"
        else:
            msg = f"Please select between {min_selected} and "
            word = str(max_selected) if max_selected != -1 else "all"
            msg += f"{word} entries"

        if hint:
            return msg
        if (
            isinstance(min_selected, int)
            and isinstance(max_selected, int)
            and isinstance(choices, Iterable)
        ):
            checked = len([choice for choice in choices if choice.checked])
            if max_selected >= checked >= min_selected:
                msg = ""

            return Validation(value=choices, error_msg=msg)
        raise TypeError

    @staticmethod
    def something(text: str = "", hint: bool = False) -> Validation | str:
        """Validate that the text is not an empty string.

        :param text: The text to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        msg = "Please provide a value (required)"
        if hint:
            return msg
        if text:
            msg = ""
        return Validation(value=text, error_msg=msg)

    @staticmethod
    def true_false(text: str = "", hint: bool = False) -> Validation | str:
        """Validate true or false.

        :param text: The text to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        msg = "Please enter true or false"
        if hint:
            return msg
        if text:
            if text[0].lower() == "t":
                value = True
                msg = ""
                return Validation(value=value, error_msg=msg)

            if text[0].lower() == "f":
                value = False
                msg = ""
                return Validation(value=value, error_msg=msg)
        return Validation(value=text, error_msg=msg)

    @staticmethod
    def valid_file_path(text: str = "", hint=False) -> Validation | str:
        """Validate that a file path is a real file.

        :param text: The text to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        msg = "Please enter a valid file path"
        if hint:
            return msg
        value = os.path.abspath(os.path.expanduser(text))
        if os.path.exists(value) and os.path.isfile(value):
            msg = ""
        else:
            value = text
        return Validation(value=value, error_msg=msg)

    @staticmethod
    def valid_path(text: str = "", hint=False) -> Validation | str:
        """Validate that a path is real.

        :param text: The text to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        msg = "Please enter a valid file or directory path"
        if hint:
            return msg
        value = os.path.abspath(os.path.expanduser(text))
        if os.path.exists(value):
            msg = ""
        else:
            value = text
        return Validation(value=value, error_msg=msg)

    @staticmethod
    def valid_path_or_none(text: str = "", hint=False) -> Validation | str:
        """Validate that a path is real or none.

        :param text: The text to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        msg = "Please enter a valid path or leave blank"
        if hint:
            return msg

        if text == "":
            msg = ""
            value = text
        else:
            value = os.path.abspath(os.path.expanduser(text))
            if os.path.exists(value):
                msg = ""
            else:
                value = text
        return Validation(value=value, error_msg=msg)

    @staticmethod
    def yes_no(text: str = "", hint: bool = False) -> Validation | str:
        """Validate yes or no.

        :param text: The text to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        msg = "Please enter yes or no"
        value = text
        if hint:
            return msg
        if text:
            if text[0] == "y":
                value = "yes"
                msg = ""
            elif text[0] == "n":
                value = "no"
                msg = ""
        return Validation(value=value, error_msg=msg)


class FormValidators:
    """Validators for a form."""

    @staticmethod
    def all_true(response: list | None = None, hint: bool = False) -> Validation | str:
        """Validate all in list are true.

        :param response: The list to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        msg = "Please ensure all values are true"
        if hint:
            return msg
        response = response or []
        if all(v is True for v in response):
            msg = ""
        return Validation(value=response, error_msg=msg)

    @staticmethod
    def no_validation(
        response: list | None = None,
        hint: bool = False,
    ) -> Validation | str:
        """No validation.

        :param response: The list to validate
        :param hint: If True, return a hint message instead of a Validation
        :returns: A Validation or a hint message
        """
        msg = ""
        if hint:
            return msg
        return Validation(value=response, error_msg=msg)
