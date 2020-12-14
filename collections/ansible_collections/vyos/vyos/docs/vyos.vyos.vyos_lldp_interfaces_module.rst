.. _vyos.vyos.vyos_lldp_interfaces_module:


******************************
vyos.vyos.vyos_lldp_interfaces
******************************

**LLDP interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages attributes of lldp interfaces on VyOS network devices.




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
                        <div>A list of lldp interfaces configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enable</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>to disable lldp on the interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>location</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>LLDP-MED location data.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>civic_based</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Civic-based location data.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ca_info</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>LLDP-MED address info</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ca_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>LLDP-MED Civic Address type.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ca_value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>LLDP-MED Civic Address value.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>country_code</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Country Code</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>coordinate_based</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Coordinate-based location.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>altitude</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Altitude in meters.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>datum</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>WGS84</li>
                                    <li>NAD83</li>
                                    <li>MLLW</li>
                        </ul>
                </td>
                <td>
                        <div>Coordinate datum type.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>latitude</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Latitude.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>longitude</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Longitude.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>elin</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Emergency Call Service ELIN number (between 10-25 numbers).</div>
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
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the  lldp interface.</div>
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
                        <div>The value of this option should be the output received from the VyOS device by executing the command <b>show configuration commands | grep lldp</b>.</div>
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
                                    <li>rendered</li>
                                    <li>parsed</li>
                                    <li>gathered</li>
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
    # vyos@vyos:~$ show configuration  commands | grep lldp
    #
    - name: Merge provided configuration with device configuration
      vyos.vyos.vyos_lldp_interfaces:
        config:
        - name: eth1
          location:
            civic_based:
              country_code: US
              ca_info:
              - ca_type: 0
                ca_value: ENGLISH

        - name: eth2
          location:
            coordinate_based:
              altitude: 2200
              datum: WGS84
              longitude: 222.267255W
              latitude: 33.524449N
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
    #        "set service lldp interface eth1 location civic-based country-code 'US'",
    #        "set service lldp interface eth1 location civic-based ca-type 0 ca-value 'ENGLISH'",
    #        "set service lldp interface eth1",
    #        "set service lldp interface eth2 location coordinate-based latitude '33.524449N'",
    #        "set service lldp interface eth2 location coordinate-based altitude '2200'",
    #        "set service lldp interface eth2 location coordinate-based datum 'WGS84'",
    #        "set service lldp interface eth2 location coordinate-based longitude '222.267255W'",
    #        "set service lldp interface eth2 location coordinate-based latitude '33.524449N'",
    #        "set service lldp interface eth2 location coordinate-based altitude '2200'",
    #        "set service lldp interface eth2 location coordinate-based datum 'WGS84'",
    #        "set service lldp interface eth2 location coordinate-based longitude '222.267255W'",
    #        "set service lldp interface eth2"
    #
    # "after": [
    #        {
    #            "location": {
    #                "coordinate_based": {
    #                    "altitude": 2200,
    #                    "datum": "WGS84",
    #                    "latitude": "33.524449N",
    #                    "longitude": "222.267255W"
    #                }
    #            },
    #            "name": "eth2"
    #        },
    #        {
    #            "location": {
    #                "civic_based": {
    #                    "ca_info": [
    #                        {
    #                            "ca_type": 0,
    #                            "ca_value": "ENGLISH"
    #                        }
    #                    ],
    #                    "country_code": "US"
    #                }
    #            },
    #            "name": "eth1"
    #        }
    #    ],
    #
    # After state:
    # -------------
    #
    # vyos@vyos:~$ show configuration commands | grep lldp
    # set service lldp interface eth1 location civic-based ca-type 0 ca-value 'ENGLISH'
    # set service lldp interface eth1 location civic-based country-code 'US'
    # set service lldp interface eth2 location coordinate-based altitude '2200'
    # set service lldp interface eth2 location coordinate-based datum 'WGS84'
    # set service lldp interface eth2 location coordinate-based latitude '33.524449N'
    # set service lldp interface eth2 location coordinate-based longitude '222.267255W'


    # Using replaced
    #
    # Before state:
    # -------------
    #
    # vyos@vyos:~$ show configuration commands | grep lldp
    # set service lldp interface eth1 location civic-based ca-type 0 ca-value 'ENGLISH'
    # set service lldp interface eth1 location civic-based country-code 'US'
    # set service lldp interface eth2 location coordinate-based altitude '2200'
    # set service lldp interface eth2 location coordinate-based datum 'WGS84'
    # set service lldp interface eth2 location coordinate-based latitude '33.524449N'
    # set service lldp interface eth2 location coordinate-based longitude '222.267255W'
    #
    - name: Replace device configurations of listed LLDP interfaces with provided configurations
      vyos.vyos.vyos_lldp_interfaces:
        config:
        - name: eth2
          location:
            civic_based:
              country_code: US
              ca_info:
              - ca_type: 0
                ca_value: ENGLISH

        - name: eth1
          location:
            coordinate_based:
              altitude: 2200
              datum: WGS84
              longitude: 222.267255W
              latitude: 33.524449N
        state: replaced
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #    "before": [
    #        {
    #            "location": {
    #                "coordinate_based": {
    #                    "altitude": 2200,
    #                    "datum": "WGS84",
    #                    "latitude": "33.524449N",
    #                    "longitude": "222.267255W"
    #                }
    #            },
    #            "name": "eth2"
    #        },
    #        {
    #            "location": {
    #                "civic_based": {
    #                    "ca_info": [
    #                        {
    #                            "ca_type": 0,
    #                            "ca_value": "ENGLISH"
    #                        }
    #                    ],
    #                    "country_code": "US"
    #                }
    #            },
    #            "name": "eth1"
    #        }
    #    ]
    #
    #    "commands": [
    #        "delete service lldp interface eth2 location",
    #        "set service lldp interface eth2 'disable'",
    #        "set service lldp interface eth2 location civic-based country-code 'US'",
    #        "set service lldp interface eth2 location civic-based ca-type 0 ca-value 'ENGLISH'",
    #        "delete service lldp interface eth1 location",
    #        "set service lldp interface eth1 'disable'",
    #        "set service lldp interface eth1 location coordinate-based latitude '33.524449N'",
    #        "set service lldp interface eth1 location coordinate-based altitude '2200'",
    #        "set service lldp interface eth1 location coordinate-based datum 'WGS84'",
    #        "set service lldp interface eth1 location coordinate-based longitude '222.267255W'"
    #    ]
    #
    #    "after": [
    #        {
    #            "location": {
    #                "civic_based": {
    #                    "ca_info": [
    #                        {
    #                            "ca_type": 0,
    #                            "ca_value": "ENGLISH"
    #                        }
    #                    ],
    #                    "country_code": "US"
    #                }
    #            },
    #            "name": "eth2"
    #        },
    #        {
    #            "location": {
    #                "coordinate_based": {
    #                    "altitude": 2200,
    #                    "datum": "WGS84",
    #                    "latitude": "33.524449N",
    #                    "longitude": "222.267255W"
    #                }
    #            },
    #            "name": "eth1"
    #        }
    #    ]
    #
    # After state:
    # -------------
    #
    # vyos@vyos:~$ show configuration commands | grep lldp
    # set service lldp interface eth1 'disable'
    # set service lldp interface eth1 location coordinate-based altitude '2200'
    # set service lldp interface eth1 location coordinate-based datum 'WGS84'
    # set service lldp interface eth1 location coordinate-based latitude '33.524449N'
    # set service lldp interface eth1 location coordinate-based longitude '222.267255W'
    # set service lldp interface eth2 'disable'
    # set service lldp interface eth2 location civic-based ca-type 0 ca-value 'ENGLISH'
    # set service lldp interface eth2 location civic-based country-code 'US'


    # Using overridden
    #
    # Before state
    # --------------
    #
    # vyos@vyos:~$ show configuration commands | grep lldp
    # set service lldp interface eth1 'disable'
    # set service lldp interface eth1 location coordinate-based altitude '2200'
    # set service lldp interface eth1 location coordinate-based datum 'WGS84'
    # set service lldp interface eth1 location coordinate-based latitude '33.524449N'
    # set service lldp interface eth1 location coordinate-based longitude '222.267255W'
    # set service lldp interface eth2 'disable'
    # set service lldp interface eth2 location civic-based ca-type 0 ca-value 'ENGLISH'
    # set service lldp interface eth2 location civic-based country-code 'US'
    #
    - name: Overrides all device configuration with provided configuration
      vyos.vyos.vyos_lldp_interfaces:
        config:
        - name: eth2
          location:
            elin: 0000000911

        state: overridden
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    # "before": [
    #        {
    #            "enable": false,
    #            "location": {
    #                "civic_based": {
    #                    "ca_info": [
    #                        {
    #                            "ca_type": 0,
    #                            "ca_value": "ENGLISH"
    #                        }
    #                    ],
    #                    "country_code": "US"
    #                }
    #            },
    #            "name": "eth2"
    #        },
    #        {
    #            "enable": false,
    #            "location": {
    #                "coordinate_based": {
    #                    "altitude": 2200,
    #                    "datum": "WGS84",
    #                    "latitude": "33.524449N",
    #                    "longitude": "222.267255W"
    #                }
    #            },
    #            "name": "eth1"
    #        }
    #    ]
    #
    #    "commands": [
    #        "delete service lldp interface eth2 location",
    #        "delete service lldp interface eth2 disable",
    #        "set service lldp interface eth2 location elin 0000000911"
    #
    #
    #    "after": [
    #        {
    #            "location": {
    #                "elin": 0000000911
    #            },
    #            "name": "eth2"
    #        }
    #    ]
    #
    #
    # After state
    # ------------
    #
    # vyos@vyos# run show configuration commands | grep lldp
    # set service lldp interface eth2 location elin '0000000911'


    # Using deleted
    #
    # Before state
    # -------------
    #
    # vyos@vyos# run show configuration commands | grep lldp
    # set service lldp interface eth2 location elin '0000000911'
    #
    - name: Delete lldp  interface attributes of given interfaces.
      vyos.vyos.vyos_lldp_interfaces:
        config:
        - name: eth2
        state: deleted
    #
    #
    # ------------------------
    # Module Execution Results
    # ------------------------
    #
        before: [{location: {elin: 0000000911}, name: eth2}]
    # "commands": [
    #    "commands": [
    #        "delete service lldp interface eth2"
    #    ]
    #
    # "after": []
    # After state
    # ------------
    # vyos@vyos# run show configuration commands | grep lldp
    # set service 'lldp'


    # Using gathered
    #
    # Before state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep lldp
    # set service lldp interface eth1 location civic-based ca-type 0 ca-value 'ENGLISH'
    # set service lldp interface eth1 location civic-based country-code 'US'
    # set service lldp interface eth2 location coordinate-based altitude '2200'
    # set service lldp interface eth2 location coordinate-based datum 'WGS84'
    # set service lldp interface eth2 location coordinate-based latitude '33.524449N'
    # set service lldp interface eth2 location coordinate-based longitude '222.267255W'
    #
    - name: Gather listed lldp interfaces from running configuration
      vyos.vyos.vyos_lldp_interfaces:
        config:
        state: gathered
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #    "gathered": [
    #         {
    #             "location": {
    #                 "coordinate_based": {
    #                     "altitude": 2200,
    #                     "datum": "WGS84",
    #                     "latitude": "33.524449N",
    #                     "longitude": "222.267255W"
    #                 }
    #             },
    #             "name": "eth2"
    #         },
    #         {
    #             "location": {
    #                 "civic_based": {
    #                     "ca_info": [
    #                         {
    #                             "ca_type": 0,
    #                             "ca_value": "ENGLISH"
    #                         }
    #                     ],
    #                     "country_code": "US"
    #                 }
    #             },
    #             "name": "eth1"
    #         }
    #     ]
    #
    #
    # After state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep lldp
    # set service lldp interface eth1 location civic-based ca-type 0 ca-value 'ENGLISH'
    # set service lldp interface eth1 location civic-based country-code 'US'
    # set service lldp interface eth2 location coordinate-based altitude '2200'
    # set service lldp interface eth2 location coordinate-based datum 'WGS84'
    # set service lldp interface eth2 location coordinate-based latitude '33.524449N'
    # set service lldp interface eth2 location coordinate-based longitude '222.267255W'


    # Using rendered
    #
    #
    - name: Render the commands for provided  configuration
      vyos.vyos.vyos_lldp_interfaces:
        config:
        - name: eth1
          location:
            civic_based:
              country_code: US
              ca_info:
              - ca_type: 0
                ca_value: ENGLISH
        - name: eth2
          location:
            coordinate_based:
              altitude: 2200
              datum: WGS84
              longitude: 222.267255W
              latitude: 33.524449N
        state: rendered
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #
    # "rendered": [
    #         "set service lldp interface eth1 location civic-based country-code 'US'",
    #         "set service lldp interface eth1 location civic-based ca-type 0 ca-value 'ENGLISH'",
    #         "set service lldp interface eth1",
    #         "set service lldp interface eth2 location coordinate-based latitude '33.524449N'",
    #         "set service lldp interface eth2 location coordinate-based altitude '2200'",
    #         "set service lldp interface eth2 location coordinate-based datum 'WGS84'",
    #         "set service lldp interface eth2 location coordinate-based longitude '222.267255W'",
    #         "set service lldp interface eth2"
    #     ]


    # Using parsed
    #
    #
    - name: Parsed the commands to provide structured configuration.
      vyos.vyos.vyos_lldp_interfaces:
        running_config:
          "set service lldp interface eth1 location civic-based ca-type 0 ca-value 'ENGLISH'
           set service lldp interface eth1 location civic-based country-code 'US'
           set service lldp interface eth2 location coordinate-based altitude '2200'
           set service lldp interface eth2 location coordinate-based datum 'WGS84'
           set service lldp interface eth2 location coordinate-based latitude '33.524449N'
           set service lldp interface eth2 location coordinate-based longitude '222.267255W'"
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
    #             "location": {
    #                 "coordinate_based": {
    #                     "altitude": 2200,
    #                     "datum": "WGS84",
    #                     "latitude": "33.524449N",
    #                     "longitude": "222.267255W"
    #                 }
    #             },
    #             "name": "eth2"
    #         },
    #         {
    #             "location": {
    #                 "civic_based": {
    #                     "ca_info": [
    #                         {
    #                             "ca_type": 0,
    #                             "ca_value": "ENGLISH"
    #                         }
    #                     ],
    #                     "country_code": "US"
    #                 }
    #             },
    #             "name": "eth1"
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&quot;set service lldp interface eth2 &#x27;disable&#x27;&quot;, &#x27;delete service lldp interface eth1 location&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Rohit Thakur (@rohitthakur2590)
