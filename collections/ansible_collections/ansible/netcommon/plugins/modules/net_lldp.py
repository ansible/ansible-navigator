#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: net_lldp
author: Ricardo Carrillo Cruz (@rcarrillocruz)
short_description: (deprecated, removed after 2022-06-01) Manage LLDP service configuration
  on network devices
description:
- This module provides declarative management of LLDP service configuration on network
  devices.
version_added: 1.0.0
deprecated:
  alternative: Use platform-specific "[netos]_lldp_global" module
  why: Updated modules released with more functionality
  removed_at_date: '2022-06-01'
extends_documentation_fragment:
- ansible.netcommon.network_agnostic
options:
  state:
    description:
    - State of the LLDP service configuration.
    default: present
    choices:
    - present
    - absent

"""

EXAMPLES = """
- name: Enable LLDP service
  ansible.netcommon.net_lldp:
    state: present

- name: Disable LLDP service
  ansible.netcommon.net_lldp:
    state: absent
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always, except for the platforms that use Netconf transport to manage the device.
  type: list
  sample:
    - set service lldp
"""
