#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_ospf_interfaces
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: nxos_ospf_interfaces
version_added: 1.3.0
short_description: OSPF Interfaces Resource Module.
description:
- This module manages OSPF(v2/v3) configuration of interfaces on devices running Cisco NX-OS.
author: Nilashish Chakraborty (@NilashishC)
options:
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the NX-OS device
      by executing the command B(show running-config | section "^interface").
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: A list of OSPF configuration for interfaces.
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Name/Identifier of the interface.
        type: str
        required: True
      address_family:
        description:
        - OSPF settings on the interfaces in address-family context.
        type: list
        elements: dict
        suboptions:
          afi:
            description:
            - Address Family Identifier (AFI) for OSPF settings on the interfaces.
            type: str
            choices: ['ipv4', 'ipv6']
            required: True
          processes:
            description:
            - Interfaces configuration for an OSPF process.
            type: list
            elements: dict
            suboptions:
              process_id:
                description:
                - OSPF process tag.
                type: str
                required: True
              area:
                description:
                - Area associated with interface.
                type: dict
                suboptions:
                  area_id:
                    description:
                    - Area ID as a decimal or IP address format.
                    type: str
                    required: True
                  secondaries:
                    description:
                    - Do not include secondary IPv4/IPv6 addresses.
                    type: bool
              multi_areas:
                description:
                - Multi-Areas associated with interface.
                - Valid values are Area Ids as an integer or IP address.
                type: list
                elements: str
          multi_areas:
            description:
            - Multi-Areas associated with interface (not tied to OSPF process).
            - Valid values are Area Ids as an integer or IP address.
            type: list
            elements: str
          authentication:
            description:
            - Authentication settings on the interface.
            type: dict
            suboptions:
              key_chain:
                description:
                - Authentication password key-chain.
                type: str
              message_digest:
                description:
                - Use message-digest authentication.
                type: bool
              enable:
                description:
                - Enable/disable authentication on the interface.
                type: bool
              null_auth:
                description:
                - Use null(disable) authentication.
                type: bool
          authentication_key:
            description:
            - Configure the authentication key for the interface.
            type: dict
            suboptions:
              encryption:
                description:
                - 0 Specifies an UNENCRYPTED authentication key will follow.
                - 3 Specifies an 3DES ENCRYPTED authentication key will follow.
                - 7 Specifies a Cisco type 7  ENCRYPTED authentication key will follow.
                type: int
              key:
                description:
                - Authentication key.
                - Valid values are Cisco type 7 ENCRYPTED password, 3DES ENCRYPTED password
                  and UNENCRYPTED (cleartext) password based on the value of encryption key.
                type: str
                required: True
          message_digest_key:
            description:
            - Message digest authentication password (key) settings.
            type: dict
            suboptions:
              key_id:
                description:
                - Key ID.
                type: int
                required: True
              encryption:
                description:
                - 0 Specifies an UNENCRYPTED ospf password (key) will follow.
                - 3 Specifies an 3DES ENCRYPTED ospf password (key) will follow.
                - 7 Specifies a Cisco type 7 ENCRYPTED the ospf password (key) will follow.
                type: int
              key:
                description:
                - Authentication key.
                - Valid values are Cisco type 7 ENCRYPTED password, 3DES ENCRYPTED password
                  and UNENCRYPTED (cleartext) password based on the value of encryption key.
                type: str
                required: True
          cost:
            description:
            - Cost associated with interface.
            type: int
          dead_interval:
            description:
            - Dead interval value (in seconds).
            type: int
          hello_interval:
            description:
            - Hello interval value (in seconds).
            type: int
          instance:
            description:
            - Instance identifier.
            type: int
          mtu_ignore:
            description:
            - Enable/disable OSPF MTU mismatch detection.
            type: bool
          network:
            description:
            - Network type.
            type: str
            choices: ["broadcast", "point-to-point"]
          passive_interface:
            description:
            - Suppress routing updates on the interface.
            type: bool
          priority:
            description:
            - Router priority.
            type: int
          retransmit_interval:
            description:
            - Packet retransmission interval.
            type: int
          shutdown:
            description:
            - Shutdown OSPF on this interface.
            type: bool
          transmit_delay:
            description:
            - Packet transmission delay.
            type: int
  state:
    description:
      - The state the configuration should be left in.
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
# Using merged

