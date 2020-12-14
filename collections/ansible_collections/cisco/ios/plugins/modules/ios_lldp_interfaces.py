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
The module file for ios_lldp_interfaces
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: ios_lldp_interfaces
short_description: LLDP interfaces resource module
description: This module manages link layer discovery protocol (LLDP) attributes of
  interfaces on Cisco IOS devices.
version_added: 1.0.0
author: Sumit Jaiswal (@justjais)
notes:
- Tested against Cisco IOSv Version 15.2 on VIRL.
options:
  config:
    description: A dictionary of LLDP options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of the interface excluding any logical unit number, i.e. GigabitEthernet0/1.
        type: str
        required: true
      receive:
        description:
        - Enable LLDP reception on interface.
        type: bool
      transmit:
        description:
        - Enable LLDP transmission on interface.
        type: bool
      med_tlv_select:
        description:
        - Selection of LLDP MED TLVs to send
        - NOTE, if med-tlv-select is configured idempotency won't be maintained as
          Cisco device doesn't record configured med-tlv-select options. As such,
          Ansible cannot verify if the respective med-tlv-select options is already
          configured or not from the device side. If you try to apply med-tlv-select
          option in every play run, Ansible will show changed as True.
        type: dict
        suboptions:
          inventory_management:
            description:
            - LLDP MED Inventory Management TLV
            type: bool
      tlv_select:
        description:
        - Selection of LLDP type-length-value i.e. TLVs to send
        - NOTE, if tlv-select is configured idempotency won't be maintained as Cisco
          device doesn't record configured tlv-select options. As such, Ansible cannot
          verify if the respective tlv-select options is already configured or not
          from the device side. If you try to apply tlv-select option in every play
          run, Ansible will show changed as True.
        type: dict
        suboptions:
          power_management:
            description:
            - IEEE 802.3 DTE Power via MDI TLV
            type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(sh lldp interface).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
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
    - rendered
    - gathered
    - parsed
    default: merged
"""

EXAMPLES = """
# Using merged
#
# Before state:
# -------------
#
# vios#sh lldp interface
# GigabitEthernet0/0:
#    Tx: enabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/2:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: INIT
#
# GigabitEthernet0/3:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#

- name: Merge provided configuration with device configuration
  cisco.ios.ios_lldp_interfaces:
    config:
    - name: GigabitEthernet0/1
      receive: true
      transmit: true
    - name: GigabitEthernet0/2
      receive: true
    - name: GigabitEthernet0/3
      transmit: true
    state: merged

# After state:
# ------------
#
# vios#sh lldp interface
# GigabitEthernet0/0:
#    Tx: enabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/2:
#    Tx: disabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: INIT
#
# GigabitEthernet0/3:
#    Tx: enabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#

# Using overridden
#
# Before state:
# -------------
#
# vios#sh lldp interface
# GigabitEthernet0/0:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/2:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: INIT
#
# GigabitEthernet0/3:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME

- name: Override device configuration of all lldp_interfaces with provided configuration
  cisco.ios.ios_lldp_interfaces:
    config:
    - name: GigabitEthernet0/2
      receive: true
      transmit: true
    state: overridden

# After state:
# ------------
#
# vios#sh lldp interface
# GigabitEthernet0/0:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/2:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: INIT
#
# GigabitEthernet0/3:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME

# Using replaced
#
# Before state:
# -------------
#
# vios#sh lldp interface
# GigabitEthernet0/0:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/2:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: INIT
#
# GigabitEthernet0/3:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#

- name: Replaces device configuration of listed lldp_interfaces with provided configuration
  cisco.ios.ios_lldp_interfaces:
    config:
    - name: GigabitEthernet0/2
      receive: true
      transmit: true
    - name: GigabitEthernet0/3
      receive: true
    state: replaced

# After state:
# ------------
#
# vios#sh lldp interface
# GigabitEthernet0/0:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/2:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: INIT
#
# GigabitEthernet0/3:
#    Tx: disabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#

