"""Tests for extended serialize module functionality."""

from __future__ import annotations

import io
import json
import os
import stat

from pathlib import Path

import yaml

from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.content_defs import ContentView
from ansible_navigator.content_defs import SerializationFormat
from ansible_navigator.utils.serialize import HumanDumper
from ansible_navigator.utils.serialize import _is_multiline_string
from ansible_navigator.utils.serialize import _json_dump
from ansible_navigator.utils.serialize import _json_dumps
from ansible_navigator.utils.serialize import _text_dump
from ansible_navigator.utils.serialize import _yaml_dump
from ansible_navigator.utils.serialize import _yaml_dumps
from ansible_navigator.utils.serialize import serialize
from ansible_navigator.utils.serialize import serialize_write_file
from ansible_navigator.utils.serialize import serialize_write_temp_file
from ansible_navigator.utils.serialize import write_diagnostics_json


class TestSerialize:
    """Tests for the serialize function."""

    def test_serialize_json(self) -> None:
        """Test serialize with JSON format."""
        result = serialize(
            content={"key": "value"},
            content_view=ContentView.NORMAL,
            serialization_format=SerializationFormat.JSON,
        )
        assert result is not None
        parsed = json.loads(result)
        assert parsed == {"key": "value"}

    def test_serialize_yaml(self) -> None:
        """Test serialize with YAML format."""
        result = serialize(
            content={"key": "value"},
            content_view=ContentView.NORMAL,
            serialization_format=SerializationFormat.YAML,
        )
        assert result is not None
        assert "key: value" in result


class TestJsonDumps:
    """Tests for the _json_dumps function."""

    def test_simple_dict(self) -> None:
        """Test JSON dumps with simple dict."""
        result = _json_dumps({"a": 1, "b": 2})
        parsed = json.loads(result)
        assert parsed == {"a": 1, "b": 2}

    def test_non_serializable(self) -> None:
        """Test JSON dumps with non-serializable object."""
        result = _json_dumps({"key": {1, 2, 3}})
        assert "could not be converted" in result


class TestJsonDump:
    """Tests for the _json_dump function."""

    def test_writes_to_file(self) -> None:
        """Test JSON dump writes to file handle."""
        fh = io.StringIO()
        _json_dump({"key": "value"}, fh)
        content = fh.getvalue()
        assert '"key": "value"' in content
        assert content.endswith("\n")

    def test_non_serializable(self) -> None:
        """Test JSON dump with non-serializable writes error."""
        fh = io.StringIO()
        _json_dump({"key": {1, 2}}, fh)
        content = fh.getvalue()
        assert "could not be converted" in content


class TestYamlDumps:
    """Tests for the _yaml_dumps function."""

    def test_simple_dict(self) -> None:
        """Test YAML dumps with simple dict."""
        result = _yaml_dumps({"key": "value"})
        assert result is not None
        assert "key: value" in result

    def test_starts_with_document_marker(self) -> None:
        """Test YAML starts with document marker."""
        result = _yaml_dumps({"a": 1})
        assert result is not None
        assert result.startswith("---")


class TestYamlDump:
    """Tests for the _yaml_dump function."""

    def test_writes_to_file(self) -> None:
        """Test YAML dump writes to file handle."""
        fh = io.StringIO()
        _yaml_dump({"key": "value"}, fh)
        content = fh.getvalue()
        assert "key: value" in content


class TestTextDump:
    """Tests for the _text_dump function."""

    def test_writes_text(self) -> None:
        """Test text dump writes text."""
        fh = io.StringIO()
        _text_dump("hello world", fh)
        assert fh.getvalue() == "hello world\n"

    def test_no_extra_newline(self) -> None:
        """Test text dump doesn't add extra newline."""
        fh = io.StringIO()
        _text_dump("hello\n", fh)
        assert fh.getvalue() == "hello\n"


class TestIsMultilineString:
    """Tests for the _is_multiline_string function."""

    def test_newline(self) -> None:
        """Test detects newline."""
        assert _is_multiline_string("line1\nline2") is True

    def test_carriage_return(self) -> None:
        """Test detects carriage return."""
        assert _is_multiline_string("line1\rline2") is True

    def test_single_line(self) -> None:
        """Test single line returns False."""
        assert _is_multiline_string("single line") is False

    def test_empty_string(self) -> None:
        """Test empty string returns False."""
        assert _is_multiline_string("") is False

    def test_unicode_line_separator(self) -> None:
        """Test detects unicode line separator."""
        assert _is_multiline_string("line1 line2") is True  # noqa: RUF001