# Before state:
# -------------
# NXOS# show running-config | section ^interface
# interface Ethernet1/1
#   no switchport
# interface Ethernet1/2
#   no switchport
# interface Ethernet1/3
#   no switchport

- name: Merge the provided configuration with the exisiting running configuration
  cisco.nxos.nxos_ospf_interfaces:
    config:
      - name: Ethernet1/1
        address_family:
        - afi: ipv4
          processes:
          - process_id: "100"
            area:
              area_id: 1.1.1.1
              secondaries: False
          multi_areas:
          - 11.11.11.11
        - afi: ipv6
          processes:
          - process_id: "200"
            area:
              area_id: 2.2.2.2
            multi_areas:
            - 21.0.0.0
          - process_id: "300"
            multi_areas:
            - 50.50.50.50
          multi_areas:
          - 16.10.10.10
      - name: Ethernet1/2
        address_family:
        - afi: ipv4
          authentication:
            enable: True
            key_chain: test-1
          message_digest_key:
            key_id: 10
            encryption: 3
            key: abc01d272be25d29
          cost: 100
        - afi: ipv6
          network: broadcast
          shutdown: True
      - name: Ethernet1/3
        address_family:
        - afi: ipv4
          authentication_key:
            encryption: 7
            key: 12090404011C03162E
    state: merged

