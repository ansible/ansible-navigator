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
from ansible_collections.vyos.vyos.plugins.modules import vyos_ospfv3
from ansible_collections.vyos.vyos.tests.unit.modules.utils import (
    set_module_args,
)
from .vyos_module import TestVyosModule, load_fixture


class TestVyosOspfv3Module(TestVyosModule):

    module = vyos_ospfv3

    def setUp(self):
        super(TestVyosOspfv3Module, self).setUp()
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

        self.mock_execute_show_command = patch(
            "ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.facts.ospfv3.ospfv3.Ospfv3Facts.get_device_data"
        )

        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestVyosOspfv3Module, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def load_fixtures(self, commands=None, transport="cli", filename=None):
        if filename is None:
            filename = "vyos_ospfv3_config.cfg"

        def load_from_file(*args, **kwargs):
            output = load_fixture(filename)
            return output

        self.execute_show_command.side_effect = load_from_file

    def test_vyos_ospfv3_merged_new_config(self):
        set_module_args(
            dict(
                config=dict(
                    redistribute=[dict(route_type="bgp")],
                    parameters=dict(router_id="192.0.2.10"),
                    areas=[
                        dict(
                            area_id="2",
                            export_list="export1",
                            import_list="import1",
                            range=[
                                dict(address="2001:db10::/32"),
                                dict(address="2001:db20::/32"),
                                dict(address="2001:db30::/32"),
                            ],
                        ),
                        dict(
                            area_id="3",
                            range=[dict(address="2001:db40::/32")],
                        ),
                    ],
                ),
                state="merged",
            )
        )
        commands = [
            "set protocols ospfv3 redistribute bgp",
            "set protocols ospfv3 parameters router-id '192.0.2.10'",
            "set protocols ospfv3 area 2 range 2001:db10::/32",
            "set protocols ospfv3 area 2 range 2001:db20::/32",
            "set protocols ospfv3 area 2 range 2001:db30::/32",
            "set protocols ospfv3 area '2'",
            "set protocols ospfv3 area 2 export-list export1",
            "set protocols ospfv3 area 2 import-list import1",
            "set protocols ospfv3 area '3'",
            "set protocols ospfv3 area 3 range 2001:db40::/32",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospfv3_merged_idem(self):
        set_module_args(
            dict(
                config=dict(
                    areas=[
                        dict(
                            area_id="12",
                            export_list="export1",
                            import_list="import1",
                            range=[
                                dict(address="2001:db11::/32"),
                                dict(address="2001:db22::/32"),
                                dict(address="2001:db33::/32"),
                            ],
                        ),
                        dict(
                            area_id="13",
                            range=[dict(address="2001:db44::/32")],
                        ),
                    ],
                ),
                state="merged",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_vyos_ospfv3_merged_update_existing(self):
        set_module_args(
            dict(
                config=dict(
                    redistribute=[dict(route_type="bgp")],
                    parameters=dict(router_id="192.0.2.10"),
                    areas=[
                        dict(
                            area_id="12",
                            export_list="export1",
                            import_list="import1",
                            range=[
                                dict(address="2001:db11::/32"),
                                dict(address="2001:db22::/32"),
                                dict(address="2001:db33::/32"),
                            ],
                        ),
                        dict(
                            area_id="13",
                            range=[
                                dict(address="2001:db44::/32"),
                                dict(address="2001:db55::/32"),
                            ],
                        ),
                    ],
                ),
                state="merged",
            )
        )
        commands = [
            "set protocols ospfv3 redistribute bgp",
            "set protocols ospfv3 parameters router-id '192.0.2.10'",
            "set protocols ospfv3 area 13 range 2001:db55::/32",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospfv3_replaced(self):
        set_module_args(
            dict(
                config=dict(
                    redistribute=[dict(route_type="bgp")],
                    parameters=dict(router_id="192.0.2.10"),
                    areas=[
                        dict(
                            area_id="12",
                            export_list="export1",
                            import_list="import1",
                            range=[
                                dict(address="2001:db10::/32"),
                                dict(address="2001:db22::/32"),
                                dict(address="2001:db33::/32"),
                            ],
                        ),
                        dict(
                            area_id="14",
                            range=[dict(address="2001:db40::/32")],
                        ),
                    ],
                ),
                state="replaced",
            )
        )
        commands = [
            "set protocols ospfv3 redistribute bgp",
            "set protocols ospfv3 parameters router-id '192.0.2.10'",
            "delete protocols ospfv3 area 12 range 2001:db11::/32",
            "set protocols ospfv3 area 12 range 2001:db10::/32",
            "delete protocols ospfv3 area 13",
            "set protocols ospfv3 area '14'",
            "set protocols ospfv3 area 14 range 2001:db40::/32",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospfv3_replaced_idem(self):
        set_module_args(
            dict(
                config=dict(
                    areas=[
                        dict(
                            area_id="12",
                            export_list="export1",
                            import_list="import1",
                            range=[
                                dict(address="2001:db11::/32"),
                                dict(address="2001:db22::/32"),
                                dict(address="2001:db33::/32"),
                            ],
                        ),
                        dict(
                            area_id="13",
                            range=[dict(address="2001:db44::/32")],
                        ),
                    ],
                ),
                state="replaced",
            )
        )
        self.execute_module(changed=False, commands=[])

    def test_vyos_ospfv3_deleted_no_config(self):
        set_module_args(dict(config=None, state="deleted"))
        commands = ["delete protocols ospfv3"]
        self.execute_module(changed=True, commands=commands)

    def test_vyos_ospfv3_gathered(self):
        set_module_args(dict(state="gathered"))
        result = self.execute_module(
            changed=False, filename="vyos_ospfv3_config.cfg"
        )
        gather_dict = {
            "areas": [
                {
                    "area_id": "12",
                    "export_list": "export1",
                    "import_list": "import1",
                    "range": [
                        {"address": "2001:db11::/32"},
                        {"address": "2001:db22::/32"},
                        {"address": "2001:db33::/32"},
                    ],
                },
                {"area_id": "13", "range": [{"address": "2001:db44::/32"}]},
            ],
        }
        self.assertEqual(sorted(gather_dict), sorted(result["gathered"]))

    def test_vyos_ospfv3_parsed(self):
        parsed_str = """set protocols ospfv3 area 2 export-list 'export1'
set protocols ospfv3 area 2 import-list 'import1'
set protocols ospfv3 area 2 range '2001:db10::/32'
set protocols ospfv3 area 2 range '2001:db20::/32'
set protocols ospfv3 area 2 range '2001:db30::/32'
set protocols ospfv3 area 3 range '2001:db40::/32'
set protocols ospfv3 parameters router-id '192.0.2.10'
set protocols ospfv3 redistribute 'bgp'"""
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)
        parsed_dict = {
            "areas": [
                {
                    "area_id": "2",
                    "export_list": "export1",
                    "import_list": "import1",
                    "range": [
                        {"address": "2001:db10::/32"},
                        {"address": "2001:db20::/32"},
                        {"address": "2001:db30::/32"},
                    ],
                },
                {"area_id": "3", "range": [{"address": "2001:db40::/32"}]},
            ],
            "parameters": {"router_id": "192.0.2.10"},
            "redistribute": [{"route_type": "bgp"}],
        }
        self.assertEqual(sorted(parsed_dict), sorted(result["parsed"]))

    def test_vyos_ospfv3_rendered(self):
        set_module_args(
            dict(
                config=dict(
                    redistribute=[dict(route_type="bgp")],
                    parameters=dict(router_id="192.0.2.10"),
                    areas=[
                        dict(
                            area_id="2",
                            export_list="export1",
                            import_list="import1",
                            range=[
                                dict(address="2001:db10::/32"),
                                dict(address="2001:db20::/32"),
                                dict(address="2001:db30::/32"),
                            ],
                        ),
                        dict(
                            area_id="3",
                            range=[dict(address="2001:db40::/32")],
                        ),
                    ],
                ),
                state="rendered",
            )
        )
        commands = [
            "set protocols ospfv3 redistribute bgp",
            "set protocols ospfv3 parameters router-id '192.0.2.10'",
            "set protocols ospfv3 area 2 range 2001:db10::/32",
            "set protocols ospfv3 area 2 range 2001:db20::/32",
            "set protocols ospfv3 area 2 range 2001:db30::/32",
            "set protocols ospfv3 area '2'",
            "set protocols ospfv3 area 2 export-list export1",
            "set protocols ospfv3 area 2 import-list import1",
            "set protocols ospfv3 area '3'",
            "set protocols ospfv3 area 3 range 2001:db40::/32",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(
            sorted(result["rendered"]), sorted(commands), result["rendered"]
        )
