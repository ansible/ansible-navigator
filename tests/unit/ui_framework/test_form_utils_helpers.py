"""Tests for pure helper functions in form_utils module."""

from __future__ import annotations

from typing import Any

from ansible_navigator.ui_framework.field_checks import FieldChecks
from ansible_navigator.ui_framework.field_option import FieldOption
from ansible_navigator.ui_framework.field_radio import FieldRadio
from ansible_navigator.ui_framework.field_text import FieldText
from ansible_navigator.ui_framework.form_utils import _build_checks_field
from ansible_navigator.ui_framework.form_utils import _build_radio_field
from ansible_navigator.ui_framework.form_utils import _build_text_field
from ansible_navigator.ui_framework.form_utils import _rekey_fields_by_name


class TestBuildTextField:
    """Tests for _build_text_field."""

    def test_returns_field_text(self) -> None:
        """The builder returns a FieldText instance."""
        field_data = {
            "name": "username",
            "prompt": "Enter username",
            "validator": {"name": "something"},
        }
        result = _build_text_field(field_data)
        assert isinstance(result, FieldText)

    def test_name_and_prompt(self) -> None:
        """Name and prompt are set correctly."""
        field_data = {
            "name": "host",
            "prompt": "Enter host",
            "validator": {"name": "something"},
        }
        result = _build_text_field(field_data)
        assert result.name == "host"
        assert result.prompt == "Enter host"

    def test_default_value(self) -> None:
        """Default is set when provided."""
        field_data = {
            "name": "port",
            "prompt": "Enter port",
            "validator": {"name": "something"},
            "default": "8080",
        }
        result = _build_text_field(field_data)
        assert result.default == "8080"

    def test_validator_with_choices(self) -> None:
        """Validator with choices creates a partial."""
        field_data = {
            "name": "color",
            "prompt": "Pick color",
            "validator": {"name": "one_of", "choices": ["red", "blue"]},
        }
        result = _build_text_field(field_data)
        assert isinstance(result, FieldText)


class TestBuildChecksField:
    """Tests for _build_checks_field."""

    def test_returns_field_checks(self) -> None:
        """The builder returns a FieldChecks instance."""
        field_data = {
            "name": "features",
            "prompt": "Select features",
            "options": [
                {"name": "opt_a", "text": "Option A"},
                {"name": "opt_b", "text": "Option B"},
            ],
        }
        result = _build_checks_field(field_data)
        assert isinstance(result, FieldChecks)

    def test_options_are_field_option_instances(self) -> None:
        """Each option should be a FieldOption."""
        field_data = {
            "name": "features",
            "prompt": "Select features",
            "options": [
                {"name": "opt_a", "text": "Option A"},
            ],
        }
        result = _build_checks_field(field_data)
        assert len(result.options) == 1
        assert isinstance(result.options[0], FieldOption)
        assert result.options[0].name == "opt_a"

    def test_max_min_selected(self) -> None:
        """Max and min selected are set when provided."""
        field_data = {
            "name": "features",
            "prompt": "Select features",
            "options": [
                {"name": "opt_a", "text": "Option A"},
            ],
            "max_selected": 3,
            "min_selected": 1,
        }
        result = _build_checks_field(field_data)
        assert result.max_selected == 3
        assert result.min_selected == 1


class TestBuildRadioField:
    """Tests for _build_radio_field."""

    def test_returns_field_radio(self) -> None:
        """The builder returns a FieldRadio instance."""
        field_data = {
            "name": "mode",
            "prompt": "Select mode",
            "options": [
                {"name": "fast", "text": "Fast"},
                {"name": "slow", "text": "Slow"},
            ],
        }
        result = _build_radio_field(field_data)
        assert isinstance(result, FieldRadio)

    def test_options_populated(self) -> None:
        """Options are populated correctly."""
        field_data = {
            "name": "mode",
            "prompt": "Select mode",
            "options": [
                {"name": "fast", "text": "Fast"},
                {"name": "slow", "text": "Slow"},
            ],
        }
        result = _build_radio_field(field_data)
        assert len(result.options) == 2
        assert result.options[0].text == "Fast"
        assert result.options[1].text == "Slow"


class TestRekeyFieldsByName:
    """Tests for _rekey_fields_by_name."""

    def test_basic_rekey(self) -> None:
        """Fields list is rekeyed by name."""
        res = {
            "fields": [
                {"name": "username", "value": "admin"},
                {"name": "password", "value": "secret"},
            ],
        }
        result = _rekey_fields_by_name(res)
        assert "username" in result
        assert "password" in result
        assert result["username"]["value"] == "admin"
        assert result["password"]["value"] == "secret"

    def test_rekey_with_options(self) -> None:
        """Fields with options are also rekeyed by name."""
        res = {
            "fields": [
                {
                    "name": "features",
                    "options": [
                        {"name": "opt_a", "checked": True},
                        {"name": "opt_b", "checked": False},
                    ],
                },
            ],
        }
        result = _rekey_fields_by_name(res)
        assert "features" in result
        assert "opt_a" in result["features"]["options"]
        assert "opt_b" in result["features"]["options"]
        assert result["features"]["options"]["opt_a"]["checked"] is True

    def test_empty_fields(self) -> None:
        """Empty fields list produces empty dict."""
        res: dict[str, list[Any]] = {"fields": []}
        result = _rekey_fields_by_name(res)
        assert not result
