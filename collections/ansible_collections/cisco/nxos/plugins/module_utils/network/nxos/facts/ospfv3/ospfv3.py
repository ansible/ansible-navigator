# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The nxos ospfv3 fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.ospfv3 import (
    Ospfv3Template,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.ospfv3.ospfv3 import (
    Ospfv3Args,
)


class Ospfv3Facts(object):
    """ The nxos ospfv3 facts class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ospfv3Args.argument_spec

    def get_config(self, connection):
        """Wrapper method for `connection.get()`
        This method exists solely to allow the unit test framework to mock device connection calls.
        """
        return connection.get("show running-config | section '^router ospfv3'")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Ospfv3 network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        if not data:
            data = self.get_config(connection)

        ipv6 = {"processes": []}
        for section in data.split("router "):
            rmmod = Ospfv3Template(lines=section.splitlines())
            entry = rmmod.parse()

            if entry:
                global_vals = entry.get("vrfs", {}).pop("vrf_", {})
                for key, value in iteritems(global_vals):
                    entry[key] = value

                if "vrfs" in entry:
                    entry["vrfs"] = list(entry["vrfs"].values())

                    for vrf in entry["vrfs"]:
                        if "areas" in vrf:
                            vrf["areas"] = list(vrf["areas"].values())

                if "areas" in entry:
                    entry["areas"] = list(entry["areas"].values())

                if "address_family" in entry:
                    if "areas" in entry["address_family"]:
                        entry["address_family"]["areas"] = list(
                            entry["address_family"]["areas"].values()
                        )

                ipv6["processes"].append(entry)

        ansible_facts["ansible_network_resources"].pop("ospfv3", None)
        facts = {}
        params = utils.validate_config(self.argument_spec, {"config": ipv6})
        params = utils.remove_empties(params)

        facts["ospfv3"] = params.get("config", [])

        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts
