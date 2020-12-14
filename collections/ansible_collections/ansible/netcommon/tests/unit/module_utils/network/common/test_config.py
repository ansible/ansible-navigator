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

import re

import pytest

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    config,
)


RUNNING = """interface Ethernet1
   speed auto
   no switchport
   no lldp receive
!
interface Ethernet2
   speed auto
   no switchport
   no lldp transmit
!
interface Management1
   ip address dhcp
!"""


def test_config_items():
    net_config = config.NetworkConfig(indent=3, contents=RUNNING)
    assert len(net_config.items) == 10

    net_config = config.NetworkConfig(
        indent=3, contents=RUNNING, ignore_lines=[r"\s*no .*"]
    )
    assert len(net_config.items) == 6

    net_config = config.NetworkConfig(
        indent=3, contents=RUNNING, ignore_lines=[re.compile(r"\s*no .*")]
    )
    assert len(net_config.items) == 6


def test_config_get_block():
    net_config = config.NetworkConfig(indent=3, contents=RUNNING)

    with pytest.raises(
        AssertionError, match="path argument must be a list object"
    ):
        net_config.get_block("interface Ethernet2")

    with pytest.raises(ValueError, match="path does not exist in config"):
        net_config.get_block(["interface Ethernet3"])

    block = net_config.get_block(["interface Ethernet2"])
    assert len(block) == 4


def test_line_hierarchy():
    net_config = config.NetworkConfig(indent=3, contents=RUNNING)

    lines = net_config.items
    assert lines[0].has_children
    assert not lines[0].has_parents
    assert not lines[1].has_children
    assert lines[1].has_parents
