#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: net_l2_interface
author: Ganesh Nalawade (@ganeshrn)
short_description: (deprecated, removed after 2022-06-01) Manage Layer-2 interface
  on network devices
description:
- This module provides declarative management of Layer-2 interface on network devices.
version_added: 1.0.0
deprecated:
  alternative: Use platform-specific "[netos]_l2_interfaces" module
  why: Updated modules released with more functionality
  removed_at_date: '2022-06-01'
extends_documentation_fragment:
- ansible.netcommon.network_agnostic
options:
  name:
    description:
    - Name of the interface excluding any logical unit number.
  aggregate:
    description:
    - List of Layer-2 interface definitions.
  mode:
    description:
    - Mode in which interface needs to be configured.
    default: access
    choices:
    - access
    - trunk
  access_vlan:
    description:
    - Configure given VLAN in access port.
  trunk_vlans:
    description:
    - List of VLANs to be configured in trunk port.
  native_vlan:
    description:
    - Native VLAN to be configured in trunk port.
  trunk_allowed_vlans:
    description:
    - List of allowed VLAN's in a given trunk port.
  state:
    description:
    - State of the Layer-2 Interface configuration.
    default: present
    choices:
    - present
    - absent

"""

EXAMPLES = """
- name: configure Layer-2 interface
  ansible.netcommon.net_l2_interface:
    name: gigabitethernet0/0/1
    mode: access
    access_vlan: 30

- name: remove Layer-2 interface configuration
  ansible.netcommon.net_l2_interface:
    name: gigabitethernet0/0/1
    state: absent
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always, except for the platforms that use Netconf transport to manage the device.
  type: list
  sample:
    - interface gigabitethernet0/0/1
    - switchport mode access
    - switchport access vlan 30
"""
