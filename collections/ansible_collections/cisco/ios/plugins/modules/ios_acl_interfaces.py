#!/usr/bin/python
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
#
"""
The module file for ios_acl_interfaces
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = """
module: ios_acl_interfaces
short_description: ACL interfaces resource module
description: This module configures and manages the access-control (ACL) attributes
  of interfaces on IOS platforms.
version_added: 1.0.0
author: Sumit Jaiswal (@justjais)
notes:
- Tested against Cisco IOSv Version 15.2 on VIRL
options:
  config:
    description: A dictionary of ACL interfaces options
    type: list
    elements: dict
    suboptions:
      name:
        description: Full name of the interface excluding any logical unit number,
          i.e. GigabitEthernet0/1.
        type: str
        required: true
      access_groups:
        description: Specify access-group for IP access list (standard or extended).
        type: list
        elements: dict
        suboptions:
          afi:
            description: Specifies the AFI for the ACLs to be configured on this interface.
            type: str
            required: true
            choices:
            - ipv4
            - ipv6
          acls:
            description: Specifies the ACLs for the provided AFI.
            type: list
            elements: dict
            suboptions:
              name:
                description: Specifies the name of the IPv4/IPv4 ACL for the interface.
                type: str
                required: true
              direction:
                description:
                - Specifies the direction of packets that the ACL will be applied
                  on.
                - With one direction already assigned, other acl direction cannot
                  be same.
                type: str
                required: true
                choices:
                - in
                - out
  running_config:
    description:
      - The module, by default, will connect to the remote device and retrieve the current
        running-config to use as a base for comparing against the contents of source.
        There are times when it is not desirable to have the task get the current running-config
        for every task in a playbook.  The I(running_config) argument allows the implementer
        to pass in the configuration to use as the base config for comparison. This
        value of this option should be the output received from device by executing
        command.
    type: str
  state:
    description:
      - The state the configuration should be left in
      - The states I(rendered), I(gathered) and I(parsed) does not perform any change
        on the device.
      - The state I(rendered) will transform the configuration in C(config) option to
        platform specific CLI commands which will be returned in the I(rendered) key
        within the result. For state I(rendered) active connection to remote host is
        not required.
      - The state I(gathered) will fetch the running configuration from device and transform
        it into structured data in the format as per the resource module argspec and
        the value is returned in the I(gathered) key within the result.
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into JSON format as per the resource module parameters and the
        value is returned in the I(parsed) key within the result. The value of C(running_config)
        option should be the same format as the output of command I(show running-config
        | include ip route|ipv6 route) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - gathered
    - parsed
    - rendered
    default: merged
"""
EXAMPLES = """
# Using Merged

# Before state:
# -------------
#
# vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
# interface Loopback888
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
# interface GigabitEthernet0/2
#  ip access-group 123 out

- name: Merge module attributes of given access-groups
  cisco.ios.ios_acl_interfaces:
    config:
    - name: GigabitEthernet0/1
      access_groups:
      - afi: ipv4
        acls:
        - name: 110
          direction: in
        - name: 123
          direction: out
      - afi: ipv6
        acls:
        - name: test_v6
          direction: out
        - name: temp_v6
          direction: in
    - name: GigabitEthernet0/2
      access_groups:
      - afi: ipv4
        acls:
        - name: 100
          direction: in
    state: merged

# Commands Fired:
# ---------------
#
# interface GigabitEthernet0/1
#  ip access-group 110 in
#  ip access-group 123 out
#  ipv6 traffic-filter test_v6 out
#  ipv6 traffic-filter temp_v6 in
# interface GigabitEthernet0/2
#  ip access-group 100 in
#  ip access-group 123 out


# After state:
# -------------
#
# vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
# interface Loopback888
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip access-group 110 in
#  ip access-group 123 out
#  ipv6 traffic-filter test_v6 out
#  ipv6 traffic-filter temp_v6 in
# interface GigabitEthernet0/2
#  ip access-group 110 in
#  ip access-group 123 out

# Using Replaced

