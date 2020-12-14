#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The eos_ospfv2 class
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
    remove_empties,
)

from ansible_collections.arista.eos.plugins.module_utils.network.eos.facts.facts import (
    Facts,
)


class Ospfv2(ConfigBase):
    """
    The eos_ospfv2 class
    """

    gather_subset = ["!all", "!min"]

    gather_network_resources = ["ospfv2"]

    def __init__(self, module):
        super(Ospfv2, self).__init__(module)

    def get_ospfv2_facts(self, data=None):
        """ Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(
            self.gather_subset, self.gather_network_resources, data=data
        )

        ospfv2_facts = facts["ansible_network_resources"].get("ospfv2")
        if not ospfv2_facts:
            return []
        return ospfv2_facts

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {"changed": False}
        warnings = list()
        commands = list()

        if self.state in self.ACTION_STATES:
            existing_ospfv2_facts = self.get_ospfv2_facts()
        else:
            existing_ospfv2_facts = []
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
            if not self._module.params["running_config"]:
                self._module.fail_json(
                    msg="value of running_config parameter must not be empty for state parsed"
                )
            result["parsed"] = self.get_ospfv2_facts(
                data=self._module.params["running_config"]
            )
        else:
            changed_ospfv2_facts = self.get_ospfv2_facts()
        if self.state in self.ACTION_STATES:
            result["before"] = existing_ospfv2_facts
            if result["changed"]:
                result["after"] = changed_ospfv2_facts
        elif self.state == "gathered":
            result["gathered"] = changed_ospfv2_facts

        result["warnings"] = warnings
        return result

    def set_config(self, existing_ospfv2_facts):
        """ Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        want = self._module.params["config"]
        have = existing_ospfv2_facts
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
        commands = []
        if (
            self.state in ("merged", "replaced", "overridden", "rendered")
            and not want
        ):
            self._module.fail_json(
                msg="value of config parameter must not be empty for state {0}".format(
                    self.state
                )
            )
        if self.state == "overridden":
            commands = self._state_overridden(want, have)
        elif self.state == "deleted":
            commands = self._state_deleted(want, have)
        elif self.state == "merged" or self.state == "rendered":
            commands = self._state_merged(want, have)
        elif self.state == "replaced":
            commands = self._state_replaced(want, have)
        return commands

    def _state_replaced(self, want, have):
        """ The command generator when state is replaced

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        commands = []
        for w in want["processes"]:
            del_cmds = w.copy()
            add_cmds = {}
            for h in have["processes"]:
                if h["process_id"] != w["process_id"]:
                    continue
                if w.get("vrf"):
                    if w["vrf"] != h["vrf"]:
                        self._module.fail_json(
                            msg="Value of vrf and process_id does not match the config present in the device"
                        )
                        break
                del_instance_list = self.compare_dicts(h, w)
                if del_instance_list:
                    del_cmds = {"processes": del_instance_list}
                add_instance_list = self.compare_dicts(w, h)
                if add_instance_list:
                    add_cmds = {"processes": add_instance_list}

            return_command = self.del_commands(del_cmds, have)
            for command in return_command:
                if "exit" not in command:
                    commands.append(command)
            return_command = self.add_commands(add_cmds, have)
            for command in return_command:
                if "router ospf" in command:
                    if command not in commands:
                        commands.append(command)
                else:
                    commands.append(command)
        commandset = []
        if commands:
            commandset.append(commands[0])
            for cmd in commands[1::]:
                if "router ospf" in cmd and commandset[-1] != "exit":
                    commandset.append("exit")
                commandset.append(cmd)
            if commandset[-1] != "exit":
                commandset.append("exit")
        return commandset

    def _state_overridden(self, want, have):
        """ The command generator when state is overridden

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        commands = []
        for h in have["processes"]:
            present = False
            for w in want["processes"]:
                if h["process_id"] == w["process_id"]:
                    present = True
                    break
            if not present:
                commands.append("no router ospf " + str(h["process_id"]))
        replace_cmds = self._state_replaced(want, have)
        for cmd in replace_cmds:
            commands.append(cmd)
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
        return_command = self.del_commands(want, have)
        if return_command:
            for cmd in return_command:
                if "no exit" in cmd:
                    cmd = "exit"
                commands.append(cmd)
        return commands

    def set_commands(self, want, have):
        commands = []
        instance_list = []
        for w in want["processes"]:
            present = False
            c = []
            if have and not have.get("processes"):
                instance_list = want["processes"]
                break
            if have:
                for h in have["processes"]:
                    if w["process_id"] == h["process_id"]:
                        if w.get("vrf"):
                            if w["vrf"] != h["vrf"]:
                                self._module.fail_json(
                                    msg="Value of vrf and process_id does not match the config present in the device"
                                )
                                continue
                        present = True
                        c = self.compare_dicts(w, h)
                        break
            if c:
                instance_list.append(c[0])
            if not present:
                if w["vrf"] in _get_vrf_list(have):
                    self._module.fail_json(
                        msg="Value of vrf and process_id does not match the config present in the device"
                    )
                instance_list.append(w)
        instance_dict = {"processes": instance_list}
        return_command = self.add_commands(instance_dict, have)
        for command in return_command:
            commands.append(command)
        return commands

    def compare_dicts(self, want_inst, have_inst):
        want_dict = remove_empties(want_inst)
        have = have_inst
        ospf_list = []
        return_ospf_dict = {}
        for w_key in want_dict.keys():
            if not have.get(w_key):
                return_ospf_dict.update({w_key: want_dict[w_key]})
            elif (
                isinstance(want_dict[w_key], str)
                or isinstance(want_dict[w_key], bool)
                or isinstance(want_dict[w_key], int)
            ):
                if want_dict[w_key] != have[w_key]:
                    return_ospf_dict.update({w_key: want_dict[w_key]})
            elif isinstance(want_dict[w_key], dict):
                diff = dict_diff(have.get(w_key, {}), want_dict[w_key])
                if diff:
                    return_ospf_dict.update({w_key: diff})
            elif isinstance(want_dict[w_key], list):
                if have.get(w_key):
                    compare_list = self.compare_ospf_list(
                        want_dict[w_key], have.get(w_key), w_key
                    )
                    if compare_list:
                        return_ospf_dict.update({w_key: compare_list})
            else:
                if want_dict[w_key] != have.get(w_key):
                    return_ospf_dict.update({w_key: want_dict[w_key]})

        if return_ospf_dict:
            if want_dict.get("vrf"):
                return_ospf_dict.update(
                    {
                        "process_id": want_dict["process_id"],
                        "vrf": want_dict["vrf"],
                    }
                )
            else:
                return_ospf_dict.update(
                    {"process_id": want_dict["process_id"]}
                )
            ospf_list.append(return_ospf_dict)
        return ospf_list

    def compare_ospf_list(self, w_list, h_list, l_key):
        return_list = []
        for w in w_list:
            present = False
            for h in h_list:
                diff = dict_diff(h, w)
                if not diff:
                    present = True
                    break
            if not present:
                return_list.append(w)
        return return_list

    def add_commands(self, want, have):
        commands = []
        if not want:
            return commands
        for ospf_params in want["processes"]:
            commands.append(_get_router_command(ospf_params))
            if ospf_params.get("traffic_engineering"):
                commands.append("traffic-engineering")
            if ospf_params.get("adjacency"):
                threshold = ospf_params["adjacency"]["exchange_start"][
                    "threshold"
                ]
                commands.append(
                    "adjacency exchange-start threshold " + str(threshold)
                )
            if ospf_params.get("areas"):
                command_list = _parse_areas(ospf_params["areas"])
                for c in command_list:
                    commands.append(c)
            if ospf_params.get("auto_cost"):
                commands.append(
                    "auto-cose reference-bandwidth " + ospf_params["auto_cost"]
                )
            if ospf_params.get("bfd"):
                commands.append("bfd default")
            if ospf_params.get("default_information"):
                commands.append(
                    _parse_default_information(
                        ospf_params["default_information"]
                    )
                )
            if ospf_params.get("default_metric"):
                commands.append(
                    "default-metric" + " " + str(ospf_params["default_metric"])
                )
            if ospf_params.get("distance"):
                for k, v in ospf_params["distance"].items():
                    if v:
                        k = re.sub(r"_", "-", k)
                        commands.append("distance ospf " + k + " " + str(v))
            if ospf_params.get("distribute_list"):
                commands.append(
                    "distribute-list "
                    + ospf_params["distribute_list"].keys()[0]
                    + " "
                    + ospf_params["distribute_list"].values()[0]
                    + " in"
                )
            if ospf_params.get("dn_bit_ignore"):
                commands.append("dn-bit-ignore")
            if ospf_params.get("graceful_restart"):
                if ospf_params["graceful_restart"].get("set"):
                    commands.append("graceful-restart")
                else:
                    commands.append(
                        "graceful-restart grace-period "
                        + str(
                            ospf_params["graceful_restart"].get("grace_period")
                        )
                    )
            if ospf_params.get("graceful_restart_helper"):
                commands.append("graceful-restart-helper")
            if ospf_params.get("log_adjacency_changes"):
                cmd = "log-adjacency-changes"
                if ospf_params["log_adjacency_changes"].get("detail"):
                    cmd = cmd + " detail"
                commands.append(cmd)
            if ospf_params.get("max_lsa"):
                commands.append(_parse_max_lsa(ospf_params["max_lsa"]))
            if ospf_params.get("max_metric"):
                commands.append(_parse_max_metric(ospf_params["max_metric"]))
            if ospf_params.get("maximum_paths"):
                commands.append(
                    "maximum-paths " + str(ospf_params["maximum_paths"])
                )
            if ospf_params.get("mpls_ldp"):
                commands.append("mpls ldp sync default")
            if ospf_params.get("networks"):
                command_list = _parse_networks(ospf_params["networks"])
                for c in command_list:
                    commands.append(c)
            if ospf_params.get("passive_interface"):
                if "interface_list" in ospf_params["passive_interface"].keys():
                    commands.append(
                        "passive-interface "
                        + ospf_params["passive_interface"]["interface_list"]
                    )
                else:
                    commands.append("passive-interface default")
            if ospf_params.get("point_to_point"):
                commands.append("point-to-point routes")
            if ospf_params.get("redistribute"):
                command_list = _parse_redistribute(ospf_params["redistribute"])
                for c in command_list:
                    commands.append(c)
            if ospf_params.get("retransmission_threshold"):
                commands.append(
                    "retransmission-threshold lsa "
                    + str(ospf_params["retransmission_threshold"])
                )
            if ospf_params.get("rfc1583compatibility"):
                commands.append("compatible rfc1583")
            if ospf_params.get("router_id"):
                commands.append("router-id " + ospf_params.get("router_id"))
            if ospf_params.get("summary_address"):
                commands.append(
                    _parse_summary_address(ospf_params["summary_address"])
                )
            if ospf_params.get("timers"):
                command_list = _parse_timers(ospf_params["timers"])
                for c in command_list:
                    commands.append(c)
            commands.append("exit")
        commandset = []
        for command in commands:
            commandset.append(command.strip())
        return commandset

    def del_commands(self, want, have):
        commands = []
        other_commands = 0
        want = remove_empties(want)
        if want.get("processes"):
            for w_inst in want["processes"]:
                router_context = 0
                d_cmds = []
                instance_list = []
                if have.get("processes"):
                    for h_inst in have["processes"]:
                        if h_inst["process_id"] == w_inst["process_id"]:
                            if w_inst.get("vrf") and w_inst.get(
                                "vrf"
                            ) == h_inst.get("vrf"):
                                if list(w_inst.keys()) == [
                                    "process_id",
                                    "vrf",
                                ]:
                                    commands.append(
                                        "no router ospf "
                                        + str(w_inst["process_id"])
                                        + " vrf "
                                        + w_inst["vrf"]
                                    )
                                    router_context = 1
                            if len(w_inst.keys()) == 1 and list(
                                w_inst.keys()
                            ) == ["process_id"]:
                                commands.append(
                                    "no router ospf "
                                    + str(w_inst["process_id"])
                                )
                                router_context = 1
                            if not router_context:
                                instance_list = self.compare_dicts(
                                    w_inst, h_inst
                                )
                                if not instance_list:
                                    del_want = {"processes": [w_inst]}
                                    d_cmds = self.add_commands(del_want, have)
                                for cmd in d_cmds:
                                    if "router ospf" in cmd:
                                        other_commands = 0
                                        if cmd not in commands:
                                            commands.append(cmd)
                                    else:
                                        cmd = "no " + cmd
                                        if cmd not in commands:
                                            commands.append(cmd)
                                            other_commands += 1
                if (
                    not other_commands
                    and len(commands) == 1
                    and not router_context
                ):
                    if (
                        "no" not in commands[0]
                        and "router ospf" in commands[0]
                    ):
                        commands[0] = "no " + commands[0]
        return commands


