#
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The nxos_ospf_interfaces config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import (
    Facts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.ospf_interfaces import (
    Ospf_interfacesTemplate,
)


class Ospf_interfaces(ResourceModule):
    """
    The nxos_ospf_interfaces config class
    """

    def __init__(self, module):
        super(Ospf_interfaces, self).__init__(
            empty_fact_val=[],
            facts_module=Facts(module),
            module=module,
            resource="ospf_interfaces",
            tmplt=Ospf_interfacesTemplate(),
        )
        self.parsers = [
            "authentication",
            "authentication_key",
            "message_digest_key",
            "cost",
            "dead_interval",
            "hello_interval",
            "instance",
            "mtu_ignore",
            "network",
            "passive_interface",
            "priority",
            "retransmit_interval",
            "shutdown",
            "transmit_delay",
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
        wantd = {entry["name"]: entry for entry in self.want}
        haved = {entry["name"]: entry for entry in self.have}

        # turn all lists of dicts into dicts prior to merge
        for entry in wantd, haved:
            self._list_to_dict(entry)

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
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Ospf_interfaces network resource.
        """
        begin = len(self.commands)
        self._compare_ospf_interfaces(want, have)
        if len(self.commands) != begin:
            self.commands.insert(
                begin, self._tmplt.render(want or have, "interface", False)
            )

    def _compare_ospf_interfaces(self, want, have):
        waf = want.get("address_family", {})
        haf = have.get("address_family", {})

        for afi in ("ipv4", "ipv6"):
            witem = waf.pop(afi, {})
            hitem = haf.pop(afi, {})

            # this key needs to be compared separately and
            # popped from `authentication` dict to
            # preserve idempotence for other keys in this dict
            self.compare(["authentication.key_chain"], want=witem, have=hitem)
            witem.get("authentication", {}).pop("key_chain", None)
            hitem.get("authentication", {}).pop("key_chain", None)

            self.compare(parsers=self.parsers, want=witem, have=hitem)

            # compare top-level `multi_areas` config
            for area in witem.get("multi_areas", []):
                if area not in hitem.get("multi_areas", []):
                    self.addcmd(
                        {"afi": afi, "area": area}, "multi_areas", negate=False
                    )
            # remove superfluous top-level `multi_areas` config
            for area in hitem.get("multi_areas", []):
                if area not in witem.get("multi_areas", []):
                    self.addcmd(
                        {"afi": afi, "area": area}, "multi_areas", negate=True
                    )

            # compare config->address_family->processes
            self._compare_processes(
                afi, witem.get("processes", {}), hitem.get("processes", {})
            )

    def _compare_processes(self, afi, want, have):
        # add and update config->address_family->processes

        for w_id, wproc in want.items():
            hproc = have.pop(w_id, {})
            hproc["afi"] = wproc["afi"] = afi

            # compare config->address_family->processes->area
            self.compare(["area"], wproc, hproc)

            # compare config->address_family->processes->multi_areas
            marea_dict = {"afi": afi, "process_id": wproc["process_id"]}
            for area in wproc.get("multi_areas", []):
                if area not in hproc.get("multi_areas", []):
                    marea_dict["area"] = area
                    self.addcmd(
                        marea_dict, "processes_multi_areas", negate=False
                    )
            # remove superfluous processes->multi_areas config
            for area in hproc.get("multi_areas", []):
                if area not in wproc.get("multi_areas", []):
                    marea_dict["area"] = area
                    self.addcmd(
                        marea_dict, "processes_multi_areas", negate=True
                    )

        # remove superflous config->address_family->processes
        for hproc in have.values():
            hproc["afi"] = afi

            # remove config->address_family->processes->area
            self.addcmd(hproc, "area", negate=True)

            # remove superfluous processes->multi_areas config
            marea_dict = {"afi": afi, "process_id": hproc["process_id"]}
            for area in hproc.get("multi_areas", []):
                marea_dict["area"] = area
                self.addcmd(marea_dict, "processes_multi_areas", negate=True)

    def _list_to_dict(self, entry):
        for item in entry.values():
            for ag in item.get("address_family", []):
                ag["processes"] = {
                    subentry["process_id"]: subentry
                    for subentry in ag.get("processes", [])
                }
            item["address_family"] = {
                subentry["afi"]: subentry
                for subentry in item.get("address_family", [])
            }
