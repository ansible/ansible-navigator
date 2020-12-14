# -*- coding: utf-8 -*-
#
# (c) 2017 Red Hat, Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from copy import deepcopy

from ansible_collections.ansible.netcommon.tests.unit.compat.mock import (
    MagicMock,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible.module_utils.common.network import (
    to_masklen,
    to_netmask,
    to_subnet,
    to_ipv6_network,
    to_ipv6_subnet,
    is_masklen,
    is_netmask,
)


def test_to_list():
    for scalar in ("string", 1, True, False, None):
        assert isinstance(utils.to_list(scalar), list)

    for container in ([1, 2, 3], {"one": 1}):
        assert isinstance(utils.to_list(container), list)

    test_list = [1, 2, 3]
    assert id(test_list) != id(utils.to_list(test_list))


def test_to_lines():
    expected_output = [
        [
            "! Command: show running-config",
            "! device: veos23 (vEOS, EOS-4.23.3M)",
            "!",
            "! boot system flash:/vEOS-lab-4.23.3M.swi",
            "!",
            "transceiver qsfp default-mode 4x10G",
            "!",
            "interface Management1",
            "   ip address dhcp",
            "!",
            "end",
        ]
    ]
    assert expected_output == list(utils.to_lines(expected_output))

    stdout = ["\n".join(expected_output[0])]
    assert expected_output == list(utils.to_lines(stdout))


def test_transform_commands():
    module = MagicMock()

    module.params = {"commands": ["show interfaces"]}
    transformed = utils.transform_commands(module)
    assert transformed == [
        {
            "answer": None,
            "check_all": False,
            "command": "show interfaces",
            "newline": True,
            "output": None,
            "prompt": None,
            "sendonly": False,
        }
    ]

    module.params = {"commands": ["show version", "show memory"]}
    transformed = utils.transform_commands(module)
    assert transformed == [
        {
            "answer": None,
            "check_all": False,
            "command": "show version",
            "newline": True,
            "output": None,
            "prompt": None,
            "sendonly": False,
        },
        {
            "answer": None,
            "check_all": False,
            "command": "show memory",
            "newline": True,
            "output": None,
            "prompt": None,
            "sendonly": False,
        },
    ]

    module.params = {
        "commands": [
            {"command": "show version", "output": "json"},
            "show memory",
        ]
    }
    transformed = utils.transform_commands(module)
    assert transformed == [
        {
            "answer": None,
            "check_all": False,
            "command": "show version",
            "newline": True,
            "output": "json",
            "prompt": None,
            "sendonly": False,
        },
        {
            "answer": None,
            "check_all": False,
            "command": "show memory",
            "newline": True,
            "output": None,
            "prompt": None,
            "sendonly": False,
        },
    ]


def test_sort_list():
    data = [3, 1, 2]
    assert [1, 2, 3] == utils.sort_list(data)

    string_data = "312"
    assert string_data == utils.sort_list(string_data)

    data = [{"a": 1, "b": 2}, {"a": 1, "c": 1}, {"a": 1, "b": 0}]
    with pytest.raises(ValueError, match="dictionaries do not match"):
        utils.sort_list(data)

    data = [{"a": 1, "b": 2}, {"a": 1, "b": 1}, {"a": 0, "b": 3}]
    assert utils.sort_list(data) == [
        {"a": 0, "b": 3},
        {"a": 1, "b": 1},
        {"a": 1, "b": 2},
    ]

    data = [
        {"a": 1, "c": [1, 2, 3], "b": 1},
        {"a": 1, "c": [3, 4, 5], "b": 0},
        {"a": 1, "c": [1, 1], "b": 0},
        {"a": 0, "c": [99, 98, 97, 96, 95], "b": 27},
    ]
    assert utils.sort_list(data) == [
        {"a": 0, "b": 27, "c": [99, 98, 97, 96, 95]},
        {"a": 1, "b": 0, "c": [1, 1]},
        {"a": 1, "b": 0, "c": [3, 4, 5]},
        {"a": 1, "b": 1, "c": [1, 2, 3]},
    ]


def test_dict_diff():
    with pytest.raises(AssertionError, match="`base` must be of type <dict>"):
        utils.dict_diff(None, {})

    with pytest.raises(
        AssertionError, match="`comparable` must be of type <dict>"
    ):
        utils.dict_diff({}, object())

    # But None is okay
    assert utils.dict_diff({}, None) == {}

    base = dict(
        obj2=dict(),
        b1=True,
        b2=False,
        b3=False,
        one=1,
        two=2,
        three=3,
        obj1=dict(key1=1, key2=2),
        l1=[1, 3],
        l2=[1, 2, 3],
        l4=[4],
        nested=dict(n1=dict(n2=2)),
    )

    other = dict(
        b1=True,
        b2=False,
        b3=True,
        b4=True,
        one=1,
        three=4,
        four=4,
        obj1=dict(key1=2),
        l1=[2, 1],
        l2=[3, 2, 1],
        l3=[1],
        nested=dict(n1=dict(n2=2, n3=3)),
    )

    result = utils.dict_diff(base, other)

    # string assertions
    assert "one" not in result
    assert "two" not in result
    assert result["three"] == 4
    assert result["four"] == 4

    # dict assertions
    assert "obj1" in result
    assert "key1" in result["obj1"]
    assert "key2" not in result["obj1"]

    # list assertions
    assert result["l1"] == [2, 1]
    assert "l2" not in result
    assert result["l3"] == [1]
    assert "l4" not in result

    # nested assertions
    assert "obj1" in result
    assert result["obj1"]["key1"] == 2
    assert "key2" not in result["obj1"]

    # bool assertions
    assert "b1" not in result
    assert "b2" not in result
    assert result["b3"]
    assert result["b4"]


def test_dict_merge():
    with pytest.raises(AssertionError, match="`base` must be of type <dict>"):
        utils.dict_merge(None, {})

    with pytest.raises(AssertionError, match="`other` must be of type <dict>"):
        utils.dict_merge({}, None)

    base = dict(
        obj2=dict(),
        b1=True,
        b2=False,
        b3=False,
        one=1,
        two=2,
        three=3,
        obj1=dict(key1=1, key2=2),
        l1=[1, 3],
        l2=[1, 2, 3],
        l4=[4],
        nested=dict(n1=dict(n2=2)),
    )

    other = dict(
        b1=True,
        b2=False,
        b3=True,
        b4=True,
        one=1,
        three=4,
        four=4,
        obj1=dict(key1=2),
        obj2=None,
        l1=[2, 1],
        l2=[3, 2, 1],
        l3=[1],
        l4=None,
        nested=dict(n1=dict(n2=2, n3=3)),
    )

    result = utils.dict_merge(base, other)

    # string assertions
    assert "one" in result
    assert "two" in result
    assert result["three"] == 4
    assert result["four"] == 4

    # dict assertions
    assert "obj1" in result
    assert "key1" in result["obj1"]
    assert "key2" in result["obj1"]

    # list assertions
    assert result["l1"] == [1, 2, 3]
    assert "l2" in result
    assert result["l3"] == [1]
    assert "l4" in result

    # nested assertions
    assert "obj1" in result
    assert result["obj1"]["key1"] == 2
    assert "key2" in result["obj1"]

    # bool assertions
    assert "b1" in result
    assert "b2" in result
    assert result["b3"]
    assert result["b4"]


def test_param_list_to_dict():
    params = [
        dict(name="interface1", mtu=1400),
        dict(name="interface2", speed="10G"),
        dict(name="interface3"),
    ]
    assert utils.param_list_to_dict(params) == {
        "interface1": dict(mtu=1400),
        "interface2": dict(speed="10G"),
        "interface3": dict(),
    }

    params = [
        dict(vlan_id=1, name="management"),
        dict(vlan_id=10, name="voice"),
        dict(vlan_id=99, name="guest"),
    ]
    assert utils.param_list_to_dict(
        params, unique_key="vlan_id", remove_key=False
    ) == {
        1: dict(vlan_id=1, name="management"),
        10: dict(vlan_id=10, name="voice"),
        99: dict(vlan_id=99, name="guest"),
    }


def test_dict_merge_src_unchanged():
    base = {
        "flist": [
            {"dir": "out", "rmap": "rmap_1"},
            {"dir": "in", "rmap": "rmap_2"},
        ]
    }
    basecp = deepcopy(base)
    other = {
        "flist": [
            {"dir": "out", "rmap": "rmap_12"},
            {"dir": "in", "rmap": "rmap_2"},
        ]
    }
    othercp = deepcopy(other)

    utils.dict_merge(base, other)
    # dict_merge() should not modify the source dicts
    assert base == basecp
    assert other == othercp


def test_conditional():
    assert utils.conditional(10, 10)
    assert utils.conditional("10", "10")
    assert utils.conditional("foo", "foo")
    assert utils.conditional(True, True)
    assert utils.conditional(False, False)
    assert utils.conditional(None, None)
    assert utils.conditional("ge(1)", 1)
    assert utils.conditional("gt(1)", 2)
    assert utils.conditional("le(2)", 2)
    assert utils.conditional("lt(3)", 2)
    assert utils.conditional("eq(1)", 1)
    assert utils.conditional("neq(0)", 1)
    assert utils.conditional("min(1)", 1)
    assert utils.conditional("max(1)", 1)
    assert utils.conditional("exactly(1)", 1)
    assert utils.conditional("gt(5)", "7", int)
    with pytest.raises(
        AssertionError, match="invalid expression: cannot contain spaces"
    ):
        utils.conditional("1 ", 1)
    with pytest.raises(ValueError, match="unknown operator: floop"):
        utils.conditional("floop(4)", 4)


def test_ternary():
    is_true = (True, False)
    assert utils.ternary(True, *is_true)
    assert utils.ternary(10, *is_true)
    assert utils.ternary(object(), *is_true)

    is_false = (False, True)
    assert utils.ternary(False, *is_false)
    assert utils.ternary(0, *is_false)
    assert utils.ternary(None, *is_false)


def test_load_provider():
    spec = dict(
        host=dict(),
        port=dict(type=int, default=80),
        user=dict(),
        password=dict(),
        authorize=dict(),
    )
    args = dict(provider=dict(user="ansible", authorize="yes"))
    provider = utils.load_provider(spec, args)
    assert provider["user"] == "ansible"
    assert provider["port"] == 80
    assert provider["authorize"] is True


def test_template():
    tmpl = utils.Template()
    assert "foo" == tmpl("{{ test }}", {"test": "foo"})


def test_to_masklen():
    assert 24 == to_masklen("255.255.255.0")


def test_to_masklen_invalid():
    with pytest.raises(ValueError):
        to_masklen("255")


def test_to_netmask():
    assert "255.0.0.0" == to_netmask(8)
    assert "255.0.0.0" == to_netmask("8")


def test_to_netmask_invalid():
    with pytest.raises(ValueError):
        to_netmask(128)


def test_to_subnet():
    result = to_subnet("192.168.1.1", 24)
    assert "192.168.1.0/24" == result

    result = to_subnet("192.168.1.1", 24, dotted_notation=True)
    assert "192.168.1.0 255.255.255.0" == result


def test_to_subnet_invalid():
    with pytest.raises(ValueError):
        to_subnet("foo", "bar")


def test_is_masklen():
    assert is_masklen(32)
    assert not is_masklen(33)
    assert not is_masklen("foo")


def test_is_netmask():
    assert is_netmask("255.255.255.255")
    assert not is_netmask(24)
    assert not is_netmask("foo")


def test_to_ipv6_network():
    assert "2001:db8::" == to_ipv6_network("2001:db8::")
    assert "2001:0db8:85a3::" == to_ipv6_network(
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    )
    assert "2001:0db8:85a3::" == to_ipv6_network(
        "2001:0db8:85a3:0:0:8a2e:0370:7334"
    )


def test_to_ipv6_subnet():
    assert "2001:db8::" == to_ipv6_subnet("2001:db8::")
    assert "2001:0db8:85a3:4242::" == to_ipv6_subnet(
        "2001:0db8:85a3:4242:0000:8a2e:0370:7334"
    )
    assert "2001:0db8:85a3:4242::" == to_ipv6_subnet(
        "2001:0db8:85a3:4242:0:8a2e:0370:7334"
    )
