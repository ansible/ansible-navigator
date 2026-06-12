# cspell:ignore buildvm
"""Unit tests for image introspection."""

import importlib
import sys
import types

from importlib.machinery import ModuleSpec
from queue import Empty
from types import SimpleNamespace
from typing import Any

import pytest

from ansible_navigator.cli import APP_NAME
from ansible_navigator.cli import cache_scripts
from ansible_navigator.data import image_introspect
from ansible_navigator.utils.functions import generate_cache_path


RPM_OUTPUT = """Name        : net-snmp
Epoch       : 1
Version     : 5.9.1
Release     : 4.fc34
Architecture: x86_64
Install Date: Tue 19 Oct 2021 09:52:47 AM PDT
Group       : Unspecified
Size        : 901010
License     : BSD
Signature   : RSA/SHA256, Fri 30 Jul 2021 05:06:50 AM PDT, Key ID 1161ae6945719a39
Source RPM  : net-snmp-5.9.1-4.fc34.src.rpm
Build Date  : Fri 30 Jul 2021 12:23:51 AM PDT
Build Host  : buildvm-x86-03.iad2.fedoraproject.org
Packager    : Fedora Project
Vendor      : Fedora Project
URL         : http://net-snmp.sourceforge.net/
Bug URL     : https://bugz.fedoraproject.org/net-snmp
Summary     : A collection of SNMP protocol tools and libraries
Description :
SNMP (Simple Network Management Protocol) is a protocol used for
network management. The NET-SNMP project includes various SNMP tools:
an extensible agent, an SNMP library, tools for requesting or setting
information from SNMP agents, tools for generating and handling SNMP
traps, a version of the netstat command which uses SNMP, and a Tk/Perl
mib browser. This package contains the snmpd and snmptrapd daemons,
documentation, etc.

Name
Name:
Name :
summary: summary_string
version: version_string

You will probably also want to install the net-snmp-utils package,
which contains NET-SNMP utilities.
"""

PIP_FREEZE_OUTPUT = """ansible-core==2.19.4
ansible-runner==2.4.2
attrs==25.4.0
bcrypt==5.0.0
cffi==2.0.0
cryptography==46.0.3
Jinja2==3.1.6
jsonschema==4.25.1
MarkupSafe==3.0.2
"""

PIP_SHOW_OUTPUT = """Name: ansible-core
Version: 2.19.4
Summary: Radically simple IT automation
Home-page: https://ansible.com/
Author: Ansible, Inc.
Author-email: info@ansible.com
License: GPLv3+
Location: /opt/app-root/lib/python3.11/site-packages
Requires: cryptography, jinja2, packaging, PyYAML, resolvelib
Required-by: ansible-runner
---
Name: Jinja2
Version: 3.1.6
Summary: A very fast and expressive template engine.
Home-page: https://palletsprojects.com/p/jinja/
Author:
Author-email:
License: BSD-3-Clause
Location: /opt/app-root/lib/python3.11/site-packages
Requires: MarkupSafe
Required-by: ansible-core
---
Name: cryptography
Version: 46.0.3
Summary: cryptography is a package which provides cryptographic recipes and primitives
Home-page: https://github.com/pyca/cryptography
Author:
Author-email: The Python Cryptographic Authority <cryptography-dev@python.org>
License:
Location: /opt/app-root/lib64/python3.11/site-packages
Requires: cffi
Required-by: ansible-core, paramiko
"""


@pytest.fixture(scope="module", name="imported_ii")
def image_introspection() -> types.ModuleType:
    """Import the image introspection script using the share directory.

    Returns:
        Image introspect module
    """
    cache_scripts()
    cache_dir = generate_cache_path(app_name=APP_NAME)
    full_path = f"{cache_dir}/image_introspect.py"
    spec = importlib.util.spec_from_file_location("module", full_path)
    assert isinstance(spec, ModuleSpec)
    module = importlib.util.module_from_spec(spec)
    assert isinstance(module, types.ModuleType)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_collectors_keys(imported_ii: Any) -> None:
    """Verify ALL_COLLECTORS contains the expected section IDs.

    Args:
        imported_ii: Image introspection
    """
    expected = {
        "ansible_collections",
        "ansible_version",
        "os_release",
        "redhat_release",
        "python_packages",
        "system_packages",
    }
    assert set(imported_ii.ALL_COLLECTORS) == expected


@pytest.mark.parametrize(
    "sections",
    (
        ["ansible_collections"],
        ["ansible_collections", "ansible_version"],
        ["system_packages"],
    ),
    ids=["single", "two", "heavy"],
)
def test_section_filtering(imported_ii: Any, sections: list[str]) -> None:
    """Verify only requested collectors are instantiated.

    Args:
        imported_ii: Image introspection
        sections: The sections to filter on
    """
    collectors = imported_ii.ALL_COLLECTORS
    selected = [collectors[s]() for s in sections if s in collectors]
    assert len(selected) == len(sections)
    for section, cls_instance in zip(sections, selected, strict=False):
        cmds = cls_instance.commands
        assert cmds
        assert cmds[0].id_ == section