def _get_router_command(inst):
    command = ""
    if inst.get("vrf") and inst.get("vrf") != "default":
        command = (
            "router ospf " + str(inst["process_id"]) + " vrf " + inst["vrf"]
        )
    else:
        command = "router ospf " + str(inst["process_id"])
    return command


def _get_vrf_list(want):
    vrf_list = []
    if not want:
        return vrf_list
    for w in want["processes"]:
        if w.get("vrf"):
            vrf_list.append(w["vrf"])
    return vrf_list


def _parse_areas(areas):
    command = []
    for area in areas:
        area_cmd = "area " + area["area_id"]
        if area.get("default_cost"):
            command.append(
                area_cmd + " default-cost " + str(area.get("default_cost"))
            )
        elif area.get("filter"):
            command.append(
                area_cmd + " " + _parse_areas_filter(area["filter"])
            )
        elif area.get("not_so_stubby"):
            command.append(
                area_cmd
                + " "
                + _parse_areas_filter_notsostubby(area["not_so_stubby"])
            )
        elif area.get("nssa"):
            command.append(
                area_cmd + " " + _parse_areas_filter_nssa(area["nssa"])
            )
        elif area.get("range"):
            command.append(area_cmd + " " + _parse_areas_range(area["range"]))
    return command


def _parse_areas_filter(filter_dict):
    filter_cmd = "filter "
    if filter_dict.get("prefix_list"):
        filter_cmd = filter_cmd + filter_dict.get("filter")
    elif filter_dict.get("address"):
        filter_cmd = filter_cmd + filter_dict.get("address")
    else:
        filter_cmd = (
            filter_cmd
            + filter_dict.get("subnet_address")
            + " "
            + filter_dict.get("subnet_mask")
        )
    return filter_cmd


