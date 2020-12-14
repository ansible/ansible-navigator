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
The module file for ios_vlans
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = """
module: ios_vlans
short_description: VLANs resource module
description: This module provides declarative management of VLANs on Cisco IOS network
  devices.
version_added: 1.0.0
author: Sumit Jaiswal (@justjais)
notes:
- Tested against Cisco IOSl2 device with Version 15.2 on VIRL.
options:
  config:
    description: A dictionary of VLANs options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Ascii name of the VLAN.
        - NOTE, I(name) should not be named/appended with I(default) as it is reserved
          for device default vlans.
        type: str
      vlan_id:
        description:
        - ID of the VLAN. Range 1-4094
        type: int
        required: true
      mtu:
        description:
        - VLAN Maximum Transmission Unit.
        - Refer to vendor documentation for valid values.
        type: int
      state:
        description:
        - Operational state of the VLAN
        type: str
        choices:
        - active
        - suspend
      remote_span:
        description:
        - Configure as Remote SPAN VLAN
        type: bool
      shutdown:
        description:
        - Shutdown VLAN switching.
        type: str
        choices:
        - enabled
        - disabled
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device
        by executing the command B(show vlan).
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

# Before state:
# -------------
#
# vios_l2#show vlan
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/1, Gi0/2
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0

- name: Merge provided configuration with device configuration
  cisco.ios.ios_vlans:
    config:
    - name: Vlan_10
      vlan_id: 10
      state: active
      shutdown: disabled
      remote_span: 10
    - name: Vlan_20
      vlan_id: 20
      mtu: 610
      state: active
      shutdown: enabled
    - name: Vlan_30
      vlan_id: 30
      state: suspend
      shutdown: enabled
    state: merged

# After state:
# ------------
#
# vios_l2#show vlan
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/1, Gi0/2
# 10   vlan_10                          active
# 20   vlan_20                          act/lshut
# 30   vlan_30                          sus/lshut
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 10   enet  100010     1500  -      -      -        -    -        0      0
# 20   enet  100020     610   -      -      -        -    -        0      0
# 30   enet  100030     1500  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
#
# Remote SPAN VLANs
# ------------------------------------------------------------------------------
# 10

# Using overridden

# Before state:
# -------------
#
# vios_l2#show vlan
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/1, Gi0/2
# 10   vlan_10                          active
# 20   vlan_20                          act/lshut
# 30   vlan_30                          sus/lshut
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 10   enet  100010     1500  -      -      -        -    -        0      0
# 20   enet  100020     610   -      -      -        -    -        0      0
# 30   enet  100030     1500  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
#
# Remote SPAN VLANs
# ------------------------------------------------------------------------------
# 10

- name: Override device configuration of all VLANs with provided configuration
  cisco.ios.ios_vlans:
    config:
    - name: Vlan_10
      vlan_id: 10
      mtu: 1000
    state: overridden

# After state:
# ------------
#
# vios_l2#show vlan
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 10   Vlan_10                          active
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 10   enet  100010     1000  -      -      -        -    -        0      0

# Using replaced

# Before state:
# -------------
#
# vios_l2#show vlan
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/1, Gi0/2
# 10   vlan_10                          active
# 20   vlan_20                          act/lshut
# 30   vlan_30                          sus/lshut
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 10   enet  100010     1500  -      -      -        -    -        0      0
# 20   enet  100020     610   -      -      -        -    -        0      0
# 30   enet  100030     1500  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
#
# Remote SPAN VLANs
# ------------------------------------------------------------------------------
# 10

- name: Replaces device configuration of listed VLANs with provided configuration
  cisco.ios.ios_vlans:
    config:
    - vlan_id: 20
      name: Test_VLAN20
      mtu: 700
      shutdown: disabled
    - vlan_id: 30
      name: Test_VLAN30
      mtu: 1000
    state: replaced

# After state:
# ------------
#
# vios_l2#show vlan
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/1, Gi0/2
# 10   vlan_10                          active
# 20   Test_VLAN20                      active
# 30   Test_VLAN30                      sus/lshut
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 10   enet  100010     1500  -      -      -        -    -        0      0
# 20   enet  100020     700   -      -      -        -    -        0      0
# 30   enet  100030     1000  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
#
# Remote SPAN VLANs
# ------------------------------------------------------------------------------
# 10

# Using deleted

# Before state:
# -------------
#
# vios_l2#show vlan
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/1, Gi0/2
# 10   vlan_10                          active
# 20   vlan_20                          act/lshut
# 30   vlan_30                          sus/lshut
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 10   enet  100010     1500  -      -      -        -    -        0      0
# 20   enet  100020     610   -      -      -        -    -        0      0
# 30   enet  100030     1500  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
#
# Remote SPAN VLANs
# ------------------------------------------------------------------------------
# 10

- name: Delete attributes of given VLANs
  cisco.ios.ios_vlans:
    config:
    - vlan_id: 10
    - vlan_id: 20
    state: deleted

# After state:
# -------------
#
# vios_l2#show vlan
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/1, Gi0/2
# 30   vlan_30                          sus/lshut
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 30   enet  100030     1500  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0

# Using Deleted without any config passed
#"(NOTE: This will delete all of configured vlans attributes)"

# Before state:
# -------------
#
# vios_l2#show vlan
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/1, Gi0/2
# 10   vlan_10                          active
# 20   vlan_20                          act/lshut
# 30   vlan_30                          sus/lshut
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 10   enet  100010     1500  -      -      -        -    -        0      0
# 20   enet  100020     610   -      -      -        -    -        0      0
# 30   enet  100030     1500  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
#
# Remote SPAN VLANs
# ------------------------------------------------------------------------------
# 10

- name: Delete attributes of ALL VLANs
  cisco.ios.ios_vlans:
    state: deleted

# After state:
# -------------
#
# vios_l2#show vlan
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/1, Gi0/2
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0

# Using Gathered

# Before state:
# -------------
#
# vios_l2#show vlan
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/1, Gi0/2
# 10   vlan_10                          active
# 20   vlan_20                          act/lshut
# 30   vlan_30                          sus/lshut
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 10   enet  100010     1500  -      -      -        -    -        0      0
# 20   enet  100020     610   -      -      -        -    -        0      0
# 30   enet  100030     1500  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
#
# Remote SPAN VLANs
# ------------------------------------------------------------------------------
# 10

- name: Gather listed vlans with provided configurations
  cisco.ios.ios_vlans:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": [
#         {
#             "mtu": 1500,
#             "name": "default",
#             "shutdown": "disabled",
#             "state": "active",
#             "vlan_id": 1
#         },
#         {
#             "mtu": 1500,
#             "name": "VLAN0010",
#             "shutdown": "disabled",
#             "state": "active",
#             "vlan_id": 10
#         },
#         {
#             "mtu": 1500,
#             "name": "VLAN0020",
#             "shutdown": "disabled",
#             "state": "active",
#             "vlan_id": 20
#         },
#         {
#             "mtu": 1500,
#             "name": "VLAN0030",
#             "shutdown": "disabled",
#             "state": "active",
#             "vlan_id": 30
#         },
#         {
#             "mtu": 1500,
#             "name": "fddi-default",
#             "shutdown": "enabled",
#             "state": "active",
#             "vlan_id": 1002
#         },
#         {
#             "mtu": 1500,
#             "name": "token-ring-default",
#             "shutdown": "enabled",
#             "state": "active",
#             "vlan_id": 1003
#         },
#         {
#             "mtu": 1500,
#             "name": "fddinet-default",
#             "shutdown": "enabled",
#             "state": "active",
#             "vlan_id": 1004
#         },
#         {
#             "mtu": 1500,
#             "name": "trnet-default",
#             "shutdown": "enabled",
#             "state": "active",
#             "vlan_id": 1005
#         }
#     ]

# After state:
# ------------
#
# vios_l2#show vlan
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/1, Gi0/2
# 10   vlan_10                          active
# 20   vlan_20                          act/lshut
# 30   vlan_30                          sus/lshut
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 10   enet  100010     1500  -      -      -        -    -        0      0
# 20   enet  100020     610   -      -      -        -    -        0      0
# 30   enet  100030     1500  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
#
# Remote SPAN VLANs
# ------------------------------------------------------------------------------
# 10

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_vlans:
    config:
    - name: Vlan_10
      vlan_id: 10
      state: active
      shutdown: disabled
      remote_span: 10
    - name: Vlan_20
      vlan_id: 20
      mtu: 610
      state: active
      shutdown: enabled
    - name: Vlan_30
      vlan_id: 30
      state: suspend
      shutdown: enabled
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#         "vlan 10",
#         "name Vlan_10",
#         "state active",
#         "remote-span",
#         "no shutdown",
#         "vlan 20",
#         "name Vlan_20",
#         "state active",
#         "mtu 610",
#         "shutdown",
#         "vlan 30",
#         "name Vlan_30",
#         "state suspend",
#         "shutdown"
#     ]

# Using Parsed

# File: parsed.cfg
# ----------------
#
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/1, Gi0/2
# 10   vlan_10                          active
# 20   vlan_20                          act/lshut
# 30   vlan_30                          sus/lshut
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 10   enet  100010     1500  -      -      -        -    -        0      0
# 20   enet  100020     1500  -      -      -        -    -        0      0
# 30   enet  100030     1500  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0

- name: Parse the commands for provided configuration
  cisco.ios.ios_vlans:
    running_config: "{{ lookup('file', './parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#         {
#             "mtu": 1500,
#             "name": "default",
#             "shutdown": "disabled",
#             "state": "active",
#             "vlan_id": 1
#         },
#         {
#             "mtu": 1500,
#             "name": "vlan_10",
#             "shutdown": "disabled",
#             "state": "active",
#             "vlan_id": 10
#         },
#         {
#             "mtu": 1500,
#             "name": "vlan_20",
#             "shutdown": "enabled",
#             "state": "active",
#             "vlan_id": 20
#         },
#         {
#             "mtu": 1500,
#             "name": "vlan_30",
#             "shutdown": "enabled",
#             "state": "suspend",
#             "vlan_id": 30
#         },
#         {
#             "mtu": 1500,
#             "name": "fddi-default",
#             "shutdown": "enabled",
#             "state": "active",
#             "vlan_id": 1002
#         },
#         {
#             "mtu": 1500,
#             "name": "token-ring-default",
#             "shutdown": "enabled",
#             "state": "active",
#             "vlan_id": 1003
#         },
#         {
#             "mtu": 1500,
#             "name": "fddinet-default",
#             "shutdown": "enabled",
#             "state": "active",
#             "vlan_id": 1004
#         },
#         {
#             "mtu": 1500,
#             "name": "trnet-default",
#             "shutdown": "enabled",
#             "state": "active",
#             "vlan_id": 1005
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
  sample: ['vlan 20', 'name vlan_20', 'mtu 600', 'remote-span']
"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vlans.vlans import (
    VlansArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.vlans.vlans import (
    Vlans,
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
        argument_spec=VlansArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    result = Vlans(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
