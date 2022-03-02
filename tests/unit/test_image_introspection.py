# cspell:ignore buildvm
"""unit tests for image introspection
"""
import importlib

import pytest

from ansible_navigator.utils.functions import get_share_directory


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


@pytest.fixture(scope="module", name="imported_ii")
def image_introspection():
    """import the image introspection script using the share directory"""
    _log_messages, _exit_messages, share_dir = get_share_directory(
        app_name="ansible_navigator",
    )
    full_path = f"{share_dir}/utils/image_introspect.py"
    spec = importlib.util.spec_from_file_location("module", full_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_system_packages_parse_one(imported_ii):
    """test parsing one package"""
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


def test_system_packages_parse_many(imported_ii):
    """test parsing many packages"""
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
