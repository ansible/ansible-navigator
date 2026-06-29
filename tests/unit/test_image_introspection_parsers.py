"""Tests for the image introspect parsers."""

from __future__ import annotations

from ansible_navigator.data.image_introspect import AnsibleCollections
from ansible_navigator.data.image_introspect import AnsibleVersion
from ansible_navigator.data.image_introspect import CmdParser
from ansible_navigator.data.image_introspect import Command
from ansible_navigator.data.image_introspect import OsRelease
from ansible_navigator.data.image_introspect import RedhatRelease
from ansible_navigator.data.image_introspect import SystemPackages


class TestCmdParserStrip:
    """Tests for CmdParser._strip."""

    def test_strip_quotes(self) -> None:
        """Test stripping double quotes."""
        assert CmdParser._strip('"hello"') == "hello"

    def test_strip_single_quotes(self) -> None:
        """Test stripping single quotes."""
        assert CmdParser._strip("'hello'") == "hello"

    def test_strip_whitespace(self) -> None:
        """Test stripping whitespace."""
        assert CmdParser._strip("  hello  ") == "hello"

    def test_strip_combined(self) -> None:
        """Test stripping quotes then whitespace."""
        assert CmdParser._strip('"hello"') == "hello"


class TestCmdParserRePartition:
    """Tests for CmdParser.re_partition."""

    def test_basic_partition(self) -> None:
        """Test basic partitioning."""
        key, delim, content = CmdParser.re_partition("key=value", "=")
        assert key == "key"
        assert delim == "="
        assert content == "value"

    def test_no_separator(self) -> None:
        """Test when no separator is found."""
        key, delim, content = CmdParser.re_partition("no separator", "=")
        assert key == ""
        assert delim == ""
        assert content == "no separator"

    def test_leading_space(self) -> None:
        """Test with leading space in content."""
        key, delim, content = CmdParser.re_partition(" key=value", "=")
        assert key == ""
        assert delim == ""
        assert content == " key=value"

    def test_regex_separator(self) -> None:
        """Test with regex separator."""
        key, _delim, content = CmdParser.re_partition("key: value", r":\s+")
        assert key == "key"
        assert content == "value"


class TestCmdParserSplitter:
    """Tests for CmdParser.splitter."""

    def test_simple_key_value(self) -> None:
        """Test simple key=value splitting."""
        parser = CmdParser()
        lines = ["name=test", "version=1.0"]
        result = parser.splitter(lines, "=")
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["name"] == "test"
        assert result[0]["version"] == "1.0"

    def test_with_section_delim(self) -> None:
        """Test splitting with section delimiter."""
        parser = CmdParser()
        lines = ["name=pkg1", "version=1.0", "---", "name=pkg2", "version=2.0"]
        result = parser.splitter(lines, "=", section_delim="---")
        assert isinstance(result, list)
        assert len(result) == 2

    def test_continuation_line(self) -> None:
        """Test continuation line (no delimiter)."""
        parser = CmdParser()
        lines = ["name: test value", " continued value"]
        result = parser.splitter(lines, r":\s+")
        assert isinstance(result, list)
        assert "continued" in result[0]["name"]


class TestAnsibleCollections:
    """Tests for AnsibleCollections parser."""

    def test_commands_property(self) -> None:
        """Test commands property returns command list."""
        collector = AnsibleCollections()
        cmds = collector.commands
        assert len(cmds) == 1
        assert cmds[0].id_ == "ansible_collections"

    def test_parse_normal_output(self) -> None:
        """Test parsing normal collection list output."""
        cmd = Command(id_="test", command="test", parse=lambda x: None)
        cmd.stdout = (
            "# /usr/share/ansible/collections\n"
            "Collection        Version\n"
            "----------------- -------\n"
            "ansible.builtin   2.14.0\n"
            "community.general 6.0.0\n"
        )
        cmd.stderr = ""
        AnsibleCollections.parse(cmd)
        assert isinstance(cmd.details, dict)
        assert cmd.details["ansible.builtin"] == "2.14.0"
        assert cmd.details["community.general"] == "6.0.0"

    def test_parse_ansible29_error(self) -> None:
        """Test parsing ansible 2.9 error."""
        cmd = Command(id_="test", command="test", parse=lambda x: None)
        cmd.stdout = ""
        cmd.stderr = "invalid choice: 'list'"
        AnsibleCollections.parse(cmd)
        assert "not supported" in cmd.details

    def test_parse_empty_output(self) -> None:
        """Test parsing empty output."""
        cmd = Command(id_="test", command="test", parse=lambda x: None)
        cmd.stdout = ""
        cmd.stderr = ""
        AnsibleCollections.parse(cmd)
        assert not cmd.details


class TestAnsibleVersion:
    """Tests for AnsibleVersion parser."""

    def test_commands_property(self) -> None:
        """Test commands property."""
        collector = AnsibleVersion()
        cmds = collector.commands
        assert len(cmds) == 1
        assert cmds[0].id_ == "ansible_version"

    def test_parse(self) -> None:
        """Test parsing version output."""
        cmd = Command(id_="test", command="test", parse=lambda x: None)
        cmd.stdout = "ansible [core 2.14.0]\n  config file = /etc/ansible/ansible.cfg"
        AnsibleVersion.parse(cmd)
        assert cmd.details == "ansible [core 2.14.0]"


class TestOsRelease:
    """Tests for OsRelease parser."""

    def test_commands_property(self) -> None:
        """Test commands property."""
        collector = OsRelease()
        cmds = collector.commands
        assert len(cmds) == 1
        assert cmds[0].id_ == "os_release"

    def test_parse(self) -> None:
        """Test parsing os-release output."""
        collector = OsRelease()
        cmd = Command(id_="test", command="test", parse=lambda x: None)
        cmd.stdout = 'NAME="Fedora"\nVERSION="38"\nID=fedora'
        collector.parse(cmd)
        assert isinstance(cmd.details, (dict, list))


class TestRedhatRelease:
    """Tests for RedhatRelease parser."""

    def test_parse(self) -> None:
        """Test parsing redhat-release content."""
        cmd = Command(id_="test", command="test", parse=lambda x: None)
        cmd.stdout = "Red Hat Enterprise Linux release 9.1 (Plow)"
        RedhatRelease.parse(cmd)
        assert "Red Hat" in cmd.details


class TestSystemPackages:
    """Tests for SystemPackages parser."""

    def test_commands_property(self) -> None:
        """Test commands property."""
        collector = SystemPackages()
        cmds = collector.commands
        assert len(cmds) == 1
        assert cmds[0].id_ == "system_packages"


class TestCmdParserCommands:
    """Tests for CmdParser base class."""

    def test_default_commands(self) -> None:
        """Test default commands property returns empty list."""
        parser = CmdParser()
        assert not parser.commands
