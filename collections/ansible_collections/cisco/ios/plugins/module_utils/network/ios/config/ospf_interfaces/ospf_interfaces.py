#
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The cisco.ios_ospf_interfaces config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ospf_interfaces import (
    Ospf_InterfacesTemplate,
)


class Ospf_Interfaces(ResourceModule):
    """
    The cisco.ios_ospf_interfaces config class
    """

    def __init__(self, module):
        super(Ospf_Interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="ospf_interfaces",
            tmplt=Ospf_InterfacesTemplate(),
        )
        self.parsers = []

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

        wantd = {}
        haved = {}
        if self.want:
            wantd = {(entry["name"]): entry for entry in self.want}
        else:
            wantd = {}
        if self.have:
            haved = {(entry["name"]): entry for entry in self.have}
        else:
            haved = {}

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
        parsers = [
            "name",
            "process",
            "adjacency",
            "authentication",
            "bfd",
            "cost_ip",
            "cost_ipv6_dynamic_cost",
            "database_filter",
            "dead_interval",
            "demand_circuit",
            "flood_reduction",
            "hello_interval",
            "lls",
            "manet",
            "mtu_ignore",
            "multi_area",
            "neighbor",
            "network",
            "prefix_suppression",
            "priority",
            "resync_timeout",
            "retransmit_interval",
            "shutdown",
            "transmit_delay",
            "ttl_security",
        ]

        if (
            want != have
        ):  # and (want.get('address_family') or self.state == 'deleted'):
            if have.get("address_family"):
                self.addcmd(have, "name", False)
            elif want.get("address_family"):
                self.addcmd(want, "name", False)

        if want.get("address_family"):
            for each in want["address_family"]:
                set_want = True
                if have.get("address_family"):
                    have_elements = len(have.get("address_family"))
                    while have_elements:
                        if have.get("address_family")[have_elements - 1].get(
                            "afi"
                        ) == each.get("afi"):
                            set_want = False
                            h_each = have["address_family"].pop(
                                have_elements - 1
                            )
                            self.compare(
                                parsers=parsers, want=each, have=h_each
                            )
                        have_elements -= 1
                else:
                    h_each = dict()
                    self.compare(parsers=parsers, want=each, have=h_each)
                    set_want = False
                if set_want:
                    self.compare(parsers=parsers, want=each, have=dict())
        if self.state in ["overridden", "deleted"]:
            if have.get("address_family"):
                for each in have["address_family"]:
                    self.compare(parsers=parsers, want=dict(), have=each)
