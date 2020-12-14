.. _cisco.nxos.nxos_l3_interfaces_module:


*****************************
cisco.nxos.nxos_l3_interfaces
*****************************

**L3 interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages Layer-3 interfaces attributes of NX-OS Interfaces.




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
                        <div>A dictionary of Layer-3 interface options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dot1q</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configures IEEE 802.1Q VLAN encapsulation on a subinterface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>evpn_multisite_tracking</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.1.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>fabric-tracking</li>
                                    <li>dci-tracking</li>
                        </ul>
                </td>
                <td>
                        <div>VxLAN evpn multisite Interface tracking. Supported only on selected model.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv4</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv4 address and attributes of the L3 interface.</div>
                </td>
            </tr>
                                <tr>
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
                        <div>IPV4 address of the L3 interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>secondary</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>A boolean attribute to manage addition of secondary IP address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tag</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>URIB route tag value for local/direct routes.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv6</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv6 address and attributes of the L3 interface.</div>
                </td>
            </tr>
                                <tr>
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
                        <div>IPV6 address of the L3 interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tag</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>URIB route tag value for local/direct routes.</div>
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
                        <div>Full name of L3 interface, i.e. Ethernet1/1.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>redirects</b>
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
                        <div>Enables/disables ip redirects</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>unreachables</b>
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
                        <div>Enables/disables ip redirects</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section &#x27;^interface&#x27;</b>.</div>
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
                        <div>The state <em>overridden</em> would override the IP address configuration of all interfaces on the device with the provided configuration in the task. Use caution with this state as you may loose access to the device.</div>
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
    # interface Ethernet1/6

    - name: Merge provided configuration with device configuration.
      cisco.nxos.nxos_l3_interfaces:
        config:
        - name: Ethernet1/6
          ipv4:
          - address: 192.168.1.1/24
            tag: 5
          - address: 10.1.1.1/24
            secondary: true
            tag: 10
          ipv6:
          - address: fd5d:12c9:2201:2::1/64
            tag: 6
        - name: Ethernet1/7.42
          dot1q: 42
          redirects: false
          unreachables: false
        state: merged

    # After state:
    # ------------
    #
    # interface Ethernet1/6
    #   ip address 192.168.22.1/24 tag 5
    #   ip address 10.1.1.1/24 secondary tag 10
    # interface Ethernet1/6
    #   ipv6 address fd5d:12c9:2201:2::1/64 tag 6
    # interface Ethernet1/7.42
    #   encapsulation dot1q 42
    #   no ip redirects
    #   no ip unreachables


    # Using replaced

    # Before state:
    # -------------
    #
    # interface Ethernet1/6
    #   ip address 192.168.22.1/24
    #   ipv6 address "fd5d:12c9:2201:1::1/64"

    - name: Replace device configuration of specified L3 interfaces with provided configuration.
      cisco.nxos.nxos_l3_interfaces:
        config:
        - name: Ethernet1/6
          ipv4:
            - address: 192.168.22.3/24
        state: replaced

    # After state:
    # ------------
    #
    # interface Ethernet1/6
    #   ip address 192.168.22.3/24


    # Using overridden

    # Before state:
    # -------------
    #
    # interface Ethernet1/2
    #   ip address 192.168.22.1/24
    # interface Ethernet1/6
    #   ipv6 address "fd5d:12c9:2201:1::1/64"

    - name: Override device configuration of all L3 interfaces on device with provided
        configuration.
      cisco.nxos.nxos_l3_interfaces:
        config:
        - name: Ethernet1/2
          ipv4: 192.168.22.3/4
        state: overridden

    # After state:
    # ------------
    #
    # interface Ethernet1/2
    #   ipv4 address 192.168.22.3/24
    # interface Ethernet1/6


    # Using deleted

    # Before state:
    # -------------
    #
    # interface Ethernet1/6
    #   ip address 192.168.22.1/24
    # interface Ethernet1/2
    #   ipv6 address "fd5d:12c9:2201:1::1/64"

    - name: Delete L3 attributes of given interfaces (This won't delete the interface
        itself).
      cisco.nxos.nxos_l3_interfaces:
        config:
        - name: Ethernet1/6
        - name: Ethernet1/2
        state: deleted

    # After state:
    # ------------
    #
    # interface Ethernet1/6
    # interface Ethernet1/2

    # Using rendered

    - name: Use rendered state to convert task input to device specific commands
      cisco.nxos.nxos_l3_interfaces:
        config:
        - name: Ethernet1/800
          ipv4:
          - address: 192.168.1.100/24
            tag: 5
          - address: 10.1.1.1/24
            secondary: true
            tag: 10
        - name: Ethernet1/800
          ipv6:
          - address: fd5d:12c9:2201:2::1/64
            tag: 6
        state: rendered

    # Task Output (redacted)
    # -----------------------

    # rendered:
    #   - "interface Ethernet1/800"
    #   - "ip address 192.168.1.100/24 tag 5"
    #   - "ip address 10.1.1.1/24 secondary tag 10"
    #   - "interface Ethernet1/800"
    #   - "ipv6 address fd5d:12c9:2201:2::1/64 tag 6"

    # Using parsed

    # parsed.cfg
    # ------------
    # interface Ethernet1/800
    #   ip address 192.168.1.100/24 tag 5
    #   ip address 10.1.1.1/24 secondary tag 10
    #   no ip redirects
    # interface Ethernet1/801
    #   ipv6 address fd5d:12c9:2201:2::1/64 tag 6
    #   ip unreachables
    # interface mgmt0
    #   ip address dhcp
    #   vrf member management

    - name: Use parsed state to convert externally supplied config to structured format
      cisco.nxos.nxos_l3_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output (redacted)
    # -----------------------

    # parsed:
    #   - name: Ethernet1/800
    #     ipv4:
    #       - address: 192.168.1.100/24
    #         tag: 5
    #       - address: 10.1.1.1/24
    #         secondary: True
    #         tag: 10
    #     redirects: False
    #   - name: Ethernet1/801
    #     ipv6:
    #      - address: fd5d:12c9:2201:2::1/64
    #        tag: 6
    #     unreachables: True

    # Using gathered

    # Existing device config state
    # -------------------------------
    # interface Ethernet1/1
    #   ip address 192.0.2.100/24
    # interface Ethernet1/2
    #   no ip redirects
    #   ip address 203.0.113.10/24
    #   ip unreachables
    #   ipv6 address 2001:db8::1/32

    - name: Gather l3_interfaces facts from the device using nxos_l3_interfaces
      cisco.nxos.nxos_l3_interfaces:
        state: gathered

    # Task output (redacted)
    # -----------------------

    # gathered:
    #   - name: Ethernet1/1
    #     ipv4:
    #       - address: 192.0.2.100/24
    #   - name: Ethernet1/2
    #     ipv4:
    #       - address: 203.0.113.10/24
    #     ipv6:
    #       - address: 2001:db8::1/32
    #     redirects: False
    #     unreachables: True



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/2&#x27;, &#x27;ip address 192.168.0.1/2&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Trishna Guha (@trishnaguha)
