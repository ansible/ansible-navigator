"""Functionality to perform json schema validation."""

from __future__ import annotations

import json

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any

from jsonschema import SchemaError
from jsonschema import ValidationError
from jsonschema.validators import validator_for

from .definitions import ExitMessage


if TYPE_CHECKING:
    from collections import deque


def to_path(schema_path: deque[Any]) -> str:
    """Flatten a path to a dot delimited string.

    Args:
        schema_path: The schema path

    Returns:
        The dot delimited path
    """
    return ".".join(str(index) for index in schema_path)


def json_path(absolute_path: deque[Any]) -> str:
    """Flatten a data path to a dot delimited string.

    Args:
        absolute_path: The path

    Returns:
        The dot delimited string
    """
    path = "$"
    for elem in absolute_path:
        if isinstance(elem, int):
            path += "[" + str(elem) + "]"
        else:
            path += "." + elem
    return path


@dataclass
class JsonSchemaError:
    # pylint: disable=too-many-instance-attributes
    """Data structure to hold a json schema validation error."""

    message: str
    data_path: str
    json_path: str
    schema_path: str
    relative_schema: str
    expected: bool | int | str
    validator: str
    found: str

    def to_friendly(self) -> str:
        """Provide a friendly explanation of the error.

        Returns:
            The error message
        """
        return f"In '{self.data_path}': {self.message}."

    def to_exit_message(self) -> ExitMessage:
        """Provide an exit message for a schema validation failure.

        Returns:
            The exit message
        """
        return ExitMessage(message=self.to_friendly())


def validate(schema: str | dict[str, Any], data: dict[str, Any]) -> list[JsonSchemaError]:
    """Validate some data against a JSON schema.

    Args:
        schema: the JSON schema to use for validation
        data: The data to validate

    Returns:
        Any errors encountered
    """
    errors: list[JsonSchemaError] = []

    if isinstance(schema, str):
        schema = json.loads(schema)
    if isinstance(schema, bool):
        msg = "Unexpected schema data."
        raise TypeError(msg)
    validator = validator_for(schema)
    try:
        validator.check_schema(schema)
    except SchemaError as exc:
        error = JsonSchemaError(
            message=str(exc),
            data_path="schema sanity check",
            json_path="",
            schema_path="",
            relative_schema="",
            expected="",
            validator="",
            found="",
        )
        errors.append(error)
        return errors

    validation_errors = sorted(validator(schema).iter_errors(data), key=lambda e: e.path)

    if not validation_errors:
        return errors

    for validation_error in validation_errors:
        if isinstance(validation_error, ValidationError):
            error = JsonSchemaError(
                message=validation_error.message,
                data_path=to_path(validation_error.absolute_path),
                json_path=json_path(validation_error.absolute_path),
                schema_path=to_path(validation_error.relative_schema_path),
                relative_schema=validation_error.schema,
                expected=validation_error.validator_value,
                validator=validation_error.validator,
                found=validation_error.instance,
            )
            errors.append(error)
    return errors
