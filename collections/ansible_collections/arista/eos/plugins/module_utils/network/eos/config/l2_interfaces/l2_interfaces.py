# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The eos_l2_interfaces class
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
    to_list,
    param_list_to_dict,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.facts.facts import (
    Facts,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.utils.utils import (
    normalize_interface,
    vlan_range_to_list,
)


class L2_interfaces(ConfigBase):
    """
    The eos_l2_interfaces class
    """

    gather_subset = ["!all", "!min"]

    gather_network_resources = ["l2_interfaces"]

    def get_l2_interfaces_facts(self, data=None):
        """ Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(
            self.gather_subset, self.gather_network_resources, data=data
        )
        l2_interfaces_facts = facts["ansible_network_resources"].get(
            "l2_interfaces"
        )
        if not l2_interfaces_facts:
            return []
        return l2_interfaces_facts

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {"changed": False}
        commands = list()
        warnings = list()

        if self.state in self.ACTION_STATES:
            existing_l2_interfaces_facts = self.get_l2_interfaces_facts()
        else:
            existing_l2_interfaces_facts = []

        if self.state in self.ACTION_STATES or self.state == "rendered":
            commands.extend(self.set_config(existing_l2_interfaces_facts))

        if commands and self.state in self.ACTION_STATES:
            if not self._module.check_mode:
                self._connection.edit_config(commands)
            result["changed"] = True

        if self.state in self.ACTION_STATES:
            result["commands"] = commands

        if self.state in self.ACTION_STATES or self.state == "gathered":
            changed_l2_interfaces_facts = self.get_l2_interfaces_facts()

        elif self.state == "rendered":
            result["rendered"] = commands

        elif self.state == "parsed":
            running_config = self._module.params["running_config"]
            if not running_config:
                self._module.fail_json(
                    msg="value of running_config parameter must not be empty for state parsed"
                )
            result["parsed"] = self.get_l2_interfaces_facts(
                data=running_config
            )

        if self.state in self.ACTION_STATES:
            result["before"] = existing_l2_interfaces_facts
            if result["changed"]:
                result["after"] = changed_l2_interfaces_facts

        elif self.state == "gathered":
            result["gathered"] = changed_l2_interfaces_facts

        result["warnings"] = warnings
        return result

    def set_config(self, existing_l2_interfaces_facts):
        """ Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        want = self._module.params["config"]
        have = existing_l2_interfaces_facts
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

            intf_commands = set_interface(desired, extant)
            intf_commands.extend(clear_interface(desired, extant))

            if intf_commands:
                commands.append("interface {0}".format(interface_name))
                commands.extend(intf_commands)

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

            intf_commands = set_interface(desired, extant)
            intf_commands.extend(clear_interface(desired, extant))

            if intf_commands:
                commands.append("interface {0}".format(key))
                commands.extend(intf_commands)

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

            intf_commands = set_interface(desired, extant)

            if intf_commands:
                commands.append("interface {0}".format(interface_name))
                commands.extend(intf_commands)

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
            intf_commands = clear_interface(desired, extant)

            if intf_commands:
                commands.append("interface {0}".format(key))
                commands.extend(intf_commands)

        return commands


def set_interface(want, have):
    commands = []

    want_mode = want.get("mode")
    if want_mode and want_mode != have.get("mode"):
        commands.append("switchport mode {0}".format(want_mode))

    wants_access = want.get("access")
    if wants_access:
        access_vlan = wants_access.get("vlan")
        if access_vlan and access_vlan != have.get("access", {}).get("vlan"):
            commands.append("switchport access vlan {0}".format(access_vlan))

    wants_trunk = want.get("trunk")
    if wants_trunk:
        allowed_vlans = []
        has_allowed_vlans = {}
        want_allowed_vlans = {}
        has_trunk = have.get("trunk", {})
        native_vlan = wants_trunk.get("native_vlan")
        if native_vlan and native_vlan != has_trunk.get("native_vlan"):
            commands.append(
                "switchport trunk native vlan {0}".format(native_vlan)
            )
        for con in [want, have]:
            expand_trunk_allowed_vlans(con)
        want_allowed_vlans = want["trunk"].get("trunk_allowed_vlans")
        if has_trunk:
            has_allowed_vlans = has_trunk.get("trunk_allowed_vlans")

        if want_allowed_vlans and has_allowed_vlans:
            allowed_vlans = list(
                set(want_allowed_vlans.split(","))
                - set(has_allowed_vlans.split(","))
            )
        elif want_allowed_vlans:
            allowed_vlans = want_allowed_vlans.split(",")
        if allowed_vlans:
            allowed_vlans.sort()
            allowed_vlans = ",".join(
                ["{0}".format(vlan) for vlan in allowed_vlans]
            )
            if has_allowed_vlans:
                commands.append(
                    "switchport trunk allowed vlan add {0}".format(
                        allowed_vlans
                    )
                )
            else:
                commands.append(
                    "switchport trunk allowed vlan {0}".format(allowed_vlans)
                )
    return commands


def expand_trunk_allowed_vlans(want):
    if not want:
        return None
    if want.get("trunk"):
        if "trunk_allowed_vlans" in want["trunk"]:
            allowed_vlans = vlan_range_to_list(
                want["trunk"]["trunk_allowed_vlans"]
            )
            vlans_list = [str(num) for num in sorted(allowed_vlans)]
            want["trunk"]["trunk_allowed_vlans"] = ",".join(vlans_list)


def clear_interface(want, have):
    commands = []

    if "mode" in have and want.get("mode") is None:
        commands.append("no switchport mode")

    if "access" in have and not want.get("access"):
        commands.append("no switchport access vlan")

    has_trunk = have.get("trunk") or {}
    wants_trunk = want.get("trunk") or {}
    if (
        "trunk_allowed_vlans" in has_trunk
        and "trunk_allowed_vlans" not in wants_trunk
    ):
        commands.append("no switchport trunk allowed vlan")
    if (
        "trunk_allowed_vlans" in has_trunk
        and "trunk_allowed_vlans" in wants_trunk
    ):
        for con in [want, have]:
            expand_trunk_allowed_vlans(con)
        want_allowed_vlans = want["trunk"].get("trunk_allowed_vlans")
        has_allowed_vlans = has_trunk.get("trunk_allowed_vlans")
        allowed_vlans = list(
            set(has_allowed_vlans.split(","))
            - set(want_allowed_vlans.split(","))
        )
        if allowed_vlans:
            allowed_vlans = ",".join(
                ["{0}".format(vlan) for vlan in allowed_vlans]
            )

            commands.append(
                "switchport trunk allowed vlan remove {0}".format(
                    allowed_vlans
                )
            )

    if "native_vlan" in has_trunk and "native_vlan" not in wants_trunk:
        commands.append("no switchport trunk native vlan")
    return commands