def _parse_areas_filter_notsostubby(nss_dict):
    nss_cmd = "not-so-stubby "
    if nss_dict.get("default_information_originate"):
        nss_cmd = nss_cmd + "default-information-originate "
        for def_keys in nss_dict["default_information_originate"].keys():
            if (
                def_keys == "nssa_only"
                and nss_dict["default_information_originate"]["nssa_only"]
            ):
                nss_cmd = nss_cmd + " nssa-only "
            elif nss_dict["default_information_originate"].get(def_keys):
                nss_cmd = (
                    nss_cmd
                    + def_keys
                    + " "
                    + nss_dict["default_information_originate"][def_keys]
                )
    elif "lsa" in nss_dict.keys() and nss_dict.get("lsa"):
        nss_cmd = nss_cmd + " lsa type-7 convert type-5"
    elif "no_summary" in nss_dict.keys() and nss_dict.get("no_summary"):
        nss_cmd = nss_cmd + " no-summary"
    elif "nssa_only" in nss_dict.keys() and nss_dict.get("nssa_only"):
        nss_cmd = nss_cmd + " nssa-only"
    return nss_cmd


def _parse_areas_filter_nssa(nss_dict):
    nss_cmd = "nssa "
    if nss_dict.get("default_information_originate"):
        nss_cmd = nss_cmd + "default-information-originate "
        for def_keys in nss_dict["default_information_originate"].keys():
            if (
                def_keys == "nssa_only"
                and nss_dict["default_information_originate"]["nssa_only"]
            ):
                nss_cmd = nss_cmd + " nssa-only "
            elif nss_dict["default_information_originate"].get(def_keys):
                nss_cmd = (
                    nss_cmd
                    + def_keys
                    + " "
                    + nss_dict["default_information_originate"][def_keys]
                )
    elif "no_summary" in nss_dict.keys() and nss_dict.get("no_summary"):
        nss_cmd = nss_cmd + " no-summary"
    elif "nssa_only" in nss_dict.keys() and nss_dict.get("nssa_only"):
        nss_cmd = nss_cmd + " nssa-only"
    return nss_cmd


