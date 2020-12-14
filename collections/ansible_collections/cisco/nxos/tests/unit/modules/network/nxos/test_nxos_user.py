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

# Make coding more python3-ish

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.plugins.modules import nxos_user
from .nxos_module import TestNxosModule, set_module_args

ignore_provider_arg = True


class TestNxosUserModule(TestNxosModule):

    module = nxos_user

    def setUp(self):
        super(TestNxosUserModule, self).setUp()

        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_user.run_commands"
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_user.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_user.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_get_device_info = patch(
            "ansible_collections.cisco.nxos.plugins.cliconf.nxos.Cliconf.get_device_info"
        )
        self.get_device_info = self.mock_get_device_info.start()

    def tearDown(self):
        super(TestNxosUserModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_get_config.stop()
        self.mock_get_device_info.stop()

    def test_mds(self):
        self.get_config.return_value = ""
        self.run_commands.return_value = [
            {
                "TABLE_template": {
                    "ROW_template": [
                        {
                            "usr_name": "admin",
                            "expire_date": "this user account has no expiry date",
                            "TABLE_role": {
                                "ROW_role": {"role": "network-admin"}
                            },
                        },
                        {
                            "usr_name": "ansible-test-1",
                            "expire_date": "this user account has no expiry date",
                            "TABLE_role": {"ROW_role": [{"role": "priv-10"}]},
                        },
                    ]
                }
            }
        ]
        self.get_device_info.return_value = {
            "network_os": "nxos",
            "network_os_version": "8.4(2b)",
            "network_os_model": 'MDS 9148S 16G 48 FC (1 Slot) Chassis ("2/4/8/16 Gbps FC/Supervisor")',
            "network_os_hostname": "sw109-Mini",
            "network_os_image": "bootflash:///m9100-s5ek9-mz.8.4.2b.bin",
            "network_os_platform": "DS-C9710",
        }
        set_module_args(
            dict(name="ansible-test-2", configured_password="ansible")
        )
        self.execute_module(
            changed=True,
            commands=[
                "username ansible-test-2",
                "username ansible-test-2 password ansible",
            ],
        )
