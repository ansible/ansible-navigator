#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# utils

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import socket
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    is_masklen,
    to_netmask,
)


def remove_command_from_config_list(interface, cmd, commands):
    # To delete the passed config
    if interface not in commands:
        commands.insert(0, interface)
    commands.append("no %s" % cmd)
    return commands


def add_command_to_config_list(interface, cmd, commands):
    # To set the passed config
    if interface not in commands:
        commands.insert(0, interface)
    commands.append(cmd)


def reverify_diff_py35(want, have):
    """ Function to re-verify the set diff for py35 as it doesn't maintains dict order which results
        into unexpected set diff
    :param config: want and have set config
    :returns: True/False post checking if there's any actual diff b/w want and have sets
    """
    if not have:
        return True
    for each_want in want:
        diff = True
        for each_have in have:
            if each_have == sorted(each_want) or sorted(each_have) == sorted(
                each_want
            ):
                diff = False
        if diff:
            return True
    return False


def check_n_return_valid_ipv6_addr(module, input_list, filtered_ipv6_list):
    # To verify the valid ipv6 address
    try:
        for each in input_list:
            if "::" in each:
                if "/" in each:
                    each = each.split("/")[0]
                if socket.inet_pton(socket.AF_INET6, each):
                    filtered_ipv6_list.append(each)
        return filtered_ipv6_list
    except socket.error:
        module.fail_json(msg="Incorrect IPV6 address!")


def new_dict_to_set(input_dict, temp_list, test_set, count=0):
    # recursive function to convert input dict to set for comparision
    test_dict = dict()
    if isinstance(input_dict, dict):
        input_dict_len = len(input_dict)
        for k, v in sorted(iteritems(input_dict)):
            count += 1
            if isinstance(v, list):
                temp_list.append(k)
                for each in v:
                    if isinstance(each, dict):
                        if [True for i in each.values() if type(i) == list]:
                            new_dict_to_set(each, temp_list, test_set, count)
                        else:
                            new_dict_to_set(each, temp_list, test_set, 0)
            else:
                if v is not None:
                    test_dict.update({k: v})
                try:
                    if (
                        tuple(iteritems(test_dict)) not in test_set
                        and count == input_dict_len
                    ):
                        test_set.add(tuple(iteritems(test_dict)))
                        count = 0
                except TypeError:
                    temp_dict = {}

                    def expand_dict(dict_to_expand):
                        temp = dict()
                        for k, v in iteritems(dict_to_expand):
                            if isinstance(v, dict):
                                expand_dict(v)
                            else:
                                if v is not None:
                                    temp.update({k: v})
                                temp_dict.update(tuple(iteritems(temp)))

                    new_dict = {k: v}
                    expand_dict(new_dict)
                    if tuple(iteritems(temp_dict)) not in test_set:
                        test_set.add(tuple(iteritems(temp_dict)))


def dict_to_set(sample_dict):
    # Generate a set with passed dictionary for comparison
    test_dict = dict()
    if isinstance(sample_dict, dict):
        for k, v in iteritems(sample_dict):
            if v is not None:
                if isinstance(v, list):
                    if isinstance(v[0], dict):
                        li = []
                        for each in v:
                            for key, value in iteritems(each):
                                if isinstance(value, list):
                                    each[key] = tuple(value)
                            li.append(tuple(iteritems(each)))
                        v = tuple(li)
                    else:
                        v = tuple(v)
                elif isinstance(v, dict):
                    li = []
                    for key, value in iteritems(v):
                        if isinstance(value, list):
                            v[key] = tuple(value)
                    li.extend(tuple(iteritems(v)))
                    v = tuple(li)
                test_dict.update({k: v})
        return_set = set(tuple(iteritems(test_dict)))
    else:
        return_set = set(sample_dict)
    return return_set


def filter_dict_having_none_value(want, have):
    # Generate dict with have dict value which is None in want dict
    test_dict = dict()
    name = want.get("name")
    if name:
        test_dict["name"] = name
    diff_ip = False
    for k, v in iteritems(want):
        if isinstance(v, dict):
            for key, value in iteritems(v):
                test_key_dict = dict()
                if value is None:
                    if have.get(k):
                        dict_val = have.get(k).get(key)
                        test_key_dict.update({key: dict_val})
                elif (
                    k == "ipv6"
                    and value.lower() != have.get(k)[0].get(key).lower()
                ):
                    # as multiple IPV6 address can be configured on same
                    # interface, for replace state in place update will
                    # actually create new entry, which isn't as expected
                    # for replace state, so in case of IPV6 address
                    # every time 1st delete the existing IPV6 config and
                    # then apply the new change
                    dict_val = have.get(k)[0].get(key)
                    test_key_dict.update({key: dict_val})
                if test_key_dict:
                    test_dict.update({k: test_key_dict})
        if isinstance(v, list):
            for key, value in iteritems(v[0]):
                test_key_dict = dict()
                if value is None:
                    if have.get(k) and key in have.get(k):
                        dict_val = have.get(k)[0].get(key)
                        test_key_dict.update({key: dict_val})
                elif have.get(k):
                    if (
                        k == "ipv6"
                        and value.lower() != have.get(k)[0].get(key).lower()
                    ):
                        dict_val = have.get(k)[0].get(key)
                        test_key_dict.update({key: dict_val})
                if test_key_dict:
                    test_dict.update({k: test_key_dict})
            # below conditions checks are added to check if
            # secondary IP is configured, if yes then delete
            # the already configured IP if want and have IP
            # is different else if it's same no need to delete
            for each in v:
                if each.get("secondary"):
                    want_ip = each.get("address").split("/")
                    have_ip = have.get("ipv4")
                    if (
                        len(want_ip) > 1
                        and have_ip
                        and have_ip[0].get("secondary")
                    ):
                        have_ip = have_ip[0]["address"].split(" ")[0]
                        if have_ip != want_ip[0]:
                            diff_ip = True
                    if each.get("secondary") and diff_ip is True:
                        test_key_dict.update({"secondary": True})
                    test_dict.update({"ipv4": test_key_dict})
        if v is None:
            val = have.get(k)
            test_dict.update({k: val})
    return test_dict


