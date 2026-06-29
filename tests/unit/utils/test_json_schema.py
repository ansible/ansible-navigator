"""Tests for the json_schema module."""

from __future__ import annotations

import json

from collections import deque

import pytest

from ansible_navigator.utils.definitions import ExitMessage
from ansible_navigator.utils.json_schema import JsonSchemaError
from ansible_navigator.utils.json_schema import json_path
from ansible_navigator.utils.json_schema import to_path
from ansible_navigator.utils.json_schema import validate


class TestToPath:
    """Tests for the to_path function."""

    def test_list_input(self) -> None:
        """Test to_path with a list."""
        assert to_path(["a", "b", "c"]) == "a.b.c"

    def test_deque_input(self) -> None:
        """Test to_path with a deque."""
        assert to_path(deque(["a", "b"])) == "a.b"

    def test_mixed_types(self) -> None:
        """Test to_path with mixed types."""
        assert to_path(["a", 1, "b"]) == "a.1.b"

    def test_single_element(self) -> None:
        """Test to_path with single element."""
        assert to_path(["a"]) == "a"

    def test_empty(self) -> None:
        """Test to_path with empty sequence."""
        assert to_path([]) == ""


class TestJsonPath:
    """Tests for the json_path function."""

    def test_string_elements(self) -> None:
        """Test json_path with string elements."""
        assert json_path(["foo", "bar"]) == "$.foo.bar"

    def test_integer_elements(self) -> None:
        """Test json_path with integer elements."""
        assert json_path([0, 1]) == "$[0][1]"

    def test_mixed_elements(self) -> None:
        """Test json_path with mixed elements."""
        assert json_path(["foo", 0, "bar"]) == "$.foo[0].bar"

    def test_empty(self) -> None:
        """Test json_path with empty path."""
        assert json_path([]) == "$"


class TestJsonSchemaError:
    """Tests for the JsonSchemaError dataclass."""

    def test_to_friendly(self) -> None:
        """Test to_friendly returns formatted message."""
        error = JsonSchemaError(
            message="is not valid",
            data_path="a.b",
            json_path="$.a.b",
            schema_path="properties.a",
            relative_schema="{}",
            expected="string",
            validator="type",
            found="42",
        )
        assert error.to_friendly() == "In 'a.b': is not valid."

    def test_to_exit_message(self) -> None:
        """Test to_exit_message returns ExitMessage."""
        error = JsonSchemaError(
            message="is not valid",
            data_path="x",
            json_path="$.x",
            schema_path="",
            relative_schema="",
            expected="",
            validator="",
            found="",
        )
        result = error.to_exit_message()
        assert isinstance(result, ExitMessage)
        assert "In 'x'" in result.message


class TestValidate:
    """Tests for the validate function."""

    def test_valid_data(self) -> None:
        """Test validate with valid data returns no errors."""
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
        }
        errors = validate(schema, {"name": "test"})
        assert not errors

    def test_invalid_data(self) -> None:
        """Test validate with invalid data returns errors."""
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
        }
        errors = validate(schema, {"name": 42})
        assert len(errors) > 0
        assert errors[0].validator == "type"

    def test_schema_as_json_string(self) -> None:
        """Test validate with schema as JSON string."""
        schema_str = json.dumps(
            {
                "type": "object",
                "properties": {"age": {"type": "integer"}},
            }
        )
        errors = validate(schema_str, {"age": 25})
        assert not errors

    def test_required_field_missing(self) -> None:
        """Test validate detects missing required fields."""
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        }
        errors = validate(schema, {})
        assert len(errors) > 0

    def test_error_fields_populated(self) -> None:
        """Test validate populates error fields correctly."""
        schema = {
            "type": "object",
            "properties": {"count": {"type": "integer"}},
        }
        errors = validate(schema, {"count": "not-a-number"})
        assert len(errors) == 1
        error = errors[0]
        assert error.data_path == "count"
        assert error.json_path == "$.count"
        assert error.message != ""

    def test_bool_schema_raises_type_error(self) -> None:
        """Test validate raises TypeError on bool schema."""
        with pytest.raises(TypeError, match="Unexpected schema data"):
            validate(True, {})  # type: ignore[arg-type]

    def test_invalid_schema(self) -> None:
        """Test validate with an invalid schema returns schema error."""
        bad_schema = {"type": "not_a_real_type"}
        errors = validate(bad_schema, {})
        assert len(errors) > 0
