.. _vyos.vyos.vyos_lag_interfaces_module:


*****************************
vyos.vyos.vyos_lag_interfaces
*****************************

**LAG interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages attributes of link aggregation groups on VyOS network devices.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="3">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A list of link aggregation group configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>arp_monitor</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>ARP Link monitoring parameters.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>ARP link monitoring frequency in milliseconds.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>target</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IP address to use for ARP monitoring.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hash_policy</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>layer2</li>
                                    <li>layer2+3</li>
                                    <li>layer3+4</li>
                        </ul>
                </td>
                <td>
                        <div>LAG or bonding transmit hash policy.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>members</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of member interfaces for the LAG (bond).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>member</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the member interface.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mode</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>802.3ad</li>
                                    <li>active-backup</li>
                                    <li>broadcast</li>
                                    <li>round-robin</li>
                                    <li>transmit-load-balance</li>
                                    <li>adaptive-load-balance</li>
                                    <li>xor-hash</li>
                        </ul>
                </td>
                <td>
                        <div>LAG or bond mode.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the link aggregation group (LAG) or bond.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>primary</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Primary device interfaces for the LAG (bond).</div>
                </td>
            </tr>

            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>running_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This option is used only with state <em>parsed</em>.</div>
                        <div>The value of this option should be the output received from the VyOS device by executing the command <b>show configuration commands | grep bond</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>merged</b>&nbsp;&larr;</div></li>
                                    <li>replaced</li>
                                    <li>overridden</li>
                                    <li>deleted</li>
                                    <li>parsed</li>
                                    <li>gathered</li>
                                    <li>rendered</li>
                        </ul>
                </td>
                <td>
                        <div>The state of the configuration after module completion.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against VyOS 1.1.8 (helium).
   - This module works with connection ``network_cli``. See `the VyOS OS Platform Options <../network/user_guide/platform_vyos.html>`_.



Examples
--------

