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
from ansible_collections.cisco.nxos.plugins.modules import nxos_vxlan_vtep_vni
from .nxos_module import TestNxosModule, load_fixture, set_module_args


class TestNxosVxlanVtepVniModule(TestNxosModule):

    module = nxos_vxlan_vtep_vni

    def setUp(self):
        super(TestNxosVxlanVtepVniModule, self).setUp()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vxlan_vtep_vni.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vxlan_vtep_vni.get_config"
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosVxlanVtepVniModule, self).tearDown()
        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, device=""):
        self.get_config.return_value = load_fixture(
            "nxos_vxlan_vtep_vni", "config.cfg"
        )
        self.load_config.return_value = None

    def test_nxos_vxlan_vtep_vni_present_no_change(self):
        set_module_args(dict(interface="nve1", vni=6000))
        self.execute_module(changed=False, commands=[])

    def test_nxos_vxlan_vtep_vni(self):
        set_module_args(dict(interface="nve1", vni=5000))
        self.execute_module(
            changed=True, commands=["interface nve1", "member vni 5000"]
        )

    def test_nxos_vxlan_vtep_vni_absent(self):
        set_module_args(dict(interface="nve1", vni=6000, state="absent"))
        self.execute_module(
            changed=True, commands=["interface nve1", "no member vni 6000"]
        )

    def test_nxos_vxlan_vtep_vni_absent_no_change(self):
        set_module_args(dict(interface="nve2", vni=6000, state="absent"))
        self.execute_module(changed=False, commands=[])

    def test_nxos_vxlan_vtep_vni_multi_ingress_repl(self):
        set_module_args(
            dict(
                interface="nve1",
                vni=5000,
                multisite_ingress_replication="enable",
            )
        )
        self.execute_module(
            changed=True,
            commands=[
                "interface nve1",
                "member vni 5000",
                "multisite ingress-replication",
            ],
        )

    def test_nxos_vxlan_vtep_vni_multi_ingress_repl_opt(self):
        set_module_args(
            dict(
                interface="nve1",
                vni=5000,
                multisite_ingress_replication="optimized",
            )
        )
        self.execute_module(
            changed=True,
            commands=[
                "interface nve1",
                "member vni 5000",
                "multisite ingress-replication optimized",
            ],
        )

    def test_nxos_vxlan_vtep_vni_multi_ingress_repl_opt_exists(self):
        set_module_args(
            dict(
                interface="nve1",
                vni=6000,
                multisite_ingress_replication="optimized",
            )
        )
        self.execute_module(changed=False, commands=[])
