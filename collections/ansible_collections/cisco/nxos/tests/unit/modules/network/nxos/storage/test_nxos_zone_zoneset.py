#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.tests.unit.modules.utils import (
    AnsibleFailJson,
    AnsibleExitJson,
)
from ansible_collections.cisco.nxos.plugins.modules.storage import (
    nxos_zone_zoneset,
)
from ansible_collections.cisco.nxos.plugins.modules.storage.nxos_zone_zoneset import (
    ShowZonesetActive,
    ShowZoneset,
    ShowZone,
    ShowZoneStatus,
)

from ..nxos_module import TestNxosModule, load_fixture, set_module_args


class TestNxosZoneZonesetModule(TestNxosModule):
    module = nxos_zone_zoneset

    def setUp(self):
        super(TestNxosZoneZonesetModule, self).setUp()
        module_path = "ansible_collections.cisco.nxos.plugins.modules.storage.nxos_zone_zoneset."

        self.mock_run_commands = patch(module_path + "run_commands")
        self.run_commands = self.mock_run_commands.start()

        self.mock_execute_show_cmd_zoneset_active = patch(
            module_path + "ShowZonesetActive.execute_show_zoneset_active_cmd"
        )
        self.execute_show_cmd_zoneset_active = (
            self.mock_execute_show_cmd_zoneset_active.start()
        )

        self.mock_execute_show_cmd_zoneset = patch(
            module_path + "ShowZoneset.execute_show_zoneset_cmd"
        )
        self.execute_show_cmd_zoneset = (
            self.mock_execute_show_cmd_zoneset.start()
        )

        self.mock_execute_show_cmd_zone = patch(
            module_path + "ShowZone.execute_show_zone_vsan_cmd"
        )
        self.execute_show_cmd_zone = self.mock_execute_show_cmd_zone.start()

        self.mock_execute_show_cmd_zone_status = patch(
            module_path + "ShowZoneStatus.execute_show_zone_status_cmd"
        )
        self.execute_show_cmd_zone_status = (
            self.mock_execute_show_cmd_zone_status.start()
        )

        self.mock_load_config = patch(module_path + "load_config")
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestNxosZoneZonesetModule, self).tearDown()
        self.mock_run_commands.stop()

        self.execute_show_cmd_zoneset_active.stop()
        self.execute_show_cmd_zoneset.stop()
        self.execute_show_cmd_zone.stop()
        self.execute_show_cmd_zone_status.stop()

        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    # Test def zone from deny to permit and vice versa
    def test_zone_defzone_deny_to_permit(self):
        # switch has def-zone deny and mode basic
        a = dict(zone_zoneset_details=[dict(vsan=922, default_zone="permit")])
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_0.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zone default-zone permit vsan 922",
                "no terminal dont-ask",
            ],
        )

    def test_zone_defzone_deny_to_permit_1(self):
        # switch has def-zone deny and mode enhanced
        a = dict(zone_zoneset_details=[dict(vsan=922, default_zone="permit")])
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_1.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zone default-zone permit vsan 922",
                "zone commit vsan 922",
                "no terminal dont-ask",
            ],
        )

    def test_zone_defzone_permit_to_deny_1(self):
        # switch has def-zone deny and mode enhanced
        a = dict(zone_zoneset_details=[dict(vsan=923, default_zone="deny")])
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_2.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "no zone default-zone permit vsan 923",
                "zone commit vsan 923",
                "no terminal dont-ask",
            ],
        )

    def test_zone_defzone_permit_to_deny_2(self):
        # switch has def-zone deny and mode enhanced
        a = dict(zone_zoneset_details=[dict(vsan=923, default_zone="deny")])
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_3.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "no zone default-zone permit vsan 923",
                "no terminal dont-ask",
            ],
        )

    # Test zone mode from basic to enhanced and vice versa
    def test_zone_mode_basic_to_enh(self):
        # switch has def-zone deny and mode basic
        a = dict(zone_zoneset_details=[dict(vsan=922, mode="enhanced")])
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_0.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zone mode enhanced vsan 922",
                "zone commit vsan 922",
                "no terminal dont-ask",
            ],
        )

    # Test zone mode from basic to enhanced and vice versa
    def test_zone_mode_basic_to_enh_1(self):
        # switch has def-zone deny and mode basic
        a = dict(zone_zoneset_details=[dict(vsan=922, mode="basic")])
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_1.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "no zone mode enhanced vsan 922",
                "no terminal dont-ask",
            ],
        )

    # Test zone smart-zone from enabled to disabled and vice versa
    def test_zone_smart_zone(self):
        # switch has def-zone deny and mode basic
        a = dict(zone_zoneset_details=[dict(vsan=922, smart_zoning=False)])
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_0.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "no zone smart-zoning enable vsan 922",
                "no terminal dont-ask",
            ],
        )

    def test_zone_smart_zone_1(self):
        # switch has def-zone deny and mode basic
        a = dict(zone_zoneset_details=[dict(vsan=923, smart_zoning=True)])
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_1.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zone smart-zoning enable vsan 923",
                "zone commit vsan 923",
                "no terminal dont-ask",
            ],
        )

    # Test zone  add/removal
    def test_zone_add_rem(self):
        a = dict(
            zone_zoneset_details=[
                dict(vsan=923, zone=[dict(name="zoneB", remove=True)])
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_1.cfg"
        )
        self.execute_show_cmd_zone.return_value = load_fixture(
            "nxos_zone_zoneset", "shzone_0.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "no zone name zoneB vsan 923",
                "zone commit vsan 923",
                "no terminal dont-ask",
            ],
        )

    def test_zone_add_rem_1(self):
        a = dict(
            zone_zoneset_details=[
                dict(vsan=923, zone=[dict(name="zoneC", remove=True)])
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_1.cfg"
        )
        self.execute_show_cmd_zone.return_value = load_fixture(
            "nxos_zone_zoneset", "shzone_0.cfg"
        )
        result = self.execute_module(changed=False, failed=False)
        m = "zone 'zoneC' is not present in vsan 923"
        assert m in str(result["messages"])
        self.assertEqual(result["commands"], [])

    def test_zone_add_rem_2(self):
        a = dict(
            zone_zoneset_details=[dict(vsan=923, zone=[dict(name="zoneBNew")])]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_1.cfg"
        )
        self.execute_show_cmd_zone.return_value = load_fixture(
            "nxos_zone_zoneset", "shzone_0.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zone name zoneBNew vsan 923",
                "zone commit vsan 923",
                "no terminal dont-ask",
            ],
        )

    def test_zone_add_rem_3(self):
        a = dict(
            zone_zoneset_details=[dict(vsan=923, zone=[dict(name="zoneB")])]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_1.cfg"
        )
        self.execute_show_cmd_zone.return_value = load_fixture(
            "nxos_zone_zoneset", "shzone_0.cfg"
        )
        result = self.execute_module(changed=False, failed=False)
        m = "zone 'zoneB' is already present in vsan 923"
        assert m in str(result["messages"])
        self.assertEqual(result["commands"], [])

    # Test zone mem add/removal
    def test_zonemem_add_rem(self):
        mem1 = {"pwwn": "10:00:10:94:00:00:00:01"}
        mem2 = {"device_alias": "somename"}
        a = dict(
            zone_zoneset_details=[
                dict(
                    vsan=923,
                    zone=[dict(name="zoneBNew", members=[mem1, mem2])],
                )
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_1.cfg"
        )
        self.execute_show_cmd_zone.return_value = load_fixture(
            "nxos_zone_zoneset", "shzone_0.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zone name zoneBNew vsan 923",
                "member pwwn 10:00:10:94:00:00:00:01",
                "member device-alias somename",
                "zone commit vsan 923",
                "no terminal dont-ask",
            ],
        )

    # Test zone mem add/removal
    def test_zonemem_add_rem_1(self):
        mem1 = {"pwwn": "11:11:11:11:11:11:11:11", "remove": True}
        mem2 = {"device_alias": "test123", "remove": True}
        a = dict(
            zone_zoneset_details=[
                dict(vsan=923, zone=[dict(name="zoneA", members=[mem1, mem2])])
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_1.cfg"
        )
        self.execute_show_cmd_zone.return_value = load_fixture(
            "nxos_zone_zoneset", "shzone_0.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zone name zoneA vsan 923",
                "no member pwwn 11:11:11:11:11:11:11:11",
                "no member device-alias test123",
                "zone commit vsan 923",
                "no terminal dont-ask",
            ],
        )

    # Test zone mem add/removal
    def test_zonemem_add_rem_2(self):
        mem1 = {"pwwn": "11:11:11:11:11:11:11:11", "remove": True}
        mem2 = {"device_alias": "test123", "remove": True}
        a = dict(
            zone_zoneset_details=[
                dict(
                    vsan=923, zone=[dict(name="zoneA1", members=[mem1, mem2])]
                )
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_1.cfg"
        )
        self.execute_show_cmd_zone.return_value = load_fixture(
            "nxos_zone_zoneset", "shzone_0.cfg"
        )
        result = self.execute_module(changed=False, failed=False)
        m = "zone 'zoneA1' is not present in vsan 923 , hence cannot remove the members"
        assert m in str(result["messages"])
        self.assertEqual(result["commands"], [])

    def test_zonemem_add_rem_3(self):
        mem1 = {"pwwn": "10:00:10:94:00:00:00:01", "devtype": "initiator"}
        mem2 = {"device_alias": "somename", "devtype": "target"}
        mem3 = {"device_alias": "somenameWithBoth", "devtype": "both"}

        a = dict(
            zone_zoneset_details=[
                dict(
                    vsan=922,
                    zone=[dict(name="zoneBNew", members=[mem1, mem2, mem3])],
                )
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_0.cfg"
        )
        self.execute_show_cmd_zone.return_value = load_fixture(
            "nxos_zone_zoneset", "shzone_1.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zone name zoneBNew vsan 922",
                "member pwwn 10:00:10:94:00:00:00:01 initiator",
                "member device-alias somename target",
                "member device-alias somenameWithBoth both",
                "no terminal dont-ask",
            ],
        )

    # Test zone mem add/removal with devtype
    def test_zonemem_add_rem_4(self):
        mem2 = {"device_alias": "test123", "devtype": "both", "remove": True}

        a = dict(
            zone_zoneset_details=[
                dict(vsan=922, zone=[dict(name="zoneA", members=[mem2])])
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_0.cfg"
        )
        self.execute_show_cmd_zone.return_value = load_fixture(
            "nxos_zone_zoneset", "shzone_1.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zone name zoneA vsan 922",
                "no member device-alias test123 both",
                "no terminal dont-ask",
            ],
        )

    # Test zoneset add/removal
    def test_zoneset_add_rem(self):
        a = dict(
            zone_zoneset_details=[
                dict(vsan=922, zoneset=[dict(name="zsetname21", remove=True)])
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_0.cfg"
        )
        self.execute_show_cmd_zoneset.return_value = load_fixture(
            "nxos_zone_zoneset", "shzoneset_0.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "no zoneset name zsetname21 vsan 922",
                "no terminal dont-ask",
            ],
        )

    def test_zoneset_add_rem_1(self):
        a = dict(
            zone_zoneset_details=[
                dict(vsan=922, zoneset=[dict(name="zsetname21New")])
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_0.cfg"
        )
        self.execute_show_cmd_zoneset.return_value = load_fixture(
            "nxos_zone_zoneset", "shzoneset_0.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zoneset name zsetname21New vsan 922",
                "no terminal dont-ask",
            ],
        )

    def test_zoneset_add_rem_2(self):
        a = dict(
            zone_zoneset_details=[
                dict(vsan=922, zoneset=[dict(name="zsetname21")])
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_0.cfg"
        )
        self.execute_show_cmd_zoneset.return_value = load_fixture(
            "nxos_zone_zoneset", "shzoneset_0.cfg"
        )
        result = self.execute_module(changed=False, failed=False)
        m = "zoneset 'zsetname21' is already present in vsan 922"
        self.assertEqual(result["commands"], [])
        self.assertEqual(result["messages"], [m])

    def test_zoneset_add_rem_3(self):
        a = dict(
            zone_zoneset_details=[
                dict(
                    vsan=922, zoneset=[dict(name="zsetname21New", remove=True)]
                )
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_0.cfg"
        )
        self.execute_show_cmd_zoneset.return_value = load_fixture(
            "nxos_zone_zoneset", "shzoneset_0.cfg"
        )
        result = self.execute_module(changed=False, failed=False)
        m = "zoneset 'zsetname21New' is not present in vsan 922 ,hence there is nothing to remove"
        self.assertEqual(result["commands"], [])
        self.assertEqual(result["messages"], [m])

    # Test zoneset mem add/removal
    def test_zoneset_mem_add_rem(self):
        mem1 = {"name": "newZoneV100"}

        a = dict(
            zone_zoneset_details=[
                dict(
                    vsan=922, zoneset=[dict(name="zsetname21", members=[mem1])]
                )
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_0.cfg"
        )
        self.execute_show_cmd_zoneset.return_value = load_fixture(
            "nxos_zone_zoneset", "shzoneset_0.cfg"
        )
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zoneset name zsetname21 vsan 922",
                "member newZoneV100",
                "no terminal dont-ask",
            ],
        )

    # Test zoneset mem add/removal
    def test_zoneset_mem_add_rem_1(self):
        mem1 = {"name": "zone21A", "remove": True}

        a = dict(
            zone_zoneset_details=[
                dict(
                    vsan=922, zoneset=[dict(name="zsetname21", members=[mem1])]
                )
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_0.cfg"
        )
        self.execute_show_cmd_zoneset.return_value = load_fixture(
            "nxos_zone_zoneset", "shzoneset_0.cfg"
        )
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zoneset name zsetname21 vsan 922",
                "no member zone21A",
                "no terminal dont-ask",
            ],
        )

    # Test zoneset mem add/removal
    def test_zoneset_mem_add_rem_2(self):
        mem1 = {"name": "zone21", "remove": True}

        a = dict(
            zone_zoneset_details=[
                dict(
                    vsan=922, zoneset=[dict(name="zsetname21", members=[mem1])]
                )
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_0.cfg"
        )
        self.execute_show_cmd_zoneset.return_value = load_fixture(
            "nxos_zone_zoneset", "shzoneset_0.cfg"
        )
        result = self.execute_module(changed=False, failed=False)
        m = "zoneset member 'zone21' is not present in zoneset 'zsetname21' in vsan 922 ,hence there is nothing to remove"
        self.assertEqual(result["commands"], [])
        self.assertEqual(result["messages"], [m])

    # Test zoneset activate/deactivate
    def test_zoneset_activate_deactivate(self):
        a = dict(
            zone_zoneset_details=[
                dict(
                    vsan=221, zoneset=[dict(name="zsv221", action="activate")]
                )
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_4.cfg"
        )
        self.execute_show_cmd_zoneset.return_value = load_fixture(
            "nxos_zone_zoneset", "shzoneset_2.cfg"
        )
        self.execute_show_cmd_zoneset_active.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonesetactive_0.cfg"
        )
        result = self.execute_module(changed=False, failed=False)
        self.assertEqual(result["commands"], [])

    def test_zoneset_activate_deactivate_1(self):
        a = dict(
            zone_zoneset_details=[
                dict(
                    vsan=221,
                    zoneset=[dict(name="zsv221", action="deactivate")],
                )
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_4.cfg"
        )
        self.execute_show_cmd_zoneset.return_value = load_fixture(
            "nxos_zone_zoneset", "shzoneset_2.cfg"
        )
        self.execute_show_cmd_zoneset_active.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonesetactive_0.cfg"
        )
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "no zoneset activate name zsv221 vsan 221",
                "zone commit vsan 221",
                "no terminal dont-ask",
            ],
        )

    def test_zoneset_activate_deactivate_2(self):
        a = dict(
            zone_zoneset_details=[
                dict(
                    vsan=221,
                    zoneset=[dict(name="zsv221New", action="activate")],
                )
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_4.cfg"
        )
        self.execute_show_cmd_zoneset.return_value = load_fixture(
            "nxos_zone_zoneset", "shzoneset_2.cfg"
        )
        self.execute_show_cmd_zoneset_active.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonesetactive_0.cfg"
        )
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zoneset name zsv221New vsan 221",
                "zoneset activate name zsv221New vsan 221",
                "zone commit vsan 221",
                "no terminal dont-ask",
            ],
        )

    def test_bug_zone_remove(self):
        mem1 = {"pwwn": "21:01:00:1b:32:a1:c0:a8", "remove": True}
        mem2 = {"pwwn": "50:06:01:6a:47:e4:6e:59", "remove": True}
        a = dict(
            zone_zoneset_details=[
                dict(vsan=221, zone=[dict(name="zv221", members=[mem1, mem2])])
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_4.cfg"
        )
        self.execute_show_cmd_zone.return_value = load_fixture(
            "nxos_zone_zoneset", "shzone_2.cfg"
        )
        self.execute_show_cmd_zoneset_active.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonesetactive_0.cfg"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zone name zv221 vsan 221",
                "no member pwwn 21:01:00:1b:32:a1:c0:a8",
                "no member pwwn 50:06:01:6a:47:e4:6e:59",
                "zone commit vsan 221",
                "no terminal dont-ask",
            ],
        )

    def test_bug_from_active_zoneset_act(self):
        a = dict(
            zone_zoneset_details=[
                dict(
                    vsan=221,
                    zoneset=[dict(name="zsv221New", action="activate")],
                )
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonestatus_4.cfg"
        )
        self.execute_show_cmd_zoneset.return_value = load_fixture(
            "nxos_zone_zoneset", "shzoneset_2.cfg"
        )
        self.execute_show_cmd_zoneset_active.return_value = load_fixture(
            "nxos_zone_zoneset", "shzonesetactive_0.cfg"
        )
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zoneset name zsv221New vsan 221",
                "zoneset activate name zsv221New vsan 221",
                "zone commit vsan 221",
                "no terminal dont-ask",
            ],
        )

    def test_bug_zone_remove_oliver(self):
        mem1 = {"pwwn": "c0:50:76:09:5b:20:00:64", "remove": True}
        a = dict(
            zone_zoneset_details=[
                dict(
                    vsan=50,
                    zone=[
                        dict(
                            name="z50_azusant_f0_unity8174_spa1",
                            members=[mem1],
                        )
                    ],
                )
            ]
        )
        set_module_args(a, True)
        self.execute_show_cmd_zone_status.return_value = load_fixture(
            "nxos_zone_zoneset", "show_zone_status_vsan.out"
        )
        self.execute_show_cmd_zone.return_value = load_fixture(
            "nxos_zone_zoneset", "show_zone_vsan.out"
        )
        self.execute_show_cmd_zoneset_active.return_value = load_fixture(
            "nxos_zone_zoneset", "show_zoneset_active_vsan.out"
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "terminal dont-ask",
                "zone name z50_azusant_f0_unity8174_spa1 vsan 50",
                "no member pwwn c0:50:76:09:5b:20:00:64",
                "no terminal dont-ask",
            ],
        )