def _parse_areas_range(range_dict):
    range_cmd = " range "
    if range_dict.get("address"):
        range_cmd = range_cmd + range_dict["address"]
    if range_dict.get("subnet_address"):
        range_cmd = (
            range_cmd
            + range_dict["subnet_address"]
            + " "
            + range_dict["subnet_mask"]
        )
    if range_dict.get("advertise") is not None:
        if range_dict["advertise"]:
            range_cmd = range_cmd + " advertise "
        else:
            range_cmd = range_cmd + " not-advertise "
    if range_dict.get("cost"):
        range_cmd = range_cmd + " cost " + str(range_dict["cost"])
    return range_cmd


def _parse_default_information(default_dict):
    def_cmd = "default-information originate"
    for def_key in sorted(default_dict.keys()):
        if def_key == "always":
            if default_dict.get(def_key):
                def_cmd = def_cmd + " " + def_key
        elif def_key in ["metric", "metric_type", "route_map"]:
            if default_dict.get(def_key):
                k = re.sub(r"_", "-", def_key)
                def_cmd = def_cmd + " " + k + " " + str(default_dict[def_key])
    return def_cmd


def _parse_max_lsa(max_lsa_dict):
    max_lsa_cmd = "max-lsa "
    if max_lsa_dict.get("count"):
        max_lsa_cmd = max_lsa_cmd + " " + str(max_lsa_dict["count"])
    if max_lsa_dict.get("threshold"):
        max_lsa_cmd = max_lsa_cmd + " " + str(max_lsa_dict["threshold"])
    for lsa_key, lsa_val in sorted(max_lsa_dict.items()):
        if lsa_key == "warning" and lsa_val:
            max_lsa_cmd = max_lsa_cmd + " warning-only"
        elif lsa_key in ["ignore_count", "reset_time", "ignore_time"]:
            if lsa_val:
                k = re.sub(r"_", "-", lsa_key)
                max_lsa_cmd = max_lsa_cmd + " " + k + " " + str(lsa_val) + " "
    return max_lsa_cmd


