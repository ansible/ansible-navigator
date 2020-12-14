.. _vyos.vyos.vyos_ospf_interfaces_module:


******************************
vyos.vyos.vyos_ospf_interfaces
******************************

**OSPF Interfaces Resource Module.**


Version added: 1.2.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages OSPF configuration of interfaces on devices running VYOS.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="5">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="5">
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
                        <div>A list of OSPF configuration for interfaces.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address_family</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPF settings on the interfaces in address-family context.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>afi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ipv4</li>
                                    <li>ipv6</li>
                        </ul>
                </td>
                <td>
                        <div>Address Family Identifier (AFI) for OSPF settings on the interfaces.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authentication</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication settings on the interface.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>md5_key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>md5 parameters.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>md5 key.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>key id.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>plaintext_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Plain Text password.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bandwidth</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Bandwidth of interface (kilobits/sec)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cost</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>metric associated with interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dead_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Time interval to detect a dead router.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hello_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Timer interval between transmission of hello packets.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ifmtu</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>interface MTU.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>instance</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Instance ID.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mtu_ignore</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>if True, Disable MTU check for Database Description packets.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>network</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface type.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>passive</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>If True, disables forming adjacency.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>priority</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface priority.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>retransmit_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>LSA retransmission interval.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>transmit_delay</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>LSA transmission delay.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name/Identifier of the interface.</div>
                </td>
            </tr>

            <tr>
                <td colspan="5">
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>sh running-config | section ^interface</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="5">
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
                                    <li>gathered</li>
                                    <li>parsed</li>
                                    <li>rendered</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    # Using merged
    #
    # Before state:
    # -------------
    #

    # @vyos:~$ show configuration commands | match "ospf"

      - name: Merge provided configuration with device configuration
        vyos.vyos.vyos_ospf_interfaces:
          config:
            - name: "eth1"
              address_family:
                - afi: "ipv4"
                  transmit_delay: 50
                  priority: 26
                  network: "point-to-point"
                - afi: "ipv6"
                  dead_interval: 39
            - name: "bond2"
              address_family:
                - afi: "ipv4"
                  transmit_delay: 45
                  bandwidth: 70
                  authentication:
                    md5_key:
                      key_id: 10
                      key: "1111111111232345"
                - afi: "ipv6"
                  passive: True
          state: merged

    # After State:
    # --------------

    # vyos@vyos:~$ show configuration commands | match "ospf"
    # set interfaces bonding bond2 ip ospf authentication md5 key-id 10 md5-key '1111111111232345'
    # set interfaces bonding bond2 ip ospf bandwidth '70'
    # set interfaces bonding bond2 ip ospf transmit-delay '45'
    # set interfaces bonding bond2 ipv6 ospfv3 'passive'
    # set interfaces ethernet eth1 ip ospf network 'point-to-point'
    # set interfaces ethernet eth1 ip ospf priority '26'
    # set interfaces ethernet eth1 ip ospf transmit-delay '50'
    # set interfaces ethernet eth1 ipv6 ospfv3 dead-interval '39'

    # "after": [
    #        "
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication": {
    #                        "md5_key": {
    #                            "key": "1111111111232345",
    #                            "key_id": 10
    #                        }
    #                    },
    #                    "bandwidth": 70,
    #                    "transmit_delay": 45
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "passive": true
    #                }
    #            ],
    #            "name": "bond2"
    #        },
    #        {
    #            "name": "eth0"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "network": "point-to-point",
    #                    "priority": 26,
    #                    "transmit_delay": 50
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "dead_interval": 39
    #                }
    #            ],
    #            "name": "eth1"
    #        },
    #        {
    #            "name": "eth2"
    #        },
    #        {
    #            "name": "eth3"
    #        }
    #    ],
    #    "before": [
    #        {
    #            "name": "eth0"
    #        },
    #        {
    #            "name": "eth1"
    #        },
    #        {
    #            "name": "eth2"
    #        },
    #        {
    #            "name": "eth3"
    #        }
    #    ],
    #    "changed": true,
    #    "commands": [
    #        "set interfaces ethernet eth1 ip ospf transmit-delay 50",
    #        "set interfaces ethernet eth1 ip ospf priority 26",
    #        "set interfaces ethernet eth1 ip ospf network point-to-point",
    #        "set interfaces ethernet eth1 ipv6 ospfv3 dead-interval 39",
    #        "set interfaces bonding bond2 ip ospf transmit-delay 45",
    #        "set interfaces bonding bond2 ip ospf bandwidth 70",
    #        "set interfaces bonding bond2 ip ospf authentication md5 key-id 10 md5-key 1111111111232345",
    #        "set interfaces bonding bond2 ipv6 ospfv3 passive"
    #    ],




    # Using replaced:

    # Before State:
    # ------------

    # vyos@vyos:~$ show configuration commands | match "ospf"
    # set interfaces bonding bond2 ip ospf authentication md5 key-id 10 md5-key '1111111111232345'
    # set interfaces bonding bond2 ip ospf bandwidth '70'
    # set interfaces bonding bond2 ip ospf transmit-delay '45'
    # set interfaces bonding bond2 ipv6 ospfv3 'passive'
    # set interfaces ethernet eth1 ip ospf network 'point-to-point'
    # set interfaces ethernet eth1 ip ospf priority '26'
    # set interfaces ethernet eth1 ip ospf transmit-delay '50'
    # set interfaces ethernet eth1 ipv6 ospfv3 dead-interval '39'

      - name: Replace provided configuration with device configuration
        vyos.vyos.vyos_ospf_interfaces:
          config:
            - name: "eth1"
              address_family:
                - afi: "ipv4"
                  cost: 100
                - afi: "ipv6"
                  ifmtu: 33
            - name: "bond2"
              address_family:
                - afi: "ipv4"
                  transmit_delay: 45
                - afi: "ipv6"
                  passive: True
          state: replaced

    # After State:
    # -----------

    # vyos@vyos:~$ show configuration commands | match "ospf"
    # set interfaces bonding bond2 ip ospf transmit-delay '45'
    # set interfaces bonding bond2 ipv6 ospfv3 'passive'
    # set interfaces ethernet eth1 ip ospf cost '100'
    # set interfaces ethernet eth1 ipv6 ospfv3 ifmtu '33'
    # vyos@vyos:~$

    # Module Execution
    # ----------------
    #    "after": [
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "transmit_delay": 45
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "passive": true
    #                }
    #            ],
    #            "name": "bond2"
    #        },
    #        {
    #            "name": "eth0"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "cost": 100
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "ifmtu": 33
    #                }
    #            ],
    #            "name": "eth1"
    #        },
    #        {
    #            "name": "eth2"
    #        },
    #        {
    #            "name": "eth3"
    #        }
    #    ],
    #    "before": [
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication": {
    #                        "md5_key": {
    #                            "key": "1111111111232345",
    #                            "key_id": 10
    #                        }
    #                    },
    #                    "bandwidth": 70,
    #                    "transmit_delay": 45
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "passive": true
    #                }
    #            ],
    #            "name": "bond2"
    #        },
    #        {
    #            "name": "eth0"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "network": "point-to-point",
    #                    "priority": 26,
    #                    "transmit_delay": 50
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "dead_interval": 39
    #                }
    #            ],
    #            "name": "eth1"
    #        },
    #        {
    #            "name": "eth2"
    #        },
    #        {
    #            "name": "eth3"
    #        }
    #    ],
    #    "changed": true,
    #    "commands": [
    #        "set interfaces ethernet eth1 ip ospf cost 100",
    #        "set interfaces ethernet eth1 ipv6 ospfv3 ifmtu 33",
    #        "delete interfaces ethernet eth1 ip ospf network point-to-point",
    #        "delete interfaces ethernet eth1 ip ospf priority 26",
    #        "delete interfaces ethernet eth1 ip ospf transmit-delay 50",
    #        "delete interfaces ethernet eth1 ipv6 ospfv3 dead-interval 39",
    #        "delete interfaces bonding bond2 ip ospf authentication",
    #        "delete interfaces bonding bond2 ip ospf bandwidth 70"
    #    ],
    #

    # Using Overridden:
    # -----------------

    # Before State:
    # ------------

    # vyos@vyos:~$ show configuration commands | match "ospf"
    # set interfaces bonding bond2 ip ospf authentication md5 key-id 10 md5-key '1111111111232345'
    # set interfaces bonding bond2 ip ospf bandwidth '70'
    # set interfaces bonding bond2 ip ospf transmit-delay '45'
    # set interfaces bonding bond2 ipv6 ospfv3 'passive'
    # set interfaces ethernet eth1 ip ospf cost '100'
    # set interfaces ethernet eth1 ip ospf network 'point-to-point'
    # set interfaces ethernet eth1 ip ospf priority '26'
    # set interfaces ethernet eth1 ip ospf transmit-delay '50'
    # set interfaces ethernet eth1 ipv6 ospfv3 dead-interval '39'
    # set interfaces ethernet eth1 ipv6 ospfv3 ifmtu '33'
    # vyos@vyos:~$

      - name: Override device configuration with provided configuration
        vyos.vyos.vyos_ospf_interfaces:
          config:
            - name: "eth0"
              address_family:
                - afi: "ipv4"
                  cost: 100
                - afi: "ipv6"
                  ifmtu: 33
                  passive: True
          state: overridden
    # After State:
    # -----------

    # 200~vyos@vyos:~$ show configuration commands | match "ospf"
    # set interfaces ethernet eth0 ip ospf cost '100'
    # set interfaces ethernet eth0 ipv6 ospfv3 ifmtu '33'
    # set interfaces ethernet eth0 ipv6 ospfv3 'passive'
    # vyos@vyos:~$
    #
    #
    #     "after": [
    #         {
    #             "name": "bond2"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "cost": 100
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "ifmtu": 33,
    #                     "passive": true
    #                 }
    #             ],
    #             "name": "eth0"
    #         },
    #         {
    #             "name": "eth1"
    #         },
    #         {
    #             "name": "eth2"
    #         },
    #         {
    #             "name": "eth3"
    #         }
    #     ],
    #     "before": [
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "authentication": {
    #                         "md5_key": {
    #                             "key": "1111111111232345",
    #                             "key_id": 10
    #                         }
    #                     },
    #                     "bandwidth": 70,
    #                     "transmit_delay": 45
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "passive": true
    #                 }
    #             ],
    #             "name": "bond2"
    #         },
    #         {
    #             "name": "eth0"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "cost": 100,
    #                     "network": "point-to-point",
    #                     "priority": 26,
    #                     "transmit_delay": 50
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "dead_interval": 39,
    #                     "ifmtu": 33
    #                 }
    #             ],
    #             "name": "eth1"
    #         },
    #         {
    #             "name": "eth2"
    #         },
    #         {
    #             "name": "eth3"
    #         }
    #     ],
    #     "changed": true,
    #     "commands": [
    #         "delete interfaces bonding bond2 ip ospf",
    #         "delete interfaces bonding bond2 ipv6 ospfv3",
    #         "delete interfaces ethernet eth1 ip ospf",
    #         "delete interfaces ethernet eth1 ipv6 ospfv3",
    #         "set interfaces ethernet eth0 ip ospf cost 100",
    #         "set interfaces ethernet eth0 ipv6 ospfv3 ifmtu 33",
    #         "set interfaces ethernet eth0 ipv6 ospfv3 passive"
    #     ],
    #

    # Using deleted:
    # -------------

    # before state:
    # -------------

    # vyos@vyos:~$ show configuration commands | match "ospf"
    # set interfaces bonding bond2 ip ospf authentication md5 key-id 10 md5-key '1111111111232345'
    # set interfaces bonding bond2 ip ospf bandwidth '70'
    # set interfaces bonding bond2 ip ospf transmit-delay '45'
    # set interfaces bonding bond2 ipv6 ospfv3 'passive'
    # set interfaces ethernet eth0 ip ospf cost '100'
    # set interfaces ethernet eth0 ipv6 ospfv3 ifmtu '33'
    # set interfaces ethernet eth0 ipv6 ospfv3 'passive'
    # set interfaces ethernet eth1 ip ospf network 'point-to-point'
    # set interfaces ethernet eth1 ip ospf priority '26'
    # set interfaces ethernet eth1 ip ospf transmit-delay '50'
    # set interfaces ethernet eth1 ipv6 ospfv3 dead-interval '39'
    # vyos@vyos:~$

      - name: Delete device configuration
        vyos.vyos.vyos_ospf_interfaces:
          config:
            - name: "eth0"
          state: deleted

    # After State:
    # -----------

    # vyos@vyos:~$ show configuration commands | match "ospf"
    # set interfaces bonding bond2 ip ospf authentication md5 key-id 10 md5-key '1111111111232345'
    # set interfaces bonding bond2 ip ospf bandwidth '70'
    # set interfaces bonding bond2 ip ospf transmit-delay '45'
    # set interfaces bonding bond2 ipv6 ospfv3 'passive'
    # set interfaces ethernet eth1 ip ospf network 'point-to-point'
    # set interfaces ethernet eth1 ip ospf priority '26'
    # set interfaces ethernet eth1 ip ospf transmit-delay '50'
    # set interfaces ethernet eth1 ipv6 ospfv3 dead-interval '39'
    # vyos@vyos:~$
    #
    #
    # "after": [
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "authentication": {
    #                         "md5_key": {
    #                             "key": "1111111111232345",
    #                             "key_id": 10
    #                         }
    #                     },
    #                     "bandwidth": 70,
    #                     "transmit_delay": 45
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "passive": true
    #                 }
    #             ],
    #             "name": "bond2"
    #         },
    #         {
    #             "name": "eth0"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "network": "point-to-point",
    #                     "priority": 26,
    #                     "transmit_delay": 50
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "dead_interval": 39
    #                 }
    #             ],
    #             "name": "eth1"
    #         },
    #         {
    #             "name": "eth2"
    #         },
    #         {
    #             "name": "eth3"
    #         }
    #     ],
    #     "before": [
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "authentication": {
    #                         "md5_key": {
    #                             "key": "1111111111232345",
    #                             "key_id": 10
    #                         }
    #                     },
    #                     "bandwidth": 70,
    #                     "transmit_delay": 45
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "passive": true
    #                 }
    #             ],
    #             "name": "bond2"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "cost": 100
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "ifmtu": 33,
    #                     "passive": true
    #                 }
    #             ],
    #             "name": "eth0"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "network": "point-to-point",
    #                     "priority": 26,
    #                     "transmit_delay": 50
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "dead_interval": 39
    #                 }
    #             ],
    #             "name": "eth1"
    #         },
    #         {
    #             "name": "eth2"
    #         },
    #         {
    #             "name": "eth3"
    #         }
    #     ],
    #     "changed": true,
    #     "commands": [
    #         "delete interfaces ethernet eth0 ip ospf",
    #         "delete interfaces ethernet eth0 ipv6 ospfv3"
    #     ],
    #
    # Using parsed:
    # parsed.cfg:

    # set interfaces bonding bond2 ip ospf authentication md5 key-id 10 md5-key '1111111111232345'
    # set interfaces bonding bond2 ip ospf bandwidth '70'
    # set interfaces bonding bond2 ip ospf transmit-delay '45'
    # set interfaces bonding bond2 ipv6 ospfv3 'passive'
    # set interfaces ethernet eth0 ip ospf cost '50'
    # set interfaces ethernet eth0 ip ospf priority '26'
    # set interfaces ethernet eth0 ipv6 ospfv3 instance-id '33'
    # set interfaces ethernet eth0 ipv6 ospfv3 'mtu-ignore'
    # set interfaces ethernet eth1 ip ospf network 'point-to-point'
    # set interfaces ethernet eth1 ip ospf priority '26'
    # set interfaces ethernet eth1 ip ospf transmit-delay '50'
    # set interfaces ethernet eth1 ipv6 ospfv3 dead-interval '39'
    #

      - name: parse configs
        vyos.vyos.vyos_ospf_interfaces:
          running_config: "{{ lookup('file', './parsed.cfg') }}"
          state: parsed

    # Module Execution:
    # ----------------

    #  "parsed": [
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "authentication": {
    #                         "md5_key": {
    #                             "key": "1111111111232345",
    #                             "key_id": 10
    #                         }
    #                     },
    #                     "bandwidth": 70,
    #                     "transmit_delay": 45
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "passive": true
    #                 }
    #             ],
    #             "name": "bond2"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "cost": 50,
    #                     "priority": 26
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "instance": "33",
    #                     "mtu_ignore": true
    #                 }
    #             ],
    #             "name": "eth0"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "network": "point-to-point",
    #                     "priority": 26,
    #                     "transmit_delay": 50
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "dead_interval": 39
    #                 }
    #             ],
    #             "name": "eth1"
    #         }
    #     ]

    # Using rendered:
    # --------------

      - name: Render
        vyos.vyos.vyos_ospf_interfaces:
          config:
            - name: "eth1"
              address_family:
                - afi: "ipv4"
                  transmit_delay: 50
                  priority: 26
                  network: "point-to-point"
                - afi: "ipv6"
                  dead_interval: 39
            - name: "bond2"
              address_family:
                - afi: "ipv4"
                  transmit_delay: 45
                  bandwidth: 70
                  authentication:
                    md5_key:
                      key_id: 10
                      key: "1111111111232345"
                - afi: "ipv6"
                  passive: True
          state: rendered

    # Module Execution:
    # ----------------

    #    "rendered": [
    #        "set interfaces ethernet eth1 ip ospf transmit-delay 50",
    #        "set interfaces ethernet eth1 ip ospf priority 26",
    #        "set interfaces ethernet eth1 ip ospf network point-to-point",
    #        "set interfaces ethernet eth1 ipv6 ospfv3 dead-interval 39",
    #        "set interfaces bonding bond2 ip ospf transmit-delay 45",
    #        "set interfaces bonding bond2 ip ospf bandwidth 70",
    #        "set interfaces bonding bond2 ip ospf authentication md5 key-id 10 md5-key 1111111111232345",
    #        "set interfaces bonding bond2 ipv6 ospfv3 passive"
    #    ]
    #

    # Using Gathered:
    # --------------

    # Native Config:

    # vyos@vyos:~$ show configuration commands | match "ospf"
    # set interfaces bonding bond2 ip ospf authentication md5 key-id 10 md5-key '1111111111232345'
    # set interfaces bonding bond2 ip ospf bandwidth '70'
    # set interfaces bonding bond2 ip ospf transmit-delay '45'
    # set interfaces bonding bond2 ipv6 ospfv3 'passive'
    # set interfaces ethernet eth1 ip ospf network 'point-to-point'
    # set interfaces ethernet eth1 ip ospf priority '26'
    # set interfaces ethernet eth1 ip ospf transmit-delay '50'
    # set interfaces ethernet eth1 ipv6 ospfv3 dead-interval '39'
    # vyos@vyos:~$

      - name: gather configs
        vyos.vyos.vyos_ospf_interfaces:
          state: gathered

    # Module Execution:
    # -----------------

    #    "gathered": [
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication": {
    #                        "md5_key": {
    #                            "key": "1111111111232345",
    #                            "key_id": 10
    #                        }
    #                    },
    #                    "bandwidth": 70,
    #                    "transmit_delay": 45
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "passive": true
    #                }
    #            ],
    #            "name": "bond2"
    #        },
    #        {
    #            "name": "eth0"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "network": "point-to-point",
    #                    "priority": 26,
    #                    "transmit_delay": 50
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "dead_interval": 39
    #                }
    #            ],
    #            "name": "eth1"
    #        },
    #        {
    #            "name": "eth2"
    #        },
    #        {
    #            "name": "eth3"
    #        }
    #    ],




Status
------


Authors
~~~~~~~

- Gomathi Selvi Srinivasan (@GomathiselviS)