.. code-block:: yaml

    # Using merged
    #
    # Before state:
    # -------------
    #
    # vyos@vyos:~$ show configuration  commands | grep bond
    # set interfaces bonding bond2
    # set interfaces bonding bond3
    #
    - name: Merge provided configuration with device configuration
      vyos.vyos.vyos_lag_interfaces:
        config:
        - name: bond2
          mode: active-backup
          members:
          - member: eth2
          - member: eth1
          hash_policy: layer2
          primary: eth2

        - name: bond3
          mode: active-backup
          hash_policy: layer2+3
          members:
          - member: eth3
          primary: eth3
        state: merged
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #    "before": [
    #        {
    #            "name": "bond2"
    #        },
    #        {
    #            "name": "bond3"
    #        }
    #    ],
    #
    # "commands": [
    #        "set interfaces bonding bond2 hash-policy 'layer2'",
    #        "set interfaces bonding bond2 mode 'active-backup'",
    #        "set interfaces ethernet eth2 bond-group bond2",
    #        "set interfaces ethernet eth1 bond-group bond2",
    #        "set interfaces bonding bond2 primary 'eth2'",
    #        "set interfaces bonding bond3 hash-policy 'layer2+3'",
    #        "set interfaces bonding bond3 mode 'active-backup'",
    #        "set interfaces ethernet eth3 bond-group bond3",
    #        "set interfaces bonding bond3 primary 'eth3'"
    #    ]
    #
    #     "after": [
    #        {
    #            "hash_policy": "layer2",
    #            "members": [
    #                {
    #                    "member": "eth1"
    #                },
    #                {
    #                    "member": "eth2"
    #                }
    #            ],
    #            "mode": "active-backup",
    #            "name": "bond2",
    #            "primary": "eth2"
    #        },
    #        {
    #            "hash_policy": "layer2+3",
    #            "members": [
    #                {
    #                    "member": "eth3"
    #                }
    #            ],
    #            "mode": "active-backup",
    #            "name": "bond3",
    #            "primary": "eth3"
    #        }
    #    ]
    #
    # After state:
    # -------------
    #
    # vyos@vyos:~$ show configuration  commands | grep bond
    # set interfaces bonding bond2 hash-policy 'layer2'
    # set interfaces bonding bond2 mode 'active-backup'
    # set interfaces bonding bond2 primary 'eth2'
    # set interfaces bonding bond3 hash-policy 'layer2+3'
    # set interfaces bonding bond3 mode 'active-backup'
    # set interfaces bonding bond3 primary 'eth3'
    # set interfaces ethernet eth1 bond-group 'bond2'
    # set interfaces ethernet eth2 bond-group 'bond2'
    # set interfaces ethernet eth3 bond-group 'bond3'


    # Using replaced
    #
    # Before state:
    # -------------
    #
    # vyos@vyos:~$ show configuration  commands | grep bond
    # set interfaces bonding bond2 hash-policy 'layer2'
    # set interfaces bonding bond2 mode 'active-backup'
    # set interfaces bonding bond2 primary 'eth2'
    # set interfaces bonding bond3 hash-policy 'layer2+3'
    # set interfaces bonding bond3 mode 'active-backup'
    # set interfaces bonding bond3 primary 'eth3'
    # set interfaces ethernet eth1 bond-group 'bond2'
    # set interfaces ethernet eth2 bond-group 'bond2'
    # set interfaces ethernet eth3 bond-group 'bond3'
    #
    - name: Replace device configurations of listed LAGs with provided configurations
      vyos.vyos.vyos_lag_interfaces:
        config:
        - name: bond3
          mode: 802.3ad
          hash_policy: layer2
          members:
          - member: eth3
        state: replaced
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #    "before": [
    #        {
    #            "hash_policy": "layer2",
    #            "members": [
    #                {
    #                    "member": "eth1"
    #                },
    #                {
    #                    "member": "eth2"
    #                }
    #            ],
    #            "mode": "active-backup",
    #            "name": "bond2",
    #            "primary": "eth2"
    #        },
    #        {
    #            "hash_policy": "layer2+3",
    #            "members": [
    #                {
    #                    "member": "eth3"
    #                }
    #            ],
    #            "mode": "active-backup",
    #            "name": "bond3",
    #            "primary": "eth3"
    #        }
    #    ],
    #
    # "commands": [
    #        "delete interfaces bonding bond3 primary",
    #        "set interfaces bonding bond3 hash-policy 'layer2'",
    #        "set interfaces bonding bond3 mode '802.3ad'"
    #    ],
    #
    # "after": [
    #        {
    #            "hash_policy": "layer2",
    #            "members": [
    #                {
    #                    "member": "eth1"
    #                },
    #                {
    #                    "member": "eth2"
    #                }
    #            ],
    #            "mode": "active-backup",
    #            "name": "bond2",
    #            "primary": "eth2"
    #        },
    #        {
    #            "hash_policy": "layer2",
    #            "members": [
    #                {
    #                    "member": "eth3"
    #                }
    #            ],
    #            "mode": "802.3ad",
    #            "name": "bond3"
    #        }
    #    ],
    #
    # After state:
    # -------------
    #
    # vyos@vyos:~$ show configuration  commands | grep bond
    # set interfaces bonding bond2 hash-policy 'layer2'
    # set interfaces bonding bond2 mode 'active-backup'
    # set interfaces bonding bond2 primary 'eth2'
    # set interfaces bonding bond3 hash-policy 'layer2'
    # set interfaces bonding bond3 mode '802.3ad'
    # set interfaces ethernet eth1 bond-group 'bond2'
    # set interfaces ethernet eth2 bond-group 'bond2'
    # set interfaces ethernet eth3 bond-group 'bond3'


    # Using overridden
    #
    # Before state
    # --------------
    #
    # vyos@vyos:~$ show configuration  commands | grep bond
    # set interfaces bonding bond2 hash-policy 'layer2'
    # set interfaces bonding bond2 mode 'active-backup'
    # set interfaces bonding bond2 primary 'eth2'
    # set interfaces bonding bond3 hash-policy 'layer2'
    # set interfaces bonding bond3 mode '802.3ad'
    # set interfaces ethernet eth1 bond-group 'bond2'
    # set interfaces ethernet eth2 bond-group 'bond2'
    # set interfaces ethernet eth3 bond-group 'bond3'
    #
    - name: Overrides all device configuration with provided configuration
      vyos.vyos.vyos_lag_interfaces:
        config:
        - name: bond3
          mode: active-backup
          members:
          - member: eth1
          - member: eth2
          - member: eth3
          primary: eth3
          hash_policy: layer2
        state: overridden
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #    "before": [
    #        {
    #            "hash_policy": "layer2",
    #            "members": [
    #                {
    #                    "member": "eth1"
    #                },
    #                {
    #                    "member": "eth2"
    #                }
    #            ],
    #            "mode": "active-backup",
    #            "name": "bond2",
    #            "primary": "eth2"
    #        },
    #        {
    #            "hash_policy": "layer2",
    #            "members": [
    #                {
    #                    "member": "eth3"
    #                }
    #            ],
    #            "mode": "802.3ad",
    #            "name": "bond3"
    #        }
    #    ],
    #
    #    "commands": [
    #        "delete interfaces bonding bond2 hash-policy",
    #        "delete interfaces ethernet eth1 bond-group bond2",
    #        "delete interfaces ethernet eth2 bond-group bond2",
    #        "delete interfaces bonding bond2 mode",
    #        "delete interfaces bonding bond2 primary",
    #        "set interfaces bonding bond3 mode 'active-backup'",
    #        "set interfaces ethernet eth1 bond-group bond3",
    #        "set interfaces ethernet eth2 bond-group bond3",
    #        "set interfaces bonding bond3 primary 'eth3'"
    #    ],
    #
    # "after": [
    #        {
    #            "name": "bond2"
    #        },
    #        {
    #            "hash_policy": "layer2",
    #            "members": [
    #                {
    #                    "member": "eth1"
    #                },
    #                {
    #                    "member": "eth2"
    #                },
    #                {
    #                    "member": "eth3"
    #                }
    #            ],
    #            "mode": "active-backup",
    #            "name": "bond3",
    #            "primary": "eth3"
    #        }
    #    ],
    #
    #
    # After state
    # ------------
    #
    # vyos@vyos:~$ show configuration  commands | grep bond
    # set interfaces bonding bond2
    # set interfaces bonding bond3 hash-policy 'layer2'
    # set interfaces bonding bond3 mode 'active-backup'
    # set interfaces bonding bond3 primary 'eth3'
    # set interfaces ethernet eth1 bond-group 'bond3'
    # set interfaces ethernet eth2 bond-group 'bond3'
    # set interfaces ethernet eth3 bond-group 'bond3'


    # Using deleted
    #
    # Before state
    # -------------
    #
    # vyos@vyos:~$ show configuration  commands | grep bond
    # set interfaces bonding bond2 hash-policy 'layer2'
    # set interfaces bonding bond2 mode 'active-backup'
    # set interfaces bonding bond2 primary 'eth2'
    # set interfaces bonding bond3 hash-policy 'layer2+3'
    # set interfaces bonding bond3 mode 'active-backup'
    # set interfaces bonding bond3 primary 'eth3'
    # set interfaces ethernet eth1 bond-group 'bond2'
    # set interfaces ethernet eth2 bond-group 'bond2'
    # set interfaces ethernet eth3 bond-group 'bond3'
    #
    - name: Delete LAG attributes of given interfaces (Note This won't delete the interface
        itself)
      vyos.vyos.vyos_lag_interfaces:
        config:
        - name: bond2
        - name: bond3
        state: deleted
    #
    #
    # ------------------------
    # Module Execution Results
    # ------------------------
    #
    # "before": [
    #        {
    #            "hash_policy": "layer2",
    #            "members": [
    #                {
    #                    "member": "eth1"
    #                },
    #                {
    #                    "member": "eth2"
    #                }
    #            ],
    #            "mode": "active-backup",
    #            "name": "bond2",
    #            "primary": "eth2"
    #        },
    #        {
    #            "hash_policy": "layer2+3",
    #            "members": [
    #                {
    #                    "member": "eth3"
    #                }
    #            ],
    #            "mode": "active-backup",
    #            "name": "bond3",
    #            "primary": "eth3"
    #        }
    #    ],
    # "commands": [
    #        "delete interfaces bonding bond2 hash-policy",
    #        "delete interfaces ethernet eth1 bond-group bond2",
    #        "delete interfaces ethernet eth2 bond-group bond2",
    #        "delete interfaces bonding bond2 mode",
    #        "delete interfaces bonding bond2 primary",
    #        "delete interfaces bonding bond3 hash-policy",
    #        "delete interfaces ethernet eth3 bond-group bond3",
    #        "delete interfaces bonding bond3 mode",
    #        "delete interfaces bonding bond3 primary"
    #    ],
    #
    # "after": [
    #        {
    #            "name": "bond2"
    #        },
    #        {
    #            "name": "bond3"
    #        }
    #    ],
    #
    # After state
    # ------------
    # vyos@vyos:~$ show configuration  commands | grep bond
    # set interfaces bonding bond2
    # set interfaces bonding bond3


    # Using gathered
    #
    # Before state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep bond
    # set interfaces bonding bond0 hash-policy 'layer2'
    # set interfaces bonding bond0 mode 'active-backup'
    # set interfaces bonding bond0 primary 'eth1'
    # set interfaces bonding bond1 hash-policy 'layer2+3'
    # set interfaces bonding bond1 mode 'active-backup'
    # set interfaces bonding bond1 primary 'eth2'
    # set interfaces ethernet eth1 bond-group 'bond0'
    # set interfaces ethernet eth2 bond-group 'bond1'
    #
    - name: Gather listed  lag interfaces with provided configurations
      vyos.vyos.vyos_lag_interfaces:
        config:
        state: gathered
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #    "gathered": [
    #        {
    #            "afi": "ipv6",
    #            "rule_sets": [
    #                {
    #                    "default_action": "accept",
    #                    "description": "This is ipv6 specific rule-set",
    #                    "name": "UPLINK",
    #                    "rules": [
    #                        {
    #                            "action": "accept",
    #                            "description": "Fwipv6-Rule 1 is configured by Ansible",
    #                            "ipsec": "match-ipsec",
    #                            "number": 1
    #                        },
    #                        {
    #                            "action": "accept",
    #                            "description": "Fwipv6-Rule 2 is configured by Ansible",
    #                            "ipsec": "match-ipsec",
    #                            "number": 2
    #                        }
    #                    ]
    #                }
    #            ]
    #        },
    #        {
    #            "afi": "ipv4",
    #            "rule_sets": [
    #                {
    #                    "default_action": "accept",
    #                    "description": "IPv4 INBOUND rule set",
    #                    "name": "INBOUND",
    #                    "rules": [
    #                        {
    #                            "action": "accept",
    #                            "description": "Rule 101 is configured by Ansible",
    #                            "ipsec": "match-ipsec",
    #                            "number": 101
    #                        },
    #                        {
    #                            "action": "reject",
    #                            "description": "Rule 102 is configured by Ansible",
    #                            "ipsec": "match-ipsec",
    #                            "number": 102
    #                        },
    #                        {
    #                            "action": "accept",
    #                            "description": "Rule 103 is configured by Ansible",
    #                            "destination": {
    #                                "group": {
    #                                    "address_group": "inbound"
    #                                }
    #                            },
    #                            "number": 103,
    #                            "source": {
    #                                "address": "192.0.2.0"
    #                            },
    #                            "state": {
    #                                "established": true,
    #                                "invalid": false,
    #                                "new": false,
    #                                "related": true
    #                            }
    #                        }
    #                    ]
    #                }
    #            ]
    #        }
    #    ]
    #
    #
    # After state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep bond
    # set interfaces bonding bond0 hash-policy 'layer2'
    # set interfaces bonding bond0 mode 'active-backup'
    # set interfaces bonding bond0 primary 'eth1'
    # set interfaces bonding bond1 hash-policy 'layer2+3'
    # set interfaces bonding bond1 mode 'active-backup'
    # set interfaces bonding bond1 primary 'eth2'
    # set interfaces ethernet eth1 bond-group 'bond0'
    # set interfaces ethernet eth2 bond-group 'bond1'


    # Using rendered
    #
    #
    - name: Render the commands for provided  configuration
      vyos.vyos.vyos_lag_interfaces:
        config:
        - name: bond0
          hash_policy: layer2
          members:
          - member: eth1
          mode: active-backup
          primary: eth1
        - name: bond1
          hash_policy: layer2+3
          members:
          - member: eth2
          mode: active-backup
          primary: eth2
        state: rendered
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #
    # "rendered": [
    #        "set interfaces bonding bond0 hash-policy 'layer2'",
    #        "set interfaces ethernet eth1 bond-group 'bond0'",
    #        "set interfaces bonding bond0 mode 'active-backup'",
    #        "set interfaces bonding bond0 primary 'eth1'",
    #        "set interfaces bonding bond1 hash-policy 'layer2+3'",
    #        "set interfaces ethernet eth2 bond-group 'bond1'",
    #        "set interfaces bonding bond1 mode 'active-backup'",
    #        "set interfaces bonding bond1 primary 'eth2'"
    #    ]


    # Using parsed
    #
    #
    - name: Parsed the commands for provided  configuration
      vyos.vyos.vyos_l3_interfaces:
        running_config:
          "set interfaces bonding bond0 hash-policy 'layer2'
           set interfaces bonding bond0 mode 'active-backup'
           set interfaces bonding bond0 primary 'eth1'
           set interfaces bonding bond1 hash-policy 'layer2+3'
           set interfaces bonding bond1 mode 'active-backup'
           set interfaces bonding bond1 primary 'eth2'
           set interfaces ethernet eth1 bond-group 'bond0'
           set interfaces ethernet eth2 bond-group 'bond1'"
        state: parsed
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #
    # "parsed": [
    #         {
    #             "hash_policy": "layer2",
    #             "members": [
    #                 {
    #                     "member": "eth1"
    #                 }
    #             ],
    #             "mode": "active-backup",
    #             "name": "bond0",
    #             "primary": "eth1"
    #         },
    #         {
    #             "hash_policy": "layer2+3",
    #             "members": [
    #                 {
    #                     "member": "eth2"
    #                 }
    #             ],
    #             "mode": "active-backup",
    #             "name": "bond1",
    #             "primary": "eth2"
    #         }
    #     ]



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>after</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when changed</td>
                <td>
                            <div>The configuration as structured data after module completion.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format
     of the parameters above.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>before</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The configuration as structured data prior to module invocation.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format
     of the parameters above.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>commands</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;set interfaces bonding bond2&#x27;, &#x27;set interfaces bonding bond2 hash-policy layer2&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Rohit Thakur (@rohitthakur2590)
