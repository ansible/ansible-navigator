# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The nxos_ospfv2 class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""
from copy import deepcopy
from ansible.module_utils.six import iteritems
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.ospfv2 import (
    Ospfv2Template,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import (
    Facts,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    get_from_dict,
)


class Ospfv2(ResourceModule):
    """
    The nxos_ospfv2 class
    """

    def __init__(self, module):
        super(Ospfv2, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="ospfv2",
            tmplt=Ospfv2Template(),
        )
        self.parsers = [
            "router_id",
            "auto_cost",
            "graceful_restart.set",
            "graceful_restart.helper_disable",
            "isolate",
            "log_adjacency_changes",
            "max_lsa",
            "mpls.traffic_eng.router_id",
            "mpls.traffic_eng.multicast_intact",
            "name_lookup",
            "passive_interface.default",
            "rfc1583compatibility",
            "shutdown",
            "default_information.originate",
            "default_metric",
            "distance",
            "table_map",
            "timers.lsa_arrival",
            "timers.lsa_group_pacing",
            "timers.throttle.lsa",
            "timers.throttle.spf",
            "maximum_paths",
            "max_metric",
            "down_bit_ignore",
            "capability.vrf_lite",
            "bfd",
        ]

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.gen_config()
            self.run_commands()
        return self.result

    def gen_config(self):
        """ Select the appropriate function based on the state provided

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
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
            self._ospf_list_to_dict(entry)

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
        begin = len(self.commands)
        self.compare(self.parsers, want=want, have=have)
        self._compare_lists(want=want, have=have)
        self._areas_compare(want=want, have=have)
        self._vrfs_compare(want=want, have=have)

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
        parsers = [
            "area.default_cost",
            "area.authentication",
            "area.nssa",
            "area.nssa.translate",
            "area.stub",
        ]
        self.compare(parsers=parsers, want=want, have=have)
        self._area_compare_lists(want=want, have=have)

    def _area_compare_lists(self, want, have):
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

    def _compare_lists(self, want, have):
        for attrib in [
            "summary_address",
            "redistribute",
            "mpls.traffic_eng.areas",
        ]:
            wdict = get_from_dict(want, attrib) or {}
            hdict = get_from_dict(have, attrib) or {}

            for key, entry in iteritems(wdict):
                if entry != hdict.pop(key, {}):
                    self.addcmd(entry, attrib, False)
            # remove remaining items in have for replaced
            for entry in hdict.values():
                self.addcmd(entry, attrib, True)

    def _vrfs_compare(self, want, have):
        wvrfs = want.get("vrfs", {})
        hvrfs = have.get("vrfs", {})
        for name, entry in iteritems(wvrfs):
            self._compare(want=entry, have=hvrfs.pop(name, {}))
        # remove remaining items in have for replaced
        for name, entry in iteritems(hvrfs):
            self.addcmd(entry, "vrf", True)

    def _ospf_list_to_dict(self, entry):
        for _pid, proc in iteritems(entry):
            for area in proc.get("areas", []):
                area["ranges"] = {
                    entry["prefix"]: entry for entry in area.get("ranges", [])
                }
                area["filter_list"] = {
                    entry["direction"]: entry
                    for entry in area.get("filter_list", [])
                }
            mpls_areas = {
                entry["area_id"]: entry
                for entry in proc.get("mpls", {})
                .get("traffic_eng", {})
                .get("areas", [])
            }
            if mpls_areas:
                proc["mpls"]["traffic_eng"]["areas"] = mpls_areas
            proc["areas"] = {
                entry["area_id"]: entry for entry in proc.get("areas", [])
            }
            proc["summary_address"] = {
                entry["prefix"]: entry
                for entry in proc.get("summary_address", [])
            }
            proc["redistribute"] = {
                (entry.get("id"), entry["protocol"]): entry
                for entry in proc.get("redistribute", [])
            }
            if "vrfs" in proc:
                proc["vrfs"] = {
                    entry["vrf"]: entry for entry in proc.get("vrfs", [])
                }
                self._ospf_list_to_dict(proc["vrfs"])
