#
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The nxos_ospfv3 config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
    get_from_dict,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import (
    Facts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.ospfv3 import (
    Ospfv3Template,
)


class Ospfv3(ResourceModule):
    """
    The nxos_ospfv3 config class
    """

    def __init__(self, module):
        super(Ospfv3, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="ospfv3",
            tmplt=Ospfv3Template(),
        )
        self.parsers = [
            "auto_cost",
            "flush_routes",
            "graceful_restart.set",
            "graceful_restart.helper_disable",
            "graceful_restart.grace_period",
            "graceful_restart.planned_only",
            "isolate",
            "log_adjacency_changes",
            "max_lsa",
            "max_metric",
            "name_lookup",
            "passive_interface.default",
            "router_id",
            "shutdown",
            "timers.lsa_arrival",
            "timers.lsa_group_pacing",
            "timers.throttle.lsa",
        ]

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """ Generate configuration commands to send based on
            want, have and desired state.
        """
        wantd = {
            (entry["process_id"]): entry
            for entry in self.want.get("processes", [])
        }
        haved = {
            (entry["process_id"]): entry
            for entry in self.have.get("processes", [])
        }

        # turn all lists of dicts into dicts prior to merge
        for entry in wantd, haved:
            self._ospfv3_list_to_dict(entry)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {
                k: v for k, v in iteritems(haved) if k in wantd or not wantd
            }
            wantd = {}

        # if state is overridden, first remove processes that are in have but not in want
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self.addcmd(have, "process_id", True)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Ospfv3 network resource.
        """
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)
        self._areas_compare(want=want, have=have)
        self._vrfs_compare(want=want, have=have)
        self._af_compare(want=want, have=have)

        if len(self.commands) != begin or (not have and want):
            self.commands.insert(
                begin,
                self._tmplt.render(
                    want or have,
                    "vrf"
                    if "vrf" in (want.keys() or have.keys())
                    else "process_id",
                    False,
                ),
            )

    def _areas_compare(self, want, have):
        wareas = want.get("areas", {})
        hareas = have.get("areas", {})
        for name, entry in iteritems(wareas):
            self._area_compare(want=entry, have=hareas.pop(name, {}))
        for name, entry in iteritems(hareas):
            self._area_compare(want={}, have=entry)

    def _area_compare(self, want, have):
        parsers = ["area.nssa", "area.nssa.translate", "area.stub"]
        self.compare(parsers=parsers, want=want, have=have)

    def _vrfs_compare(self, want, have):
        wvrfs = want.get("vrfs", {})
        hvrfs = have.get("vrfs", {})
        for name, entry in iteritems(wvrfs):
            self._compare(want=entry, have=hvrfs.pop(name, {}))
        # remove remaining items in have for replaced
        for name, entry in iteritems(hvrfs):
            self.addcmd(entry, "vrf", True)

    def _af_compare(self, want, have):
        parsers = [
            "default_information.originate",
            "distance",
            "maximum_paths",
            "table_map",
            "timers.throttle.spf",
        ]
        waf = want.get("address_family", {})
        haf = have.get("address_family", {})

        cmd_ptr = len(self.commands)

        self._af_areas_compare(want=waf, have=haf)
        self._af_compare_lists(want=waf, have=haf)
        self.compare(parsers=parsers, want=waf, have=haf)

        cmd_ptr_nxt = len(self.commands)
        if cmd_ptr < cmd_ptr_nxt:
            self.commands.insert(cmd_ptr, "address-family ipv6 unicast")

    def _af_areas_compare(self, want, have):
        wareas = want.get("areas", {})
        hareas = have.get("areas", {})
        for name, entry in iteritems(wareas):
            self._af_area_compare(want=entry, have=hareas.pop(name, {}))
        for name, entry in iteritems(hareas):
            self._af_area_compare(want={}, have=entry)

    def _af_area_compare(self, want, have):
        self.compare(parsers=["area.default_cost"], want=want, have=have)
        self._af_area_compare_lists(want=want, have=have)

    def _af_area_compare_lists(self, want, have):
        for attrib in ["filter_list", "ranges"]:
            wdict = want.get(attrib, {})
            hdict = have.get(attrib, {})
            for key, entry in iteritems(wdict):
                if entry != hdict.pop(key, {}):
                    entry["area_id"] = want["area_id"]
                    self.addcmd(entry, "area.{0}".format(attrib), False)
            # remove remaining items in have for replaced
            for entry in hdict.values():
                entry["area_id"] = have["area_id"]
                self.addcmd(entry, "area.{0}".format(attrib), True)

    def _af_compare_lists(self, want, have):
        for attrib in ["summary_address", "redistribute"]:
            wdict = get_from_dict(want, attrib) or {}
            hdict = get_from_dict(have, attrib) or {}

            for key, entry in iteritems(wdict):
                if entry != hdict.pop(key, {}):
                    self.addcmd(entry, attrib, False)
            # remove remaining items in have for replaced
            for entry in hdict.values():
                self.addcmd(entry, attrib, True)

    def _ospfv3_list_to_dict(self, entry):
        for _pid, proc in iteritems(entry):
            proc["areas"] = {
                entry["area_id"]: entry for entry in proc.get("areas", [])
            }
            af = proc.get("address_family")
            if af:
                for area in af.get("areas", []):
                    area["ranges"] = {
                        entry["prefix"]: entry
                        for entry in area.get("ranges", [])
                    }
                    area["filter_list"] = {
                        entry["direction"]: entry
                        for entry in area.get("filter_list", [])
                    }
                af["areas"] = {
                    entry["area_id"]: entry for entry in af.get("areas", [])
                }
                af["summary_address"] = {
                    entry["prefix"]: entry
                    for entry in af.get("summary_address", [])
                }
                af["redistribute"] = {
                    (entry.get("id"), entry["protocol"]): entry
                    for entry in af.get("redistribute", [])
                }
            if "vrfs" in proc:
                proc["vrfs"] = {
                    entry["vrf"]: entry for entry in proc.get("vrfs", [])
                }
                self._ospfv3_list_to_dict(proc["vrfs"])
