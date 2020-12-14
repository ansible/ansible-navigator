#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: net_vrf
author: Ricardo Carrillo Cruz (@rcarrillocruz)
short_description: (deprecated, removed after 2022-06-01) Manage VRFs on network devices
description:
- This module provides declarative management of VRFs on network devices.
version_added: 1.0.0
deprecated:
  alternative: Use platform-specific "[netos]_vrf" module
  why: Updated modules released with more functionality
  removed_at_date: '2022-06-01'
extends_documentation_fragment:
- ansible.netcommon.network_agnostic
options:
  name:
    description:
    - Name of the VRF.
  interfaces:
    description:
    - List of interfaces the VRF should be configured on.
  aggregate:
    description: List of VRFs definitions
  purge:
    description:
    - Purge VRFs not defined in the I(aggregate) parameter.
    default: false
  state:
    description:
    - State of the VRF configuration.
    default: present
    choices:
    - present
    - absent

"""

EXAMPLES = """
- name: Create VRF named MANAGEMENT
  ansible.netcommon.net_vrf:
    name: MANAGEMENT

- name: remove VRF named MANAGEMENT
  ansible.netcommon.net_vrf:
    name: MANAGEMENT
    state: absent

- name: Create aggregate of VRFs with purge
  ansible.netcommon.net_vrf:
    aggregate:
    - {name: test4, rd: 1:204}
    - {name: test5, rd: 1:205}
    state: present
    purge: yes

- name: Delete aggregate of VRFs
  ansible.netcommon.net_vrf:
    aggregate:
    - name: test2
    - name: test3
    - name: test4
    - name: test5
    state: absent
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always, except for the platforms that use Netconf transport to manage the device.
  type: list
  sample:
    - vrf definition MANAGEMENT
"""
