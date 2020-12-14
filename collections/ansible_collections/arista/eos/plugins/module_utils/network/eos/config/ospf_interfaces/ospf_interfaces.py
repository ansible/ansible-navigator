#
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The eos_ospf_interfaces config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""
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
from ansible_collections.arista.eos.plugins.module_utils.network.eos.rm_templates.ospf_interfaces import (
    Ospf_interfacesTemplate,
)


class Ospf_interfaces(ResourceModule):
    """
    The eos_ospf_interfaces config class
    """

    def __init__(self, module):
        super(Ospf_interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="ospf_interfaces",
            tmplt=Ospf_interfacesTemplate(),
        )
        self.parsers = [
            "interfaces",
            "area",
            "authentication_v2",
            "authentication_v3",
            "authentication_key",
            "deadinterval",
            "encryption",
            "hellointerval",
            "bfd",
            "cost",
            "ip_params_area",
            "ip_params_bfd",
            "ip_params_cost",
            "ip_params_dead_interval",
            "ip_params_hello_interval",
            "ip_params_mtu_ignore",
            "ip_params_network",
            "ip_params_priority",
            "ip_params_passive_interface",
            "ip_params_retransmit_interval",
            "ip_params_transmit_delay",
            "mtu_ignore",
            "network",
            "priority",
            "passive_interface",
            "retransmit_interval",
            "transmit_delay",
            "message_digest_key",
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

        # convert list of dicts to dicts of dicts
        wantd = {entry["name"]: entry for entry in self.want}
        haved = {entry["name"]: entry for entry in self.have}

        # turn all lists of dicts into dicts prior to merge
        for entry in wantd, haved:
            self._ospf_int_list_to_dict(entry)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {
                k: v for k, v in iteritems(haved) if k in wantd or not wantd
            }
            for k, have in iteritems(haved):
                self._compare(want={}, have=have)
            wantd = {}

        # remove superfluous config for overridden
        if self.state == "overridden":
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
        self._compare_addr_family(want=want, have=have)
        if len(self.commands) != begin:

            tmp = want or have
            tmp.pop("address_family", {})
            self.commands.insert(
                begin, self._tmplt.render(tmp, "interfaces", False)
            )

    def _compare_addr_family(self, want, have):
        wdict = want.get("address_family", {})
        hdict = have.get("address_family", {})
        for afi in ["ipv4", "ipv6"]:
            w_family = wdict.pop(afi, {})
            h_family = hdict.pop(afi, {})
            for k in w_family.keys():
                if k == "afi":
                    continue
                w = {"afi": afi, k: w_family[k]}
                h = {"afi": afi, k: h_family.pop(k, {})}
                if k == "ip_params":
                    self._compare_ip_params(want=w, have=h)
                self.compare(parsers=self.parsers, want=w, have=h)
            for k in h_family.keys():
                if k in ["afi"]:
                    continue
                w = {"afi": afi, k: None}
                h = {"afi": afi, k: h_family[k]}
                if k == "ip_params":
                    w = {"afi": afi, k: {}}
                    self._compare_ip_params(want=w, have=h)
                self.compare(parsers=self.parsers, want=w, have=h)

    def _compare_ip_params(self, want, have):
        w_params = want.get("ip_params", {})
        h_params = have.get("ip_params", {})
        for afi in ["ipv4", "ipv6"]:
            w_p = w_params.pop(afi, {})
            h_p = h_params.pop(afi, {})
            for k, params in iteritems(w_p):
                if k == "afi":
                    continue
                w = {"afi": afi, k: params}
                h = {"afi": afi, k: h_p.pop(k, None)}
                self.compare(
                    parsers=self.parsers,
                    want={"ip_params": w},
                    have={"ip_params": h},
                )
            for k, params in iteritems(h_p):
                if k == "afi":
                    continue
                w = {"afi": afi, k: None}
                h = {"afi": afi, k: params}
                self.compare(
                    parsers=self.parsers,
                    want={"ip_params": w},
                    have={"ip_params": h},
                )

    def _ospf_int_list_to_dict(self, entry):
        for name, family in iteritems(entry):
            if family.get("ip_params"):
                family["ip_params"] = {
                    entry["afi"]: entry for entry in family["ip_params"]
                }
            if "address_family" in family:
                family["address_family"] = {
                    entry["afi"]: entry
                    for entry in family.get("address_family", [])
                }
                self._ospf_int_list_to_dict(family["address_family"])
