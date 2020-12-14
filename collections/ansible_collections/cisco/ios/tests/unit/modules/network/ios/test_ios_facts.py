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

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_facts
from ansible.module_utils.six import assertCountEqual
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule, load_fixture


class TestIosFactsModule(TestIosModule):

    module = ios_facts

    def setUp(self):
        super(TestIosFactsModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.legacy.base.run_commands"
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection"
        )
        self.get_resource_connection = (
            self.mock_get_resource_connection.start()
        )

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.legacy.base.get_capabilities"
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {
            "device_info": {
                "network_os": "ios",
                "network_os_hostname": "an-ios-01",
                "network_os_image": "flash0:/vios-adventerprisek9-m",
                "network_os_model": "WS-C3750-24TS",
                "network_os_version": "15.6(3)M2",
            },
            "network_api": "cliconf",
        }

    def tearDown(self):
        super(TestIosFactsModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_get_capabilities.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            commands = kwargs["commands"]
            output = list()

            for command in commands:
                filename = str(command).split(" | ")[0].replace(" ", "_")
                output.append(load_fixture("ios_facts_%s" % filename))
            return output

        self.run_commands.side_effect = load_from_file

    def test_ios_facts_stacked(self):
        set_module_args(dict(gather_subset="default"))
        result = self.execute_module()
        self.assertEqual(
            result["ansible_facts"]["ansible_net_model"], "WS-C3750-24TS"
        )
        self.assertEqual(
            result["ansible_facts"]["ansible_net_serialnum"], "CAT0726R0ZU"
        )
        self.assertEqual(
            result["ansible_facts"]["ansible_net_stacked_models"],
            ["WS-C3750-24TS-E", "WS-C3750-24TS-E", "WS-C3750G-12S-E"],
        )
        self.assertEqual(
            result["ansible_facts"]["ansible_net_stacked_serialnums"],
            ["CAT0726R0ZU", "CAT0726R10A", "CAT0732R0M4"],
        )

    def test_ios_facts_tunnel_address(self):
        set_module_args(dict(gather_subset="interfaces"))
        result = self.execute_module()
        self.assertEqual(
            result["ansible_facts"]["ansible_net_interfaces"][
                "GigabitEthernet0/0"
            ]["macaddress"],
            "5e00.0003.0000",
        )
        self.assertEqual(
            result["ansible_facts"]["ansible_net_interfaces"][
                "GigabitEthernet1"
            ]["macaddress"],
            "5e00.0006.0000",
        )
        self.assertIsNone(
            result["ansible_facts"]["ansible_net_interfaces"]["Tunnel1110"][
                "macaddress"
            ]
        )

    def test_ios_facts_filesystems_info(self):
        set_module_args(dict(gather_subset="hardware"))
        result = self.execute_module()
        self.assertEqual(
            result["ansible_facts"]["ansible_net_filesystems_info"][
                "bootflash:"
            ]["spacetotal_kb"],
            7712692.0,
        )
        self.assertEqual(
            result["ansible_facts"]["ansible_net_filesystems_info"][
                "bootflash:"
            ]["spacefree_kb"],
            6453180.0,
        )

    def test_ios_facts_neighbors(self):
        set_module_args(dict(gather_subset="interfaces"))
        result = self.execute_module()
        assertCountEqual(
            self,
            result["ansible_facts"]["ansible_net_neighbors"].keys(),
            ["GigabitEthernet1", "GigabitEthernet3"],
        )
        assertCountEqual(
            self,
            result["ansible_facts"]["ansible_net_neighbors"][
                "GigabitEthernet1"
            ],
            [
                {
                    "platform": "cisco CSR1000V",
                    "host": "R2",
                    "port": "GigabitEthernet2",
                },
                {
                    "platform": "cisco CSR1000V",
                    "host": "R3",
                    "port": "GigabitEthernet3",
                },
            ],
        )
        assertCountEqual(
            self,
            result["ansible_facts"]["ansible_net_neighbors"][
                "GigabitEthernet3"
            ],
            [{"host": "Rtest", "port": "Gi1"}],
        )
