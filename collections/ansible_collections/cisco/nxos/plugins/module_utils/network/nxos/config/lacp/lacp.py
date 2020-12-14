#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The nxos_lacp class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base import (
    ConfigBase,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_diff,
    to_list,
    remove_empties,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import (
    Facts,
)


class Lacp(ConfigBase):
    """
    The nxos_lacp class
    """

    gather_subset = ["!all", "!min"]

    gather_network_resources = ["lacp"]

    exclude_params = ["priority", "mac"]

    def __init__(self, module):
        super(Lacp, self).__init__(module)

    def get_lacp_facts(self, data=None):
        """ Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(
            self.gather_subset, self.gather_network_resources, data=data
        )
        lacp_facts = facts["ansible_network_resources"].get("lacp", {})

        return lacp_facts

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {"changed": False}
        commands = list()
        warnings = list()

        if self.state in self.ACTION_STATES:
            existing_lacp_facts = self.get_lacp_facts()
        else:
            existing_lacp_facts = {}

        if self.state in self.ACTION_STATES or self.state == "rendered":
            commands.extend(self.set_config(existing_lacp_facts))

        if commands and self.state in self.ACTION_STATES:
            if not self._module.check_mode:
                self._connection.edit_config(commands)
            result["changed"] = True

        if self.state in self.ACTION_STATES:
            result["commands"] = commands

        if self.state in self.ACTION_STATES or self.state == "gathered":
            changed_lacp_facts = self.get_lacp_facts()

        elif self.state == "rendered":
            result["rendered"] = commands

        elif self.state == "parsed":
            running_config = self._module.params["running_config"]
            if not running_config:
                self._module.fail_json(
                    msg="value of running_config parameter must not be empty for state parsed"
                )
            result["parsed"] = self.get_lacp_facts(data=running_config)

        if self.state in self.ACTION_STATES:
            result["before"] = existing_lacp_facts
            if result["changed"]:
                result["after"] = changed_lacp_facts

        elif self.state == "gathered":
            result["gathered"] = changed_lacp_facts

        result["warnings"] = warnings
        return result

    def set_config(self, existing_lacp_facts):
        """ Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        want = remove_empties(self._module.params["config"])
        have = existing_lacp_facts
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
        if state in ("merged", "replaced", "rendered") and not want:
            self._module.fail_json(
                msg="value of config parameter must not be empty for state {0}".format(
                    state
                )
            )

        commands = list()

        if state == "deleted":
            commands.extend(self._state_deleted(want, have))
        elif state in ["merged", "rendered"]:
            commands.extend(self._state_merged(want, have))
        elif state == "replaced":
            commands.extend(self._state_replaced(want, have))
        return commands

    def _state_replaced(self, want, have):
        """ The command generator when state is replaced

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        commands = []
        diff = dict_diff(want, have)
        wkeys = want.keys()
        dkeys = diff.keys()
        for k in wkeys:
            if k in self.exclude_params and k in dkeys:
                del diff[k]
        deleted_commands = self.del_all(diff)
        merged_commands = self._state_merged(want, have)

        commands.extend(deleted_commands)
        if merged_commands:
            commands.extend(merged_commands)

        return commands

    def _state_merged(self, want, have):
        """ The command generator when state is merged

        :rtype: A list
        :returns: the commands necessary to merge the provided into
                  the current configuration
        """
        return self.set_commands(want, have)

    def _state_deleted(self, want, have):
        """ The command generator when state is deleted

        :rtype: A list
        :returns: the commands necessary to remove the current configuration
                  of the provided objects
        """
        commands = []
        if not have:
            return commands
        commands.extend(self.del_all(have))
        return commands

    def get_diff(self, comparable, base):
        diff = {}
        if not base:
            diff = comparable
        else:
            diff = dict_diff(base, comparable)
        return diff

    def del_all(self, diff):
        commands = []
        base = "no lacp system-"
        diff = diff.get("system")
        if diff:
            if "priority" in diff:
                commands.append(base + "priority")
            if "mac" in diff:
                commands.append(base + "mac")
        return commands

    def add_commands(self, diff):
        commands = []
        base = "lacp system-"
        diff = diff.get("system")
        if diff and "priority" in diff:
            cmd = base + "priority" + " " + str(diff["priority"])
            commands.append(cmd)
        if diff and "mac" in diff:
            cmd = ""
            if "address" in diff["mac"]:
                cmd += base + "mac" + " " + diff["mac"]["address"]
            if "role" in diff["mac"]:
                cmd += " " + "role" + " " + diff["mac"]["role"]
            if cmd:
                commands.append(cmd)

        return commands

    def set_commands(self, want, have):
        if not want:
            return []
        diff = self.get_diff(want, have)
        return self.add_commands(diff)
