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

from textwrap import dedent
from ansible_collections.cisco.nxos.tests.unit.compat.mock import (
    patch,
    PropertyMock,
)
from ansible_collections.cisco.nxos.plugins.modules import nxos_lacp_interfaces
from .nxos_module import TestNxosModule, set_module_args

ignore_provider_arg = True


class TestNxosLacpInterfacesModule(TestNxosModule):

    module = nxos_lacp_interfaces

    def setUp(self):
        super(TestNxosLacpInterfacesModule, self).setUp()

        self.mock_FACT_LEGACY_SUBSETS = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts.FACT_LEGACY_SUBSETS"
        )
        self.FACT_LEGACY_SUBSETS = self.mock_FACT_LEGACY_SUBSETS.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base.get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection"
        )
        self.get_resource_connection_facts = (
            self.mock_get_resource_connection_facts.start()
        )

        self.mock_edit_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.l3_interfaces.l3_interfaces.L3_interfaces.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

    def tearDown(self):
        super(TestNxosLacpInterfacesModule, self).tearDown()
        self.mock_FACT_LEGACY_SUBSETS.stop()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()

    # ---------------------------
    # Lacp_interfaces Test Cases
    # ---------------------------

    SHOW_CMD = "show running-config | section ^interface"

    def test_lacp_mode_parse(self):
        # basic tests
        existing = dedent(
            """\
          interface port-channel1
            switchport
            switchport mode trunk
            switchport trunk native vlan 5
            switchport trunk allowed vlan 10
            no lacp graceful-convergence
        """
        )
        self.get_resource_connection_facts.return_value = {
            self.SHOW_CMD: existing
        }
        playbook = dict(
            config=[
                dict(
                    name="port-channel1",
                    convergence={"graceful": False},
                    suspend_individual=True,
                    mode="delay",
                )
            ]
        )
        # Expected result commands for each 'state'
        merged = [
            "interface port-channel1",
            "lacp mode delay",
            "lacp suspend-individual",
        ]

        playbook["state"] = "merged"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=merged)
