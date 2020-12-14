#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The vyos_ospfv2 class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base import (
    ConfigBase,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    to_list,
    remove_empties,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.facts.facts import (
    Facts,
)
from ansible.module_utils.six import iteritems

from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.utils.utils import (
    list_diff_want_only,
    _in_target,
    _is_w_same,
    _bool_to_str,
)


class Ospfv2(ConfigBase):

    """
    The vyos_ospfv2 class
    """

    gather_subset = ["!all", "!min"]

    gather_network_resources = ["ospfv2"]

    def __init__(self, module):
        super(Ospfv2, self).__init__(module)

    def get_ospfv2_facts(self, data=None):
        """Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """

        (facts, _warnings) = Facts(self._module).get_facts(
            self.gather_subset, self.gather_network_resources, data=data
        )
        ospfv2_facts = facts["ansible_network_resources"].get("ospfv2", {})
        return ospfv2_facts

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """

        result = {"changed": False}
        warnings = list()
        commands = list()

        if self.state in self.ACTION_STATES:
            existing_ospfv2_facts = self.get_ospfv2_facts()
        else:
            existing_ospfv2_facts = {}

        if self.state in self.ACTION_STATES or self.state == "rendered":
            commands.extend(self.set_config(existing_ospfv2_facts))

        if commands and self.state in self.ACTION_STATES:
            if not self._module.check_mode:
                self._connection.edit_config(commands)
            result["changed"] = True

        if self.state in self.ACTION_STATES:
            result["commands"] = commands

        if self.state in self.ACTION_STATES or self.state == "gathered":
            changed_ospfv2_facts = self.get_ospfv2_facts()
        elif self.state == "rendered":
            result["rendered"] = commands
        elif self.state == "parsed":
            running_config = self._module.params["running_config"]
            if not running_config:
                self._module.fail_json(
                    msg="value of running_config parameter must not be empty for state parsed"
                )
            result["parsed"] = self.get_ospfv2_facts(data=running_config)
        else:
            changed_ospfv2_facts = {}

        if self.state in self.ACTION_STATES:
            result["before"] = existing_ospfv2_facts
            if result["changed"]:
                result["after"] = changed_ospfv2_facts
        elif self.state == "gathered":
            result["gathered"] = changed_ospfv2_facts

        result["warnings"] = warnings
        return result

    def set_config(self, existing_ospfv2_facts):
        """Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """

        want = self._module.params["config"]
        have = existing_ospfv2_facts
        resp = self.set_state(want, have)
        return to_list(resp)

    def set_state(self, w, h):
        """Select the appropriate function based on the state provided

        :param want: the desired configuration as a dictionary
        :param have: the current configuration as a dictionary
        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """

        commands = []
        if (
            self.state in ("merged", "replaced", "overridden", "rendered")
            and not w
        ):
            self._module.fail_json(
                msg="value of config parameter must not be empty for state {0}".format(
                    self.state
                )
            )

        if self.state == "deleted":
            commands.extend(self._state_deleted(h))
        elif self.state in ("merged", "rendered"):
            commands.extend(self._state_merged(w, h))
        elif self.state == "replaced":
            commands.extend(self._state_replaced(w, h))
        return commands

    def search_obj_in_have(self, have, w_name, key):
        """
        This function  returns the rule-set/rule if it is present in target config.
        :param have: target config.
        :param w_name: rule-set name.
        :param type: rule_sets/rule/r_list.
        :return: rule-set/rule.
        """

        if have:
            for item in have:
                if item[key] == w_name[key]:
                    return item
        return None

    def _state_replaced(self, want, have):
        """The command generator when state is replaced

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """

        commands = []
        if have:
            commands.extend(self._render_ospf_param(have, want, opr=False))
        commands.extend(self._render_ospf_param(want, have))
        return commands

    def _state_merged(self, want, have):
        """The command generator when state is merged

        :rtype: A list
        :returns: the commands necessary to merge the provided into
                  the current configuration
        """

        commands = []
        commands.extend(self._render_ospf_param(want, have))
        return commands

    def _state_deleted(self, have):
        """The command generator when state is deleted

        :rtype: A list
        :returns: the commands necessary to remove the current configuration
                  of the provided objects
        """

        commands = []
        if have:
            commands.append("delete protocols ospf")
        return commands

    def _render_ospf_param(self, want, have, opr=True):
        """
        This function forms the set/delete commands for ospf leaf attributes
        and triggers the process for other child attributes.
        for firewall_global attributes.
        :param w: the desired config.
        :param h: the target config.
        :param opr: True/False.
        :return: generated commands list.
        """

        commands = []
        w = deepcopy(remove_empties(want))
        leaf = ("default_metric", "log_adjacency_changes")
        if w:
            for (key, val) in iteritems(w):
                if opr and key in leaf and not _is_w_same(w, have, key):
                    commands.append(
                        self._form_attr_cmd(
                            attr=key, val=_bool_to_str(val), opr=opr
                        )
                    )
                elif not opr and key in leaf and not _in_target(have, key):
                    commands.append(
                        self._form_attr_cmd(
                            attr=key, val=_bool_to_str(val), opr=opr
                        )
                    )
                else:
                    commands.extend(
                        self._render_child_param(w, have, key, opr)
                    )
        return commands

    def _render_child_param(self, w, h, key, opr=True):
        """
        This function invoke the function to extend commands
        based on the key.
        :param w: the desired configuration.
        :param h: the current configuration.
        :param key: attribute name.
        :param opr: operation.
        :return: list of commands.
        """

        commands = []
        if key in ("neighbor", "redistribute"):
            commands.extend(self._render_list_dict_param(key, w, h, opr=opr))
        elif key in ("default_information", "max_metric"):
            commands.extend(self._render_nested_dict_param(key, w, h, opr=opr))
        elif key in ("mpls_te", "auto_cost", "parameters", "auto_cost"):
            commands.extend(self._render_dict_param(key, w, h, opr=opr))
        elif key in (
            "route_map",
            "passive_interface",
            "passive_interface_exclude",
        ):
            commands.extend(self._render_list_param(key, w, h, opr=opr))
        elif key == "areas":
            commands.extend(self._render_areas(key, w, h, opr=opr))
        elif key == "timers":
            commands.extend(self._render_timers(key, w, h, opr=opr))
        elif key == "distance":
            commands.extend(self._render_distance(key, w, h, opr=opr))
        return commands

    def _render_dict_param(self, attr, want, have, opr=True):
        """
        This function generate the commands for dictionary elements.
        :param attr: attribute name.
        :param w: the desired configuration.
        :param h: the target config.
        :param opr: True/False.
        :return: generated list of commands.
        """

        commands = []
        h = {}
        if have:
            h = have.get(attr) or {}
        if not opr and not h:
            commands.append(self._form_attr_cmd(attr=attr, opr=opr))
        elif want[attr]:
            leaf_dict = {
                "auto_cost": "reference_bandwidth",
                "mpls_te": ("enabled", "router_address"),
                "parameters": (
                    "router_id",
                    "abr_type",
                    "opaque_lsa",
                    "rfc1583_compatibility",
                ),
            }
            leaf = leaf_dict[attr]
            for (item, value) in iteritems(want[attr]):
                if (
                    opr
                    and item in leaf
                    and not _is_w_same(want[attr], h, item)
                ):
                    if item == "enabled":
                        item = "enable"
                    if item in (
                        "opaque_lsa",
                        "enable",
                        "rfc1583_compatibility",
                    ):
                        commands.append(
                            self._form_attr_cmd(key=attr, attr=item, opr=opr)
                        )
                    else:
                        commands.append(
                            self._form_attr_cmd(
                                key=attr, attr=item, val=value, opr=opr
                            )
                        )
                elif not opr and item in leaf and not _in_target(h, item):
                    if item == "enabled":
                        commands.append(
                            self._form_attr_cmd(
                                key=attr, attr="enable", opr=opr
                            )
                        )
                    else:
                        commands.append(
                            self._form_attr_cmd(key=attr, attr=item, opr=opr)
                        )
        return commands

    def _render_list_param(self, attr, want, have, cmd=None, opr=True):
        """
        This function forms the commands for passed target list attributes'.
        :param attr: attribute name.
        :param w: the desired config.
        :param h: the target config.
        :param cmd: commands to be prepend.
        :param opr: True/False.
        :return: generated list of commands.
        """

        commands = []
        h = []
        if want:
            w = want.get(attr) or []
        if have:
            h = have.get(attr) or []
        if not cmd:
            cmd = self._compute_command(opr=opr)
        if w:
            if opr:
                members = list_diff_want_only(w, h)
                for member in members:
                    command = cmd + attr.replace("_", "-") + " "
                    if attr == "network":
                        command += member["address"]
                    else:
                        command += member
                    commands.append(command)
            elif not opr:
                if h:
                    for member in w:
                        if attr == "network":
                            if not self.search_obj_in_have(
                                h, member, "address"
                            ):
                                commands.append(
                                    cmd
                                    + attr.replace("_", "-")
                                    + " "
                                    + member["address"]
                                )
                        elif member not in h:
                            commands.append(
                                cmd + attr.replace("_", "-") + " " + member
                            )
                else:
                    commands.append(cmd + " " + attr.replace("_", "-"))
        return commands

    def _render_vlink(self, attr, want, have, cmd=None, opr=True):
        """
        This function forms the set/delete commands based on the 'opr' type
        for attributes with in desired list of dictionary.
        :param attr: attribute name.
        :param w: the desired config.
        :param h: the target config.
        :param cmd: commands to be prepend.
        :param opr: True/False.
        :return: generated commands list.
        """

        commands = []
        h = []
        name = {"virtual_link": "address"}
        leaf_dict = {
            "virtual_link": (
                "address",
                "dead_interval",
                "transmit_delay",
                "hello_interval",
                "retransmit_interval",
            )
        }
        leaf = leaf_dict[attr]
        w = want.get(attr) or []
        if have:
            h = have.get(attr) or []
        if not opr and not h:
            commands.append(cmd + attr.replace("_", "-"))
        elif w:
            for w_item in w:
                for (key, val) in iteritems(w_item):
                    if not cmd:
                        cmd = self._compute_command(opr=opr)
                    h_item = self.search_obj_in_have(h, w_item, name[attr])
                    if (
                        opr
                        and key in leaf
                        and not _is_w_same(w_item, h_item, key)
                    ):
                        if key in "address":
                            commands.append(
                                cmd + attr.replace("_", "-") + " " + str(val)
                            )
                        else:
                            commands.append(
                                cmd
                                + attr.replace("_", "-")
                                + " "
                                + w_item[name[attr]]
                                + " "
                                + key.replace("_", "-")
                                + " "
                                + str(val)
                            )
                    elif (
                        not opr and key in leaf and not _in_target(h_item, key)
                    ):
                        if key in "address":
                            commands.append(
                                cmd + attr.replace("_", "-") + " " + str(val)
                            )
                        else:
                            commands.append(
                                cmd
                                + attr.replace("_", "-")
                                + " "
                                + w_item[name[attr]]
                                + " "
                                + key
                            )
                    elif key == "authentication":
                        commands.extend(
                            self._render_vlink_auth(
                                attr,
                                key,
                                w_item,
                                h_item,
                                w_item["address"],
                                cmd,
                                opr,
                            )
                        )
        return commands

    def _render_vlink_auth(
        self, attr, key, want, have, address, cmd=None, opr=True
    ):
        """
        This function forms the set/delete commands based on the 'opr' type
        for attributes with in desired list of dictionary.
        :param attr: attribute name.
        :param w: the desired config.
        :param h: the target config.
        :param cmd: commands to be prepend.
        :param opr: True/False.
        :return: generated commands list.
        """

        commands = []
        h = []

        w = want.get(key) or {}
        if have:
            h = have.get(key) or {}
        cmd += attr.replace("_", "-") + " " + address + " " + key + " "
        commands.extend(self._render_list_dict_param("md5", w, h, cmd, opr))
        return commands

    def _render_list_dict_param(self, attr, want, have, cmd=None, opr=True):
        """
        This function forms the set/delete commands based on the 'opr' type
        for attributes with in desired list of dictionary.
        :param attr: attribute name.
        :param w: the desired config.
        :param h: the target config.
        :param cmd: commands to be prepend.
        :param opr: True/False.
        :return: generated commands list.
        """

        commands = []
        h = []
        name = {
            "redistribute": "route_type",
            "neighbor": "neighbor_id",
            "range": "address",
            "md5": "key_id",
            "vlink": "address",
        }
        leaf_dict = {
            "md5": "md5_key",
            "redistribute": (
                "metric",
                "route_map",
                "route_type",
                "metric_type",
            ),
            "neighbor": ("priority", "poll_interval", "neighbor_id"),
            "range": ("cost", "address", "substitute", "not_advertise"),
            "vlink": (
                "address",
                "dead_interval",
                "transmit_delay",
                "hello_interval",
                "retransmit_interval",
            ),
        }
        leaf = leaf_dict[attr]
        w = want.get(attr) or []
        if have:
            h = have.get(attr) or []
        if not opr and not h:
            commands.append(self._compute_command(attr=attr, opr=opr))
        elif w:
            for w_item in w:
                for (key, val) in iteritems(w_item):
                    if not cmd:
                        cmd = self._compute_command(opr=opr)
                    h_item = self.search_obj_in_have(h, w_item, name[attr])
                    if (
                        opr
                        and key in leaf
                        and not _is_w_same(w_item, h_item, key)
                    ):
                        if key in (
                            "route_type",
                            "neighbor_id",
                            "address",
                            "key_id",
                        ):
                            commands.append(cmd + attr + " " + str(val))
                        elif key == "cost":
                            commands.append(
                                cmd
                                + attr
                                + " "
                                + w_item[name[attr]]
                                + " "
                                + key
                                + " "
                                + str(val)
                            )
                        elif key == "not_advertise":
                            commands.append(
                                cmd
                                + attr
                                + " "
                                + w_item[name[attr]]
                                + " "
                                + key.replace("_", "-")
                            )
                        elif key == "md5_key":
                            commands.append(
                                cmd
                                + attr
                                + " "
                                + "key-id"
                                + " "
                                + str(w_item[name[attr]])
                                + " "
                                + key.replace("_", "-")
                                + " "
                                + w_item[key]
                            )
                        else:
                            commands.append(
                                cmd
                                + attr
                                + " "
                                + w_item[name[attr]]
                                + " "
                                + key.replace("_", "-")
                                + " "
                                + str(val)
                            )
                    elif (
                        not opr and key in leaf and not _in_target(h_item, key)
                    ):
                        if key in (
                            "route_type",
                            "neighbor_id",
                            "address",
                            "key_id",
                        ):
                            commands.append(cmd + attr + " " + str(val))
                        else:
                            commands.append(
                                cmd
                                + attr
                                + " "
                                + w_item[name[attr]]
                                + " "
                                + key
                            )
        return commands

    def _render_nested_dict_param(self, attr, want, have, opr=True):
        """
        This function forms the set/delete commands based on the 'opr' type
        for attributes with in desired nested dicts.
        :param attr: attribute name.
        :param w: the desired config.
        :param h: the target config.
        :param cmd: commands to be prepend.
        :param opr: True/False.
        :return: generated commands list.
        """

        commands = []
        attr_dict = {
            "default_information": "originate",
            "max_metric": "router_lsa",
        }
        leaf_dict = {
            "default_information": (
                "always",
                "metric",
                "metric_type",
                "route_map",
            ),
            "max_metric": ("administrative", "on_startup", "on_shutdown"),
        }
        h = {}
        w = want.get(attr) or {}
        if have:
            h = have.get(attr) or {}
        if not opr and not h:
            commands.append(self._form_attr_cmd(attr=attr, opr=opr))
        elif w:
            key = attr_dict[attr]
            w_attrib = want[attr].get(key) or {}
            cmd = self._compute_command(opr=opr)
            h_attrib = {}
            if w_attrib:
                leaf = leaf_dict[attr]
                if h and key in h.keys():
                    h_attrib = h.get(key) or {}
                for (item, val) in iteritems(w[key]):
                    if (
                        opr
                        and item in leaf
                        and not _is_w_same(w[key], h_attrib, item)
                    ):
                        if item in ("administrative", "always") and val:
                            commands.append(
                                cmd
                                + attr.replace("_", "-")
                                + " "
                                + key.replace("_", "-")
                                + " "
                                + item.replace("_", "-")
                            )
                        elif item not in ("administrative", "always"):
                            commands.append(
                                cmd
                                + attr.replace("_", "-")
                                + " "
                                + key.replace("_", "-")
                                + " "
                                + item.replace("_", "-")
                                + " "
                                + str(val)
                            )
                    elif (
                        not opr
                        and item in leaf
                        and not _in_target(h_attrib, item)
                    ):

                        commands.append(cmd + attr + " " + item)
        return commands

    def _render_areas(self, attr, want, have, opr=True):
        """
        This function forms the set/delete commands based on the 'opr' type
        for ospf area attributes.
        :param attr: attribute name.
        :param w: the desired config.
        :param h: the target config.
        :param opr: True/False.
        :return: generated commands list.
        """

        commands = []
        h_lst = {}
        w_lst = want.get(attr) or []
        l_set = ("area_id", "shortcut", "authentication")
        if have:
            h_lst = have.get(attr) or []
        if not opr and not h_lst:
            commands.append(self._form_attr_cmd(attr="area", opr=opr))
        elif w_lst:
            for w_area in w_lst:
                cmd = (
                    self._compute_command(
                        key="area",
                        attr=_bool_to_str(w_area["area_id"]),
                        opr=opr,
                    )
                    + " "
                )
                h_area = self.search_obj_in_have(h_lst, w_area, "area_id")
                if not opr and not h_area:
                    commands.append(
                        self._form_attr_cmd(
                            key="area", attr=w_area["area_id"], opr=opr
                        )
                    )
                else:
                    for (key, val) in iteritems(w_area):
                        if (
                            opr
                            and key in l_set
                            and not _is_w_same(w_area, h_area, key)
                        ):
                            if key == "area_id":
                                commands.append(
                                    self._form_attr_cmd(
                                        attr="area",
                                        val=_bool_to_str(val),
                                        opr=opr,
                                    )
                                )
                            else:
                                commands.append(
                                    cmd
                                    + key
                                    + " "
                                    + _bool_to_str(val).replace("_", "-")
                                )
                        elif not opr and key in l_set:
                            if key == "area_id" and not _in_target(
                                h_area, key
                            ):
                                commands.append(cmd)
                                continue
                            if key != "area_id" and not _in_target(
                                h_area, key
                            ):
                                commands.append(cmd + val + " " + key)
                        elif key == "area_type":
                            commands.extend(
                                self._render_area_type(
                                    w_area, h_area, key, cmd, opr
                                )
                            )
                        elif key == "network":
                            commands.extend(
                                self._render_list_param(
                                    key, w_area, h_area, cmd, opr
                                )
                            )
                        elif key == "range":
                            commands.extend(
                                self._render_list_dict_param(
                                    key, w_area, h_area, cmd, opr
                                )
                            )
                        elif key == "virtual_link":
                            commands.extend(
                                self._render_vlink(
                                    key, w_area, h_area, cmd, opr
                                )
                            )
        return commands

    def _render_area_type(self, want, have, attr, cmd, opr=True):
        """
        This function forms the set/delete commands based on the 'opr' type
        for area_types attributes.
        :param attr: attribute name.
        :param w: the desired config.
        :param h: the target config.
        :param cmd: command to prepend.
        :param opr: True/False.
        :return: generated commands list.
        """

        commands = []
        h_type = {}
        w_type = want.get(attr) or []
        if have:
            h_type = have.get(attr) or {}
        if not opr and not h_type:
            commands.append(cmd + attr.replace("_", "-"))
        elif w_type:
            key = "normal"
            if (
                opr
                and key in w_type.keys()
                and not _is_w_same(w_type, h_type, key)
            ):
                if not w_type[key] and h_type and h_type[key]:
                    commands.append(
                        cmd.replace("set", "delete")
                        + attr.replace("_", "-")
                        + " "
                        + key
                    )
                elif w_type[key]:
                    commands.append(cmd + attr.replace("_", "-") + " " + key)
            elif (
                not opr
                and key in w_type.keys()
                and not (h_type and key in h_type.keys())
            ):
                commands.append(
                    cmd + want["area"] + " " + attr.replace("_", "-")
                )

            a_type = {
                "nssa": ("set", "default_cost", "no_summary", "translate"),
                "stub": ("set", "default_cost", "no_summary"),
            }
            for key in a_type:
                w_area = want[attr].get(key) or {}
                h_area = {}
                if w_area:
                    if h_type and key in h_type.keys():
                        h_area = h_type.get(key) or {}
                    for (item, val) in iteritems(w_type[key]):
                        if (
                            opr
                            and item in a_type[key]
                            and not _is_w_same(w_type[key], h_area, item)
                        ):
                            if item == "set" and val:
                                commands.append(
                                    cmd + attr.replace("_", "-") + " " + key
                                )
                            elif not val and h_area and h_area[item]:
                                commands.append(
                                    cmd.replace("set", "delete")
                                    + attr.replace("_", "-")
                                    + " "
                                    + key
                                )
                            elif item != "set":
                                commands.append(
                                    cmd
                                    + attr.replace("_", "-")
                                    + " "
                                    + key
                                    + " "
                                    + item.replace("_", "-")
                                    + " "
                                    + str(val)
                                )
                        elif (
                            not opr
                            and item in a_type[key]
                            and not (h_type and key in h_type)
                        ):
                            if item == "set":
                                commands.append(
                                    cmd + attr.replace("_", "-") + " " + key
                                )
                            else:
                                commands.append(
                                    cmd
                                    + want["area"]
                                    + " "
                                    + attr.replace("_", "-")
                                    + " "
                                    + key
                                    + " "
                                    + item.replace("_", "-")
                                )
        return commands

    def _form_attr_cmd(self, key=None, attr=None, val=None, opr=True):
        """
        This function forms the command for leaf attribute.
        :param key: parent key.
        :param attr: attribute name
        :param value: value
        :param opr: True/False.
        :return: generated command.
        """

        return self._compute_command(
            key, attr=self._map_attrib(attr), val=val, opr=opr
        )

    def _compute_command(
        self, key=None, attr=None, val=None, remove=False, opr=True
    ):
        """
        This function construct the add/delete command based on passed attributes.
        :param key: parent key.
        :param attr: attribute name
        :param value: value
        :param opr: True/False.
        :return: generated command.
        """

        if remove or not opr:
            cmd = "delete protocols ospf "
        else:
            cmd = "set protocols ospf "
        if key:
            cmd += key.replace("_", "-") + " "
        if attr:
            cmd += attr.replace("_", "-")
        if val:
            cmd += " '" + str(val) + "'"
        return cmd

    def _map_attrib(self, attrib):
        """
        - This function construct the regex string.
        - replace the underscore with hyphen.
        :param attrib: attribute
        :return: regex string
        """

        return "disable" if attrib == "disabled" else attrib.replace("_", "-")
