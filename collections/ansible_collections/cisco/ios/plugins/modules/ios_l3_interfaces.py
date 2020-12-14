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
The module file for ios_l3_interfaces
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: ios_l3_interfaces
short_description: L3 interfaces resource module
description:
- This module provides declarative management of Layer-3 interface on Cisco IOS devices.
version_added: 1.0.0
author: Sumit Jaiswal (@justjais)
notes:
- Tested against Cisco IOSv Version 15.2 on VIRL.
options:
  config:
    description: A dictionary of Layer-3 interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of the interface excluding any logical unit number, i.e. GigabitEthernet0/1.
        type: str
        required: true
      ipv4:
        description:
        - IPv4 address to be set for the Layer-3 interface mentioned in I(name) option.
          The address format is <ipv4 address>/<mask>, the mask is number in range
          0-32 eg. 192.168.0.1/24.
        type: list
        elements: dict
        suboptions:
          address:
            description:
            - Configures the IPv4 address for Interface.
            type: str
          secondary:
            description:
            - Configures the IP address as a secondary address.
            type: bool
          dhcp_client:
            description:
            - Configures and specifies client-id to use over DHCP ip. Note, This option
              shall work only when dhcp is configured as IP.
            - GigabitEthernet interface number
            type: int
          dhcp_hostname:
            description:
            - Configures and specifies value for hostname option over DHCP ip. Note,
              This option shall work only when dhcp is configured as IP.
            type: str
      ipv6:
        description:
        - IPv6 address to be set for the Layer-3 interface mentioned in I(name) option.
        - The address format is <ipv6 address>/<mask>, the mask is number in range
          0-128 eg. fd5d:12c9:2201:1::1/64
        type: list
        elements: dict
        suboptions:
          address:
            description:
            - Configures the IPv6 address for Interface.
            type: str
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device
        by executing the command B(show running-config | section ^interface).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - rendered
    - gathered
    - parsed
    default: merged
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
        option should be the same format as the output of command
        I(show running-config | section ^interface) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str

"""

EXAMPLES = """
# Using merged
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  ip address 10.1.1.1 255.255.255.0
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  no ip address
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20

- name: Merge provided configuration with device configuration
  cisco.ios.ios_l3_interfaces:
    config:
    - name: GigabitEthernet0/1
      ipv4:
      - address: 192.168.0.1/24
        secondary: true
    - name: GigabitEthernet0/2
      ipv4:
      - address: 192.168.0.2/24
    - name: GigabitEthernet0/3
      ipv6:
      - address: fd5d:12c9:2201:1::1/64
    - name: GigabitEthernet0/3.100
      ipv4:
      - address: 192.168.0.3/24
    state: merged

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  ip address 10.1.1.1 255.255.255.0
#  ip address 192.168.0.1 255.255.255.0 secondary
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  ip address 192.168.0.2 255.255.255.0
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ip address 192.168.0.3 255.255.255.0

# Using replaced
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  ip address 10.1.1.1 255.255.255.0
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  ip address 192.168.2.0 255.255.255.0
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ip address 192.168.0.2 255.255.255.0

- name: Replaces device configuration of listed interfaces with provided configuration
  cisco.ios.ios_l3_interfaces:
    config:
    - name: GigabitEthernet0/2
      ipv4:
      - address: 192.168.2.0/24
    - name: GigabitEthernet0/3
      ipv4:
      - address: dhcp
        dhcp_client: 2
        dhcp_hostname: test.com
    - name: GigabitEthernet0/3.100
      ipv4:
      - address: 192.168.0.3/24
        secondary: true
    state: replaced

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  ip address 10.1.1.1 255.255.255.0
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  ip address 192.168.2.1 255.255.255.0
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  ip address dhcp client-id GigabitEthernet0/2 hostname test.com
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ip address 192.168.0.2 255.255.255.0
#  ip address 192.168.0.3 255.255.255.0 secondary

# Using overridden
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  ip address 10.1.1.1 255.255.255.0
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  ip address 192.168.2.1 255.255.255.0
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ip address 192.168.0.2 255.255.255.0

- name: Override device configuration of all interfaces with provided configuration
  cisco.ios.ios_l3_interfaces:
    config:
    - name: GigabitEthernet0/2
      ipv4:
      - address: 192.168.0.1/24
    - name: GigabitEthernet0/3.100
      ipv6:
      - address: autoconfig
    state: overridden

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  ip address 192.168.0.1 255.255.255.0
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ipv6 address autoconfig

# Using Deleted
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  ip address 192.0.2.10 255.255.255.0
#  shutdown
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  ip address 192.168.1.0 255.255.255.0
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  ip address 192.168.0.1 255.255.255.0
#  shutdown
#  duplex full
#  speed 10
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ip address 192.168.0.2 255.255.255.0

