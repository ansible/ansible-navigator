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

from ansible_collections.vyos.vyos.tests.unit.compat.mock import patch
from ansible_collections.vyos.vyos.plugins.modules import vyos_interface
from ansible_collections.vyos.vyos.tests.unit.modules.utils import (
    set_module_args,
)
from .vyos_module import TestVyosModule, load_fixture


class TestVyosInterfaceModule(TestVyosModule):

    module = vyos_interface

    def setUp(self):
        super(TestVyosInterfaceModule, self).setUp()
        self.mock_get_config = patch(
            "ansible_collections.vyos.vyos.plugins.modules.vyos_interface.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.vyos.vyos.plugins.modules.vyos_interface.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_execute_interfaces_command = patch(
            "ansible_collections.vyos.vyos.plugins.modules.vyos_interface.get_interfaces_data"
        )
        self.execute_interfaces_command = (
            self.mock_execute_interfaces_command.start()
        )
        self.mock_execute_lldp_command = patch(
            "ansible_collections.vyos.vyos.plugins.modules.vyos_interface.get_lldp_neighbor"
        )
        self.execute_lldp_command = self.mock_execute_lldp_command.start()

    #        self.mock_get_config = patch(
    #            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
    #        )
    #        self.get_config = self.mock_get_config.start()

    #        self.mock_load_config = patch(
    #            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
    #        )
    #        self.load_config = self.mock_load_config.start()

    #        self.mock_get_resource_connection_config = patch(
    #            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base.get_resource_connection"
    #        )
    #        self.get_resource_connection_config = (
    #            self.mock_get_resource_connection_config.start()
    #        )

    #        self.mock_get_resource_connection_facts = patch(
    #            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection"
    #        )
    #        self.get_resource_connection_facts = (
    #            self.mock_get_resource_connection_facts.start()
    #        )

    def tearDown(self):
        super(TestVyosInterfaceModule, self).tearDown()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_lldp_command.stop()
        self.mock_execute_interfaces_command.stop()

    def load_fixtures(self, commands=None, transport="cli"):
        self.get_config.return_value = load_fixture(
            "vyos_interface_config.cfg"
        )
        self.execute_interfaces_command.return_value = [
            0,
            load_fixture("vyos_interface_config.cfg"),
            None,
        ]
        self.execute_lldp_command.return_value = [
            0,
            load_fixture("vyos_lldp_neighbor_config.cfg"),
            None,
        ]
        self.load_config.return_value = dict(diff=None, session="session")

    def test_vyos_setup_int(self):
        set_module_args(
            dict(
                name="eth1",
                enabled=True,
                state="present",
                speed="100",
                duplex="half",
            )
        )
        commands = [
            "set interfaces ethernet eth1 speed 100",
            "set interfaces ethernet eth1 duplex half",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_setup_required_params(self):
        set_module_args(
            dict(
                name="eth1",
                enabled=True,
                state="present",
                speed="100",
            )
        )
        result = self.execute_module(failed=True)
        self.assertIn(
            "parameters are required together: speed, duplex", result["msg"]
        )

    def test_vyos_setup_int_idempotent(self):
        set_module_args(
            dict(
                name="eth1",
                enabled=True,
                state="present",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_vyos_disable_int(self):
        set_module_args(
            dict(
                name="eth1",
                state="absent",
            )
        )
        commands = ["delete interfaces ethernet eth1"]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_setup_int_aggregate(self):
        set_module_args(
            dict(
                aggregate=[
                    dict(
                        name="eth1",
                        enabled=True,
                        state="present",
                        mtu="512",
                        duplex="half",
                        speed="100",
                    ),
                    dict(
                        name="eth2",
                        enabled=True,
                        state="present",
                        speed="1000",
                        duplex="full",
                        mtu="256",
                    ),
                ]
            )
        )
        commands = [
            "set interfaces ethernet eth1 speed 100",
            "set interfaces ethernet eth1 duplex half",
            "set interfaces ethernet eth1 mtu 512",
            "set interfaces ethernet eth2 speed 1000",
            "set interfaces ethernet eth2 duplex full",
            "set interfaces ethernet eth2 mtu 256",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_delete_int_aggregate(self):
        set_module_args(
            dict(
                aggregate=[
                    dict(
                        name="eth1",
                        state="absent",
                    ),
                    dict(
                        name="eth2",
                        state="absent",
                    ),
                ]
            )
        )
        commands = [
            "delete interfaces ethernet eth1",
            "delete interfaces ethernet eth2",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_disable_int_aggregate(self):
        set_module_args(
            dict(
                aggregate=[
                    dict(
                        name="eth1",
                        enabled=False,
                    ),
                    dict(
                        name="eth2",
                        enabled=False,
                    ),
                ]
            )
        )
        commands = [
            "set interfaces ethernet eth1 disable",
            "set interfaces ethernet eth2 disable",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_intent_wrongport(self):
        set_module_args(
            dict(
                name="eth0",
                neighbors=[dict(port="dummy_port", host="dummy_host")],
            )
        )
        result = self.execute_module(failed=True)
        self.assertIn(
            "One or more conditional statements have not been satisfied",
            result["msg"],
        )

    def test_vyos_intent_neighbor_fail(self):
        set_module_args(
            dict(
                name="eth0",
                neighbors=[
                    dict(
                        port="eth0",
                    )
                ],
            )
        )
        result = self.execute_module(failed=True)
        self.assertIn(
            "One or more conditional statements have not been satisfied",
            result["msg"],
        )

    def test_vyos_intent_neighbor(self):
        set_module_args(
            dict(
                name="eth1",
                neighbors=[
                    dict(
                        port="eth0",
                    )
                ],
            )
        )
        self.execute_module(failed=False)

    def test_vyos_intent_neighbor_aggregate(self):
        set_module_args(
            dict(
                aggregate=[
                    dict(
                        name="eth1",
                        neighbors=[
                            dict(
                                port="eth0",
                            )
                        ],
                    )
                ]
            )
        )
        self.execute_module(failed=False)
