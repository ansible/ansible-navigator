# (c) 2019 Red Hat Inc.
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
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.tests.unit.modules.utils import (
    AnsibleFailJson,
)
from ansible_collections.cisco.nxos.plugins.modules import nxos_vlans
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.vlans.vlans import (
    Vlans,
)
from .nxos_module import TestNxosModule, load_fixture, set_module_args

ignore_provider_arg = True


class TestNxosVlansModule(TestNxosModule):

    module = nxos_vlans

    def setUp(self):
        super(TestNxosVlansModule, self).setUp()

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
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.vlans.vlans.Vlans.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_get_device_data = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.vlans.vlans.VlansFacts.get_device_data"
        )
        self.get_device_data = self.mock_get_device_data.start()

        self.mock_get_platform = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.vlans.vlans.Vlans.get_platform"
        )
        self.get_platform = self.mock_get_platform.start()

    def tearDown(self):
        super(TestNxosVlansModule, self).tearDown()
        self.mock_FACT_LEGACY_SUBSETS.stop()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_platform.stop()

    def prepare(self, test=""):
        if test == "_no_facts":
            self.get_device_data.side_effect = self.load_from_file_no_facts
        else:
            self.get_device_data.side_effect = self.load_from_file
        self.get_platform.return_value = "N9K-NXOSv"

    def load_from_file(self, *args, **kwargs):
        cmd = args[1]
        filename = str(cmd).split(" | ")[0].replace(" ", "_")
        return load_fixture("nxos_vlans", filename)

    def load_from_file_no_facts(self, *args, **kwargs):
        cmd = args[1]
        filename = str(cmd).split(" | ")[0].replace(" ", "_")
        filename += "_no_facts"
        return load_fixture("nxos_vlans", filename)

    def test_1(self):
        """
        **NOTE** This config is for reference only! See fixtures files for real data.
        vlan 1,3-5,8
        vlan 3
          name test-vlan3
        !Note:vlan 4 is present with default settings
        vlan 5
          shutdown
          name test-changeme
          mode fabricpath
          state suspend
          vn-segment 942
        !Note:vlan 7 is not present
        vlan 8
          shutdown
          name test-changeme-not
          state suspend
        """
        self.prepare()
        self.get_platform.return_value = "N7K-Cxxx"

        playbook = dict(
            config=[
                dict(vlan_id=4),
                dict(vlan_id=5, mapped_vni=555, mode="ce"),
                dict(
                    vlan_id=7, mapped_vni=777, name="test-vlan7", enabled=False
                ),
                dict(vlan_id="8", state="active", name="test-changeme-not")
                # vlan 3 is not present in playbook.
            ]
        )

        merged = [
            # Update existing device states with any differences in the playbook.
            "vlan 5",
            "vn-segment 555",
            "mode ce",
            "vlan 7",
            "vn-segment 777",
            "name test-vlan7",
            "shutdown",
            "vlan 8",
            "state active",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=merged)

        self.get_platform.return_value = "N9K-NXOSv"
        deleted = [
            # Reset existing device state to default values. Scope is limited to
            # objects in the play when the 'config' key is specified. For vlans
            # this means deleting each vlan listed in the playbook and ignoring
            # any play attrs other than 'vlan_id'.
            "no vlan 4",
            "no vlan 5",
            "no vlan 8",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=deleted)

        self.get_platform.return_value = "N5K-Cxxx"
        overridden = [
            # The play is the source of truth. Similar to replaced but the scope
            # includes all objects on the device; i.e. it will also reset state
            # on objects not found in the play.
            "no vlan 1",
            "no vlan 3",
            "vlan 5",
            "mode ce",
            "vn-segment 555",
            "no state",
            "no shutdown",
            "no name",
            "vlan 8",
            "no shutdown",
            "state active",
            "vlan 7",
            "name test-vlan7",
            "shutdown",
            "vn-segment 777",
        ]
        playbook["state"] = "overridden"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=overridden)

        self.get_platform.return_value = "N7K-NXOSv"
        replaced = [
            # Scope is limited to objects in the play.
            # replaced should ignore existing vlan 3.
            "vlan 5",
            "mode ce",
            "vn-segment 555",
            "no state",
            "no shutdown",
            "no name",
            "vlan 7",
            "shutdown",
            "name test-vlan7",
            "vn-segment 777",
            "vlan 8",
            "no shutdown",
            "state active",
        ]
        playbook["state"] = "replaced"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=replaced)

    def test_2(self):
        # Test when no 'config' key is used in playbook.
        self.prepare()
        deleted = [
            "no vlan 1",
            "no vlan 3",
            "no vlan 4",
            "no vlan 5",
            "no vlan 8",
        ]
        playbook = dict(state="deleted")
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=deleted)

        for test_state in ["merged", "replaced", "overridden"]:
            set_module_args(dict(state=test_state), ignore_provider_arg)
            self.execute_module(failed=True)

    def test_3(self):
        # Test no facts returned
        self.prepare(test="_no_facts")
        playbook = dict(state="deleted")
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=False)

    def test_4(self):
        self.prepare()
        # Misc tests to hit codepaths highlighted by code coverage tool as missed.
        playbook = dict(config=[dict(vlan_id=8, enabled=True)])
        replaced = [
            # Update existing device states with any differences in the playbook.
            "vlan 8",
            "no shutdown",
            "no state",
            "no name",
        ]
        playbook["state"] = "replaced"
        playbook["_ansible_check_mode"] = True
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=replaced)

    def test_5(self):
        """
        Idempotency test
        """

        self.prepare()
        playbook = dict(
            config=[
                dict(vlan_id=1, name="default", enabled=True),
                dict(vlan_id=3, name="test-vlan3", enabled=True),
                dict(vlan_id=4, enabled=True),
                dict(
                    vlan_id=5,
                    name="test-changeme",
                    mapped_vni=942,
                    state="suspend",
                    enabled=False,
                ),
                dict(
                    vlan_id=8,
                    name="test-changeme-not",
                    state="suspend",
                    enabled=False,
                ),
            ]
        )

        playbook["state"] = "merged"
        set_module_args(playbook, ignore_provider_arg)
        r = self.execute_module(changed=False)

        playbook["state"] = "overridden"
        set_module_args(playbook, ignore_provider_arg)
        r = self.execute_module(changed=False)

        playbook["state"] = "replaced"
        set_module_args(playbook, ignore_provider_arg)
        r = self.execute_module(changed=False)
