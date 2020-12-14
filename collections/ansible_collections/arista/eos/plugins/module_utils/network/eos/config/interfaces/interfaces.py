# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The eos_interfaces class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base import (
    ConfigBase,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    to_list,
    dict_diff,
    param_list_to_dict,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.facts.facts import (
    Facts,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.utils.utils import (
    normalize_interface,
)


class Interfaces(ConfigBase):
    """
    The eos_interfaces class
    """

    gather_subset = ["!all", "!min"]

    gather_network_resources = ["interfaces"]

    def get_interfaces_facts(self, data=None):
        """ Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(
            self.gather_subset, self.gather_network_resources, data=data
        )
        interfaces_facts = facts["ansible_network_resources"].get("interfaces")
        if not interfaces_facts:
            return []
        return interfaces_facts

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {"changed": False}
        commands = list()
        warnings = list()

        if self.state in self.ACTION_STATES:
            existing_interfaces_facts = self.get_interfaces_facts()
        else:
            existing_interfaces_facts = []

        if self.state in self.ACTION_STATES or self.state == "rendered":
            commands.extend(self.set_config(existing_interfaces_facts))

        if commands and self.state in self.ACTION_STATES:
            if not self._module.check_mode:
                self._connection.edit_config(commands)
            result["changed"] = True
        if self.state in self.ACTION_STATES:
            result["commands"] = commands

        if self.state in self.ACTION_STATES or self.state == "gathered":
            changed_interfaces_facts = self.get_interfaces_facts()

        elif self.state == "rendered":
            result["rendered"] = commands

        elif self.state == "parsed":
            running_config = self._module.params["running_config"]
            if not running_config:
                self._module.fail_json(
                    msg="value of running_config parameter must not be empty for state parsed"
                )
            result["parsed"] = self.get_interfaces_facts(data=running_config)

        if self.state in self.ACTION_STATES:
            result["before"] = existing_interfaces_facts
            if result["changed"]:
                result["after"] = changed_interfaces_facts

        elif self.state == "gathered":
            result["gathered"] = changed_interfaces_facts
        result["warnings"] = warnings
        return result

    def set_config(self, existing_interfaces_facts):
        """ Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        want = self._module.params["config"]
        have = existing_interfaces_facts
        resp = self.set_state(want, have)
        return to_list(resp)

    def set_state(self, want, have):
        """ Select the appropriate function based on the state provided

        :param want: the desired configuration as a dictionary
        :param have: the current configuration as a dictionary
        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        state = self._module.params["state"]
        if (
            state in ("merged", "replaced", "overridden", "rendered")
            and not want
        ):
            self._module.fail_json(
                msg="value of config parameter must not be empty for state {0}".format(
                    state
                )
            )
        want = param_list_to_dict(want)
        have = param_list_to_dict(have)
        commands = []
        if state == "overridden":
            commands = self._state_overridden(want, have)
        elif state == "deleted":
            commands = self._state_deleted(want, have)
        elif state == "merged" or state == "rendered":
            commands = self._state_merged(want, have)
        elif state == "replaced":
            commands = self._state_replaced(want, have)
        return commands

    @staticmethod
    def _state_replaced(want, have):
        """ The command generator when state is replaced

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        commands = []
        for key, desired in want.items():
            interface_name = normalize_interface(key)
            if interface_name in have:
                extant = have[interface_name]
            else:
                extant = dict()

            add_config = dict_diff(extant, desired)
            del_config = dict_diff(desired, extant)

            if (
                "speed" in add_config.keys()
                and "duplex" not in add_config.keys()
            ):
                add_config.update({"duplex": desired.get("duplex")})

            commands.extend(generate_commands(key, add_config, del_config))

        return commands

    @staticmethod
    def _state_overridden(want, have):
        """ The command generator when state is overridden

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        commands = []
        for key, extant in have.items():
            if key in want:
                desired = want[key]
            else:
                desired = dict()

            add_config = dict_diff(extant, desired)
            del_config = dict_diff(desired, extant)

            if (
                "speed" in add_config.keys()
                and "duplex" not in add_config.keys()
            ):
                add_config.update({"duplex": desired.get("duplex")})

            commands.extend(generate_commands(key, add_config, del_config))

        return commands

    @staticmethod
    def _state_merged(want, have):
        """ The command generator when state is merged

        :rtype: A list
        :returns: the commands necessary to merge the provided into
                  the current configuration
        """
        commands = []
        for key, desired in want.items():
            interface_name = normalize_interface(key)
            if interface_name in have:
                extant = have[interface_name]
            else:
                extant = dict()

            add_config = dict_diff(extant, desired)
            if (
                "speed" in add_config.keys()
                and "duplex" not in add_config.keys()
            ):
                add_config.update({"duplex": desired.get("duplex")})
            commands.extend(generate_commands(key, add_config, {}))

        return commands

    @staticmethod
    def _state_deleted(want, have):
        """ The command generator when state is deleted

        :rtype: A list
        :returns: the commands necessary to remove the current configuration
                  of the provided objects
        """
        commands = []
        for key in want:
            desired = dict()
            if key in have:
                extant = have[key]
            else:
                continue

            del_config = dict_diff(desired, extant)

            commands.extend(generate_commands(key, {}, del_config))

        return commands


def generate_commands(interface, to_set, to_remove):
    commands = []
    for key, value in to_set.items():
        if value is None:
            continue

        if key == "enabled":
            commands.append("{0}shutdown".format("no " if value else ""))
        elif key == "speed":
            if value == "auto":
                commands.append("{0} {1}".format(key, value))
            else:
                commands.append("speed {0}{1}".format(value, to_set["duplex"]))
        elif key == "duplex":
            # duplex is handled with speed
            continue
        elif key == "mode":
            if not re.search(r"(M|m)anagement.*", interface):
                if value == "layer3":
                    # switching from default (layer2) mode to layer3
                    commands.append("no switchport")
                else:
                    # setting to default (layer 2) mode
                    commands.append("switchport")
        else:
            commands.append("{0} {1}".format(key, value))

        # Don't try to also remove the same key, if present in to_remove
        to_remove.pop(key, None)

    for key in to_remove.keys():
        if key == "enabled":
            commands.append("no shutdown")
        elif key == "speed":
            commands.append("speed auto")
        elif key == "duplex":
            # duplex is handled with speed
            continue
        elif key == "mode":
            if not re.search(r"(M|m)anagement.*", interface):
                commands.append("switchport")
        else:
            commands.append("no {0}".format(key))

    if commands:
        commands.insert(0, "interface {0}".format(interface))

    return commands