def _parse_max_metric(max_metric_dict):
    metric_cmd = "max-metric router-lsa "
    for k, v in max_metric_dict["router_lsa"].items():
        if not v:
            continue
        if k == "include_stub" and v:
            metric_cmd = metric_cmd + " include-stub"
        elif k == "on_startup":
            metric_cmd = metric_cmd + " on-startup " + str(v["wait_period"])
        elif k in ["summary_lsa", "external_lsa"]:
            k = re.sub(r"_", "-", k)
            if v.get("set"):
                metric_cmd = metric_cmd + " " + k
            else:
                metric_cmd = (
                    metric_cmd + " " + k + " " + str(v.get("max_metric_value"))
                )
    return metric_cmd


def _parse_networks(net_list):
    network_cmd = []
    for net_dict in net_list:
        net_cmd = "network "
        if net_dict.get("prefix"):
            net_cmd = net_cmd + net_dict.get("prefix")
        else:
            net_cmd = (
                net_cmd
                + net_dict.get("network_address")
                + " "
                + net_dict.get("mask")
            )
        if net_dict.get("area"):
            net_cmd = net_cmd + " area " + net_dict.get("area")
        network_cmd.append(net_cmd)
    return network_cmd


def _parse_redistribute(r_list):
    rcmd_list = []
    for r_dict in r_list:
        r_cmd = "redistribute "
        r_cmd = r_cmd + r_dict["routes"]
        if r_dict.get("isis_level"):
            k = re.sub(r"_", "-", r_dict["isis_level"])
            r_cmd = r_cmd + " " + k
        if r_dict.get("route_map"):
            r_cmd = r_cmd + " route-map " + r_dict["route_map"]
        rcmd_list.append(r_cmd)
    return rcmd_list


def _parse_summary_address(addr_dict):
    sum_cmd = "summary-address "
    if addr_dict.get("prefix"):
        sum_cmd = sum_cmd + addr_dict.get("prefix")
    else:
        sum_cmd = (
            sum_cmd + addr_dict.get("address") + " " + addr_dict.get("mask")
        )
    if "attribute_map" in addr_dict.keys():
        sum_cmd = sum_cmd + " attribute-map " + addr_dict["attribute_map"]
    elif addr_dict.get("not_advertise"):
        sum_cmd = sum_cmd + " not-advertise "
    elif "tag" in addr_dict.keys():
        sum_cmd = sum_cmd + " tag " + addr_dict["tag"]
    return sum_cmd


def _parse_timers(timers_list):
    timers_cmd = []
    for t_dict in timers_list:
        t_cmd = "timers "
        for t_key in t_dict.keys():
            if not t_dict.get(t_key):
                break
            if t_key == "lsa":
                if t_dict["lsa"].get("rx"):
                    t_cmd = (
                        t_cmd
                        + "lsa rx min interval "
                        + str(t_dict["lsa"]["rx"]["min_interval"])
                    )
                else:
                    t_cmd = (
                        t_cmd
                        + "lsa tx delay initial "
                        + str(t_dict["lsa"]["tx"]["delay"]["initial"])
                        + " "
                        + str(t_dict["lsa"]["tx"]["delay"]["min"])
                        + " "
                        + str(t_dict["lsa"]["tx"]["delay"]["max"])
                    )
            elif t_key == "out_delay":
                t_cmd = t_cmd + " out-delay " + str(t_dict["out_delay"])
            elif t_key == "pacing":
                t_cmd = t_cmd + " pacing flood " + str(t_dict["pacing"])
            elif t_key == "spf":
                if "seconds" in t_dict["spf"].keys():
                    t_cmd = t_cmd + " spf " + str(t_dict["spf"]["seconds"])
                else:
                    t_cmd = (
                        t_cmd
                        + " spf delay initial "
                        + str(t_dict["spf"]["initial"])
                        + " "
                        + str(t_dict["spf"]["max"])
                        + " "
                        + str(t_dict["spf"]["min"])
                    )
            timers_cmd.append(t_cmd)
    return timers_cmd