# Before state:
# -------------
#
# vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
# interface Loopback888
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip access-group 110 in
#  ip access-group 123 out
#  ipv6 traffic-filter test_v6 out
#  ipv6 traffic-filter temp_v6 in
# interface GigabitEthernet0/2
#  ip access-group 110 in
#  ip access-group 123 out

- name: Replace module attributes of given access-groups
  cisco.ios.ios_acl_interfaces:
    config:
    - name: GigabitEthernet0/1
      access_groups:
      - afi: ipv4
        acls:
        - name: 100
          direction: out
        - name: 110
          direction: in
    state: replaced

# Commands Fired:
# ---------------
#
# interface GigabitEthernet0/1
# no ip access-group 123 out
# no ipv6 traffic-filter temp_v6 in
# no ipv6 traffic-filter test_v6 out
# ip access-group 100 out

# After state:
# -------------
#
# vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
# interface Loopback888
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip access-group 100 out
#  ip access-group 110 in
# interface GigabitEthernet0/2
#  ip access-group 110 in
#  ip access-group 123 out

# Using Overridden

# Before state:
# -------------
#
# vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
# interface Loopback888
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip access-group 110 in
#  ip access-group 123 out
#  ipv6 traffic-filter test_v6 out
#  ipv6 traffic-filter temp_v6 in
# interface GigabitEthernet0/2
#  ip access-group 110 in
#  ip access-group 123 out

- name: Overridden module attributes of given access-groups
  cisco.ios.ios_acl_interfaces:
    config:
    - name: GigabitEthernet0/1
      access_groups:
      - afi: ipv4
        acls:
        - name: 100
          direction: out
        - name: 110
          direction: in
    state: overridden

# Commands Fired:
# ---------------
#
# interface GigabitEthernet0/1
# no ip access-group 123 out
# no ipv6 traffic-filter test_v6 out
# no ipv6 traffic-filter temp_v6 in
# ip access-group 100 out
# interface GigabitEthernet0/2
# no ip access-group 110 in
# no ip access-group 123 out

# After state:
# -------------
#
# vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
# interface Loopback888
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip access-group 100 out
#  ip access-group 110 in
# interface GigabitEthernet0/2

# Using Deleted

# Before state:
# -------------
#
# vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
# interface Loopback888
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip access-group 110 in
#  ip access-group 123 out
#  ipv6 traffic-filter test_v6 out
#  ipv6 traffic-filter temp_v6 in
# interface GigabitEthernet0/2
#  ip access-group 110 in
#  ip access-group 123 out

- name: Delete module attributes of given Interface
  cisco.ios.ios_acl_interfaces:
    config:
    - name: GigabitEthernet0/1
    state: deleted

# Commands Fired:
# ---------------
#
# interface GigabitEthernet0/1
# no ip access-group 110 in
# no ip access-group 123 out
# no ipv6 traffic-filter test_v6 out
# no ipv6 traffic-filter temp_v6 in

# After state:
# -------------
#
# vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
# interface Loopback888
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
# interface GigabitEthernet0/2
#  ip access-group 110 in
#  ip access-group 123 out

# Using DELETED without any config passed
#"(NOTE: This will delete all of configured resource module attributes from each configured interface)"

# Before state:
# -------------
#
# vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
# interface Loopback888
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip access-group 110 in
#  ip access-group 123 out
#  ipv6 traffic-filter test_v6 out
#  ipv6 traffic-filter temp_v6 in
# interface GigabitEthernet0/2
#  ip access-group 110 in
#  ip access-group 123 out

- name: Delete module attributes of given access-groups from ALL Interfaces
  cisco.ios.ios_acl_interfaces:
    config:
    state: deleted

# Commands Fired:
# ---------------
#
# interface GigabitEthernet0/1
# no ip access-group 110 in
# no ip access-group 123 out
# no ipv6 traffic-filter test_v6 out
# no ipv6 traffic-filter temp_v6 in
# interface GigabitEthernet0/2
# no ip access-group 110 out
# no ip access-group 123 out

# After state:
# -------------
#
# vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
# interface Loopback888
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
# interface GigabitEthernet0/2

# Using Gathered

