"""Tests for the content_defs module."""

from __future__ import annotations

from dataclasses import dataclass

from ansible_navigator.content_defs import ContentBase
from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.content_defs import ContentView
from ansible_navigator.content_defs import SerializationFormat


class TestContentView:
    """Tests for the ContentView enum."""

    def test_full(self) -> None:
        """Test FULL value."""
        assert ContentView.FULL.value == "full"

    def test_normal(self) -> None:
        """Test NORMAL value."""
        assert ContentView.NORMAL.value == "normal"


class TestSerializationFormat:
    """Tests for the SerializationFormat enum."""

    def test_yaml(self) -> None:
        """Test YAML value."""
        assert SerializationFormat.YAML.value == "YAML"

    def test_json(self) -> None:
        """Test JSON value."""
        assert SerializationFormat.JSON.value == "JSON"


class TestCFormat:
    """Tests for the CFormat dataclass."""

    def test_json_format(self) -> None:
        """Test JSON content format properties."""
        fmt = ContentFormat.JSON.value
        assert fmt.scope == "source.json"
        assert fmt.file_extension == ".json"
        assert fmt.serialization == SerializationFormat.JSON

    def test_yaml_format(self) -> None:
        """Test YAML content format properties."""
        fmt = ContentFormat.YAML.value
        assert fmt.scope == "source.yaml"
        assert fmt.file_extension == ".yml"
        assert fmt.serialization == SerializationFormat.YAML

    def test_ansi_format(self) -> None:
        """Test ANSI content format has no serialization."""
        fmt = ContentFormat.ANSI.value
        assert fmt.serialization is None

    def test_log_format(self) -> None:
        """Test LOG content format."""
        fmt = ContentFormat.LOG.value
        assert fmt.file_extension == ".log"

    def test_txt_format(self) -> None:
        """Test TXT content format."""
        fmt = ContentFormat.TXT.value
        assert fmt.file_extension == ".txt"

    def test_markdown_format(self) -> None:
        """Test MARKDOWN content format."""
        fmt = ContentFormat.MARKDOWN.value
        assert fmt.file_extension == ".md"


@dataclass
class SampleContent(ContentBase[dict[str, str]]):
    """A sample content dataclass for testing."""

    name: str = "test"
    value: int = 42


class TestContentBase:
    """Tests for the ContentBase class."""

    def test_asdict_normal_json(self) -> None:
        """Test asdict with normal JSON view."""
        content = SampleContent()
        result = content.asdict(ContentView.NORMAL, SerializationFormat.JSON)
        assert result["name"] == "test"
        assert result["value"] == 42

    def test_asdict_full_yaml(self) -> None:
        """Test asdict with full YAML view."""
        content = SampleContent()
        result = content.asdict(ContentView.FULL, SerializationFormat.YAML)
        assert result["name"] == "test"

    def test_get(self) -> None:
        """Test get method returns attribute."""
        content = SampleContent()
        assert content.get("name") == "test"
        assert content.get("value") == 42

    def test_items(self) -> None:
        """Test items method returns ItemsView."""
        content = SampleContent()
        items = dict(content.items())
        assert items["name"] == "test"
        assert items["value"] == 42
