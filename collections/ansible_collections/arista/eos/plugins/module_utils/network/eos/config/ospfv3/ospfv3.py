#
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The eos_ospfv3 config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

import re
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.facts.facts import (
    Facts,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.rm_templates.ospfv3 import (
    Ospfv3Template,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    get_from_dict,
)


class Ospfv3(ResourceModule):
    """
    The eos_ospfv3 config class
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
            "vrf",
            "address_family",
            "adjacency",
            "auto_cost",
            "area.default_cost",
            "area.authentication",
            "area.encryption",
            "area.nssa",
            "area.ranges",
            "area.stub",
            "bfd",
            "default_information",
            "default_metric",
            "distance",
            "fips_restrictions",
            "graceful_restart",
            "graceful_restart_period",
            "graceful_restart_helper",
            "log_adjacency_changes",
            "max_metric",
            "maximum_paths",
            "passive_interface",
            "redistribute",
            "router_id",
            "shutdown",
            "timers.lsa",
            "timers.out_delay",
            "timers.pacing",
            "timers.throttle.lsa",
            "timers.throttle.spf",
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
            entry["vrf"]: entry for entry in self.want.get("processes", [])
        }
        haved = {
            entry["vrf"]: entry for entry in self.have.get("processes", [])
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

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd and have.get("vrf") == k:
                    self.commands.append(self._tmplt.render(have, "vrf", True))

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Ospfv3 network resource.
        """
        begin = len(self.commands)
        self._af_compare(want=want, have=have)
        self._global_compare(want=want, have=have)

        if len(self.commands) != begin or (not have and want):
            self.commands.insert(
                begin, self._tmplt.render(want or have, "vrf", False)
            )
            self.commands.append("exit")

    def _global_compare(self, want, have):
        for name, entry in iteritems(want):
            if name in ["vrf", "address_family"]:
                continue
            if not isinstance(entry, dict) and name != "areas":
                self.compare(
                    parsers=self.parsers,
                    want={name: entry},
                    have={name: have.pop(name, None)},
                )
            else:
                if name == "areas" and entry:
                    self._areas_compare(
                        want={name: entry}, have={name: have.get(name, {})}
                    )
                else:
                    # passing dict without vrf, inorder to avoid  no router ospfv3 command
                    h = {i: have[i] for i in have if i != "vrf"}
                    self.compare(
                        parsers=self.parsers,
                        want={name: entry},
                        have={name: h.pop(name, {})},
                    )
        # remove remaining items in have for replaced
        for name, entry in iteritems(have):
            if name in ["vrf", "address_family"]:
                continue
            if not isinstance(entry, dict):
                self.compare(
                    parsers=self.parsers,
                    want={name: want.pop(name, None)},
                    have={name: entry},
                )
            else:
                # passing dict without vrf, inorder to avoid  no router ospfv3 command
                # w = {i: want[i] for i in want if i != "vrf"}
                self.compare(
                    parsers=self.parsers,
                    want={name: want.pop(name, {})},
                    have={name: entry},
                )

    def _af_compare(self, want, have):
        wafs = want.get("address_family", {})
        hafs = have.get("address_family", {})
        for name, entry in iteritems(wafs):
            begin = len(self.commands)
            self._compare_lists(want=entry, have=hafs.get(name, {}))
            self._areas_compare(want=entry, have=hafs.get(name, {}))
            self.compare(
                parsers=self.parsers, want=entry, have=hafs.pop(name, {})
            )
            if (
                len(self.commands) != begin
                and "afi" in entry
                and entry["afi"] != "router"
            ):
                self._rotate_commands(begin=begin)
                self.commands.insert(
                    begin, self._tmplt.render(entry, "address_family", False)
                )
                self.commands.append("exit")
        for name, entry in iteritems(hafs):
            self.addcmd(entry, "address_family", True)

    def _rotate_commands(self, begin=0):
        # move negate commands to beginning
        for cmd in self.commands[begin::]:
            negate = re.match(r"^no .*", cmd)
            if negate:
                self.commands.insert(
                    begin, self.commands.pop(self.commands.index(cmd))
                )
                begin += 1

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
            "area.encryption",
            "area.authentication",
            "area.nssa",
            "area.stub",
        ]
        self.compare(parsers=parsers, want=want, have=have)
        self._area_compare_lists(want=want, have=have)

    def _area_compare_lists(self, want, have):
        for attrib in ["ranges"]:
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
        for attrib in ["redistribute"]:
            wdict = get_from_dict(want, attrib) or {}
            hdict = get_from_dict(have, attrib) or {}
            for key, entry in iteritems(wdict):
                if entry != hdict.pop(key, {}):
                    self.addcmd(entry, attrib, False)
            # remove remaining items in have for replaced
            for entry in hdict.values():
                self.addcmd(entry, attrib, True)

    def _ospf_list_to_dict(self, entry):
        for name, proc in iteritems(entry):
            for area in proc.get("areas", []):
                if "ranges" in area:
                    area["ranges"] = {
                        entry["address"]: entry
                        for entry in area.get("ranges", [])
                    }
            proc["areas"] = {
                entry["area_id"]: entry for entry in proc.get("areas", [])
            }
            proc["redistribute"] = {
                entry["routes"]: entry
                for entry in proc.get("redistribute", [])
            }
            if "address_family" in proc:
                proc["address_family"] = {
                    entry["afi"]: entry
                    for entry in proc.get("address_family", [])
                }
                self._ospf_list_to_dict(proc["address_family"])