class TestHumanDumper:
    """Tests for the HumanDumper class."""

    def test_ignore_aliases(self) -> None:
        """Test ignore_aliases always returns True."""
        dumper = HumanDumper(io.StringIO(""))
        assert dumper.ignore_aliases(None) is True
        assert dumper.ignore_aliases([1, 2, 3]) is True

    def test_multiline_block_style(self) -> None:
        """Test multiline strings use block style."""
        data = {"text": "line1\nline2\nline3"}
        result = yaml.dump(data, Dumper=HumanDumper)
        assert "|" in result


class TestWriteDiagnosticsJson:
    """Tests for the write_diagnostics_json function."""

    def test_creates_file(self, tmp_path: Path) -> None:
        """Test write_diagnostics_json creates a file."""
        path = str(tmp_path / "diag.json")
        write_diagnostics_json(path, 0o600, {"test": "data"})
        assert Path(path).exists()

    def test_file_content(self, tmp_path: Path) -> None:
        """Test written file contains correct JSON."""
        path = str(tmp_path / "diag.json")
        write_diagnostics_json(path, 0o600, {"key": "value"})
        content = json.loads(Path(path).read_text())
        assert content == {"key": "value"}

    def test_file_permissions(self, tmp_path: Path) -> None:
        """Test written file has correct permissions."""
        path = str(tmp_path / "diag.json")
        write_diagnostics_json(path, 0o600, {})
        file_stat = Path(path).stat()
        mode = stat.S_IMODE(file_stat.st_mode)
        assert mode == 0o600

    def test_umask_restored(self, tmp_path: Path) -> None:
        """Test umask is restored after writing."""
        original_umask = os.umask(0o022)
        os.umask(original_umask)
        path = str(tmp_path / "diag.json")
        write_diagnostics_json(path, 0o600, {})
        current_umask = os.umask(0o022)
        os.umask(current_umask)
        assert current_umask == original_umask


class TestSerializeWriteFile:
    """Tests for the serialize_write_file function."""

    def test_write_json(self, tmp_path: Path) -> None:
        """Test writing JSON to a file."""
        output = tmp_path / "out.json"
        serialize_write_file(
            content={"a": 1},
            content_view=ContentView.NORMAL,
            file_mode="w",
            file=output,
            serialization_format=SerializationFormat.JSON,
        )
        content = json.loads(output.read_text())
        assert content == {"a": 1}

    def test_write_yaml(self, tmp_path: Path) -> None:
        """Test writing YAML to a file."""
        output = tmp_path / "out.yml"
        serialize_write_file(
            content={"b": 2},
            content_view=ContentView.NORMAL,
            file_mode="w",
            file=output,
            serialization_format=SerializationFormat.YAML,
        )
        text = output.read_text()
        assert "b: 2" in text


class TestSerializeWriteTempFile:
    """Tests for the serialize_write_temp_file function."""

    def test_write_json_temp(self) -> None:
        """Test writing JSON to a temp file."""
        result = serialize_write_temp_file(
            content={"x": 1},
            content_view=ContentView.NORMAL,
            content_format=ContentFormat.JSON,
        )
        assert result.exists()
        assert result.suffix == ".json"
        content = json.loads(result.read_text())
        assert content == {"x": 1}
        result.unlink()

    def test_write_yaml_temp(self) -> None:
        """Test writing YAML to a temp file."""
        result = serialize_write_temp_file(
            content={"y": 2},
            content_view=ContentView.NORMAL,
            content_format=ContentFormat.YAML,
        )
        assert result.exists()
        assert result.suffix == ".yml"
        assert "y: 2" in result.read_text()
        result.unlink()

    def test_write_text_temp(self) -> None:
        """Test writing text (non-serialized) to a temp file."""
        result = serialize_write_temp_file(
            content="plain text content",
            content_view=ContentView.NORMAL,
            content_format=ContentFormat.TXT,
        )
        assert result.exists()
        assert result.suffix == ".txt"
        assert "plain text content" in result.read_text()
        result.unlink()
