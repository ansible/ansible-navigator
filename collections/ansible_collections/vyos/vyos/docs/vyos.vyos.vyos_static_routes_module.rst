.. _vyos.vyos.vyos_static_routes_module:


****************************
vyos.vyos.vyos_static_routes
****************************

**Static routes resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages attributes of static routes on VyOS network devices.




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
                        <div>A provided static route configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address_families</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A dictionary specifying the address family to which the static route(s) belong.</div>
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
                        <div>Specifies the type of route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>routes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A ditionary that specify the static route configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>blackhole_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configured to silently discard packets.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>distance</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Distance for the route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This is to configure only blackhole.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dest</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>An IPv4/v6 address in CIDR notation that specifies the destination network for the static route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>next_hops</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Next hops to the specified destination.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>admin_distance</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Distance value for the route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enabled</b>
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
                        <div>Disable IPv4/v6 next-hop static route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>forward_router_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The IP address of the next hop that can be used to reach the destination network.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the outgoing interface.</div>
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
                        <div>The value of this option should be the output received from the VyOS device by executing the command <b>show configuration commands | grep static route</b>.</div>
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
                                    <li>rendered</li>
                                    <li>parsed</li>
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
    # vyos@vyos:~$ show configuration  commands | grep static
    #
    - name: Merge the provided configuration with the exisiting running configuration
      vyos.vyos.vyos_static_routes:
        config:
        - address_families:
          - afi: ipv4
            routes:
            - dest: 192.0.2.32/28
              blackhole_config:
                type: blackhole
              next_hops:
              - forward_router_address: 192.0.2.6
              - forward_router_address: 192.0.2.7
        - address_families:
          - afi: ipv6
            routes:
            - dest: 2001:db8:1000::/36
              blackhole_config:
                distance: 2
              next_hops:
              - forward_router_address: 2001:db8:2000:2::1
              - forward_router_address: 2001:db8:2000:2::2
        state: merged
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    # before": []
    #
    #    "commands": [
    #        "set protocols static route 192.0.2.32/28",
    #        "set protocols static route 192.0.2.32/28 blackhole",
    #        "set protocols static route 192.0.2.32/28 next-hop '192.0.2.6'",
    #        "set protocols static route 192.0.2.32/28 next-hop '192.0.2.7'",
    #        "set protocols static route6 2001:db8:1000::/36",
    #        "set protocols static route6 2001:db8:1000::/36 blackhole distance '2'",
    #        "set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::1'",
    #        "set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::2'"
    #    ]
    #
    # "after": [
    #        {
    #            "address_families": [
    #                {
    #                    "afi": "ipv4",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "type": "blackhole"
    #                            },
    #                            "dest": "192.0.2.32/28",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "192.0.2.6"
    #                                },
    #                                {
    #                                    "forward_router_address": "192.0.2.7"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "distance": 2
    #                            },
    #                            "dest": "2001:db8:1000::/36",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::1"
    #                                },
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::2"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                }
    #            ]
    #        }
    #    ]
    #
    # After state:
    # -------------
    #
    # vyos@vyos:~$ show configuration commands| grep static
    # set protocols static route 192.0.2.32/28 'blackhole'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.6'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.7'
    # set protocols static route6 2001:db8:1000::/36 blackhole distance '2'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::1'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::2'


    # Using replaced
    #
    # Before state:
    # -------------
    #
    # vyos@vyos:~$ show configuration commands| grep static
    # set protocols static route 192.0.2.32/28 'blackhole'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.6'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.7'
    # set protocols static route 192.0.2.33/28 'blackhole'
    # set protocols static route 192.0.2.33/28 next-hop '192.0.2.3'
    # set protocols static route 192.0.2.33/28 next-hop '192.0.2.4'
    # set protocols static route6 2001:db8:1000::/36 blackhole distance '2'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::1'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::2'
    #
    - name: Replace device configurations of listed static routes with provided configurations
      vyos.vyos.vyos_static_routes:
        config:
        - address_families:
          - afi: ipv4
            routes:
            - dest: 192.0.2.32/28
              blackhole_config:
                distance: 2
              next_hops:
              - forward_router_address: 192.0.2.7
                enabled: false
              - forward_router_address: 192.0.2.9
        state: replaced
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #    "before": [
    #        {
    #            "address_families": [
    #                {
    #                    "afi": "ipv4",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "type": "blackhole"
    #                            },
    #                            "dest": "192.0.2.32/28",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "192.0.2.6"
    #                                },
    #                                {
    #                                    "forward_router_address": "192.0.2.7"
    #                                }
    #                            ]
    #                        },
    #                        {
    #                            "blackhole_config": {
    #                                "type": "blackhole"
    #                            },
    #                            "dest": "192.0.2.33/28",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "192.0.2.3"
    #                                },
    #                                {
    #                                    "forward_router_address": "192.0.2.4"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "distance": 2
    #                            },
    #                            "dest": "2001:db8:1000::/36",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::1"
    #                                },
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::2"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                }
    #            ]
    #        }
    #    ]
    #
    # "commands": [
    #        "delete protocols static route 192.0.2.32/28 next-hop '192.0.2.6'",
    #        "delete protocols static route 192.0.2.32/28 next-hop '192.0.2.7'",
    #        "set protocols static route 192.0.2.32/28 next-hop 192.0.2.7 'disable'",
    #        "set protocols static route 192.0.2.32/28 next-hop '192.0.2.7'",
    #        "set protocols static route 192.0.2.32/28 next-hop '192.0.2.9'",
    #        "set protocols static route 192.0.2.32/28 blackhole distance '2'"
    #    ]
    #
    #    "after": [
    #        {
    #            "address_families": [
    #                {
    #                    "afi": "ipv4",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "distance": 2
    #                            },
    #                            "dest": "192.0.2.32/28",
    #                            "next_hops": [
    #                                {
    #                                    "enabled": false,
    #                                    "forward_router_address": "192.0.2.7"
    #                                },
    #                                {
    #                                    "forward_router_address": "192.0.2.9"
    #                                }
    #                            ]
    #                        },
    #                        {
    #                            "blackhole_config": {
    #                                "type": "blackhole"
    #                            },
    #                            "dest": "192.0.2.33/28",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "192.0.2.3"
    #                                },
    #                                {
    #                                    "forward_router_address": "192.0.2.4"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "distance": 2
    #                            },
    #                            "dest": "2001:db8:1000::/36",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::1"
    #                                },
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::2"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                }
    #            ]
    #        }
    #    ]
    #
    # After state:
    # -------------
    #
    # vyos@vyos:~$ show configuration commands| grep static
    # set protocols static route 192.0.2.32/28 blackhole distance '2'
    # set protocols static route 192.0.2.32/28 next-hop 192.0.2.7 'disable'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.9'
    # set protocols static route 192.0.2.33/28 'blackhole'
    # set protocols static route 192.0.2.33/28 next-hop '192.0.2.3'
    # set protocols static route 192.0.2.33/28 next-hop '192.0.2.4'
    # set protocols static route6 2001:db8:1000::/36 blackhole distance '2'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::1'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::2'


    # Using overridden
    #
    # Before state
    # --------------
    #
    # vyos@vyos:~$ show configuration commands| grep static
    # set protocols static route 192.0.2.32/28 blackhole distance '2'
    # set protocols static route 192.0.2.32/28 next-hop 192.0.2.7 'disable'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.9'
    # set protocols static route6 2001:db8:1000::/36 blackhole distance '2'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::1'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::2'
    #
    - name: Overrides all device configuration with provided configuration
      vyos.vyos.vyos_static_routes:
        config:
        - address_families:
          - afi: ipv4
            routes:
            - dest: 198.0.2.48/28
              next_hops:
              - forward_router_address: 192.0.2.18
        state: overridden
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    # "before": [
    #        {
    #            "address_families": [
    #                {
    #                    "afi": "ipv4",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "distance": 2
    #                            },
    #                            "dest": "192.0.2.32/28",
    #                            "next_hops": [
    #                                {
    #                                    "enabled": false,
    #                                    "forward_router_address": "192.0.2.7"
    #                                },
    #                                {
    #                                    "forward_router_address": "192.0.2.9"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "distance": 2
    #                            },
    #                            "dest": "2001:db8:1000::/36",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::1"
    #                                },
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::2"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                }
    #            ]
    #        }
    #    ]
    #
    #    "commands": [
    #        "delete protocols static route 192.0.2.32/28",
    #        "delete protocols static route6 2001:db8:1000::/36",
    #        "set protocols static route 198.0.2.48/28",
    #        "set protocols static route 198.0.2.48/28 next-hop '192.0.2.18'"
    #
    #
    #    "after": [
    #        {
    #            "address_families": [
    #                {
    #                    "afi": "ipv4",
    #                    "routes": [
    #                        {
    #                            "dest": "198.0.2.48/28",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "192.0.2.18"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                }
    #            ]
    #        }
    #    ]
    #
    #
    # After state
    # ------------
    #
    # vyos@vyos:~$ show configuration commands| grep static
    # set protocols static route 198.0.2.48/28 next-hop '192.0.2.18'


    # Using deleted to delete static route based on afi
    #
    # Before state
    # -------------
    #
    # vyos@vyos:~$ show configuration commands| grep static
    # set protocols static route 192.0.2.32/28 'blackhole'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.6'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.7'
    # set protocols static route6 2001:db8:1000::/36 blackhole distance '2'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::1'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::2'
    #
    - name: Delete static route based on afi.
      vyos.vyos.vyos_static_routes:
        config:
        - address_families:
          - afi: ipv4
          - afi: ipv6
        state: deleted
    #
    #
    # ------------------------
    # Module Execution Results
    # ------------------------
    #
    #    "before": [
    #        {
    #            "address_families": [
    #                {
    #                    "afi": "ipv4",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "type": "blackhole"
    #                            },
    #                            "dest": "192.0.2.32/28",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "192.0.2.6"
    #                                },
    #                                {
    #                                    "forward_router_address": "192.0.2.7"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "distance": 2
    #                            },
    #                            "dest": "2001:db8:1000::/36",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::1"
    #                                },
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::2"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                }
    #            ]
    #        }
    #    ]
    #    "commands": [
    #       "delete protocols static route",
    #       "delete protocols static route6"
    #    ]
    #
    # "after": []
    # After state
    # ------------
    # vyos@vyos# run show configuration commands | grep static
    # set protocols 'static'


    # Using deleted to delete all the static routes when passes config is empty
    #
    # Before state
    # -------------
    #
    # vyos@vyos:~$ show configuration commands| grep static
    # set protocols static route 192.0.2.32/28 'blackhole'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.6'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.7'
    # set protocols static route6 2001:db8:1000::/36 blackhole distance '2'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::1'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::2'
    #
    - name: Delete all the static routes.
      vyos.vyos.vyos_static_routes:
        config:
        state: deleted
    #
    #
    # ------------------------
    # Module Execution Results
    # ------------------------
    #
    #    "before": [
    #        {
    #            "address_families": [
    #                {
    #                    "afi": "ipv4",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "type": "blackhole"
    #                            },
    #                            "dest": "192.0.2.32/28",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "192.0.2.6"
    #                                },
    #                                {
    #                                    "forward_router_address": "192.0.2.7"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "distance": 2
    #                            },
    #                            "dest": "2001:db8:1000::/36",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::1"
    #                                },
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::2"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                }
    #            ]
    #        }
    #    ]
    #    "commands": [
    #       "delete protocols static route",
    #       "delete protocols static route6"
    #    ]
    #
    # "after": []
    # After state
    # ------------
    # vyos@vyos# run show configuration commands | grep static
    # set protocols 'static'


    # Using rendered
    #
    #
    - name: Render the commands for provided  configuration
      vyos.vyos.vyos_static_routes:
        config:
        - address_families:
          - afi: ipv4
            routes:
            - dest: 192.0.2.32/28
              blackhole_config:
                type: blackhole
              next_hops:
              - forward_router_address: 192.0.2.6
              - forward_router_address: 192.0.2.7
        - address_families:
          - afi: ipv6
            routes:
            - dest: 2001:db8:1000::/36
              blackhole_config:
                distance: 2
              next_hops:
              - forward_router_address: 2001:db8:2000:2::1
              - forward_router_address: 2001:db8:2000:2::2
        state: rendered
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #
    # "rendered": [
    #        "set protocols static route 192.0.2.32/28",
    #        "set protocols static route 192.0.2.32/28 blackhole",
    #        "set protocols static route 192.0.2.32/28 next-hop '192.0.2.6'",
    #        "set protocols static route 192.0.2.32/28 next-hop '192.0.2.7'",
    #        "set protocols static route6 2001:db8:1000::/36",
    #        "set protocols static route6 2001:db8:1000::/36 blackhole distance '2'",
    #        "set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::1'",
    #        "set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::2'"
    #    ]


    # Using parsed
    #
    #
    - name: Parse the provided running configuration
      vyos.vyos.vyos_static_routes:
        running_config:
          "set protocols static route 192.0.2.32/28 'blackhole'
           set protocols static route 192.0.2.32/28 next-hop '192.0.2.6'
           set protocols static route 192.0.2.32/28 next-hop '192.0.2.7'
           set protocols static route6 2001:db8:1000::/36 blackhole distance '2'
           set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::1'
           set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::2'"
        state: parsed
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #
    # "parsed": [
    #        {
    #            "address_families": [
    #                {
    #                    "afi": "ipv4",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "distance": 2
    #                            },
    #                            "dest": "192.0.2.32/28",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::2"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "distance": 2
    #                            },
    #                            "dest": "2001:db8:1000::/36",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::2"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                }
    #            ]
    #        }
    #    ]


    # Using gathered
    #
    # Before state:
    # -------------
    #
    # vyos@vyos:~$ show configuration commands| grep static
    # set protocols static route 192.0.2.32/28 'blackhole'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.6'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.7'
    # set protocols static route6 2001:db8:1000::/36 blackhole distance '2'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::1'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::2'
    #
    - name: Gather listed static routes with provided configurations
      vyos.vyos.vyos_static_routes:
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
    #            "address_families": [
    #                {
    #                    "afi": "ipv4",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "type": "blackhole"
    #                            },
    #                            "dest": "192.0.2.32/28",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "192.0.2.6"
    #                                },
    #                                {
    #                                    "forward_router_address": "192.0.2.7"
    #                                }
    #                            ]
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "routes": [
    #                        {
    #                            "blackhole_config": {
    #                                "distance": 2
    #                            },
    #                            "dest": "2001:db8:1000::/36",
    #                            "next_hops": [
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::1"
    #                                },
    #                                {
    #                                    "forward_router_address": "2001:db8:2000:2::2"
    #                                }
    #                            ]
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
    # vyos@vyos:~$ show configuration commands| grep static
    # set protocols static route 192.0.2.32/28 'blackhole'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.6'
    # set protocols static route 192.0.2.32/28 next-hop '192.0.2.7'
    # set protocols static route6 2001:db8:1000::/36 blackhole distance '2'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::1'
    # set protocols static route6 2001:db8:1000::/36 next-hop '2001:db8:2000:2::2'



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
                            <div>The resulting configuration model invocation.</div>
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
                            <div>The configuration prior to the model invocation.</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&quot;set protocols static route 192.0.2.32/28 next-hop &#x27;192.0.2.6&#x27;&quot;, &quot;set protocols static route 192.0.2.32/28 &#x27;blackhole&#x27;&quot;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Rohit Thakur (@rohitthakur2590)
