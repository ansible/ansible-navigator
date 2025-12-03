# cspell:ignore buildvm
"""Unit tests for image introspection."""

import importlib
import types

from importlib.machinery import ModuleSpec
from typing import Any

import pytest

from ansible_navigator.cli import APP_NAME
from ansible_navigator.cli import cache_scripts
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
