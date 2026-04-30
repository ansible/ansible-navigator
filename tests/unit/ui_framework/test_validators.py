"""Tests for the validators module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

from ansible_navigator.ui_framework.validators import FieldValidators
from ansible_navigator.ui_framework.validators import FormValidators
from ansible_navigator.ui_framework.validators import Validation


if TYPE_CHECKING:
    from pathlib import Path


class TestFieldValidatorsHttp:
    """Tests for the http validator."""

    def test_hint(self) -> None:
        """Test hint returns a message string."""
        result = FieldValidators.http(hint=True)
        assert isinstance(result, str)
        assert "URL" in result

    def test_valid_http(self) -> None:
        """Test valid http URL."""
        result = FieldValidators.http(text="http://example.com")
        assert isinstance(result, Validation)
        assert result.error_msg == ""

    def test_valid_https(self) -> None:
        """Test valid https URL."""
        result = FieldValidators.http(text="https://example.com/path")
        assert isinstance(result, Validation)
        assert result.error_msg == ""

    def test_invalid_url(self) -> None:
        """Test invalid URL."""
        result = FieldValidators.http(text="not-a-url")
        assert isinstance(result, Validation)
        assert result.error_msg != ""

    def test_empty_text(self) -> None:
        """Test empty text."""
        result = FieldValidators.http(text="")
        assert isinstance(result, Validation)
        assert result.error_msg != ""

    def test_ftp_scheme(self) -> None:
        """Test ftp scheme is rejected."""
        result = FieldValidators.http(text="ftp://example.com")
        assert isinstance(result, Validation)
        assert result.error_msg != ""


class TestFieldValidatorsMaskedOrNone:
    """Tests for the masked_or_none validator."""

    def test_hint(self) -> None:
        """Test hint returns a message string."""
        result = FieldValidators.masked_or_none(hint=True)
        assert isinstance(result, str)

    def test_with_text(self) -> None:
        """Test with text returns masked value."""
        result = FieldValidators.masked_or_none(text="secret")
        assert isinstance(result, Validation)
        assert result.error_msg == ""
        assert all(c == "*" for c in result.value)
        assert 15 <= len(result.value) <= 19

    def test_empty_text(self) -> None:
        """Test empty text returns empty value."""
        result = FieldValidators.masked_or_none(text="")
        assert isinstance(result, Validation)
        assert result.value == ""


class TestFieldValidatorsNone:
    """Tests for the none validator."""

    def test_hint(self) -> None:
        """Test hint returns a message string."""
        result = FieldValidators.none(hint=True)
        assert isinstance(result, str)

    def test_with_text(self) -> None:
        """Test with text passes through."""
        result = FieldValidators.none(text="anything")
        assert isinstance(result, Validation)
        assert result.value == "anything"
        assert result.error_msg == ""


class TestFieldValidatorsNull:
    """Tests for the null validator."""

    def test_hint(self) -> None:
        """Test hint returns empty string."""
        result = FieldValidators.null(hint=True)
        assert result == ""

    def test_with_text(self) -> None:
        """Test with text passes through."""
        result = FieldValidators.null(text="value")
        assert isinstance(result, Validation)
        assert result.error_msg == ""


class TestFieldValidatorsOneOf:
    """Tests for the one_of validator."""

    def test_hint(self) -> None:
        """Test hint includes choices."""
        result = FieldValidators.one_of(choices=["a", "b", "c"], hint=True)
        assert isinstance(result, str)
        assert "a" in result

    def test_valid_choice(self) -> None:
        """Test valid choice."""
        result = FieldValidators.one_of(choices=["yes", "no"], text="yes")
        assert isinstance(result, Validation)
        assert result.error_msg == ""
        assert result.value == "yes"

    def test_case_insensitive(self) -> None:
        """Test case insensitive matching."""
        result = FieldValidators.one_of(choices=["Yes", "No"], text="yes")
        assert isinstance(result, Validation)
        assert result.value == "Yes"
        assert result.error_msg == ""

    def test_invalid_choice(self) -> None:
        """Test invalid choice."""
        result = FieldValidators.one_of(choices=["a", "b"], text="c")
        assert isinstance(result, Validation)
        assert result.error_msg != ""


class TestFieldValidatorsSomething:
    """Tests for the something validator."""

    def test_hint(self) -> None:
        """Test hint returns message."""
        result = FieldValidators.something(hint=True)
        assert isinstance(result, str)
        assert "required" in result

    def test_with_text(self) -> None:
        """Test with text passes."""
        result = FieldValidators.something(text="hello")
        assert isinstance(result, Validation)
        assert result.error_msg == ""

    def test_empty_text(self) -> None:
        """Test empty text fails."""
        result = FieldValidators.something(text="")
        assert isinstance(result, Validation)
        assert result.error_msg != ""


class TestFieldValidatorsTrueFalse:
    """Tests for the true_false validator."""

    def test_hint(self) -> None:
        """Test hint returns message."""
        result = FieldValidators.true_false(hint=True)
        assert isinstance(result, str)

    def test_true(self) -> None:
        """Test 'true' input."""
        result = FieldValidators.true_false(text="true")
        assert isinstance(result, Validation)
        assert result.value is True
        assert result.error_msg == ""

    def test_true_prefix(self) -> None:
        """Test 't' prefix is accepted."""
        result = FieldValidators.true_false(text="t")
        assert isinstance(result, Validation)
        assert result.value is True

    def test_false(self) -> None:
        """Test 'false' input."""
        result = FieldValidators.true_false(text="false")
        assert isinstance(result, Validation)
        assert result.value is False
        assert result.error_msg == ""

    def test_false_prefix(self) -> None:
        """Test 'f' prefix is accepted."""
        result = FieldValidators.true_false(text="f")
        assert isinstance(result, Validation)
        assert result.value is False

    def test_invalid(self) -> None:
        """Test invalid input."""
        result = FieldValidators.true_false(text="maybe")
        assert isinstance(result, Validation)
        assert result.error_msg != ""

    def test_empty(self) -> None:
        """Test empty input."""
        result = FieldValidators.true_false(text="")
        assert isinstance(result, Validation)
        assert result.error_msg != ""


class TestFieldValidatorsValidFilePath:
    """Tests for the valid_file_path validator."""

    def test_hint(self) -> None:
        """Test hint returns message."""
        result = FieldValidators.valid_file_path(hint=True)
        assert isinstance(result, str)

    def test_valid_file(self, tmp_path: Path) -> None:
        """Test with a valid file path."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        result = FieldValidators.valid_file_path(text=str(test_file))
        assert isinstance(result, Validation)
        assert result.error_msg == ""

    def test_invalid_file(self) -> None:
        """Test with a nonexistent file."""
        result = FieldValidators.valid_file_path(text="/nonexistent/file.txt")
        assert isinstance(result, Validation)
        assert result.error_msg != ""

    def test_directory_not_file(self, tmp_path: Path) -> None:
        """Test with a directory path (not a file)."""
        result = FieldValidators.valid_file_path(text=str(tmp_path))
        assert isinstance(result, Validation)
        assert result.error_msg != ""


