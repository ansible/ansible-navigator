.. _cisco.nxos.nxos_vlans_module:


*********************
cisco.nxos.nxos_vlans
*********************

**VLANs resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module creates and manages VLAN configurations on Cisco NX-OS.




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
                        <div>A dictionary of Vlan options</div>
                </td>
            </tr>
                                <tr>
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
                        <div>Manage administrative state of the vlan.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mapped_vni</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The Virtual Network Identifier (VNI) ID that is mapped to the VLAN.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mode</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ce</li>
                                    <li>fabricpath</li>
                        </ul>
                </td>
                <td>
                        <div>Set vlan mode to classical ethernet or fabricpath. This is a valid option for Nexus 5000, 6000 and 7000 series.</div>
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
                        <div>Name of VLAN.</div>
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
                        <div>Manage operational state of the vlan.</div>
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
                        <div>Vlan ID.</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the commands <b>show vlans | json-pretty</b> and <b>show running-config | section ^vlan</b> in order and delimited by a line.</div>
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
                                    <li>gathered</li>
                                    <li>rendered</li>
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state of the configuration after module completion.</div>
                        <div>The state <em>overridden</em> would override the configuration of all the VLANs on the device (including VLAN 1) with the provided configuration in the task. Use caution with this state.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NXOS 7.3.(0)D1(1) on VIRL



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    # vlan 1

    - name: Merge provided configuration with device configuration.
      cisco.nxos.nxos_vlans:
        config:
        - vlan_id: 5
          name: test-vlan5
        - vlan_id: 10
          enabled: false
        state: merged

    # After state:
    # ------------
    # vlan 5
    #   name test-vlan5
    #   state active
    #   no shutdown
    # vlan 10
    #   state active
    #   shutdown


    # Using replaced

    # Before state:
    # -------------
    # vlan 1
    # vlan 5
    #   name test-vlan5
    # vlan 10
    #   shutdown

    - name: Replace device configuration of specified vlan with provided configuration.
      cisco.nxos.nxos_vlans:
        config:
        - vlan_id: 5
          name: test-vlan
          enabled: false
        - vlan_id: 10
          enabled: false
        state: replaced

    # After state:
    # ------------
    # vlan 1
    # vlan 5
    #   name test-vlan
    #   state active
    #   shutdown
    # vlan 10
    #   state active
    #   shutdown


    # Using overridden

    # Before state:
    # -------------
    # vlan 1
    # vlan 3
    #   name testing
    # vlan 5
    #   name test-vlan5
    #   shutdown
    # vlan 10
    #   shutdown

    - name: Override device configuration of all vlans with provided configuration.
      cisco.nxos.nxos_vlans:
        config:
        - vlan_id: 5
          name: test-vlan
        - vlan_id: 10
          state: active
        state: overridden

    # After state:
    # ------------
    # vlan 5
    #   name test-vlan
    #   state active
    #   no shutdown
    # vlan 10
    #   state active
    #   no shutdown


    # Using deleted

    # Before state:
    # -------------
    # vlan 1
    # vlan 5
    # vlan 10

    - name: Delete vlans.
      cisco.nxos.nxos_vlans:
        config:
        - vlan_id: 5
        - vlan_id: 10
        state: deleted

    # After state:
    # ------------
    #

    # Using rendered

    - name: Use rendered state to convert task input to device specific commands
      cisco.nxos.nxos_vlans:
        config:
        - vlan_id: 5
          name: vlan5
          mapped_vni: 100

        - vlan_id: 6
          name: vlan6
          state: suspend
        state: rendered

    # Task Output (redacted)
    # -----------------------

    # rendered:
    #   - vlan 5
    #   - name vlan5
    #   - vn-segment 100
    #   - vlan 6
    #   - name vlan6
    #   - state suspend

    # Using parsed

    # parsed.cfg
    # ------------
    # {
    #     "TABLE_vlanbrief": {
    #        "ROW_vlanbrief": [
    #            {
    #                "vlanshowbr-vlanid": "1",
    #                "vlanshowbr-vlanid-utf": "1",
    #                "vlanshowbr-vlanname": "default",
    #                "vlanshowbr-vlanstate": "active",
    #                "vlanshowbr-shutstate": "noshutdown"
    #            },
    #            {
    #                "vlanshowbr-vlanid": "5",
    #                "vlanshowbr-vlanid-utf": "5",
    #                "vlanshowbr-vlanname": "vlan5",
    #                "vlanshowbr-vlanstate": "suspend",
    #                "vlanshowbr-shutstate": "noshutdown"
    #            },
    #            {
    #                "vlanshowbr-vlanid": "6",
    #                "vlanshowbr-vlanid-utf": "6",
    #                "vlanshowbr-vlanname": "VLAN0006",
    #                "vlanshowbr-vlanstate": "active",
    #                "vlanshowbr-shutstate": "noshutdown"
    #            },
    #            {
    #                "vlanshowbr-vlanid": "7",
    #                "vlanshowbr-vlanid-utf": "7",
    #                "vlanshowbr-vlanname": "vlan7",
    #                "vlanshowbr-vlanstate": "active",
    #                "vlanshowbr-shutstate": "noshutdown"
    #            }
    #        ]
    #    },
    #    "TABLE_mtuinfo": {
    #        "ROW_mtuinfo": [
    #            {
    #                "vlanshowinfo-vlanid": "1",
    #                "vlanshowinfo-media-type": "enet",
    #                "vlanshowinfo-vlanmode": "ce-vlan"
    #            },
    #            {
    #                "vlanshowinfo-vlanid": "5",
    #                "vlanshowinfo-media-type": "enet",
    #                "vlanshowinfo-vlanmode": "ce-vlan"
    #            },
    #            {
    #                "vlanshowinfo-vlanid": "6",
    #                "vlanshowinfo-media-type": "enet",
    #                "vlanshowinfo-vlanmode": "ce-vlan"
    #            },
    #            {
    #                "vlanshowinfo-vlanid": "7",
    #                "vlanshowinfo-media-type": "enet",
    #                "vlanshowinfo-vlanmode": "ce-vlan"
    #             }
    #        ]
    #    }
    # }
    #
    # vlan 1,5-7
    # vlan 5
    #   state suspend
    #   name vlan5
    # vlan 7
    #   name vlan7
    #   vn-segment 100

    - name: Use parsed state to convert externally supplied config to structured format
      cisco.nxos.nxos_vlans:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output (redacted)
    # -----------------------

    # parsed:
    #   - vlan_id: 5
    #     enabled: True
    #     mode: "ce"
    #     name: "vlan5"
    #     state: suspend
    #
    #   - vlan_id: 6
    #     enabled: True
    #     mode: "ce"
    #     state: active
    #
    #   - vlan_id: 7
    #     enabled: True
    #     mode: "ce"
    #     name: "vlan7"
    #     state: active
    #     mapped_vni: 100

    # Using gathered

    # Existing device config state
    # -------------------------------
    # nxos-9k# show vlan | json
    # {"TABLE_vlanbrief": {"ROW_vlanbrief": [{"vlanshowbr-vlanid": "1", "vlanshowbr-vlanid-utf": "1", "vlanshowbr-vlanname": "default", "vlanshowbr-vlanstate
    # ": "active", "vlanshowbr-shutstate": "noshutdown"}, {"vlanshowbr-vlanid": "5", "vlanshowbr-vlanid-utf": "5", "vlanshowbr-vlanname": "vlan5", "vlanshowb
    # r-vlanstate": "suspend", "vlanshowbr-shutstate": "noshutdown"}, {"vlanshowbr-vlanid": "6", "vlanshowbr-vlanid-utf": "6", "vlanshowbr-vlanname": "VLAN00
    # 06", "vlanshowbr-vlanstate": "active", "vlanshowbr-shutstate": "noshutdown"}, {"vlanshowbr-vlanid": "7", "vlanshowbr-vlanid-utf": "7", "vlanshowbr-vlan
    # name": "vlan7", "vlanshowbr-vlanstate": "active", "vlanshowbr-shutstate": "shutdown"}]}, "TABLE_mtuinfo": {"ROW_mtuinfo": [{"vlanshowinfo-vlanid": "1",
    # "vlanshowinfo-media-type": "enet", "vlanshowinfo-vlanmode": "ce-vlan"}, {"vlanshowinfo-vlanid": "5", "vlanshowinfo-media-type": "enet", "vlanshowinfo-
    # vlanmode": "ce-vlan"}, {"vlanshowinfo-vlanid": "6", "vlanshowinfo-media-type": "enet", "vlanshowinfo-vlanmode": "ce-vlan"}, {"vlanshowinfo-vlanid": "7"
    # , "vlanshowinfo-media-type": "enet", "vlanshowinfo-vlanmode": "ce-vlan"}]}}
    #
    # nxos-9k#  show running-config | section ^vlan
    # vlan 1,5-7
    # vlan 5
    #   state suspend
    #   name vlan5
    # vlan 7
    #   shutdown
    #   name vlan7
    #   vn-segment 190

    - name: Gather vlans facts from the device using nxos_vlans
      cisco.nxos.nxos_vlans:
        state: gathered

    # Task output (redacted)
    # -----------------------
    # gathered:
    #   - vlan_id: 5
    #     enabled: True
    #     mode: "ce"
    #     name: "vlan5"
    #     state: suspend
    #
    #   - vlan_id: 6
    #     enabled: True
    #     mode: "ce"
    #     state: active
    #
    #   - vlan_id: 7
    #     enabled: False
    #     mode: "ce"
    #     name: "vlan7"
    #     state: active
    #     mapped_vni: 190



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;vlan 5&#x27;, &#x27;name test-vlan5&#x27;, &#x27;state suspend&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Trishna Guha (@trishnaguha)
