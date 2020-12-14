#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


from copy import deepcopy
import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    get_interface_type,
    normalize_interface,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.interfaces.interfaces import (
    InterfacesArgs,
)


class InterfacesFacts(object):
    """ The ios interfaces fact class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = InterfacesArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_interfaces_data(self, connection):
        return connection.get("sh running-config | section ^interface")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for interfaces
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        objs = []

        if not data:
            data = self.get_interfaces_data(connection)
        # operate on a collection of resource x
        config = data.split("interface ")
        for conf in config:
            if conf:
                obj = self.render_config(self.generated_spec, conf)
                if obj:
                    objs.append(obj)
        facts = {}

        if objs:
            facts["interfaces"] = []
            params = utils.validate_config(
                self.argument_spec, {"config": objs}
            )
            for cfg in params["config"]:
                facts["interfaces"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    def render_config(self, spec, conf):
        """
        Render config as dictionary structure and delete keys from spec for null values

        :param spec: The facts tree, generated from the argspec
        :param conf: The configuration
        :rtype: dictionary
        :returns: The generated config
        """
        config = deepcopy(spec)
        match = re.search(r"^(\S+)", conf)
        intf = match.group(1)

        if get_interface_type(intf) == "unknown":
            return {}
        # populate the facts from the configuration
        config["name"] = normalize_interface(intf)
        config["description"] = utils.parse_conf_arg(conf, "description")
        config["speed"] = utils.parse_conf_arg(conf, "speed")
        if utils.parse_conf_arg(conf, "mtu"):
            config["mtu"] = int(utils.parse_conf_arg(conf, "mtu"))
        config["duplex"] = utils.parse_conf_arg(conf, "duplex")
        enabled = utils.parse_conf_cmd_arg(conf, "shutdown", False)
        config["enabled"] = enabled if enabled is not None else True

        return utils.remove_empties(config)
