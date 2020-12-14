# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios ospfv2 fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.ospfv2.ospfv2 import (
    Ospfv2Args,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ospfv2 import (
    Ospfv2Template,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


class Ospfv2Facts(object):
    """ The ios ospfv2 fact class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ospfv2Args.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_ospfv2_data(self, connection):
        return connection.get("sh running-config | section ^router ospf")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for ospfv2
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        if not data:
            data = self.get_ospfv2_data(connection)

        ipv4 = {"processes": []}
        rmmod = NetworkTemplate(
            lines=data.splitlines(), tmplt=Ospfv2Template()
        )
        current = rmmod.parse()

        # convert some of the dicts to lists
        for key, sortv in [("processes", "process_id")]:
            if key in current and current[key]:
                current[key] = current[key].values()
                current[key] = sorted(
                    current[key], key=lambda k, sk=sortv: k[sk]
                )

        for process in current.get("processes", []):
            if "areas" in process:
                process["areas"] = list(process["areas"].values())
                process["areas"] = sorted(
                    process["areas"], key=lambda k, sk="area_id": k[sk]
                )
                for area in process["areas"]:
                    # if 'ranges' in area:
                    #     area['ranges'] = sorted(area['ranges'],
                    #                             key=lambda k, s='ranges': k[s])
                    if "filters" in area:
                        area["filters"].sort()
            ipv4["processes"].append(process)

        ansible_facts["ansible_network_resources"].pop("ospfv2", None)
        facts = {}
        if current:
            params = utils.validate_config(
                self.argument_spec, {"config": ipv4}
            )
            params = utils.remove_empties(params)

            facts["ospfv2"] = params["config"]

            ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts
