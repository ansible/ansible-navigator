# (c) 2016 Red Hat Inc.
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
from ansible_collections.cisco.nxos.plugins.modules import nxos_vxlan_vtep
from .nxos_module import TestNxosModule, load_fixture, set_module_args


class TestNxosVxlanVtepVniModule(TestNxosModule):

    module = nxos_vxlan_vtep

    def setUp(self):
        super(TestNxosVxlanVtepVniModule, self).setUp()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vxlan_vtep.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vxlan_vtep.get_config"
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosVxlanVtepVniModule, self).tearDown()
        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, device=""):
        self.get_config.return_value = load_fixture(
            "nxos_vxlan_vtep", "config.cfg"
        )
        self.load_config.return_value = None

    def test_nxos_vxlan_vtep(self):
        set_module_args(
            dict(interface="nve1", description="simple description")
        )
        self.execute_module(
            changed=True,
            commands=[
                "interface nve1",
                "terminal dont-ask",
                "description simple description",
            ],
        )

    def test_nxos_vxlan_vtep_present_no_change(self):
        set_module_args(dict(interface="nve1"))
        self.execute_module(changed=False, commands=[])

    def test_nxos_vxlan_vtep_absent(self):
        set_module_args(dict(interface="nve1", state="absent"))
        self.execute_module(changed=True, commands=["no interface nve1"])

    def test_nxos_vxlan_vtep_absent_no_change(self):
        set_module_args(dict(interface="nve2", state="absent"))
        self.execute_module(changed=False, commands=[])

    def test_nxos_vxlan_vtep_multisite(self):
        set_module_args(
            dict(
                interface="nve1",
                multisite_border_gateway_interface="Loopback10",
            )
        )
        self.execute_module(
            changed=True,
            commands=[
                "interface nve1",
                "terminal dont-ask",
                "multisite border-gateway interface loopback10",
            ],
        )

    def test_nxos_vxlan_vtep_multisite_exists(self):
        set_module_args(
            dict(
                interface="nve1",
                multisite_border_gateway_interface="Loopback1",
            )
        )
        self.execute_module(changed=False, commands=[])