# Task output
# -------------
# "before": [
#        {
#            "name": "Ethernet1/1"
#        },
#        {
#            "name": "Ethernet1/2"
#        },
#        {
#            "name": "Ethernet1/3"
#        },
# ]
#
# "commands": [
#        "interface Ethernet1/1",
#        "ip router ospf multi-area 11.11.11.11",
#        "ip router ospf 100 area 1.1.1.1 secondaries none",
#        "ipv6 router ospfv3 multi-area 16.10.10.10",
#        "ipv6 router ospfv3 200 area 2.2.2.2",
#        "ipv6 router ospfv3 200 multi-area 21.0.0.0",
#        "ipv6 router ospfv3 300 multi-area 50.50.50.50",
#        "interface Ethernet1/2",
#        "ip ospf authentication key-chain test-1",
#        "ip ospf authentication",
#        "ip ospf message-digest-key 10 md5 3 abc01d272be25d29",
#        "ip ospf cost 100",
#        "ospfv3 network broadcast",
#        "ospfv3 shutdown",
#        "interface Ethernet1/3",
#        "ip ospf authentication-key 7 12090404011C03162E"
# ]
#
# "after": [
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "multi_areas": [
#                        "11.11.11.11"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "1.1.1.1",
#                                "secondaries": false
#                            },
#                            "process_id": "100"
#                        }
#                    ]
#                },
#                {
#                    "afi": "ipv6",
#                    "multi_areas": [
#                        "16.10.10.10"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "2.2.2.2"
#                            },
#                            "multi_areas": [
#                                "21.0.0.0"
#                            ],
#                            "process_id": "200"
#                        },
#                        {
#                            "multi_areas": [
#                                "50.50.50.50"
#                            ],
#                            "process_id": "300"
#                        }
#                    ]
#                }
#            ],
#            "name": "Ethernet1/1"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication": {
#                       "enable": true,
#                       "key_chain": "test-1"
#                    },
#                    "cost": 100,
#                    "message_digest_key": {
#                        "encryption": 3,
#                        "key": "abc01d272be25d29",
#                        "key_id": 10
#                    }
#                },
#                {
#                    "afi": "ipv6",
#                    "network": "broadcast",
#                    "shutdown": true
#                }
#            ],
#            "name": "Ethernet1/2"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication_key": {
#                        "encryption": 7,
#                        "key": "12090404011C03162E"
#                    }
#                }
#            ],
#            "name": "Ethernet1/3"
#        },
# ]

# After state:
# -------------
# NXOS# show running-config | section ^interface
# interface Ethernet1/1
#   no switchport
#   ip router ospf 100 area 1.1.1.1 secondaries none
#   ip router ospf multi-area 11.11.11.11
#   ipv6 router ospfv3 200 area 2.2.2.2
#   ipv6 router ospfv3 multi-area 16.10.10.10
#   ipv6 router ospfv3 200 multi-area 21.0.0.0
#   ipv6 router ospfv3 300 multi-area 50.50.50.50
# interface Ethernet1/2
#   no switchport
#   ip ospf authentication
#   ip ospf authentication key-chain test-1
#   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
#   ip ospf cost 100
#   ospfv3 network broadcast
#   ospfv3 shutdown
# interface Ethernet1/3
#   no switchport
#   ip ospf authentication-key 7 12090404011C03162E


# Using replaced

# Before state:
# ------------
# NXOS# show running-config | section ^interface
# interface Ethernet1/1
#   no switchport
#   ip router ospf 100 area 1.1.1.1 secondaries none
#   ip router ospf multi-area 11.11.11.11
#   ipv6 router ospfv3 200 area 2.2.2.2
#   ipv6 router ospfv3 multi-area 16.10.10.10
#   ipv6 router ospfv3 200 multi-area 21.0.0.0
#   ipv6 router ospfv3 300 multi-area 50.50.50.50
# interface Ethernet1/2
#   no switchport
#   ip ospf authentication
#   ip ospf authentication key-chain test-1
#   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
#   ip ospf cost 100
#   ospfv3 network broadcast
#   ospfv3 shutdown
# interface Ethernet1/3
#   no switchport
#   ip ospf authentication-key 7 12090404011C03162E

- name: Replace OSPF configurations of listed interfaces with provided configurations
  cisco.nxos.nxos_ospf_interfaces:
    config:
    - name: Ethernet1/1
      address_family:
      - afi: ipv4
        processes:
        - process_id: "100"
          area:
            area_id: 1.1.1.1
            secondaries: False
        multi_areas:
        - 11.11.11.12
    - name: Ethernet1/3
    state: replaced

# Task output
# -------------
# "before": [
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "multi_areas": [
#                        "11.11.11.11"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "1.1.1.1",
#                                "secondaries": false
#                            },
#                            "process_id": "100"
#                        }
#                    ]
#                },
#                {
#                    "afi": "ipv6",
#                    "multi_areas": [
#                        "16.10.10.10"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "2.2.2.2"
#                            },
#                            "multi_areas": [
#                                "21.0.0.0"
#                            ],
#                            "process_id": "200"
#                        },
#                        {
#                            "multi_areas": [
#                                "50.50.50.50"
#                            ],
#                            "process_id": "300"
#                        }
#                    ]
#                }
#            ],
#            "name": "Ethernet1/1"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication": {
#                       "enable": true,
#                       "key_chain": "test-1"
#                    },
#                    "cost": 100,
#                    "message_digest_key": {
#                        "encryption": 3,
#                        "key": "abc01d272be25d29",
#                        "key_id": 10
#                    }
#                },
#                {
#                    "afi": "ipv6",
#                    "network": "broadcast",
#                    "shutdown": true
#                }
#            ],
#            "name": "Ethernet1/2"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication_key": {
#                        "encryption": 7,
#                        "key": "12090404011C03162E"
#                    }
#                }
#            ],
#            "name": "Ethernet1/3"
#        },
# ]
#
# "commands": [
#        "interface Ethernet1/1",
#        "ip router ospf multi-area 11.11.11.12",
#        "no ip router ospf multi-area 11.11.11.11",
#        "no ipv6 router ospfv3 multi-area 16.10.10.10",
#        "no ipv6 router ospfv3 200 area 2.2.2.2",
#        "no ipv6 router ospfv3 200 multi-area 21.0.0.0",
#        "no ipv6 router ospfv3 300 multi-area 50.50.50.50",
#        "interface Ethernet1/3",
#        "no ip ospf authentication-key 7 12090404011C03162E"
# ]
#
# "after": [
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "multi_areas": [
#                        "11.11.11.12"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "1.1.1.1",
#                                "secondaries": false
#                            },
#                            "process_id": "100"
#                        }
#                    ]
#                }
#            ],
#            "name": "Ethernet1/1"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication": {
#                        "enable": true,
#                        "key_chain": "test-1"
#                    },
#                    "cost": 100,
#                    "message_digest_key": {
#                        "encryption": 3,
#                        "key": "abc01d272be25d29",
#                        "key_id": 10
#                    }
#                },
#                {
#                    "afi": "ipv6",
#                    "network": "broadcast",
#                    "shutdown": true
#                }
#            ],
#            "name": "Ethernet1/2"
#        },
#        {
#            "name": "Ethernet1/3"
#        },
#
# After state:
# -------------
# NXOS# show running-config | section ^interface
# interface Ethernet1/1
#   no switchport
#   ip router ospf 100 area 1.1.1.1 secondaries none
#   ip router ospf multi-area 11.11.11.12
# interface Ethernet1/2
#   no switchport
#   ip ospf authentication
#   ip ospf authentication key-chain test-1
#   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
#   ip ospf cost 100
#   ospfv3 network broadcast
#   ospfv3 shutdown
# interface Ethernet1/3
#   no switchport


# Using overridden

# Before state:
# ------------
# NXOS# show running-config | section ^interface
# interface Ethernet1/1
#   no switchport
#   ip router ospf 100 area 1.1.1.1 secondaries none
#   ip router ospf multi-area 11.11.11.11
#   ipv6 router ospfv3 200 area 2.2.2.2
#   ipv6 router ospfv3 multi-area 16.10.10.10
#   ipv6 router ospfv3 200 multi-area 21.0.0.0
#   ipv6 router ospfv3 300 multi-area 50.50.50.50
# interface Ethernet1/2
#   no switchport
#   ip ospf authentication
#   ip ospf authentication key-chain test-1
#   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
#   ip ospf cost 100
#   ospfv3 network broadcast
#   ospfv3 shutdown
# interface Ethernet1/3
#   no switchport
#   ip ospf authentication-key 7 12090404011C03162E

- name: Overridde all OSPF interfaces configuration with provided configuration
  cisco.nxos.nxos_ospf_interfaces:
    config:
    - name: Ethernet1/1
      address_family:
      - afi: ipv4
        processes:
        - process_id: "100"
          area:
            area_id: 1.1.1.1
            secondaries: False
        multi_areas:
        - 11.11.11.12
    state: overridden

# Task output
# -------------
# "before": [
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "multi_areas": [
#                        "11.11.11.11"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "1.1.1.1",
#                                "secondaries": false
#                            },
#                            "process_id": "100"
#                        }
#                    ]
#                },
#                {
#                    "afi": "ipv6",
#                    "multi_areas": [
#                        "16.10.10.10"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "2.2.2.2"
#                            },
#                            "multi_areas": [
#                                "21.0.0.0"
#                            ],
#                            "process_id": "200"
#                        },
#                        {
#                            "multi_areas": [
#                                "50.50.50.50"
#                            ],
#                            "process_id": "300"
#                        }
#                    ]
#                }
#            ],
#            "name": "Ethernet1/1"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication": {
#                       "enable": true,
#                       "key_chain": "test-1"
#                    },
#                    "cost": 100,
#                    "message_digest_key": {
#                        "encryption": 3,
#                        "key": "abc01d272be25d29",
#                        "key_id": 10
#                    }
#                },
#                {
#                    "afi": "ipv6",
#                    "network": "broadcast",
#                    "shutdown": true
#                }
#            ],
#            "name": "Ethernet1/2"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication_key": {
#                        "encryption": 7,
#                        "key": "12090404011C03162E"
#                    }
#                }
#            ],
#            "name": "Ethernet1/3"
#        },
# ]
#
# "commands": [
#        "interface Ethernet1/2",
#        "no ip ospf authentication key-chain test-1",
#        "no ip ospf authentication",
#        "no ip ospf message-digest-key 10 md5 3 abc01d272be25d29",
#        "no ip ospf cost 100",
#        "no ospfv3 network broadcast",
#        "no ospfv3 shutdown",
#        "interface Ethernet1/3",
#        "no ip ospf authentication-key 7 12090404011C03162E",
#        "interface Ethernet1/1",
#        "ip router ospf multi-area 11.11.11.12",
#        "no ip router ospf multi-area 11.11.11.11",
#        "no ipv6 router ospfv3 multi-area 16.10.10.10",
#        "no ipv6 router ospfv3 200 area 2.2.2.2",
#        "no ipv6 router ospfv3 200 multi-area 21.0.0.0",
#        "no ipv6 router ospfv3 300 multi-area 50.50.50.50"
# ]
#
# "after": [
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "multi_areas": [
#                        "11.11.11.12"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "1.1.1.1",
#                                "secondaries": false
#                            },
#                            "process_id": "100"
#                        }
#                    ]
#                }
#            ],
#            "name": "Ethernet1/1"
#        },
#        {
#            "name": "Ethernet1/2"
#        },
#        {
#            "name": "Ethernet1/3"
#        },
# ]

# After state:
# -------------
# NXOS# show running-config | section ^interface
# interface Ethernet1/1
#   no switchport
#   ip router ospf 100 area 1.1.1.1 secondaries none
#   ip router ospf multi-area 11.11.11.12
# interface Ethernet1/2
#   no switchport
# interface Ethernet1/3
#   no switchport

# Using deleted to delete OSPF config of a single interface

# Before state:
# ------------
# NXOS# show running-config | section ^interface
# interface Ethernet1/1
#   no switchport
#   ip router ospf 100 area 1.1.1.1 secondaries none
#   ip router ospf multi-area 11.11.11.11
#   ipv6 router ospfv3 200 area 2.2.2.2
#   ipv6 router ospfv3 multi-area 16.10.10.10
#   ipv6 router ospfv3 200 multi-area 21.0.0.0
#   ipv6 router ospfv3 300 multi-area 50.50.50.50
# interface Ethernet1/2
#   no switchport
#   ip ospf authentication
#   ip ospf authentication key-chain test-1
#   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
#   ip ospf cost 100
#   ospfv3 network broadcast
#   ospfv3 shutdown
# interface Ethernet1/3
#   no switchport
#   ip ospf authentication-key 7 12090404011C03162E

- name: Delete OSPF config from a single interface
  cisco.nxos.nxos_ospf_interfaces:
    config:
      - name: Ethernet1/1
    state: deleted

# Task output
# -------------
# "before": [
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "multi_areas": [
#                        "11.11.11.11"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "1.1.1.1",
#                                "secondaries": false
#                            },
#                            "process_id": "100"
#                        }
#                    ]
#                },
#                {
#                    "afi": "ipv6",
#                    "multi_areas": [
#                        "16.10.10.10"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "2.2.2.2"
#                            },
#                            "multi_areas": [
#                                "21.0.0.0"
#                            ],
#                            "process_id": "200"
#                        },
#                        {
#                            "multi_areas": [
#                                "50.50.50.50"
#                            ],
#                            "process_id": "300"
#                        }
#                    ]
#                }
#            ],
#            "name": "Ethernet1/1"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication": {
#                       "enable": true,
#                       "key_chain": "test-1"
#                    },
#                    "cost": 100,
#                    "message_digest_key": {
#                        "encryption": 3,
#                        "key": "abc01d272be25d29",
#                        "key_id": 10
#                    }
#                },
#                {
#                    "afi": "ipv6",
#                    "network": "broadcast",
#                    "shutdown": true
#                }
#            ],
#            "name": "Ethernet1/2"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication_key": {
#                        "encryption": 7,
#                        "key": "12090404011C03162E"
#                    }
#                }
#            ],
#            "name": "Ethernet1/3"
#        },
# ]
#
# "commands": [
#        "interface Ethernet1/1",
#        "no ip router ospf multi-area 11.11.11.11",
#        "no ip router ospf 100 area 1.1.1.1 secondaries none",
#        "no ipv6 router ospfv3 multi-area 16.10.10.10",
#        "no ipv6 router ospfv3 200 area 2.2.2.2",
#        "no ipv6 router ospfv3 200 multi-area 21.0.0.0",
#        "no ipv6 router ospfv3 300 multi-area 50.50.50.50"
# ]
#
# "before": [
#        {
#            "name": "Ethernet1/1"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication": {
#                       "enable": true,
#                       "key_chain": "test-1"
#                    },
#                    "cost": 100,
#                    "message_digest_key": {
#                        "encryption": 3,
#                        "key": "abc01d272be25d29",
#                        "key_id": 10
#                    }
#                },
#                {
#                    "afi": "ipv6",
#                    "network": "broadcast",
#                    "shutdown": true
#                }
#            ],
#            "name": "Ethernet1/2"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication_key": {
#                        "encryption": 7,
#                        "key": "12090404011C03162E"
#                    }
#                }
#            ],
#            "name": "Ethernet1/3"
#        },
# ]

# After state:
# ------------
# NXOS# show running-config | section ^interface
# interface Ethernet1/1
#   no switchport
# interface Ethernet1/2
#   no switchport
#   ip ospf authentication
#   ip ospf authentication key-chain test-1
#   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
#   ip ospf cost 100
#   ospfv3 network broadcast
#   ospfv3 shutdown
# interface Ethernet1/3
#   no switchport
#   ip ospf authentication-key 7 12090404011C03162E

# Using deleted to delete OSPF config from all interfaces

# Before state:
# ------------
# NXOS# show running-config | section ^interface
# interface Ethernet1/1
#   no switchport
#   ip router ospf 100 area 1.1.1.1 secondaries none
#   ip router ospf multi-area 11.11.11.11
#   ipv6 router ospfv3 200 area 2.2.2.2
#   ipv6 router ospfv3 multi-area 16.10.10.10
#   ipv6 router ospfv3 200 multi-area 21.0.0.0
#   ipv6 router ospfv3 300 multi-area 50.50.50.50
# interface Ethernet1/2
#   no switchport
#   ip ospf authentication
#   ip ospf authentication key-chain test-1
#   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
#   ip ospf cost 100
#   ospfv3 network broadcast
#   ospfv3 shutdown
# interface Ethernet1/3
#   no switchport
#   ip ospf authentication-key 7 12090404011C03162E

- name: Delete OSPF config from all interfaces
  cisco.nxos.nxos_ospf_interfaces:
    state: deleted

# Task output
# -------------
# "before": [
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "multi_areas": [
#                        "11.11.11.11"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "1.1.1.1",
#                                "secondaries": false
#                            },
#                            "process_id": "100"
#                        }
#                    ]
#                },
#                {
#                    "afi": "ipv6",
#                    "multi_areas": [
#                        "16.10.10.10"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "2.2.2.2"
#                            },
#                            "multi_areas": [
#                                "21.0.0.0"
#                            ],
#                            "process_id": "200"
#                        },
#                        {
#                            "multi_areas": [
#                                "50.50.50.50"
#                            ],
#                            "process_id": "300"
#                        }
#                    ]
#                }
#            ],
#            "name": "Ethernet1/1"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication": {
#                       "enable": true,
#                       "key_chain": "test-1"
#                    },
#                    "cost": 100,
#                    "message_digest_key": {
#                        "encryption": 3,
#                        "key": "abc01d272be25d29",
#                        "key_id": 10
#                    }
#                },
#                {
#                    "afi": "ipv6",
#                    "network": "broadcast",
#                    "shutdown": true
#                }
#            ],
#            "name": "Ethernet1/2"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication_key": {
#                        "encryption": 7,
#                        "key": "12090404011C03162E"
#                    }
#                }
#            ],
#            "name": "Ethernet1/3"
#        },
# ]
#
# "commands": [
#        "interface Ethernet1/1",
#        "no ip router ospf multi-area 11.11.11.11",
#        "no ip router ospf 100 area 1.1.1.1 secondaries none",
#        "no ipv6 router ospfv3 multi-area 16.10.10.10",
#        "no ipv6 router ospfv3 200 area 2.2.2.2",
#        "no ipv6 router ospfv3 200 multi-area 21.0.0.0",
#        "no ipv6 router ospfv3 300 multi-area 50.50.50.50",
#        "interface Ethernet1/2",
#        "no ip ospf authentication key-chain test-1",
#        "no ip ospf authentication",
#        "no ip ospf message-digest-key 10 md5 3 abc01d272be25d29",
#        "no ip ospf cost 100",
#        "no ospfv3 network broadcast",
#        "no ospfv3 shutdown",
#        "interface Ethernet1/3",
#        "no ip ospf authentication-key 7 12090404011C03162E"
# ]
#
# "after": [
#        {
#            "name": "Ethernet1/1"
#        },
#        {
#            "name": "Ethernet1/2"
#        },
#        {
#            "name": "Ethernet1/3"
#        },
# ]

# After state:
# ------------
# NXOS# show running-config | section ^interface
# interface Ethernet1/1
#   no switchport
# interface Ethernet1/2
#   no switchport
# interface Ethernet1/3
#   no switchport

# Using rendered

- name: Render platform specific configuration lines with state rendered (without connecting to the device)
  cisco.nxos.nxos_ospf_interfaces:
    config:
      - name: Ethernet1/1
        address_family:
        - afi: ipv4
          processes:
          - process_id: "100"
            area:
              area_id: 1.1.1.1
              secondaries: False
          multi_areas:
          - 11.11.11.11
        - afi: ipv6
          processes:
          - process_id: "200"
            area:
              area_id: 2.2.2.2
            multi_areas:
            - 21.0.0.0
          - process_id: "300"
            multi_areas:
            - 50.50.50.50
          multi_areas:
          - 16.10.10.10
      - name: Ethernet1/2
        address_family:
        - afi: ipv4
          authentication:
            enable: True
            key_chain: test-1
          message_digest_key:
            key_id: 10
            encryption: 3
            key: abc01d272be25d29
          cost: 100
        - afi: ipv6
          network: broadcast
          shutdown: True
      - name: Ethernet1/3
        address_family:
        - afi: ipv4
          authentication_key:
            encryption: 7
            key: 12090404011C03162E
    state: rendered

# Task Output (redacted)
# -----------------------
# "rendered": [
#        "interface Ethernet1/1",
#        "ip router ospf multi-area 11.11.11.11",
#        "ip router ospf 100 area 1.1.1.1 secondaries none",
#        "ipv6 router ospfv3 multi-area 16.10.10.10",
#        "ipv6 router ospfv3 200 area 2.2.2.2",
#        "ipv6 router ospfv3 200 multi-area 21.0.0.0",
#        "ipv6 router ospfv3 300 multi-area 50.50.50.50",
#        "interface Ethernet1/2",
#        "ip ospf authentication key-chain test-1",
#        "ip ospf authentication",
#        "ip ospf message-digest-key 10 md5 3 abc01d272be25d29",
#        "ip ospf cost 100",
#        "ospfv3 network broadcast",
#        "ospfv3 shutdown",
#        "interface Ethernet1/3",
#        "ip ospf authentication-key 7 12090404011C03162E"
# ]

# Using parsed

# parsed.cfg
# ------------
# interface Ethernet1/1
#   ip router ospf 100 area 1.1.1.1 secondaries none
#   ip router ospf multi-area 11.11.11.11
#   ipv6 router ospfv3 200 area 2.2.2.2
#   ipv6 router ospfv3 200 multi-area 21.0.0.0
#   ipv6 router ospfv3 300 multi-area 50.50.50.50
#   ipv6 router ospfv3 multi-area 16.10.10.10
# interface Ethernet1/2
#   ip ospf authentication
#   ip ospf authentication key-chain test-1
#   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
#   ip ospf cost 100
#   ospfv3 network broadcast
#   ospfv3 shutdown
# interface Ethernet1/3
#   ip ospf authentication-key 7 12090404011C03162E

- name: arse externally provided OSPF interfaces config
  cisco.nxos.nxos_ospf_interfaces:
    running_config: "{{ lookup('file', 'ospf_interfaces.cfg') }}"
    state: parsed

# Task output (redacted)
# -----------------------
# "parsed": [
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "multi_areas": [
#                        "11.11.11.11"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "1.1.1.1",
#                                "secondaries": false
#                            },
#                            "process_id": "100"
#                        }
#                    ]
#                },
#                {
#                    "afi": "ipv6",
#                    "multi_areas": [
#                        "16.10.10.10"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "2.2.2.2"
#                            },
#                            "multi_areas": [
#                                "21.0.0.0"
#                            ],
#                            "process_id": "200"
#                        },
#                        {
#                            "multi_areas": [
#                                "50.50.50.50"
#                            ],
#                            "process_id": "300"
#                        }
#                    ]
#                }
#            ],
#            "name": "Ethernet1/1"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication": {
#                       "enable": true,
#                       "key_chain": "test-1"
#                    },
#                    "cost": 100,
#                    "message_digest_key": {
#                        "encryption": 3,
#                        "key": "abc01d272be25d29",
#                        "key_id": 10
#                    }
#                },
#                {
#                    "afi": "ipv6",
#                    "network": "broadcast",
#                    "shutdown": true
#                }
#            ],
#            "name": "Ethernet1/2"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication_key": {
#                        "encryption": 7,
#                        "key": "12090404011C03162E"
#                    }
#                }
#            ],
#            "name": "Ethernet1/3"
#        },
# ]

# Using gathered

# On-box config

# NXOS# show running-config | section ^interface
# interface Ethernet1/1
#   no switchport
#   ip router ospf 100 area 1.1.1.1 secondaries none
#   ip router ospf multi-area 11.11.11.12
# interface Ethernet1/2
#   no switchport
#   ip ospf authentication
#   ip ospf authentication key-chain test-1
#   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
#   ip ospf cost 100
#   ospfv3 network broadcast
#   ospfv3 shutdown
# interface Ethernet1/3
#   no switchport

# Task output (redacted)
# -----------------------
# "gathered": [
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "multi_areas": [
#                        "11.11.11.12"
#                    ],
#                    "processes": [
#                        {
#                            "area": {
#                                "area_id": "1.1.1.1",
#                                "secondaries": false
#                            },
#                            "process_id": "100"
#                        }
#                    ]
#                }
#            ],
#            "name": "Ethernet1/1"
#        },
#        {
#            "address_family": [
#                {
#                    "afi": "ipv4",
#                    "authentication": {
#                        "enable": true,
#                        "key_chain": "test-1"
#                    },
#                    "cost": 100,
#                    "message_digest_key": {
#                        "encryption": 3,
#                        "key": "abc01d272be25d29",
#                        "key_id": 10
#                    }
#                },
#                {
#                    "afi": "ipv6",
#                    "network": "broadcast",
#                    "shutdown": true
#                }
#            ],
#            "name": "Ethernet1/2"
#        },
#        {
#            "name": "Ethernet1/3"
#        },
"""
RETURN = """
before:
  description: The configuration prior to the model invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The resulting configuration model invocation.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample:
    - interface Ethernet1/1
    - ip router ospf multi-area 11.11.11.11
    - ip router ospf 100 area 1.1.1.1 secondaries none
    - no ipv6 router ospfv3 multi-area 16.10.10.10
    - ipv6 router ospfv3 200 area 2.2.2.2
    - ipv6 router ospfv3 200 multi-area 21.0.0.0
    - ipv6 router ospfv3 300 multi-area 50.50.50.50
    - interface Ethernet1/2
    - no ip ospf authentication key-chain test-1
    - ip ospf authentication
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.ospf_interfaces.ospf_interfaces import (
    Ospf_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.ospf_interfaces.ospf_interfaces import (
    Ospf_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Ospf_interfacesArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Ospf_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
