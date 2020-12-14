.. _arista.eos.eos_l2_interfaces_module:


****************************
arista.eos.eos_l2_interfaces
****************************

**L2 interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of Layer-2 interface on Arista EOS devices.




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
                        <div>Full name of interface, e.g. Ethernet1.</div>
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
                        <div>Switchport mode trunk command to configure the interface as a Layer 2 trunk.</div>
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
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>trunk_allowed_vlans</b>
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
                        <div>The value of this option should be the output received from the EOS device by executing the command <b>show running-config | section ^interface</b>.</div>
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
                                    <li>rendered</li>
                                    <li>gathered</li>
                        </ul>
                </td>
                <td>
                        <div>The state of the configuration after module completion</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Arista EOS 4.20.10M
   - This module works with connection ``network_cli``. See the `EOS Platform Options <../network/user_guide/platform_eos.html>`_.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    #    switchport access vlan 20
    # !
    # interface Ethernet2
    #    switchport trunk native vlan 20
    #    switchport mode trunk
    # !
    # interface Management1
    #    ip address dhcp
    #    ipv6 address auto-config
    # !

    - name: Merge provided configuration with device configuration.
      arista.eos.eos_l2_interfaces:
        config:
        - name: Ethernet1
          mode: trunk
          trunk:
            native_vlan: 10
        - name: Ethernet2
          mode: access
          access:
            vlan: 30
        state: merged

    # After state:
    # ------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    #    switchport trunk native vlan 10
    #    switchport mode trunk
    # !
    # interface Ethernet2
    #    switchport access vlan 30
    # !
    # interface Management1
    #    ip address dhcp
    #    ipv6 address auto-config
    # !

    # Using replaced

    # Before state:
    # -------------
    #
    # veos2#show running-config | s int
    # interface Ethernet1
    #    switchport access vlan 20
    # !
    # interface Ethernet2
    #    switchport trunk native vlan 20
    #    switchport mode trunk
    # !
    # interface Management1
    #    ip address dhcp
    #    ipv6 address auto-config
    # !

    - name: Replace device configuration of specified L2 interfaces with provided configuration.
      arista.eos.eos_l2_interfaces:
        config:
        - name: Ethernet1
          mode: trunk
          trunk:
            native_vlan: 20
            trunk_vlans: 5-10, 15
        state: replaced

    # After state:
    # ------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    #    switchport trunk native vlan 20
    #    switchport trunk allowed vlan 5-10,15
    #    switchport mode trunk
    # !
    # interface Ethernet2
    #    switchport trunk native vlan 20
    #    switchport mode trunk
    # !
    # interface Management1
    #    ip address dhcp
    #    ipv6 address auto-config
    # !

    # Using overridden

    # Before state:
    # -------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    #    switchport access vlan 20
    # !
    # interface Ethernet2
    #    switchport trunk native vlan 20
    #    switchport mode trunk
    # !
    # interface Management1
    #    ip address dhcp
    #    ipv6 address auto-config
    # !

    - name: Override device configuration of all L2 interfaces on device with provided
        configuration.
      arista.eos.eos_l2_interfaces:
        config:
        - name: Ethernet2
          mode: access
          access:
            vlan: 30
        state: overridden

    # After state:
    # ------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    # !
    # interface Ethernet2
    #    switchport access vlan 30
    # !
    # interface Management1
    #    ip address dhcp
    #    ipv6 address auto-config
    # !

    # Using deleted

    # Before state:
    # -------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    #    switchport access vlan 20
    # !
    # interface Ethernet2
    #    switchport trunk native vlan 20
    #    switchport mode trunk
    # !
    # interface Management1
    #    ip address dhcp
    #    ipv6 address auto-config
    # !

    - name: Delete EOS L2 interfaces as in given arguments.
      arista.eos.eos_l2_interfaces:
        config:
        - name: Ethernet1
        - name: Ethernet2
        state: deleted

    # After state:
    # ------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    # !
    # interface Ethernet2
    # !
    # interface Management1
    #    ip address dhcp
    #    ipv6 address auto-config

    # using rendered

    - name: Use Rendered to convert the structured data to native config
      arista.eos.eos_l2_interfaces:
        config:
        - name: Ethernet1
          mode: trunk
          trunk:
            native_vlan: 10
        - name: Ethernet2
          mode: access
          access:
            vlan: 30
        state: merged

    # Output :
    # ------------
    #
    # - "interface Ethernet1"
    # - "switchport trunk native vlan 10"
    # - "switchport mode trunk"
    # - "interface Ethernet2"
    # - "switchport access vlan 30"
    # - "interface Management1"
    # - "ip address dhcp"
    # - "ipv6 address auto-config"


    # using parsed

    # parsed.cfg

    # interface Ethernet1
    #    switchport trunk native vlan 10
    #    switchport mode trunk
    # !
    # interface Ethernet2
    #    switchport access vlan 30
    # !

    - name: Use parsed to convert native configs to structured data
      arista.eos.l2_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Output:
    #   parsed:
    #      - name: Ethernet1
    #        mode: trunk
    #        trunk:
    #          native_vlan: 10
    #      - name: Ethernet2
    #        mode: access
    #        access:
    #          vlan: 30


    # Using gathered:
    # Existing config on the device:
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    #    switchport trunk native vlan 10
    #    switchport mode trunk
    # !
    # interface Ethernet2
    #    switchport access vlan 30
    # !

    - name: Gather interfaces facts from the device
      arista.eos.l2_interfaces:
        state: gathered
    # output:
    #   gathered:
    #      - name: Ethernet1
    #        mode: trunk
    #        trunk:
    #          native_vlan: 10
    #      - name: Ethernet2
    #        mode: access
    #        access:
    #          vlan: 30



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
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet2&#x27;, &#x27;switchport access vlan 20&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Nathaniel Case (@qalthos)
