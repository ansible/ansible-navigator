.. _cisco.ios.ios_lldp_interfaces_module:


*****************************
cisco.ios.ios_lldp_interfaces
*****************************

**LLDP interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages link layer discovery protocol (LLDP) attributes of interfaces on Cisco IOS devices.




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
                        <div>A dictionary of LLDP options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>med_tlv_select</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Selection of LLDP MED TLVs to send</div>
                        <div>NOTE, if med-tlv-select is configured idempotency won&#x27;t be maintained as Cisco device doesn&#x27;t record configured med-tlv-select options. As such, Ansible cannot verify if the respective med-tlv-select options is already configured or not from the device side. If you try to apply med-tlv-select option in every play run, Ansible will show changed as True.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>inventory_management</b>
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
                        <div>LLDP MED Inventory Management TLV</div>
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
                        <div>Full name of the interface excluding any logical unit number, i.e. GigabitEthernet0/1.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>receive</b>
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
                        <div>Enable LLDP reception on interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tlv_select</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Selection of LLDP type-length-value i.e. TLVs to send</div>
                        <div>NOTE, if tlv-select is configured idempotency won&#x27;t be maintained as Cisco device doesn&#x27;t record configured tlv-select options. As such, Ansible cannot verify if the respective tlv-select options is already configured or not from the device side. If you try to apply tlv-select option in every play run, Ansible will show changed as True.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>power_management</b>
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
                        <div>IEEE 802.3 DTE Power via MDI TLV</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>transmit</b>
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
                        <div>Enable LLDP transmission on interface.</div>
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>sh lldp interface</b>.</div>
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
   - Tested against Cisco IOSv Version 15.2 on VIRL.



Examples
--------

.. code-block:: yaml

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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet 0/1&#x27;, &#x27;lldp transmit&#x27;, &#x27;lldp receive&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sumit Jaiswal (@justjais)