class TestFieldValidatorsValidPath:
    """Tests for the valid_path validator."""

    def test_hint(self) -> None:
        """Test hint returns message."""
        result = FieldValidators.valid_path(hint=True)
        assert isinstance(result, str)

    def test_valid_directory(self, tmp_path: Path) -> None:
        """Test with a valid directory path."""
        result = FieldValidators.valid_path(text=str(tmp_path))
        assert isinstance(result, Validation)
        assert result.error_msg == ""

    def test_invalid_path(self) -> None:
        """Test with a nonexistent path."""
        result = FieldValidators.valid_path(text="/nonexistent/path")
        assert isinstance(result, Validation)
        assert result.error_msg != ""


class TestFieldValidatorsValidPathOrNone:
    """Tests for the valid_path_or_none validator."""

    def test_hint(self) -> None:
        """Test hint returns message."""
        result = FieldValidators.valid_path_or_none(hint=True)
        assert isinstance(result, str)

    def test_empty_is_valid(self) -> None:
        """Test empty string is valid."""
        result = FieldValidators.valid_path_or_none(text="")
        assert isinstance(result, Validation)
        assert result.error_msg == ""

    def test_valid_path(self, tmp_path: Path) -> None:
        """Test with a valid path."""
        result = FieldValidators.valid_path_or_none(text=str(tmp_path))
        assert isinstance(result, Validation)
        assert result.error_msg == ""

    def test_invalid_path(self) -> None:
        """Test with a nonexistent path."""
        result = FieldValidators.valid_path_or_none(text="/nonexistent")
        assert isinstance(result, Validation)
        assert result.error_msg != ""


