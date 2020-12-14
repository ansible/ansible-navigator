#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The vyos_ospfv3 class
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
    search_obj_in_list,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.facts.facts import (
    Facts,
)
from ansible.module_utils.six import iteritems

from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.utils.utils import (
    _in_target,
    _is_w_same,
    _bool_to_str,
)


class Ospfv3(ConfigBase):
    """
    The vyos_ospfv3 class
    """

    gather_subset = [
        "!all",
        "!min",
    ]

    gather_network_resources = [
        "ospfv3",
    ]

    def __init__(self, module):
        super(Ospfv3, self).__init__(module)

    def get_ospfv3_facts(self, data=None):
        """Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(
            self.gather_subset, self.gather_network_resources, data=data
        )
        ospfv3_facts = facts["ansible_network_resources"].get("ospfv3", {})
        return ospfv3_facts

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {"changed": False}
        warnings = list()
        commands = list()

        if self.state in self.ACTION_STATES:
            existing_ospfv3_facts = self.get_ospfv3_facts()
        else:
            existing_ospfv3_facts = {}

        if self.state in self.ACTION_STATES or self.state == "rendered":
            commands.extend(self.set_config(existing_ospfv3_facts))

        if commands and self.state in self.ACTION_STATES:
            if not self._module.check_mode:
                self._connection.edit_config(commands)
            result["changed"] = True

        if self.state in self.ACTION_STATES:
            result["commands"] = commands

        if self.state in self.ACTION_STATES or self.state == "gathered":
            changed_ospfv3_facts = self.get_ospfv3_facts()
        elif self.state == "rendered":
            result["rendered"] = commands
        elif self.state == "parsed":
            running_config = self._module.params["running_config"]
            if not running_config:
                self._module.fail_json(
                    msg="value of running_config parameter must not be empty for state parsed"
                )
            result["parsed"] = self.get_ospfv3_facts(data=running_config)
        else:
            changed_ospfv3_facts = {}

        if self.state in self.ACTION_STATES:
            result["before"] = existing_ospfv3_facts
            if result["changed"]:
                result["after"] = changed_ospfv3_facts
        elif self.state == "gathered":
            result["gathered"] = changed_ospfv3_facts

        result["warnings"] = warnings
        return result

    def set_config(self, existing_ospfv3_facts):
        """Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        want = self._module.params["config"]
        have = existing_ospfv3_facts
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
            commands.extend(self._state_deleted(w, h))
        elif self.state in ("merged", "rendered"):
            commands.extend(self._state_merged(w, h))
        elif self.state == "replaced":
            commands.extend(self._state_replaced(w, h))
        return commands

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

    def _state_deleted(self, want, have):
        """The command generator when state is deleted

        :rtype: A list
        :returns: the commands necessary to remove the current configuration
                  of the provided objects
        """
        commands = []
        if have:
            commands.append("delete protocols ospfv3")
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
        if w:
            for key, val in iteritems(w):
                commands.extend(self._render_child_param(w, have, key, opr))
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
        if key == "areas":
            commands.extend(self._render_areas(key, w, h, opr=opr))
        elif key == "parameters":
            commands.extend(self._render_dict_param(key, w, h, opr=opr))
        elif key == "redistribute":
            commands.extend(self._render_list_dict_param(key, w, h, opr=opr))
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
            leaf_dict = {"parameters": "router_id"}
            leaf = leaf_dict[attr]
            for item, value in iteritems(want[attr]):
                if (
                    opr
                    and item in leaf
                    and not _is_w_same(want[attr], h, item)
                ):
                    commands.append(
                        self._form_attr_cmd(
                            key=attr, attr=item, val=value, opr=opr
                        )
                    )
                elif not opr and item in leaf and not _in_target(h, item):
                    commands.append(
                        self._form_attr_cmd(key=attr, attr=item, opr=opr)
                    )
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
            "range": "address",
        }
        leaf_dict = {
            "redistribute": ("route_map", "route_type"),
            "range": ("address", "advertise", "not_advertise"),
        }
        leaf = leaf_dict[attr]
        w = want.get(attr) or []
        if have:
            h = have.get(attr) or []
        if not opr and not h:
            commands.append(self._compute_command(attr=attr, opr=opr))
        elif w:
            for w_item in w:
                for key, val in iteritems(w_item):
                    if not cmd:
                        cmd = self._compute_command(opr=opr)
                    h_item = search_obj_in_list(
                        w_item[name[attr]], h, name[attr]
                    )
                    if (
                        opr
                        and key in leaf
                        and not _is_w_same(w_item, h_item, key)
                    ):
                        if key == "route_type" or (
                            key == "address"
                            and "advertise" not in w_item
                            and "not-advertise" not in w_item
                        ):
                            if not val:
                                cmd = cmd.replace("set", "delete")
                            commands.append(cmd + attr + " " + str(val))
                        elif key in leaf_dict["range"] and key != "address":
                            commands.append(
                                cmd
                                + attr
                                + " "
                                + w_item[name[attr]]
                                + " "
                                + key.replace("_", "-")
                            )
                        elif key == "route_map":
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
                        if key in ("route_type", "address"):
                            commands.append(cmd + attr + " " + str(val))
                        else:
                            commands.append(
                                cmd
                                + (attr + " " + w_item[name[attr]] + " " + key)
                            )
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
        l_set = ("area_id", "export_list", "import_list")
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
                h_area = search_obj_in_list(
                    w_area["area_id"], h_lst, "area_id"
                )
                if not opr and not h_area:
                    commands.append(
                        self._form_attr_cmd(
                            key="area", attr=w_area["area_id"], opr=opr
                        )
                    )
                else:
                    for key, val in iteritems(w_area):
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
                                    + key.replace("_", "-")
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
                        elif key == "range":
                            commands.extend(
                                self._render_list_dict_param(
                                    key, w_area, h_area, cmd, opr
                                )
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
            cmd = "delete protocols ospfv3 "
        else:
            cmd = "set protocols ospfv3 "
        if key:
            cmd += key.replace("_", "-") + " "
        if attr:
            cmd += attr.replace("_", "-")
        if val and opr:
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
