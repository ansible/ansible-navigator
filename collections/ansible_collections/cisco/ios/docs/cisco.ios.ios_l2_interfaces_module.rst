.. _cisco.ios.ios_l2_interfaces_module:


***************************
cisco.ios.ios_l2_interfaces
***************************

**L2 interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of Layer-2 interface on Cisco IOS devices.




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
                        <div>A dictionary of Layer-2 interface options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>access</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Switchport mode access command to configure the interface as a layer 2 access.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vlan</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure given VLAN in access port. It&#x27;s used as the access VLAN ID.</div>
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
                                    <li>access</li>
                                    <li>trunk</li>
                        </ul>
                </td>
                <td>
                        <div>Mode in which interface needs to be configured.</div>
                        <div>An interface whose trunk encapsulation is &quot;Auto&quot; can not be configured to &quot;trunk&quot; mode.</div>
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
                    <b>trunk</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Switchport mode trunk command to configure the interface as a Layer 2 trunk. Note The encapsulation is always set to dot1q.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>allowed_vlans</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of allowed VLANs in a given trunk port. These are the only VLANs that will be configured on the trunk.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>encapsulation</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>dot1q</li>
                                    <li>isl</li>
                                    <li>negotiate</li>
                        </ul>
                </td>
                <td>
                        <div>Trunking encapsulation when interface is in trunking mode.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>native_vlan</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Native VLAN to be configured in trunk port. It&#x27;s used as the trunk native VLAN ID.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>pruning_vlans</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Pruning VLAN to be configured in trunk port. It&#x27;s used as the trunk pruning VLAN ID.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>voice</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Switchport mode voice command to configure the interface with a voice vlan.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vlan</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure given voice VLAN on access port. It&#x27;s used as the voice VLAN ID.</div>
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show running-config | section ^interface</b>.</div>
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

    # Before state:
    # -------------
    #
    # viosl2#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  negotiation auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  switchport access vlan 20
    #  media-type rj45
    #  negotiation auto

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_l2_interfaces:
        config:
        - name: GigabitEthernet0/1
          mode: access
          access:
            vlan: 10
          voice:
            vlan: 40
        - name: GigabitEthernet0/2
          mode: trunk
          trunk:
            allowed_vlans: 10-20,40
            native_vlan: 20
            pruning_vlans: 10,20
            encapsulation: dot1q
        state: merged

    # After state:
    # ------------
    #
    # viosl2#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  switchport access vlan 10
    #  switchport voice vlan 40
    #  switchport mode access
    #  negotiation auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  switchport trunk allowed vlan 10-20,40
    #  switchport trunk encapsulation dot1q
    #  switchport trunk native vlan 20
    #  switchport trunk pruning vlan 10,20
    #  switchport mode trunk
    #  media-type rj45
    #  negotiation auto

    # Using replaced

    # Before state:
    # -------------
    #
    # viosl2#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  switchport access vlan 20
    #  negotiation auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  switchport access vlan 20
    #  media-type rj45
    #  negotiation auto

    - name: Replaces device configuration of listed l2 interfaces with provided configuration
      cisco.ios.ios_l2_interfaces:
        config:
        - name: GigabitEthernet0/2
          trunk:
            allowed_vlans: 20-25,40
            native_vlan: 20
            pruning_vlans: 10
            encapsulation: isl
        state: replaced

    # After state:
    # -------------
    #
    # viosl2#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  switchport access vlan 20
    #  negotiation auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  switchport trunk allowed vlan 20-25,40
    #  switchport trunk encapsulation isl
    #  switchport trunk native vlan 20
    #  switchport trunk pruning vlan 10
    #  media-type rj45
    #  negotiation auto

    # Using overridden

    # Before state:
    # -------------
    #
    # viosl2#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  switchport trunk encapsulation dot1q
    #  switchport trunk native vlan 20
    #  negotiation auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  switchport access vlan 20
    #  switchport trunk encapsulation dot1q
    #  switchport trunk native vlan 20
    #  media-type rj45
    #  negotiation auto

    - name: Override device configuration of all l2 interfaces with provided configuration
      cisco.ios.ios_l2_interfaces:
        config:
        - name: GigabitEthernet0/2
          access:
            vlan: 20
          voice:
            vlan: 40
        state: overridden

    # After state:
    # -------------
    #
    # viosl2#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  negotiation auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  switchport access vlan 20
    #  switchport voice vlan 40
    #  media-type rj45
    #  negotiation auto

    # Using Deleted

    # Before state:
    # -------------
    #
    # viosl2#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  switchport access vlan 20
    #  negotiation auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  switchport access vlan 20
    #  switchport trunk allowed vlan 20-40,60,80
    #  switchport trunk encapsulation dot1q
    #  switchport trunk native vlan 10
    #  switchport trunk pruning vlan 10
    #  media-type rj45
    #  negotiation auto

    - name: Delete IOS L2 interfaces as in given arguments
      cisco.ios.ios_l2_interfaces:
        config:
        - name: GigabitEthernet0/1
        state: deleted

    # After state:
    # -------------
    #
    # viosl2#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  negotiation auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  switchport access vlan 20
    #  switchport trunk allowed vlan 20-40,60,80
    #  switchport trunk encapsulation dot1q
    #  switchport trunk native vlan 10
    #  switchport trunk pruning vlan 10
    #  media-type rj45
    #  negotiation auto


    # Using Deleted without any config passed
    #"(NOTE: This will delete all of configured resource module attributes from each configured interface)"

    # Before state:
    # -------------
    #
    # viosl2#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  switchport access vlan 20
    #  negotiation auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  switchport access vlan 20
    #  switchport trunk allowed vlan 20-40,60,80
    #  switchport trunk encapsulation dot1q
    #  switchport trunk native vlan 10
    #  switchport trunk pruning vlan 10
    #  media-type rj45
    #  negotiation auto

    - name: Delete IOS L2 interfaces as in given arguments
      cisco.ios.ios_l2_interfaces:
        state: deleted

    # After state:
    # -------------
    #
    # viosl2#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  negotiation auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  media-type rj45
    #  negotiation auto

    # Using Gathered

    # Before state:
    # -------------
    #
    # vios#sh running-config | section ^interface
    # interface GigabitEthernet0/1
    #  switchport access vlan 10
    # interface GigabitEthernet0/2
    #  switchport trunk allowed vlan 10-20,40
    #  switchport trunk encapsulation dot1q
    #  switchport trunk native vlan 10
    #  switchport trunk pruning vlan 10,20
    #  switchport mode trunk

    - name: Gather listed l2 interfaces with provided configurations
      cisco.ios.ios_l2_interfaces:
        config:
        state: gathered

    # Module Execution Result:
    # ------------------------
    #
    # "gathered": [
    #         {
    #             "name": "GigabitEthernet0/0"
    #         },
    #         {
    #             "access": {
    #                 "vlan": 10
    #             },
    #             "name": "GigabitEthernet0/1"
    #         },
    #         {
    #             "mode": "trunk",
    #             "name": "GigabitEthernet0/2",
    #             "trunk": {
    #                 "allowed_vlans": [
    #                     "10-20",
    #                     "40"
    #                 ],
    #                 "encapsulation": "dot1q",
    #                 "native_vlan": 10,
    #                 "pruning_vlans": [
    #                     "10",
    #                     "20"
    #                 ]
    #             }
    #         }
    #     ]

    # After state:
    # ------------
    #
    # vios#sh running-config | section ^interface
    # interface GigabitEthernet0/1
    #  switchport access vlan 10
    # interface GigabitEthernet0/2
    #  switchport trunk allowed vlan 10-20,40
    #  switchport trunk encapsulation dot1q
    #  switchport trunk native vlan 10
    #  switchport trunk pruning vlan 10,20
    #  switchport mode trunk

    # Using Rendered

    - name: Render the commands for provided  configuration
      cisco.ios.ios_l2_interfaces:
        config:
        - name: GigabitEthernet0/1
          access:
            vlan: 30
        - name: GigabitEthernet0/2
          trunk:
            allowed_vlans: 10-20,40
            native_vlan: 20
            pruning_vlans: 10,20
            encapsulation: dot1q
        state: rendered

    # Module Execution Result:
    # ------------------------
    #
    # "rendered": [
    #         "interface GigabitEthernet0/1",
    #         "switchport access vlan 30",
    #         "interface GigabitEthernet0/2",
    #         "switchport trunk encapsulation dot1q",
    #         "switchport trunk native vlan 20",
    #         "switchport trunk allowed vlan 10-20,40",
    #         "switchport trunk pruning vlan 10,20"
    #     ]

    # Using Parsed

    # File: parsed.cfg
    # ----------------
    #
    # interface GigabitEthernet0/1
    # switchport mode access
    # switchport access vlan 30
    # interface GigabitEthernet0/2
    # switchport trunk allowed vlan 15-20,40
    # switchport trunk encapsulation dot1q
    # switchport trunk native vlan 20
    # switchport trunk pruning vlan 10,20

    - name: Parse the commands for provided configuration
      cisco.ios.ios_l2_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------
    #
    # "parsed": [
    #         {
    #             "access": {
    #                 "vlan": 30
    #             },
    #             "mode": "access",
    #             "name": "GigabitEthernet0/1"
    #         },
    #         {
    #             "name": "GigabitEthernet0/2",
    #             "trunk": {
    #                 "allowed_vlans": [
    #                     "15-20",
    #                     "40"
    #                 ],
    #                 "encapsulation": "dot1q",
    #                 "native_vlan": 20,
    #                 "pruning_vlans": [
    #                     "10",
    #                     "20"
    #                 ]
    #             }
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format of the parameters above.</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format of the parameters above.</div>
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
                            <div>The set of commands pushed to the remote device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet0/1&#x27;, &#x27;switchport access vlan 20&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sumit Jaiswal (@justjais)