def remove_duplicate_interface(commands):
    # Remove duplicate interface from commands
    set_cmd = []
    for each in commands:
        if "interface" in each:
            if each not in set_cmd:
                set_cmd.append(each)
        else:
            set_cmd.append(each)

    return set_cmd


def validate_ipv4(value, module):
    if value:
        address = value.split("/")
        if len(address) != 2:
            module.fail_json(
                msg="address format is <ipv4 address>/<mask>, got invalid format {0}".format(
                    value
                )
            )

        if not is_masklen(address[1]):
            module.fail_json(
                msg="invalid value for mask: {0}, mask should be in range 0-32".format(
                    address[1]
                )
            )


def validate_ipv6(value, module):
    if value:
        address = value.split("/")
        if len(address) != 2:
            module.fail_json(
                msg="address format is <ipv6 address>/<mask>, got invalid format {0}".format(
                    value
                )
            )
        else:
            if not 0 <= int(address[1]) <= 128:
                module.fail_json(
                    msg="invalid value for mask: {0}, mask should be in range 0-128".format(
                        address[1]
                    )
                )


def validate_n_expand_ipv4(module, want):
    # Check if input IPV4 is valid IP and expand IPV4 with its subnet mask
    ip_addr_want = want.get("address")
    if len(ip_addr_want.split(" ")) > 1:
        return ip_addr_want
    validate_ipv4(ip_addr_want, module)
    ip = ip_addr_want.split("/")
    if len(ip) == 2:
        ip_addr_want = "{0} {1}".format(ip[0], to_netmask(ip[1]))

    return ip_addr_want


def netmask_to_cidr(netmask):
    # convert netmask to cidr and returns the cidr notation
    return str(sum([bin(int(x)).count("1") for x in netmask.split(".")]))


def normalize_interface(name):
    """Return the normalized interface name
    """
    if not name:
        return

    def _get_number(name):
        digits = ""
        for char in name:
            if char.isdigit() or char in "/.":
                digits += char
        return digits

    if name.lower().startswith("gi"):
        if_type = "GigabitEthernet"
    elif name.lower().startswith("te"):
        if_type = "TenGigabitEthernet"
    elif name.lower().startswith("fa"):
        if_type = "FastEthernet"
    elif name.lower().startswith("fo"):
        if_type = "FortyGigabitEthernet"
    elif name.lower().startswith("long"):
        if_type = "LongReachEthernet"
    elif name.lower().startswith("et"):
        if_type = "Ethernet"
    elif name.lower().startswith("vl"):
        if_type = "Vlan"
    elif name.lower().startswith("lo"):
        if_type = "loopback"
    elif name.lower().startswith("po"):
        if_type = "Port-channel"
    elif name.lower().startswith("nv"):
        if_type = "nve"
    elif name.lower().startswith("twe"):
        if_type = "TwentyFiveGigE"
    elif name.lower().startswith("hu"):
        if_type = "HundredGigE"
    elif name.lower().startswith("virtual-te"):
        if_type = "Virtual-Template"
    elif name.lower().startswith("tu"):
        if_type = "Tunnel"
    else:
        if_type = None

    number_list = name.split(" ")
    if len(number_list) == 2:
        number = number_list[-1].strip()
    else:
        number = _get_number(name)

    if if_type:
        proper_interface = if_type + number
    else:
        proper_interface = name

    return proper_interface


def get_interface_type(interface):
    """Gets the type of interface
    """

    if interface.upper().startswith("GI"):
        return "GigabitEthernet"
    elif interface.upper().startswith("TE"):
        return "TenGigabitEthernet"
    elif interface.upper().startswith("FA"):
        return "FastEthernet"
    elif interface.upper().startswith("FO"):
        return "FortyGigabitEthernet"
    elif interface.upper().startswith("LON"):
        return "LongReachEthernet"
    elif interface.upper().startswith("ET"):
        return "Ethernet"
    elif interface.upper().startswith("VL"):
        return "Vlan"
    elif interface.upper().startswith("LO"):
        return "loopback"
    elif interface.upper().startswith("PO"):
        return "Port-channel"
    elif interface.upper().startswith("NV"):
        return "nve"
    elif interface.upper().startswith("TWE"):
        return "TwentyFiveGigE"
    elif interface.upper().startswith("HU"):
        return "HundredGigE"
    elif interface.upper().startswith("VIRTUAL-TE"):
        return "Virtual-Template"
    elif interface.upper().startswith("TU"):
        return "Tunnel"
    else:
        return "unknown"
