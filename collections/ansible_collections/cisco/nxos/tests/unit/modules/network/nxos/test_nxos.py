#
# (c) 2020 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from os import path

from mock import MagicMock

from ansible_collections.cisco.nxos.tests.unit.compat import unittest
from ansible_collections.cisco.nxos.plugins.cliconf import nxos
from ansible.module_utils._text import to_bytes, to_text


class TestPluginCLIConfNXOS(unittest.TestCase):
    """ Test class for NXOS CLI Conf Methods
    """

    def setUp(self):
        self._mock_connection = MagicMock()
        self._prepare()
        self._cliconf = nxos.Cliconf(self._mock_connection)
        self.maxDiff = None

    def _prepare(self, platform="nxos"):
        b_FIXTURE_DIR = b"%s/fixtures/cliconf/%s" % (
            to_bytes(
                path.dirname(path.abspath(__file__)),
                errors="surrogate_or_strict",
            ),
            to_bytes(platform),
        )

        def _connection_side_effect(*args, **kwargs):
            try:
                if args:
                    value = args[0]
                else:
                    value = kwargs.get("command")

                fixture_path = path.abspath(
                    b"%s/%s" % (b_FIXTURE_DIR, b"_".join(value.split(b" ")))
                )
                with open(fixture_path, "rb") as file_desc:
                    return to_text(file_desc.read())
            except (OSError, IOError):
                if args:
                    value = args[0]
                    return value
                elif kwargs.get("command"):
                    value = kwargs.get("command")
                    return value
                return "NO-OP"

        self._mock_connection.send.side_effect = _connection_side_effect

    def tearDown(self):
        pass

    def test_get_device_info_nxos(self):
        """ Test get_device_info for nxos
        """
        device_info = self._cliconf.get_device_info()

        mock_device_info = {
            "network_os": "nxos",
            "network_os_hostname": "nxos-9kv-933",
            "network_os_image": "bootflash:///nxos.9.3.3.bin",
            "network_os_model": "Nexus9000 C9300v Chassis",
            "network_os_platform": "N9K-C9300v",
            "network_os_version": "9.3(3)",
        }

        self.assertEqual(device_info, mock_device_info)

    def test_get_device_info_mds(self):
        """ Test get_device_info for mds
        """
        self._prepare(platform="mds")
        device_info = self._cliconf.get_device_info()
        mock_device_info = {
            "network_os": "nxos",
            "network_os_version": "8.4(2b)",
            "network_os_model": 'MDS 9148S 16G 48 FC (1 Slot) Chassis ("2/4/8/16 Gbps FC/Supervisor")',
            "network_os_hostname": "sw109-Mini",
            "network_os_image": "bootflash:///m9100-s5ek9-mz.8.4.2b.bin",
            "network_os_platform": "DS-C9710",
        }

        self.assertEqual(device_info, mock_device_info)

    def test_get_command_with_output_nxos(self):
        """ Test _get_command_with_output for nxos
        """
        self._prepare()
        cmd = self._cliconf._get_command_with_output(
            command="show version", output="json"
        )

        self.assertEqual(cmd, "show version | json")

    def test_get_command_with_output_mds(self):
        """ Test _get_command_with_output for mds
        """
        self._prepare(platform="mds")
        cmd = self._cliconf._get_command_with_output(
            command="show version", output="json"
        )

        self.assertEqual(cmd, "show version | json native")
