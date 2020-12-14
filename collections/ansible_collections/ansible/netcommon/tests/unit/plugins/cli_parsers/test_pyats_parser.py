# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os

import pytest

from ansible_collections.ansible.netcommon.tests.unit.compat import unittest
from ansible_collections.ansible.netcommon.plugins.cli_parsers.pyats_parser import (
    CliParser,
)

pyats = pytest.importorskip("pyats")


class TestPyatsParser(unittest.TestCase):
    _nxos_parsed_output = {
        "platform": {
            "hardware": {
                "bootflash": "3509454 kB",
                "chassis": "Nexus9000 9000v",
                "cpu": "",
                "device_name": "an-nxos9k-01",
                "memory": "4041236 kB",
                "model": "Nexus9000 9000v",
                "processor_board_id": "96NK4OUJH32",
                "rp": "None",
                "slots": "None",
            },
            "kernel_uptime": {
                "days": 12,
                "hours": 23,
                "minutes": 48,
                "seconds": 10,
            },
            "name": "Nexus",
            "os": "NX-OS",
            "reason": "Unknown",
            "software": {
                "system_compile_time": "8/31/2017 14:00:00 [08/31/2017 22:29:32]",
                "system_image_file": "bootflash:///nxos.7.0.3.I7.1.bin",
                "system_version": "7.0(3)I7(1)",
            },
        }
    }
    _ios_parsed_output = {
        "interface": {
            "GigabitEthernet0/0": {
                "interface_is_ok": "YES",
                "ip_address": "10.8.38.75",
                "method": "manual",
                "protocol": "up",
                "status": "up",
            },
            "GigabitEthernet0/1": {
                "interface_is_ok": "YES",
                "ip_address": "unassigned",
                "method": "unset",
                "protocol": "up",
                "status": "up",
            },
            "GigabitEthernet0/2": {
                "interface_is_ok": "YES",
                "ip_address": "unassigned",
                "method": "unset",
                "protocol": "up",
                "status": "up",
            },
        }
    }

    def _debug(self, msg):
        self._debug_msgs.append(msg)

    def _load_fixture(self, filename):
        cfg_path = os.path.join(
            os.path.dirname(__file__), "fixtures", filename
        )

        with open(cfg_path) as f:
            return f.read()

    def test_pyats_parser(self):
        self._debug_msgs = []
        task_args = {
            "text": self._load_fixture("nxos_show_version.cfg"),
            "parser": {"command": "show version"},
        }
        parser = CliParser(
            task_args=task_args,
            task_vars={"ansible_network_os": "cisco.nxos.nxos"},
            debug=self._debug,
        )
        result = parser.parse()
        self.assertEqual(result, {"parsed": self._nxos_parsed_output})

    def test_pyats_parser_invalid_args(self):
        self._debug_msgs = []
        task_args = {
            "text": self._load_fixture("nxos_show_version.cfg"),
            "parser": {},
        }
        parser = CliParser(
            task_args=task_args,
            task_vars={"ansible_network_os": "cisco.nxos.nxos"},
            debug=self._debug,
        )
        result = parser.parse()
        error = {
            "errors": ["The pyats parser requires parser/command be provided."]
        }
        self.assertEqual(result, error)

    def test_pyats_parser_ano_shortname(self):
        self._debug_msgs = []
        task_args = {
            "text": self._load_fixture("nxos_show_version.cfg"),
            "parser": {"command": "show version"},
        }
        parser = CliParser(
            task_args=task_args,
            task_vars={"ansible_network_os": "nxos"},
            debug=self._debug,
        )
        result = parser.parse()

        self.assertEqual(result, {"parsed": self._nxos_parsed_output})

    def test_pyats_parser_ano_invalid(self):
        self._debug_msgs = []
        task_args = {
            "text": "random config",
            "parser": {"command": "show inventory"},
        }
        parser = CliParser(
            task_args=task_args,
            task_vars={"ansible_network_os": "wrong_os"},
            debug=self._debug,
        )
        result = parser.parse()
        error = {
            "errors": [
                "The pyats library return an error for 'show inventory' for 'wrong_os'. "
                "Error: Could not find parser for 'show inventory' under ('wrong_os',)."
            ]
        }
        self.assertEqual(result, error)

    def test_pyats_parser_ios2xe(self):
        self._debug_msgs = []
        task_args = {
            "text": self._load_fixture("ios_show_ip_interface_brief.cfg"),
            "parser": {"command": "show ip interface brief"},
        }
        parser = CliParser(
            task_args=task_args,
            task_vars={"ansible_network_os": "cisco.ios.ios"},
            debug=self._debug,
        )
        result = parser.parse()
        self.assertEqual(result, {"parsed": self._ios_parsed_output})

        self.assertEqual(
            self._debug_msgs,
            [
                "ansible_network_os was ios, using iosxe.",
                "OS set to 'iosxe' using 'ansible_network_os'.",
            ],
        )
