#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: net_banner
author: Ricardo Carrillo Cruz (@rcarrillocruz)
short_description: (deprecated, removed after 2022-06-01) Manage multiline banners
  on network devices
description:
- This will configure both login and motd banners on network devices. It allows playbooks
  to add or remove banner text from the active running configuration.
version_added: 1.0.0
deprecated:
  alternative: Use platform-specific "[netos]_banner" module
  why: Updated modules released with more functionality
  removed_at_date: '2022-06-01'
extends_documentation_fragment:
- ansible.netcommon.network_agnostic
options:
  banner:
    description:
    - Specifies which banner that should be configured on the remote device.
    required: true
    choices:
    - login
    - motd
  text:
    description:
    - The banner text that should be present in the remote device running configuration.  This
      argument accepts a multiline string, with no empty lines. Requires I(state=present).
  state:
    description:
    - Specifies whether or not the configuration is present in the current devices
      active running configuration.
    default: present
    choices:
    - present
    - absent

"""

EXAMPLES = """
- name: configure the login banner
  ansible.netcommon.net_banner:
    banner: login
    text: |
      this is my login banner
      that contains a multiline
      string
    state: present

- name: remove the motd banner
  ansible.netcommon.net_banner:
    banner: motd
    state: absent

- name: Configure banner from file
  ansible.netcommon.net_banner:
    banner: motd
    text: "{{ lookup('file', './config_partial/raw_banner.cfg') }}"
    state: present

"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always, except for the platforms that use Netconf transport to manage the device.
  type: list
  sample:
    - banner login
    - this is my login banner
    - that contains a multiline
    - string
"""
