#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: net_vlan
author: Ricardo Carrillo Cruz (@rcarrillocruz)
short_description: (deprecated, removed after 2022-06-01) Manage VLANs on network
  devices
description:
- This module provides declarative management of VLANs on network devices.
version_added: 1.0.0
deprecated:
  alternative: Use platform-specific "[netos]_vlans" module
  why: Updated modules released with more functionality
  removed_at_date: '2022-06-01'
extends_documentation_fragment:
- ansible.netcommon.network_agnostic
options:
  name:
    description:
    - Name of the VLAN.
  vlan_id:
    description:
    - ID of the VLAN.
  interfaces:
    description:
    - List of interfaces the VLAN should be configured on.
  aggregate:
    description: List of VLANs definitions.
  purge:
    description:
    - Purge VLANs not defined in the I(aggregate) parameter.
    default: false
  state:
    description:
    - State of the VLAN configuration.
    default: present
    choices:
    - present
    - absent
    - active
    - suspend

"""

EXAMPLES = """
- name: configure VLAN ID and name
  ansible.netcommon.net_vlan:
    vlan_id: 20
    name: test-vlan

- name: remove configuration
  ansible.netcommon.net_vlan:
    state: absent

- name: configure VLAN state
  ansible.netcommon.net_vlan:
    vlan_id:
    state: suspend

"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always, except for the platforms that use Netconf transport to manage the device.
  type: list
  sample:
    - vlan 20
    - name test-vlan
"""
