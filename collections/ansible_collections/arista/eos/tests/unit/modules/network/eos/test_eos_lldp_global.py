# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.arista.eos.tests.unit.compat.mock import patch
from ansible_collections.arista.eos.plugins.modules import eos_lldp_global
from ansible_collections.arista.eos.tests.unit.modules.utils import (
    set_module_args,
)
from .eos_module import TestEosModule, load_fixture


class TestEosLldpGlobalModule(TestEosModule):
    module = eos_lldp_global

    def setUp(self):
        super(TestEosLldpGlobalModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
        )
        self.load_config = self.mock_load_config.start()

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
            "ansible_collections.arista.eos.plugins.module_utils.network.eos.providers.providers.CliProvider.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.arista.eos.plugins.module_utils.network.eos.facts.lldp_global.lldp_global.Lldp_globalFacts.get_device_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestEosLldpGlobalModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None, transport="cli"):
        def load_from_file(*args, **kwargs):
            return load_fixture("eos_lldp_global_config.cfg")

        self.execute_show_command.side_effect = load_from_file

    def test_eos_lldp_global_merged(self):
        set_module_args(
            dict(
                config=dict(
                    holdtime=100,
                    tlv_select=dict(
                        management_address=False,
                        port_description=False,
                        system_description=True,
                    ),
                ),
                state="merged",
            )
        )
        commands = [
            "lldp holdtime 100",
            "lldp tlv-select system-description",
            "no lldp tlv-select port-description",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_lldp_global_merged_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    holdtime=200,
                    reinit=5,
                    timer=3000,
                    tlv_select=dict(
                        management_address=False, system_description=False
                    ),
                ),
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_lldp_global_replaced(self):
        set_module_args(
            dict(
                config=dict(
                    holdtime=100,
                    tlv_select=dict(
                        management_address=False,
                        port_description=False,
                        system_description=True,
                    ),
                ),
                state="replaced",
            )
        )
        commands = [
            "no lldp holdtime",
            "no lldp reinit",
            "no lldp timer",
            "lldp holdtime 100",
            "lldp tlv-select system-description",
            "no lldp tlv-select port-description",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_lldp_global_replaced_idempotent(self):
        set_module_args(
            dict(
                config=dict(
                    holdtime=200,
                    reinit=5,
                    timer=3000,
                    tlv_select=dict(
                        management_address=False, system_description=False
                    ),
                ),
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_eos_lldp_global_deleted(self):
        set_module_args(dict(state="deleted"))
        commands = [
            "no lldp holdtime",
            "no lldp reinit",
            "no lldp timer",
            "lldp tlv-select management-address",
            "lldp tlv-select system-description",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_eos_lldp_global_parsed(self):
        commands = [
            "lldp holdtime 100",
            "lldp tlv-select system-description",
            "lldp reinit 5",
            "no lldp tlv-select port-description",
        ]
        parsed_str = "\n".join(commands)
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)
        parsed_list = {
            "holdtime": "100",
            "reinit": "5",
            "tlv_select": {"port_description": False},
        }
        self.assertEqual(sorted(parsed_list), sorted(result["parsed"]))

    def test_eos_lldp_global_rendered(self):
        set_module_args(
            dict(
                config=dict(
                    holdtime=100,
                    reinit=5,
                    timer=400,
                    tlv_select=dict(
                        management_address=False,
                        port_description=False,
                        system_description=True,
                    ),
                ),
                state="rendered",
            )
        )
        commands = [
            "lldp holdtime 100",
            "lldp reinit 5",
            "lldp timer 400",
            "lldp tlv-select system-description",
            "no lldp tlv-select port-description",
            "no lldp tlv-select management-address",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(
            sorted(result["rendered"]), sorted(commands), result["rendered"]
        )

    def test_eos_lldp_global_gathered(self):
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        gather_list = {
            "holdtime": "200",
            "reinit": "5",
            "timer": "3000",
            "tlv_select": {
                "management_address": False,
                "system_description": False,
            },
        }
        self.assertEqual(sorted(gather_list), sorted(result["gathered"]))
