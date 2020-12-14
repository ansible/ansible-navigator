# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_ospfv3 class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.six import iteritems
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ospfv3 import (
    Ospfv3Template,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)


class Ospfv3(ResourceModule):
    """
    The ios_ospfv3 class
    """

    gather_subset = ["!all", "!min"]

    gather_network_resources = ["ospfv3"]

    def __init__(self, module):
        super(Ospfv3, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="ospfv3",
            tmplt=Ospfv3Template(),
        )

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        self.gen_config()
        self.run_commands()
        return self.result

    def gen_config(self):
        """ Select the appropriate function based on the state provided

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        if self.want:
            wantd = {
                (entry["process_id"], entry.get("vrf")): entry
                for entry in self.want.get("processes", [])
            }
        else:
            wantd = {}
        if self.have:
            haved = {
                (entry["process_id"], entry.get("vrf")): entry
                for entry in self.have.get("processes", [])
            }
        else:
            haved = {}

        # turn all lists of dicts into dicts prior to merge
        for thing in wantd, haved:
            for _pid, proc in iteritems(thing):
                for area in proc.get("areas", []):
                    ranges = {
                        entry["address"]: entry
                        for entry in area.get("ranges", [])
                    }
                    if bool(ranges):
                        area["ranges"] = ranges
                    filter_list = {
                        entry["direction"]: entry
                        for entry in area.get("filter_list", [])
                    }
                    if bool(filter_list):
                        area["filter_list"] = filter_list
                proc["areas"] = {
                    entry["area_id"]: entry for entry in proc.get("areas", [])
                }
                if proc.get("distribute_list"):
                    if "acls" in proc.get("distribute_list"):
                        proc["distribute_list"]["acls"] = {
                            entry["name"]: entry
                            for entry in proc["distribute_list"].get(
                                "acls", []
                            )
                        }

        # if state is merged, merge want onto have
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, limit the have to anything in want
        # set want to nothing
        if self.state == "deleted":
            haved = {
                k: v for k, v in iteritems(haved) if k in wantd or not wantd
            }
            wantd = {}

        # delete processes first so we do run into "more than one" errors
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self.addcmd(have, "pid", True)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        parsers = [
            "adjacency",
            "auto_cost",
            "bfd",
            "compatible",
            "event_log",
            "help",
            "interface_id",
            "limit",
            "local_rib_criteria",
            "log_adjacency_changes",
            "manet",
            "max_lsa",
            "max_metric",
            "passive_interface",
            "prefix_suppression",
            "queue_depth.hello",
            "queue_depth.update",
            "router_id",
            "shutdown",
            "timers.throttle.lsa",
            "timers.throttle.spf",
        ]

        if want != have:
            self.addcmd(want or have, "pid", False)
            self.compare(parsers, want, have)
            self._areas_compare(want, have)
            self._address_family_compare(want, have)

            if len(self.commands) == 1 and "router" in self.commands[0]:
                del self.commands[0]

    def _areas_compare(self, want, have):
        wareas = want.get("areas", {})
        hareas = have.get("areas", {})
        for name, entry in iteritems(wareas):
            self._area_compare(want=entry, have=hareas.pop(name, {}))
        for name, entry in iteritems(hareas):
            self._area_compare(want={}, have=entry)

    def _area_compare(self, want, have):
        parsers = [
            "area.authentication",
            "area.capability",
            "area.default_cost",
            "area.nssa",
            "area.nssa.translate",
            "area.ranges",
            "area.sham_link",
            "area.stub",
        ]
        self.compare(parsers=parsers, want=want, have=have)
        self._area_compare_filters(want, have)

    def _area_compare_filters(self, wantd, haved):
        for name, entry in iteritems(wantd):
            h_item = haved.pop(name, {})
            if entry != h_item and name == "filter_list":
                filter_list_entry = {}
                filter_list_entry["area_id"] = wantd["area_id"]
                if h_item:
                    li_diff = [
                        item
                        for item in entry + h_item
                        if item not in entry or item not in h_item
                    ]
                else:
                    li_diff = entry
                filter_list_entry["filter_list"] = li_diff
                self.addcmd(filter_list_entry, "area.filter_list", False)
        for name, entry in iteritems(haved):
            if name == "filter_list":
                self.addcmd(entry, "area.filter_list", True)

    def _address_family_compare(self, want, have):
        if want["process_id"] == have.get("process_id") or want["process_id"]:
            af_parsers = [
                "address_family.adjacency",
                "address_family.auto_cost",
                "address_family.bfd",
                "address_family.capability",
                "address_family.compatible",
                "address_family.default_information",
                "address_family.default_metric",
                "address_family.distance.admin_distance",
                "address_family.distance.ospf",
                "address_family.distribute_list.acls",
                "address_family.distribute_list.prefix",
                "address_family.distribute_list.route_map",
                "address_family.event_log",
                "address_family.graceful_restart",
                "address_family.interface_id",
                "address_family.limit",
                "address_family.local_rib_criteria",
                "address_family.log_adjacency_changes",
                "address_family.manet",
                "address_family.max_lsa",
                "address_family.max_metric",
                "address_family.maximum_paths",
                "address_family.passive_interface",
                "address_family.prefix_suppression",
                "address_family.queue_depth.hello",
                "address_family.queue_depth.update",
                "address_family.router_id",
                "address_family.shutdown",
                "address_family.summary_prefix",
                "address_family.timers.throttle.lsa",
                "address_family.timers.throttle.spf",
            ]
            delete_exit_family = False
            for each_want_af in want["address_family"]:
                if have.get("address_family"):
                    for each_have_af in have["address_family"]:
                        if each_have_af.get("vrf") == each_want_af.get(
                            "vrf"
                        ) and each_have_af.get("afi") == each_want_af.get(
                            "afi"
                        ):
                            self.compare(
                                parsers=["address_family"],
                                want={"address_family": each_want_af},
                                have={"address_family": each_have_af},
                            )
                            self.compare(
                                parsers=af_parsers,
                                want=each_want_af,
                                have=each_have_af,
                            )
                        elif each_have_af.get("afi") == each_want_af.get(
                            "afi"
                        ):
                            self.compare(
                                parsers=["address_family"],
                                want={"address_family": each_want_af},
                                have={"address_family": each_have_af},
                            )
                            self.compare(
                                parsers=af_parsers,
                                want={"address_family": each_want_af},
                                have={"address_family": each_have_af},
                            )
                        if each_want_af.get("areas"):
                            af_want_areas = {}
                            af_have_areas = {}
                            for each_area in each_want_af["areas"]:
                                af_want_areas.update(
                                    {each_area["area_id"]: each_area}
                                )
                            if each_have_af.get("areas"):
                                for each_area in each_have_af["areas"]:
                                    af_have_areas.update(
                                        {each_area["area_id"]: each_area}
                                    )

                            if "exit-address-family" in self.commands:
                                del self.commands[
                                    self.commands.index("exit-address-family")
                                ]
                                delete_exit_family = True

                            if af_have_areas:
                                self._areas_compare(
                                    {"areas": af_want_areas},
                                    {"areas": af_have_areas},
                                )
                            else:
                                self._areas_compare(
                                    {"areas": af_want_areas}, dict()
                                )
                            if delete_exit_family:
                                self.commands.append("exit-address-family")
                else:
                    temp_cmd_before = self.commands
                    self.commands = []
                    self.compare(
                        parsers=["address_family"],
                        want={"address_family": each_want_af},
                        have=dict(),
                    )
                    self.compare(
                        parsers=af_parsers, want=each_want_af, have=dict()
                    )
                    if each_want_af.get("areas"):
                        af_areas = {}
                        for each_area in each_want_af["areas"]:
                            af_areas.update({each_area["area_id"]: each_area})
                        self._areas_compare({"areas": af_areas}, dict())
                    del self.commands[
                        self.commands.index("exit-address-family")
                    ]
                    self.commands.append("exit-address-family")
                    self.commands[0:0] = temp_cmd_before