class TestFieldValidatorsYesNo:
    """Tests for the yes_no validator."""

    def test_hint(self) -> None:
        """Test hint returns message."""
        result = FieldValidators.yes_no(hint=True)
        assert isinstance(result, str)

    def test_yes(self) -> None:
        """Test 'yes' input."""
        result = FieldValidators.yes_no(text="yes")
        assert isinstance(result, Validation)
        assert result.value == "yes"
        assert result.error_msg == ""

    def test_yes_prefix(self) -> None:
        """Test 'y' prefix is accepted."""
        result = FieldValidators.yes_no(text="y")
        assert isinstance(result, Validation)
        assert result.value == "yes"

    def test_no(self) -> None:
        """Test 'no' input."""
        result = FieldValidators.yes_no(text="no")
        assert isinstance(result, Validation)
        assert result.value == "no"
        assert result.error_msg == ""

    def test_no_prefix(self) -> None:
        """Test 'n' prefix is accepted."""
        result = FieldValidators.yes_no(text="n")
        assert isinstance(result, Validation)
        assert result.value == "no"

    def test_invalid(self) -> None:
        """Test invalid input."""
        result = FieldValidators.yes_no(text="maybe")
        assert isinstance(result, Validation)
        assert result.error_msg != ""

    def test_empty(self) -> None:
        """Test empty input."""
        result = FieldValidators.yes_no(text="")
        assert isinstance(result, Validation)
        assert result.error_msg != ""


@dataclass
class MockCheckbox:
    """A mock checkbox for testing some_of_or_none."""

    checked: bool


class TestFieldValidatorsSomeOfOrNone:
    """Tests for the some_of_or_none validator."""

    def test_hint_equal_min_max(self) -> None:
        """Test hint with equal min and max."""
        result = FieldValidators.some_of_or_none(min_selected=1, max_selected=1, hint=True)
        assert isinstance(result, str)
        assert "1 entry" in result

    def test_hint_range(self) -> None:
        """Test hint with range."""
        result = FieldValidators.some_of_or_none(min_selected=1, max_selected=3, hint=True)
        assert isinstance(result, str)
        assert "1" in result
        assert "3" in result

    def test_hint_unlimited(self) -> None:
        """Test hint with max_selected=-1 (all)."""
        result = FieldValidators.some_of_or_none(min_selected=1, max_selected=-1, hint=True)
        assert isinstance(result, str)
        assert "all" in result

    def test_valid_selection(self) -> None:
        """Test valid number of selections."""
        choices = [MockCheckbox(checked=True), MockCheckbox(checked=False)]
        result = FieldValidators.some_of_or_none(
            choices=choices,
            min_selected=1,
            max_selected=2,
        )
        assert isinstance(result, Validation)
        assert result.error_msg == ""

    def test_too_few_selected(self) -> None:
        """Test too few selections."""
        choices = [MockCheckbox(checked=False), MockCheckbox(checked=False)]
        result = FieldValidators.some_of_or_none(
            choices=choices,
            min_selected=1,
            max_selected=2,
        )
        assert isinstance(result, Validation)
        assert result.error_msg != ""

    def test_type_error(self) -> None:
        """Test TypeError with wrong types."""
        from ansible_navigator.ui_framework.sentinels import unknown

        with pytest.raises(TypeError):
            FieldValidators.some_of_or_none(
                choices=unknown,
                min_selected=unknown,
                max_selected=unknown,
            )


class TestFormValidatorsAllTrue:
    """Tests for the all_true form validator."""

    def test_hint(self) -> None:
        """Test hint returns message."""
        result = FormValidators.all_true(hint=True)
        assert isinstance(result, str)

    def test_all_true(self) -> None:
        """Test all values are True."""
        result = FormValidators.all_true(response=[True, True, True])
        assert isinstance(result, Validation)
        assert result.error_msg == ""

    def test_not_all_true(self) -> None:
        """Test not all values are True."""
        result = FormValidators.all_true(response=[True, False, True])
        assert isinstance(result, Validation)
        assert result.error_msg != ""

    def test_empty_list(self) -> None:
        """Test empty list is valid."""
        result = FormValidators.all_true(response=[])
        assert isinstance(result, Validation)
        assert result.error_msg == ""

    def test_none_response(self) -> None:
        """Test None response defaults to empty list."""
        result = FormValidators.all_true(response=None)
        assert isinstance(result, Validation)
        assert result.error_msg == ""


class TestFormValidatorsNoValidation:
    """Tests for the no_validation form validator."""

    def test_hint(self) -> None:
        """Test hint returns empty string."""
        result = FormValidators.no_validation(hint=True)
        assert result == ""

    def test_with_response(self) -> None:
        """Test with response passes through."""
        result = FormValidators.no_validation(response=[1, 2, 3])
        assert isinstance(result, Validation)
        assert result.error_msg == ""
