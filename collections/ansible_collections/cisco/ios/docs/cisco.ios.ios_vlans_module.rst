.. _cisco.ios.ios_vlans_module:


*******************
cisco.ios.ios_vlans
*******************

**VLANs resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of VLANs on Cisco IOS network devices.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
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
                        <div>A dictionary of VLANs options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mtu</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VLAN Maximum Transmission Unit.</div>
                        <div>Refer to vendor documentation for valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Ascii name of the VLAN.</div>
                        <div>NOTE, <em>name</em> should not be named/appended with <em>default</em> as it is reserved for device default vlans.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>remote_span</b>
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
                        <div>Configure as Remote SPAN VLAN</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>shutdown</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>enabled</li>
                                    <li>disabled</li>
                        </ul>
                </td>
                <td>
                        <div>Shutdown VLAN switching.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>active</li>
                                    <li>suspend</li>
                        </ul>
                </td>
                <td>
                        <div>Operational state of the VLAN</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vlan_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>ID of the VLAN. Range 1-4094</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show vlan</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
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
                                    <li>gathered</li>
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | include ip route|ipv6 route</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Cisco IOSl2 device with Version 15.2 on VIRL.



Examples
--------

.. code-block:: yaml

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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;vlan 20&#x27;, &#x27;name vlan_20&#x27;, &#x27;mtu 600&#x27;, &#x27;remote-span&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sumit Jaiswal (@justjais)
