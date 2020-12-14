.. _cisco.nxos.nxos_l2_interfaces_module:


*****************************
cisco.nxos.nxos_l2_interfaces
*****************************

**L2 interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages Layer-2 interfaces attributes of NX-OS Interfaces.




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
                        <div>Switchport mode access command to configure the interface as a Layer-2 access.</div>
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
                                    <li>fex-fabric</li>
                        </ul>
                </td>
                <td>
                        <div>Mode in which interface needs to be configured.</div>
                        <div>Access mode is not shown in interface facts, so idempotency will not be maintained for switchport mode access and every time the output will come as changed=True.</div>
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
                        <div>Full name of interface, i.e. Ethernet1/1.</div>
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
                        <div>Switchport mode trunk command to configure the interface as a Layer-2 trunk.</div>
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
                        <span style="color: purple">string</span>
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
                    <b>native_vlan</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Native VLAN to be configured in trunk port. It is used as the trunk native VLAN ID.</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section ^interface</b>.</div>
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
   - Tested against NXOS 7.3.(0)D1(1) on VIRL



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # interface Ethernet1/1
    #   switchport access vlan 20
    # interface Ethernet1/2
    #   switchport trunk native vlan 20
    # interface mgmt0
    #   ip address dhcp
    #   ipv6 address auto-config

    - name: Merge provided configuration with device configuration.
      cisco.nxos.nxos_l2_interfaces:
        config:
        - name: Ethernet1/1
          trunk:
            native_vlan: 10
            allowed_vlans: 2,4,15
        - name: Ethernet1/2
          access:
            vlan: 30
        state: merged

    # After state:
    # ------------
    #
    # interface Ethernet1/1
    #   switchport trunk native vlan 10
    #   switchport trunk allowed vlans 2,4,15
    # interface Ethernet1/2
    #   switchport access vlan 30
    # interface mgmt0
    #   ip address dhcp
    #   ipv6 address auto-config


    # Using replaced

    # Before state:
    # -------------
    #
    # interface Ethernet1/1
    #   switchport access vlan 20
    # interface Ethernet1/2
    #   switchport trunk native vlan 20
    # interface mgmt0
    #   ip address dhcp
    #   ipv6 address auto-config

    - name: Replace device configuration of specified L2 interfaces with provided configuration.
      cisco.nxos.nxos_l2_interfaces:
        config:
        - name: Ethernet1/1
          trunk:
            native_vlan: 20
            allowed_vlans: 5-10, 15
        state: replaced

    # After state:
    # ------------
    #
    # interface Ethernet1/1
    #   switchport trunk native vlan 20
    #   switchport trunk allowed vlan 5-10,15
    # interface Ethernet1/2
    #   switchport trunk native vlan 20
    #   switchport mode trunk
    # interface mgmt0
    #   ip address dhcp
    #   ipv6 address auto-config


    # Using overridden

    # Before state:
    # -------------
    #
    # interface Ethernet1/1
    #   switchport access vlan 20
    # interface Ethernet1/2
    #   switchport trunk native vlan 20
    # interface mgmt0
    #   ip address dhcp
    #   ipv6 address auto-config

    - name: Override device configuration of all L2 interfaces on device with provided
        configuration.
      cisco.nxos.nxos_l2_interfaces:
        config:
        - name: Ethernet1/2
          access:
            vlan: 30
        state: overridden

    # After state:
    # ------------
    #
    # interface Ethernet1/1
    # interface Ethernet1/2
    #   switchport access vlan 30
    # interface mgmt0
    #   ip address dhcp
    #   ipv6 address auto-config


    # Using deleted

    # Before state:
    # -------------
    #
    # interface Ethernet1/1
    #   switchport access vlan 20
    # interface Ethernet1/2
    #   switchport trunk native vlan 20
    # interface mgmt0
    #   ip address dhcp
    #   ipv6 address auto-config

    - name: Delete L2 attributes of given interfaces (Note This won't delete the interface
        itself).
      cisco.nxos.nxos_l2_interfaces:
        config:
        - name: Ethernet1/1
        - name: Ethernet1/2
        state: deleted

    # After state:
    # ------------
    #
    # interface Ethernet1/1
    # interface Ethernet1/2
    # interface mgmt0
    #   ip address dhcp
    #   ipv6 address auto-config

    # Using rendered

    - name: Render platform specific configuration lines (without connecting to the device)
      cisco.nxos.nxos_l2_interfaces:
        config:
        - name: Ethernet1/1
          trunk:
            native_vlan: 10
            allowed_vlans: 2,4,15
        - name: Ethernet1/2
          access:
            vlan: 30
        - name: Ethernet1/3
          trunk:
            native_vlan: 20
            allowed_vlans: 5-10, 15
        state: rendered

    # Task Output (redacted)
    # -----------------------

    # rendered:
    #  - "interface Ethernet1/1"
    #  - "switchport trunk allowed vlan 2,4,15"
    #  - "switchport trunk native vlan 10"
    #  - "interface Ethernet1/2"
    #  - "switchport access vlan 30"
    #  - "interface Ethernet1/3"
    #  - "switchport trunk allowed vlan 5,6,7,8,9,10,15"
    #  - "switchport trunk native vlan 20"

    # Using parsed

    # parsed.cfg
    # ------------
    # interface Ethernet1/800
    #   switchport access vlan 18
    #   switchport trunk allowed vlan 210
    # interface Ethernet1/801
    #   switchport trunk allowed vlan 2,4,15

    - name: Use parsed state to convert externally supplied config to structured format
      cisco.nxos.nxos_l2_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output (redacted)
    # -----------------------
    # parsed:
    #  - name: Ethernet1/800
    #    access:
    #      vlan: 18
    #    trunk:
    #      allowed_vlans: "210"
    #  - name: Ethernet1/801
    #    trunk:
    #      allowed_vlans: "2,4,15"

    # Using gathered

    # Existing device config state
    # -------------------------------
    # Nexus9kvI5# sh running-config | section ^interface
    # interface Ethernet1/1
    #   switchport access vlan 6
    #   switchport trunk allowed vlan 200
    # interface Ethernet1/2
    #   switchport trunk native vlan 10

    - name: Gather l2_interfaces facts from the device using nxos_l2_interfaces
      cisco.nxos.nxos_l2_interfaces:
        state: gathered

    # Task output (redacted)
    # -----------------------
    # gathered:
    #  - name: "Ethernet1/1"
    #    access:
    #      vlan: 6
    #    trunk:
    #      allowed_vlans: "200"
    #
    #  - name: "Ethernet1/2"
    #    trunk:
    #      native_vlan: 10



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/1&#x27;, &#x27;switchport trunk allowed vlan 2,4,15&#x27;, &#x27;switchport trunk native vlan 10&#x27;, &#x27;interface Ethernet1/2&#x27;, &#x27;switchport access vlan 30&#x27;, &#x27;interface Ethernet1/3&#x27;, &#x27;switchport trunk allowed vlan 5,6,7,8,9,10,15&#x27;, &#x27;switchport trunk native vlan 20&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Trishna Guha (@trishnaguha)