def test_section_everything_runs_all(imported_ii: Any) -> None:
    """Verify ``everything`` causes all collectors to be selected.

    Args:
        imported_ii: Image introspection
    """
    sections = ["everything"]
    collectors = imported_ii.ALL_COLLECTORS
    if sections and "everything" not in sections:
        selected = [collectors[s]() for s in sections if s in collectors]
    else:
        selected = [cls() for cls in collectors.values()]
    assert len(selected) == len(collectors)


def test_system_packages_parse_one(imported_ii: Any) -> None:
    """Test parsing one package.

    Args:
        imported_ii: Image introspection
    """
    command = imported_ii.Command(id="test", parse=lambda x: x, stdout=RPM_OUTPUT)
    imported_ii.SystemPackages().parse(command)
    assert len(command.details) == 1
    assert command.details[0]["name"] == "net-snmp"
    assert command.details[0]["version"] == "5.9.1"
    assert command.details[0]["summary"] == "A collection of SNMP protocol tools and libraries"
    assert command.details[0]["description"].startswith("SNMP")
    assert command.details[0]["description"].endswith("utilities.")
    assert "summary: summary_string" in command.details[0]["description"]
    assert "version: version_string" in command.details[0]["description"]


def test_system_packages_parse_many(imported_ii: Any) -> None:
    """Test parsing many packages.

    Args:
        imported_ii: Image introspection
    """
    count = 10

    command = imported_ii.Command(id="test", parse=lambda x: x, stdout=RPM_OUTPUT * count)
    imported_ii.SystemPackages().parse(command)
    assert len(command.details) == count
    for entry in command.details:
        assert entry["name"] == "net-snmp"
        assert entry["version"] == "5.9.1"
        assert entry["summary"] == "A collection of SNMP protocol tools and libraries"
        assert entry["description"].startswith("SNMP")
        assert entry["description"].endswith("utilities.")
        assert "summary: summary_string" in entry["description"]
        assert "version: version_string" in entry["description"]


def test_python_packages_parse_freeze(imported_ii: Any) -> None:
    """Test parsing pip freeze output.

    Args:
        imported_ii: Image introspection
    """
    command = imported_ii.Command(id="test", parse=lambda x: x, stdout=PIP_FREEZE_OUTPUT)
    imported_ii.PythonPackages().parse_freeze(command)

    assert isinstance(command.details, list)
    assert len(command.details) == 1
    packages = command.details[0]

    # Verify some package names and versions were parsed correctly
    assert packages["ansible-core"] == "2.19.4"
    assert packages["jinja2"] == "3.1.6"
    assert packages["cryptography"] == "46.0.3"
    assert packages["ansible-runner"] == "2.4.2"
    assert len(packages) == 9


def test_python_packages_parse_show(imported_ii: Any) -> None:
    """Test parsing pip show output.

    Args:
        imported_ii: Image introspection
    """
    command = imported_ii.Command(id="test", parse=lambda x: x, stdout=PIP_SHOW_OUTPUT)
    imported_ii.PythonPackages().parse(command)

    assert isinstance(command.details, list)
    assert len(command.details) == 3

    # Check ansible-core details
    ansible_core = command.details[0]
    assert ansible_core["name"] == "ansible-core"
    assert ansible_core["version"] == "2.19.4"
    assert ansible_core["summary"] == "Radically simple IT automation"
    assert ansible_core["location"] == "/opt/app-root/lib/python3.11/site-packages"
    assert "cryptography" in ansible_core["requires"]
    assert "jinja2" in ansible_core["requires"]
    assert ansible_core["required-by"] == ["ansible-runner"]

    # Check Jinja2 details
    jinja2 = command.details[1]
    assert jinja2["name"] == "Jinja2"
    assert jinja2["version"] == "3.1.6"
    assert jinja2["requires"] == ["MarkupSafe"]
    assert jinja2["required-by"] == ["ansible-core"]

    # Check cryptography details
    crypto = command.details[2]
    assert crypto["name"] == "cryptography"
    assert crypto["version"] == "46.0.3"
    expected_summary = (
        "cryptography is a package which provides cryptographic recipes and primitives"
    )
    assert crypto["summary"] == expected_summary
    assert crypto["location"] == "/opt/app-root/lib64/python3.11/site-packages"
    assert crypto["requires"] == ["cffi"]
    assert "ansible-core" in crypto["required-by"]
    assert "paramiko" in crypto["required-by"]


