.. _vyos.vyos.vyos_ospfv3_module:


*********************
vyos.vyos.vyos_ospfv3
*********************

**OSPFV3 resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This resource module configures and manages attributes of OSPFv3 routes on VyOS network devices.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="4">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A provided OSPFv3 route configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>areas</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv3 area.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>area_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv3 Area name/identity.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>export_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of export-list.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>import_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of import-list.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>range</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Summarize routes matching prefix (border routers only).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>border router IPv4 address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>advertise</b>
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
                        <div>Advertise this range.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>not_advertise</b>
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
                        <div>Don&#x27;t advertise this range.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parameters</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv3 specific parameters.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>router_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Override the default router identifier.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>redistribute</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Redistribute information from another routing protocol.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route map references.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>bgp</li>
                                    <li>connected</li>
                                    <li>kernel</li>
                                    <li>ripng</li>
                                    <li>static</li>
                        </ul>
                </td>
                <td>
                        <div>Route type to redistribute.</div>
                </td>
            </tr>


            <tr>
                <td colspan="4">
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
                        <div>The value of this option should be the output received from the VyOS device by executing the command <b>show configuration commands | grep ospfv3</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
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
                                    <li>deleted</li>
                                    <li>parsed</li>
                                    <li>gathered</li>
                                    <li>rendered</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in.</div>
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
    # vyos@vyos# run show  configuration commands | grep ospfv3
    #
    #
    - name: Merge the provided configuration with the exisiting running configuration
      vyos.vyos.vyos_ospfv3:
        config:
          redistribute:
          - route_type: bgp
          parameters:
            router_id: 192.0.2.10
          areas:
          - area_id: '2'
            export_list: export1
            import_list: import1
            range:
            - address: 2001:db10::/32
            - address: 2001:db20::/32
            - address: 2001:db30::/32
          - area_id: '3'
            range:
            - address: 2001:db40::/32
        state: merged
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    # before": {}
    #
    #    "commands": [
    #       "set protocols ospfv3 redistribute bgp",
    #       "set protocols ospfv3 parameters router-id '192.0.2.10'",
    #       "set protocols ospfv3 area 2 range 2001:db10::/32",
    #       "set protocols ospfv3 area 2 range 2001:db20::/32",
    #       "set protocols ospfv3 area 2 range 2001:db30::/32",
    #       "set protocols ospfv3 area '2'",
    #       "set protocols ospfv3 area 2 export-list export1",
    #       "set protocols ospfv3 area 2 import-list import1",
    #       "set protocols ospfv3 area '3'",
    #       "set protocols ospfv3 area 3 range 2001:db40::/32"
    #    ]
    #
    # "after": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "export_list": "export1",
    #                "import_list": "import1",
    #                "range": [
    #                    {
    #                        "address": "2001:db10::/32"
    #                    },
    #                    {
    #                        "address": "2001:db20::/32"
    #                    },
    #                    {
    #                        "address": "2001:db30::/32"
    #                    }
    #                ]
    #            },
    #            {
    #                "area_id": "3",
    #                "range": [
    #                    {
    #                        "address": "2001:db40::/32"
    #                    }
    #                ]
    #            }
    #        ],
    #        "parameters": {
    #            "router_id": "192.0.2.10"
    #        },
    #        "redistribute": [
    #            {
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    #
    # After state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospfv3
    # set protocols ospfv3 area 2 export-list 'export1'
    # set protocols ospfv3 area 2 import-list 'import1'
    # set protocols ospfv3 area 2 range '2001:db10::/32'
    # set protocols ospfv3 area 2 range '2001:db20::/32'
    # set protocols ospfv3 area 2 range '2001:db30::/32'
    # set protocols ospfv3 area 3 range '2001:db40::/32'
    # set protocols ospfv3 parameters router-id '192.0.2.10'
    # set protocols ospfv3 redistribute 'bgp'


    # Using replaced
    #
    # Before state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospfv3
    # set protocols ospfv3 area 2 export-list 'export1'
    # set protocols ospfv3 area 2 import-list 'import1'
    # set protocols ospfv3 area 2 range '2001:db10::/32'
    # set protocols ospfv3 area 2 range '2001:db20::/32'
    # set protocols ospfv3 area 2 range '2001:db30::/32'
    # set protocols ospfv3 area 3 range '2001:db40::/32'
    # set protocols ospfv3 parameters router-id '192.0.2.10'
    # set protocols ospfv3 redistribute 'bgp'
    #
    - name: Replace ospfv3 routes attributes configuration.
      vyos.vyos.vyos_ospfv3:
        config:
          redistribute:
          - route_type: bgp
          parameters:
            router_id: 192.0.2.10
          areas:
          - area_id: '2'
            export_list: export1
            import_list: import1
            range:
            - address: 2001:db10::/32
            - address: 2001:db30::/32
            - address: 2001:db50::/32
          - area_id: '4'
            range:
            - address: 2001:db60::/32
        state: replaced
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #    "before": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "export_list": "export1",
    #                "import_list": "import1",
    #                "range": [
    #                    {
    #                        "address": "2001:db10::/32"
    #                    },
    #                    {
    #                        "address": "2001:db20::/32"
    #                    },
    #                    {
    #                        "address": "2001:db30::/32"
    #                    }
    #                ]
    #            },
    #            {
    #                "area_id": "3",
    #                "range": [
    #                    {
    #                        "address": "2001:db40::/32"
    #                    }
    #                ]
    #            }
    #        ],
    #        "parameters": {
    #            "router_id": "192.0.2.10"
    #        },
    #        "redistribute": [
    #            {
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    #
    # "commands": [
    #     "delete protocols ospfv3 area 2 range 2001:db20::/32",
    #     "delete protocols ospfv3 area 3",
    #     "set protocols ospfv3 area 2 range 2001:db50::/32",
    #     "set protocols ospfv3 area '4'",
    #     "set protocols ospfv3 area 4 range 2001:db60::/32"
    #    ]
    #
    #    "after": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "export_list": "export1",
    #                "import_list": "import1",
    #                "range": [
    #                    {
    #                        "address": "2001:db10::/32"
    #                    },
    #                    {
    #                        "address": "2001:db30::/32"
    #                    },
    #                    {
    #                        "address": "2001:db50::/32"
    #                    }
    #                ]
    #            },
    #            {
    #                "area_id": "4",
    #                "range": [
    #                    {
    #                        "address": "2001:db60::/32"
    #                    }
    #                ]
    #            }
    #        ],
    #        "parameters": {
    #            "router_id": "192.0.2.10"
    #        },
    #        "redistribute": [
    #            {
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    #
    # After state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospfv3
    # set protocols ospfv3 area 2 export-list 'export1'
    # set protocols ospfv3 area 2 import-list 'import1'
    # set protocols ospfv3 area 2 range '2001:db10::/32'
    # set protocols ospfv3 area 2 range '2001:db30::/32'
    # set protocols ospfv3 area 2 range '2001:db50::/32'
    # set protocols ospfv3 area 4 range '2001:db60::/32'
    # set protocols ospfv3 parameters router-id '192.0.2.10'
    # set protocols ospfv3 redistribute 'bgp'


    # Using rendered
    #
    #
    - name: Render the commands for provided  configuration
      vyos.vyos.vyos_ospfv3:
        config:
          redistribute:
          - route_type: bgp
          parameters:
            router_id: 192.0.2.10
          areas:
          - area_id: '2'
            export_list: export1
            import_list: import1
            range:
            - address: 2001:db10::/32
            - address: 2001:db20::/32
            - address: 2001:db30::/32
          - area_id: '3'
            range:
            - address: 2001:db40::/32
        state: rendered
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #
    # "rendered": [
    #        [
    #       "set protocols ospfv3 redistribute bgp",
    #       "set protocols ospfv3 parameters router-id '192.0.2.10'",
    #       "set protocols ospfv3 area 2 range 2001:db10::/32",
    #       "set protocols ospfv3 area 2 range 2001:db20::/32",
    #       "set protocols ospfv3 area 2 range 2001:db30::/32",
    #       "set protocols ospfv3 area '2'",
    #       "set protocols ospfv3 area 2 export-list export1",
    #       "set protocols ospfv3 area 2 import-list import1",
    #       "set protocols ospfv3 area '3'",
    #       "set protocols ospfv3 area 3 range 2001:db40::/32"
    #    ]


    # Using parsed
    #
    #
    - name: Parse the commands to provide structured configuration.
      vyos.vyos.vyos_ospfv3:
        running_config:
          "set protocols ospfv3 area 2 export-list 'export1'
           set protocols ospfv3 area 2 import-list 'import1'
           set protocols ospfv3 area 2 range '2001:db10::/32'
           set protocols ospfv3 area 2 range '2001:db20::/32'
           set protocols ospfv3 area 2 range '2001:db30::/32'
           set protocols ospfv3 area 3 range '2001:db40::/32'
           set protocols ospfv3 parameters router-id '192.0.2.10'
           set protocols ospfv3 redistribute 'bgp'"
        state: parsed
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #
    # "parsed": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "export_list": "export1",
    #                "import_list": "import1",
    #                "range": [
    #                    {
    #                        "address": "2001:db10::/32"
    #                    },
    #                    {
    #                        "address": "2001:db20::/32"
    #                    },
    #                    {
    #                        "address": "2001:db30::/32"
    #                    }
    #                ]
    #            },
    #            {
    #                "area_id": "3",
    #                "range": [
    #                    {
    #                        "address": "2001:db40::/32"
    #                    }
    #                ]
    #            }
    #        ],
    #        "parameters": {
    #            "router_id": "192.0.2.10"
    #        },
    #        "redistribute": [
    #            {
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }


    # Using gathered
    #
    # Before state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospfv3
    # set protocols ospfv3 area 2 export-list 'export1'
    # set protocols ospfv3 area 2 import-list 'import1'
    # set protocols ospfv3 area 2 range '2001:db10::/32'
    # set protocols ospfv3 area 2 range '2001:db20::/32'
    # set protocols ospfv3 area 2 range '2001:db30::/32'
    # set protocols ospfv3 area 3 range '2001:db40::/32'
    # set protocols ospfv3 parameters router-id '192.0.2.10'
    # set protocols ospfv3 redistribute 'bgp'
    #
    - name: Gather ospfv3 routes config with provided configurations
      vyos.vyos.vyos_ospfv3:
        config:
        state: gathered
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #    "gathered": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "export_list": "export1",
    #                "import_list": "import1",
    #                "range": [
    #                    {
    #                        "address": "2001:db10::/32"
    #                    },
    #                    {
    #                        "address": "2001:db20::/32"
    #                    },
    #                    {
    #                        "address": "2001:db30::/32"
    #                    }
    #                ]
    #            },
    #            {
    #                "area_id": "3",
    #                "range": [
    #                    {
    #                        "address": "2001:db40::/32"
    #                    }
    #                ]
    #            }
    #        ],
    #        "parameters": {
    #            "router_id": "192.0.2.10"
    #        },
    #        "redistribute": [
    #            {
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    #
    # After state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospfv3
    # set protocols ospfv3 area 2 export-list 'export1'
    # set protocols ospfv3 area 2 import-list 'import1'
    # set protocols ospfv3 area 2 range '2001:db10::/32'
    # set protocols ospfv3 area 2 range '2001:db20::/32'
    # set protocols ospfv3 area 2 range '2001:db30::/32'
    # set protocols ospfv3 area 3 range '2001:db40::/32'
    # set protocols ospfv3 parameters router-id '192.0.2.10'
    # set protocols ospfv3 redistribute 'bgp'


    # Using deleted
    #
    # Before state
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospfv3
    # set protocols ospfv3 area 2 export-list 'export1'
    # set protocols ospfv3 area 2 import-list 'import1'
    # set protocols ospfv3 area 2 range '2001:db10::/32'
    # set protocols ospfv3 area 2 range '2001:db20::/32'
    # set protocols ospfv3 area 2 range '2001:db30::/32'
    # set protocols ospfv3 area 3 range '2001:db40::/32'
    # set protocols ospfv3 parameters router-id '192.0.2.10'
    # set protocols ospfv3 redistribute 'bgp'
    #
    - name: Delete attributes of ospfv3 routes.
      vyos.vyos.vyos_ospfv3:
        config:
        state: deleted
    #
    #
    # ------------------------
    # Module Execution Results
    # ------------------------
    #
    #    "before": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "export_list": "export1",
    #                "import_list": "import1",
    #                "range": [
    #                    {
    #                        "address": "2001:db10::/32"
    #                    },
    #                    {
    #                        "address": "2001:db20::/32"
    #                    },
    #                    {
    #                        "address": "2001:db30::/32"
    #                    }
    #                ]
    #            },
    #            {
    #                "area_id": "3",
    #                "range": [
    #                    {
    #                        "address": "2001:db40::/32"
    #                    }
    #                ]
    #            }
    #        ],
    #        "parameters": {
    #            "router_id": "192.0.2.10"
    #        },
    #        "redistribute": [
    #            {
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    # "commands": [
    #        "delete protocols ospfv3"
    #    ]
    #
    # "after": {}
    # After state
    # ------------
    # vyos@192# run show configuration commands | grep ospfv3



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
                      <span style="color: purple">dictionary</span>
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
                      <span style="color: purple">dictionary</span>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;set protocols ospf parameters router-id 192.0.1.1&#x27;, &quot;set protocols ospfv3 area 2 range &#x27;2001:db10::/32&#x27;&quot;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Rohit Thakur (@rohitthakur2590)
