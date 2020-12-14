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
The module file for ios_interfaces
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_interfaces
short_description: Interfaces resource module
description: This module manages the interface attributes of Cisco IOS network devices.
version_added: 1.0.0
author: Sumit Jaiswal (@justjais)
notes:
- Tested against Cisco IOSv Version 15.2 on VIRL
options:
  config:
    description: A dictionary of interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of interface, e.g. GigabitEthernet0/2, loopback999.
        type: str
        required: true
      description:
        description:
        - Interface description.
        type: str
      enabled:
        description:
        - Administrative state of the interface.
        - Set the value to C(true) to administratively enable the interface or C(false)
          to disable it.
        type: bool
        default: true
      speed:
        description:
        - Interface link speed. Applicable for Ethernet interfaces only.
        type: str
      mtu:
        description:
        - MTU for a specific interface. Applicable for Ethernet interfaces only.
        - Refer to vendor documentation for valid values.
        type: int
      duplex:
        description:
        - Interface link status. Applicable for Ethernet interfaces only, either in
          half duplex, full duplex or in automatic state which negotiates the duplex
          automatically.
        type: str
        choices:
        - full
        - half
        - auto
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^interface).
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
        option should be the same format as the output of command I(show running-config
        | include ip route|ipv6 route) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  no ip address
#  duplex auto
#  speed auto

- name: Merge provided configuration with device configuration
  cisco.ios.ios_interfaces:
    config:
    - name: GigabitEthernet0/2
      description: Configured and Merged by Ansible Network
      enabled: true
    - name: GigabitEthernet0/3
      description: Configured and Merged by Ansible Network
      mtu: 2800
      enabled: false
      speed: 100
      duplex: full
    state: merged

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
#  description Configured and Merged by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured and Merged by Ansible Network
#  mtu 2800
#  no ip address
#  shutdown
#  duplex full
#  speed 100

# Using replaced

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  mtu 2000
#  no ip address
#  shutdown
#  duplex full
#  speed 100

- name: Replaces device configuration of listed interfaces with provided configuration
  cisco.ios.ios_interfaces:
    config:
    - name: GigabitEthernet0/3
      description: Configured and Replaced by Ansible Network
      enabled: false
      duplex: auto
      mtu: 2500
      speed: 1000
    state: replaced

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured and Replaced by Ansible Network
#  mtu 2500
#  no ip address
#  shutdown
#  duplex full
#  speed 1000

# Using overridden

# Before state:
# -------------
#
# vios#show running-config | section ^interface#
# interface GigabitEthernet0/1
#  description Configured by Ansible
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible
#  mtu 2800
#  no ip address
#  shutdown
#  duplex full
#  speed 100

- name: Override device configuration of all interfaces with provided configuration
  cisco.ios.ios_interfaces:
    config:
    - name: GigabitEthernet0/2
      description: Configured and Overridden by Ansible Network
      speed: 1000
    - name: GigabitEthernet0/3
      description: Configured and Overridden by Ansible Network
      enabled: false
      duplex: full
      mtu: 2000
    state: overridden

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured and Overridden by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured and Overridden by Ansible Network
#  mtu 2000
#  no ip address
#  shutdown
#  duplex full
#  speed 100

# Using Deleted

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  mtu 2500
#  no ip address
#  shutdown
#  duplex full
#  speed 1000

- name: "Delete module attributes of given interfaces (Note: This won't delete the interface itself)"
  cisco.ios.ios_interfaces:
    config:
    - name: GigabitEthernet0/2
    state: deleted

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  mtu 2500
#  no ip address
#  shutdown
#  duplex full
#  speed 1000

# Using Deleted without any config passed
#"(NOTE: This will delete all of configured resource module attributes from each configured interface)"

# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Ansible Network
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Ansible Network
#  mtu 2500
#  no ip address
#  shutdown
#  duplex full
#  speed 1000

- name: "Delete module attributes of all interfaces (Note: This won't delete the interface itself)"
  cisco.ios.ios_interfaces:
    state: deleted

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/3
#  no ip address
#  duplex auto
#  speed auto

# Using Gathered

# Before state:
# -------------
#
# vios#sh running-config | section ^interface
# interface GigabitEthernet0/1
#  description this is interface1
#  mtu 65
#  duplex auto
#  speed 10
# interface GigabitEthernet0/2
#  description this is interface2
#  mtu 110
#  shutdown
#  duplex auto
#  speed 100

- name: Gather listed interfaces with provided configurations
  cisco.ios.ios_interfaces:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": [
#         {
#             "description": "this is interface1",
#             "duplex": "auto",
#             "enabled": true,
#             "mtu": 65,
#             "name": "GigabitEthernet0/1",
#             "speed": "10"
#         },
#         {
#             "description": "this is interface2",
#             "duplex": "auto",
#             "enabled": false,
#             "mtu": 110,
#             "name": "GigabitEthernet0/2",
#             "speed": "100"
#         }
#     ]

# After state:
# ------------
#
# vios#sh running-config | section ^interface
# interface GigabitEthernet0/1
#  description this is interface1
#  mtu 65
#  duplex auto
#  speed 10
# interface GigabitEthernet0/2
#  description this is interface2
#  mtu 110
#  shutdown
#  duplex auto
#  speed 100

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_interfaces:
    config:
    - name: GigabitEthernet0/1
      description: Configured by Ansible-Network
      mtu: 110
      enabled: true
      duplex: half
    - name: GigabitEthernet0/2
      description: Configured by Ansible-Network
      mtu: 2800
      enabled: false
      speed: 100
      duplex: full
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#         "interface GigabitEthernet0/1",
#         "description Configured by Ansible-Network",
#         "mtu 110",
#         "duplex half",
#         "no shutdown",
#         "interface GigabitEthernet0/2",
#         "description Configured by Ansible-Network",
#         "mtu 2800",
#         "speed 100",
#         "duplex full",
#         "shutdown"

# Using Parsed

# File: parsed.cfg
# ----------------
#
# interface GigabitEthernet0/1
# description interfaces 0/1
# mtu 110
# duplex half
# no shutdown
# interface GigabitEthernet0/2
# description interfaces 0/2
# mtu 2800
# speed 100
# duplex full
# shutdown

- name: Parse the commands for provided configuration
  cisco.ios.ios_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#         {
#             "description": "interfaces 0/1",
#             "duplex": "half",
#             "enabled": true,
#             "mtu": 110,
#             "name": "GigabitEthernet0/1"
#         },
#         {
#             "description": "interfaces 0/2",
#             "duplex": "full",
#             "enabled": true,
#             "mtu": 2800,
#             "name": "GigabitEthernet0/2",
#             "speed": "100"
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
  sample: ['interface GigabitEthernet 0/1', 'description This is test', 'speed 100']
"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.interfaces.interfaces import (
    InterfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.interfaces.interfaces import (
    Interfaces,
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
        argument_spec=InterfacesArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    result = Interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