- name: "Delete attributes of given interfaces (NOTE: This won't delete the interface sitself)"
  cisco.ios.ios_l3_interfaces:
    config:
    - name: GigabitEthernet0/2
    - name: GigabitEthernet0/3.100
    state: deleted

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  shutdown
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  no ip address
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  ip address 192.168.0.1 255.255.255.0
#  shutdown
#  duplex full
#  speed 10
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20

# Using Deleted without any config passed
#"(NOTE: This will delete all of configured L3 resource module attributes from each configured interface)"

#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  ip address 192.0.2.10 255.255.255.0
#  shutdown
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  ip address 192.168.1.0 255.255.255.0
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  ip address 192.168.0.1 255.255.255.0
#  shutdown
#  duplex full
#  speed 10
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ip address 192.168.0.2 255.255.255.0

- name: "Delete L3 attributes of ALL interfaces together (NOTE: This won't delete the interface itself)"
  cisco.ios.ios_l3_interfaces:
    state: deleted

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  shutdown
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  no ip address
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  shutdown
#  duplex full
#  speed 10
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20

# Using Gathered

# Before state:
# -------------
#
# vios#sh running-config | section ^interface
# interface GigabitEthernet0/1
#  ip address 203.0.113.27 255.255.255.0
# interface GigabitEthernet0/2
#  ip address 192.0.2.1 255.255.255.0 secondary
#  ip address 192.0.2.2 255.255.255.0
#  ipv6 address 2001:DB8:0:3::/64

- name: Gather listed l3 interfaces with provided configurations
  cisco.ios.ios_l3_interfaces:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": [
#         {
#             "ipv4": [
#                 {
#                     "address": "203.0.113.27 255.255.255.0"
#                 }
#             ],
#             "name": "GigabitEthernet0/1"
#         },
#         {
#             "ipv4": [
#                 {
#                     "address": "192.0.2.1 255.255.255.0",
#                     "secondary": true
#                 },
#                 {
#                     "address": "192.0.2.2 255.255.255.0"
#                 }
#             ],
#             "ipv6": [
#                 {
#                     "address": "2001:db8:0:3::/64"
#                 }
#             ],
#             "name": "GigabitEthernet0/2"
#         }
#     ]

# After state:
# ------------
#
# vios#sh running-config | section ^interface
# interface GigabitEthernet0/1
#  ip address 203.0.113.27 255.255.255.0
# interface GigabitEthernet0/2
#  ip address 192.0.2.1 255.255.255.0 secondary
#  ip address 192.0.2.2 255.255.255.0
#  ipv6 address 2001:DB8:0:3::/64

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_l3_interfaces:
    config:
    - name: GigabitEthernet0/1
      ipv4:
      - address: dhcp
        dhcp_client: 0
        dhcp_hostname: test.com
    - name: GigabitEthernet0/2
      ipv4:
      - address: 198.51.100.1/24
        secondary: true
      - address: 198.51.100.2/24
      ipv6:
      - address: 2001:db8:0:3::/64
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#         "interface GigabitEthernet0/1",
#         "ip address dhcp client-id GigabitEthernet 0/0 hostname test.com",
#         "interface GigabitEthernet0/2",
#         "ip address 198.51.100.1 255.255.255.0 secondary",
#         "ip address 198.51.100.2 255.255.255.0",
#         "ipv6 address 2001:db8:0:3::/64"
#     ]

# Using Parsed

# File: parsed.cfg
# ----------------
#
# interface GigabitEthernet0/1
# ip address dhcp client-id
# GigabitEthernet 0/0 hostname test.com
# interface GigabitEthernet0/2
# ip address 198.51.100.1 255.255.255.0
# secondary ip address 198.51.100.2 255.255.255.0
# ipv6 address 2001:db8:0:3::/64

- name: Parse the commands for provided configuration
  cisco.ios.ios_l3_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#         {
#             "ipv4": [
#                 {
#                     "address": "dhcp",
#                     "dhcp_client": 0,
#                     "dhcp_hostname": "test.com"
#                 }
#             ],
#             "name": "GigabitEthernet0/1"
#         },
#         {
#             "ipv4": [
#                 {
#                     "address": "198.51.100.1 255.255.255.0",
#                     "secondary": true
#                 },
#                 {
#                     "address": "198.51.100.2 255.255.255.0"
#                 }
#             ],
#             "ipv6": [
#                 {
#                     "address": "2001:db8:0:3::/64"
#                 }
#             ],
#             "name": "GigabitEthernet0/2"
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
  sample: ['interface GigabitEthernet0/1', 'ip address 192.168.0.2 255.255.255.0']
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.l3_interfaces.l3_interfaces import (
    L3_InterfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.l3_interfaces.l3_interfaces import (
    L3_Interfaces,
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
        argument_spec=L3_InterfacesArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    result = L3_Interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
