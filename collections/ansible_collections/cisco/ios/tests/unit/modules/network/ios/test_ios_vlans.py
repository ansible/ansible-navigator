#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_vlans
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule, load_fixture


class TestIosVlansModule(TestIosModule):
    module = ios_vlans

    def setUp(self):
        super(TestIosVlansModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts."
            "get_resource_connection"
        )
        self.get_resource_connection_facts = (
            self.mock_get_resource_connection_facts.start()
        )

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vlans.vlans."
            "VlansFacts.get_vlans_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosVlansModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None, transport="cli"):
        def load_from_file(*args, **kwargs):
            return load_fixture("ios_vlans_config.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_ios_vlans_merged(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="test_vlan_200",
                        state="active",
                        shutdown="disabled",
                        remote_span=True,
                        vlan_id=200,
                    )
                ],
                state="merged",
            )
        )
        result = self.execute_module(changed=True)
        commands = [
            "vlan 200",
            "name test_vlan_200",
            "state active",
            "remote-span",
            "no shutdown",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_vlans_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        mtu=1500,
                        name="default",
                        shutdown="disabled",
                        state="active",
                        vlan_id=1,
                    ),
                    dict(
                        mtu=610,
                        name="RemoteIsInMyName",
                        shutdown="enabled",
                        state="active",
                        vlan_id=123,
                    ),
                    dict(
                        mtu=1500,
                        name="VLAN0150",
                        remote_span=True,
                        shutdown="disabled",
                        state="active",
                        vlan_id=150,
                    ),
                    dict(
                        mtu=1500,
                        name="a_very_long_vlan_name_a_very_long_vlan_name",
                        shutdown="disabled",
                        state="active",
                        vlan_id=888,
                    ),
                    dict(
                        mtu=1500,
                        name="fddi-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1002,
                    ),
                    dict(
                        mtu=4472,
                        name="trcrf-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1003,
                    ),
                    dict(
                        mtu=1500,
                        name="fddinet-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1004,
                    ),
                    dict(
                        mtu=4472,
                        name="trbrf-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1005,
                    ),
                ],
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_vlans_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="test_vlan_200",
                        state="active",
                        shutdown="disabled",
                        remote_span=True,
                        vlan_id=200,
                    )
                ],
                state="replaced",
            )
        )
        result = self.execute_module(changed=True)
        commands = [
            "vlan 200",
            "name test_vlan_200",
            "state active",
            "remote-span",
            "no shutdown",
        ]
        self.assertEqual(result["commands"], commands)

    def test_ios_vlans_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        mtu=1500,
                        name="default",
                        shutdown="disabled",
                        state="active",
                        vlan_id=1,
                    ),
                    dict(
                        mtu=610,
                        name="RemoteIsInMyName",
                        shutdown="enabled",
                        state="active",
                        vlan_id=123,
                    ),
                    dict(
                        mtu=1500,
                        name="VLAN0150",
                        remote_span=True,
                        shutdown="disabled",
                        state="active",
                        vlan_id=150,
                    ),
                    dict(
                        mtu=1500,
                        name="a_very_long_vlan_name_a_very_long_vlan_name",
                        shutdown="disabled",
                        state="active",
                        vlan_id=888,
                    ),
                    dict(
                        mtu=1500,
                        name="fddi-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1002,
                    ),
                    dict(
                        mtu=4472,
                        name="trcrf-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1003,
                    ),
                    dict(
                        mtu=1500,
                        name="fddinet-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1004,
                    ),
                    dict(
                        mtu=4472,
                        name="trbrf-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1005,
                    ),
                ],
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_vlans_overridden(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="test_vlan_200",
                        state="active",
                        shutdown="disabled",
                        remote_span=True,
                        vlan_id=200,
                    )
                ],
                state="overridden",
            )
        )
        result = self.execute_module(changed=True)
        commands = [
            "no vlan 123",
            "no vlan 150",
            "no vlan 888",
            "vlan 200",
            "name test_vlan_200",
            "state active",
            "remote-span",
            "no shutdown",
        ]

        self.assertEqual(result["commands"], commands)

    def test_ios_vlans_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        mtu=1500,
                        name="default",
                        shutdown="disabled",
                        state="active",
                        vlan_id=1,
                    ),
                    dict(
                        mtu=610,
                        name="RemoteIsInMyName",
                        shutdown="enabled",
                        state="active",
                        vlan_id=123,
                    ),
                    dict(
                        mtu=1500,
                        name="VLAN0150",
                        remote_span=True,
                        shutdown="disabled",
                        state="active",
                        vlan_id=150,
                    ),
                    dict(
                        mtu=1500,
                        name="a_very_long_vlan_name_a_very_long_vlan_name",
                        shutdown="disabled",
                        state="active",
                        vlan_id=888,
                    ),
                    dict(
                        mtu=1500,
                        name="fddi-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1002,
                    ),
                    dict(
                        mtu=4472,
                        name="trcrf-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1003,
                    ),
                    dict(
                        mtu=1500,
                        name="fddinet-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1004,
                    ),
                    dict(
                        mtu=4472,
                        name="trbrf-default",
                        shutdown="enabled",
                        state="active",
                        vlan_id=1005,
                    ),
                ],
                state="overridden",
            )
        )
        self.execute_module(changed=False, commands=[], sort=True)

    def test_ios_delete_vlans_config(self):
        set_module_args(dict(config=[dict(vlan_id=150)], state="deleted"))
        result = self.execute_module(changed=True)
        commands = ["no vlan 150"]
        self.assertEqual(result["commands"], commands)

    def test_vlans_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="test_vlan_200",
                        state="active",
                        shutdown="disabled",
                        remote_span=True,
                        vlan_id=200,
                    )
                ],
                state="rendered",
            )
        )
        commands = [
            "name test_vlan_200",
            "no shutdown",
            "remote-span",
            "state active",
            "vlan 200",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), commands)