# Before state:
# -------------
#
# vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
# interface Loopback888
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip access-group 110 in
#  ip access-group 123 out
#  ipv6 traffic-filter test_v6 out
#  ipv6 traffic-filter temp_v6 in
# interface GigabitEthernet0/2
#  ip access-group 110 in
#  ip access-group 123 out

- name: Gather listed acl interfaces with provided configurations
  cisco.ios.ios_acl_interfaces:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": [
#         {
#             "name": "Loopback888"
#         },
#         {
#             "name": "GigabitEthernet0/0"
#         },
#         {
#             "access_groups": [
#                 {
#                     "acls": [
#                         {
#                             "direction": "in",
#                             "name": "110"
#                         },
#                         {
#                             "direction": "out",
#                             "name": "123"
#                         }
#                     ],
#                     "afi": "ipv4"
#                 },
#                 {
#                     "acls": [
#                         {
#                             "direction": "in",
#                             "name": "temp_v6"
#                         },
#                         {
#                             "direction": "out",
#                             "name": "test_v6"
#                         }
#                     ],
#                     "afi": "ipv6"
#                 }
#             ],
#             "name": "GigabitEthernet0/1"
#         },
#         {
#             "access_groups": [
#                 {
#                     "acls": [
#                         {
#                             "direction": "in",
#                             "name": "100"
#                         },
#                         {
#                             "direction": "out",
#                             "name": "123"
#                         }
#                     ],
#                     "afi": "ipv4"
#                 }
#             ],
#             "name": "GigabitEthernet0/2"
#         }
#     ]

# After state:
# ------------
#
# vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
# interface Loopback888
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  ip access-group 110 in
#  ip access-group 123 out
#  ipv6 traffic-filter test_v6 out
#  ipv6 traffic-filter temp_v6 in
# interface GigabitEthernet0/2
#  ip access-group 110 in
#  ip access-group 123 out

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_acl_interfaces:
    config:
    - name: GigabitEthernet0/1
      access_groups:
      - afi: ipv4
        acls:
        - name: 110
          direction: in
        - name: 123
          direction: out
      - afi: ipv6
        acls:
        - name: test_v6
          direction: out
        - name: temp_v6
          direction: in
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#         "interface GigabitEthernet0/1",
#         "ip access-group 110 in",
#         "ip access-group 123 out",
#         "ipv6 traffic-filter temp_v6 in",
#         "ipv6 traffic-filter test_v6 out"
#     ]

# Using Parsed

# File: parsed.cfg
# ----------------
#
# interface GigabitEthernet0/1
# ip access-group 110 in
# ip access-group 123 out
# ipv6 traffic-filter temp_v6 in
# ipv6 traffic-filter test_v6 out

- name: Parse the commands for provided configuration
  cisco.ios.ios_acl_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#         {
#             "access_groups": [
#                 {
#                     "acls": [
#                         {
#                             "direction": "in",
#                             "name": "110"
#                         }
#                     ],
#                     "afi": "ipv4"
#                 },
#                 {
#                     "acls": [
#                         {
#                             "direction": "in",
#                             "name": "temp_v6"
#                         }
#                     ],
#                     "afi": "ipv6"
#                 }
#             ],
#             "name": "GigabitEthernet0/1"
#         }
#     ]
"""
RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: The configuration returned will always be in the same format of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: The configuration returned will always be in the same format of the parameters above.
commands:
  description: The set of commands pushed to the remote device
  returned: always
  type: list
  sample: ['interface GigabitEthernet0/1', 'ip access-group 110 in', 'ipv6 traffic-filter test_v6 out']
"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.acl_interfaces.acl_interfaces import (
    Acl_InterfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.acl_interfaces.acl_interfaces import (
    Acl_Interfaces,
)


def main():
    """
    Main entry point for module execution
    :returns: the result form module invocation
    """
    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "overridden", ("config",)),
        ("state", "rendered", ("config",)),
        ("state", "parsed", ("running_config",)),
    ]
    mutually_exclusive = [("config", "running_config")]
    module = AnsibleModule(
        argument_spec=Acl_InterfacesArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    result = Acl_Interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