class TestMainSectionFiltering:
    """Tests for the main() function's section filtering logic."""

    def test_main_with_specific_sections(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify main() only runs requested collectors when sections are given.

        Args:
            monkeypatch: Pytest monkeypatch fixture
        """
        ran_commands: list[Any] = []

        def mock_run_multi_thread(
            self: Any,
            command_classes: list[Any],
        ) -> list[Any]:
            ran_commands.extend(command_classes)
            return []

        monkeypatch.setattr(
            image_introspect.CommandRunner,
            "run_multi_thread",
            mock_run_multi_thread,
        )
        result = image_introspect.main(serialize=False, sections=["ansible_version"])
        assert result is not None
        assert len(ran_commands) == 1

    def test_main_with_everything_runs_all(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify main() runs all collectors when sections contains 'everything'.

        Args:
            monkeypatch: Pytest monkeypatch fixture
        """
        ran_commands: list[Any] = []

        def mock_run_multi_thread(
            self: Any,
            command_classes: list[Any],
        ) -> list[Any]:
            ran_commands.extend(command_classes)
            return []

        monkeypatch.setattr(
            image_introspect.CommandRunner,
            "run_multi_thread",
            mock_run_multi_thread,
        )
        result = image_introspect.main(serialize=False, sections=["everything"])
        assert result is not None
        assert len(ran_commands) == len(image_introspect.ALL_COLLECTORS)

    def test_main_with_none_sections_runs_all(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify main() runs all collectors when sections is None.

        Args:
            monkeypatch: Pytest monkeypatch fixture
        """
        ran_commands: list[Any] = []

        def mock_run_multi_thread(
            self: Any,
            command_classes: list[Any],
        ) -> list[Any]:
            ran_commands.extend(command_classes)
            return []

        monkeypatch.setattr(
            image_introspect.CommandRunner,
            "run_multi_thread",
            mock_run_multi_thread,
        )
        result = image_introspect.main(serialize=False, sections=None)
        assert result is not None
        assert len(ran_commands) == len(image_introspect.ALL_COLLECTORS)

    def test_main_with_invalid_section_skipped(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify main() skips section names not in ALL_COLLECTORS.

        Args:
            monkeypatch: Pytest monkeypatch fixture
        """
        ran_commands: list[Any] = []

        def mock_run_multi_thread(
            self: Any,
            command_classes: list[Any],
        ) -> list[Any]:
            ran_commands.extend(command_classes)
            return []

        monkeypatch.setattr(
            image_introspect.CommandRunner,
            "run_multi_thread",
            mock_run_multi_thread,
        )
        result = image_introspect.main(
            serialize=False,
            sections=["nonexistent_section"],
        )
        assert result is not None
        assert len(ran_commands) == 0


class TestParseArgs:
    """Tests for the _parse_args() function."""

    def test_parse_args_no_arguments(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify _parse_args returns None when no --sections flag is given.

        Args:
            monkeypatch: Pytest monkeypatch fixture
        """
        monkeypatch.setattr(sys, "argv", ["image_introspect.py"])
        result = image_introspect._parse_args()
        assert result is None

    def test_parse_args_with_sections(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify _parse_args returns the requested section list.

        Args:
            monkeypatch: Pytest monkeypatch fixture
        """
        monkeypatch.setattr(
            sys,
            "argv",
            ["image_introspect.py", "--sections", "ansible_version", "os_release"],
        )
        result = image_introspect._parse_args()
        assert result == ["ansible_version", "os_release"]

    def test_parse_args_with_everything(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify _parse_args accepts 'everything' keyword.

        Args:
            monkeypatch: Pytest monkeypatch fixture
        """
        monkeypatch.setattr(sys, "argv", ["image_introspect.py", "--sections", "everything"])
        result = image_introspect._parse_args()
        assert result == ["everything"]

    def test_parse_args_empty_sections(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify _parse_args returns empty list when --sections given without values.

        Args:
            monkeypatch: Pytest monkeypatch fixture
        """
        monkeypatch.setattr(sys, "argv", ["image_introspect.py", "--sections"])
        result = image_introspect._parse_args()
        assert result == []


def test_always_collected_constant() -> None:
    """Verify ALWAYS_COLLECTED contains expected section IDs."""
    assert "python_version" in image_introspect.ALWAYS_COLLECTED
    assert "environment_variables" in image_introspect.ALWAYS_COLLECTED


class TestRunMultiThreadHealthCheck:
    """Tests for the timeout and thread health check paths in run_multi_thread."""

    def test_raises_when_all_threads_dead(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify RuntimeError when all threads die without completing.

        Args:
            monkeypatch: Pytest monkeypatch fixture
        """
        runner = image_introspect.CommandRunner()

        def _mock_get(timeout: int = 0) -> None:
            raise Empty

        mock_queue: Any = SimpleNamespace(get=_mock_get)
        runner._completed_queue = mock_queue
        runner._pending_queue = SimpleNamespace(put=lambda x: None)  # type: ignore[assignment]

        dead_thread = SimpleNamespace(is_alive=lambda: False, join=lambda: None)

        cmd_parser: Any = SimpleNamespace(
            commands=[
                image_introspect.Command(id_="test", command="echo hi", parse=lambda x: x),
            ],
        )

        monkeypatch.setattr(runner, "start_workers", lambda jobs: [dead_thread])

        with pytest.raises(RuntimeError, match="All worker threads have terminated"):
            runner.run_multi_thread([cmd_parser])