# Using Deleted
#
# Before state:
# -------------
#
# vios#sh lldp interface
# GigabitEthernet0/0:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/2:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: INIT
#
# GigabitEthernet0/3:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME

- name: "Delete LLDP attributes of given interfaces (Note: This won't delete the interface itself)"
  cisco.ios.ios_lldp_interfaces:
    config:
    - name: GigabitEthernet0/1
    state: deleted

# After state:
# -------------
#
# vios#sh lldp interface
# GigabitEthernet0/0:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/2:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: INIT
#
# GigabitEthernet0/3:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#

# Using Deleted without any config passed
# "(NOTE: This will delete all of configured LLDP module attributes)"
#
# Before state:
# -------------
#
# vios#sh lldp interface
# GigabitEthernet0/0:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/2:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: INIT
#
# GigabitEthernet0/3:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME

- name: "Delete LLDP attributes for all configured interfaces (Note: This won't delete the interface itself)"
  cisco.ios.ios_lldp_interfaces:
    state: deleted

# After state:
# -------------
#
# vios#sh lldp interface
# GigabitEthernet0/0:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/2:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: INIT
#
# GigabitEthernet0/3:
#    Tx: disabled
#    Rx: disabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME

# Using Gathered

# Before state:
# -------------
#
# vios#sh lldp interface
# GigabitEthernet0/0:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/2:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME

- name: Gather listed LLDP interfaces with provided configurations
  cisco.ios.ios_lldp_interfaces:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": [
#         {
#             "name": "GigabitEthernet0/0",
#             "receive": true,
#             "transmit": true
#         },
#         {
#             "name": "GigabitEthernet0/1",
#             "receive": true,
#             "transmit": true
#         },
#         {
#             "name": "GigabitEthernet0/2",
#             "receive": true,
#             "transmit": true
#         }
#     ]

# After state:
# ------------
#
# vios#sh lldp interface
# GigabitEthernet0/0:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME

# GigabitEthernet0/2:
#    Tx: enabled
#    Rx: enabled
#    Tx state: IDLE
#    Rx state: WAIT FOR FRAME

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_lldp_interfaces:
    config:
    - name: GigabitEthernet0/0
      receive: true
      transmit: true
    - name: GigabitEthernet0/1
      receive: true
      transmit: true
    - name: GigabitEthernet0/2
      receive: true
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#         "interface GigabitEthernet0/0",
#         "lldp receive",
#         "lldp transmit",
#         "interface GigabitEthernet0/1",
#         "lldp receive",
#         "lldp transmit",
#         "interface GigabitEthernet0/2",
#         "lldp receive"
#     ]

# Using Parsed

# File: parsed.cfg
# ----------------
#
# GigabitEthernet0/0:
#   Tx: enabled
#   Rx: disabled
#   Tx state: IDLE
#   Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/1:
#   Tx: enabled
#   Rx: enabled
#   Tx state: IDLE
#   Rx state: WAIT FOR FRAME
#
# GigabitEthernet0/2:
#   Tx: disabled
#   Rx: enabled
#   Tx state: IDLE
#   Rx state: INIT

- name: Parse the commands for provided configuration
  cisco.ios.ios_lldp_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#         {
#             "name": "GigabitEthernet0/0",
#             "receive": false,
#             "transmit": true
#         },
#         {
#             "name": "GigabitEthernet0/1",
#             "receive": true,
#             "transmit": true
#         },
#         {
#             "name": "GigabitEthernet0/2",
#             "receive": true,
#             "transmit": false
#         }
#     ]

"""
RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['interface GigabitEthernet 0/1', 'lldp transmit', 'lldp receive']
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.lldp_interfaces.lldp_interfaces import (
    Lldp_InterfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.lldp_interfaces.lldp_interfaces import (
    Lldp_Interfaces,
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
        argument_spec=Lldp_InterfacesArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    result = Lldp_Interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
