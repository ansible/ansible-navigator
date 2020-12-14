#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: net_system
author: Ricardo Carrillo Cruz (@rcarrillocruz)
short_description: (deprecated, removed after 2022-06-01) Manage the system attributes
  on network devices
description:
- This module provides declarative management of node system attributes on network
  devices.  It provides an option to configure host system parameters or remove those
  parameters from the device active configuration.
version_added: 1.0.0
deprecated:
  alternative: Use platform-specific "[netos]_system" module
  why: Updated modules released with more functionality
  removed_at_date: '2022-06-01'
extends_documentation_fragment:
- ansible.netcommon.network_agnostic
options:
  hostname:
    description:
    - Configure the device hostname parameter. This option takes an ASCII string value.
  domain_name:
    description:
    - Configure the IP domain name on the remote device to the provided value. Value
      should be in the dotted name form and will be appended to the C(hostname) to
      create a fully-qualified domain name.
  domain_search:
    description:
    - Provides the list of domain suffixes to append to the hostname for the purpose
      of doing name resolution. This argument accepts a name or list of names and
      will be reconciled with the current active configuration on the running node.
  lookup_source:
    description:
    - Provides one or more source interfaces to use for performing DNS lookups.  The
      interface provided in C(lookup_source) must be a valid interface configured
      on the device.
  name_servers:
    description:
    - List of DNS name servers by IP address to use to perform name resolution lookups.  This
      argument accepts either a list of DNS servers See examples.
  state:
    description:
    - State of the configuration values in the device's current active configuration.  When
      set to I(present), the values should be configured in the device active configuration
      and when set to I(absent) the values should not be in the device active configuration
    default: present
    choices:
    - present
    - absent

"""

EXAMPLES = """
- name: configure hostname and domain name
  ansible.netcommon.net_system:
    hostname: ios01
    domain_name: test.example.com
    domain_search:
    - ansible.com
    - redhat.com
    - cisco.com

- name: domain search on single domain
  ansible.netcommon.net_system:
    domain_search: ansible.com

- name: remove configuration
  ansible.netcommon.net_system:
    state: absent

- name: configure DNS lookup sources
  ansible.netcommon.net_system:
    lookup_source: MgmtEth0/0/CPU0/0

- name: configure name servers
  ansible.netcommon.net_system:
    name_servers:
    - 8.8.8.8
    - 8.8.4.4
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always, except for the platforms that use Netconf transport to manage the device.
  type: list
  sample:
    - hostname ios01
    - ip domain name test.example.com
"""
