.. _cisco.nxos.nxos_interfaces_module:


**************************
cisco.nxos.nxos_interfaces
**************************

**Interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the interface attributes of NX-OS interfaces.




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
                        <div>A dictionary of interface options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>description</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface description.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>duplex</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>full</li>
                                    <li>half</li>
                                    <li>auto</li>
                        </ul>
                </td>
                <td>
                        <div>Interface link status. Applicable for Ethernet interfaces only.</div>
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
                        <div>Administrative state of the interface. Set the value to <code>true</code> to administratively enable the interface or <code>false</code> to disable it</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>fabric_forwarding_anycast_gateway</b>
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
                        <div>Associate SVI with anycast gateway under VLAN configuration mode. Applicable for SVI interfaces only.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ip_forward</b>
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
                        <div>Enable or disable IP forward feature on SVIs. Set the value to <code>true</code> to enable  or <code>false</code> to disable.</div>
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
                                    <li>layer2</li>
                                    <li>layer3</li>
                        </ul>
                </td>
                <td>
                        <div>Manage Layer2 or Layer3 state of the interface. Applicable for Ethernet and port channel interfaces only.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mtu</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>MTU for a specific interface. Must be an even number between 576 and 9216. Applicable for Ethernet interfaces only.</div>
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
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Full name of interface, e.g. Ethernet1/1, port-channel10.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>speed</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface link speed. Applicable for Ethernet interfaces only.</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section ^interface</b></div>
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
                        <div>The state of the configuration after module completion</div>
                        <div>The state <em>rendered</em> considers the system default mode for interfaces to be &quot;Layer 3&quot; and the system default state for interfaces to be shutdown.</div>
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
    #   description testing
    #   mtu 1800

    - name: Merge provided configuration with device configuration
      cisco.nxos.nxos_interfaces:
        config:
        - name: Ethernet1/1
          description: Configured by Ansible
          enabled: true
        - name: Ethernet1/2
          description: Configured by Ansible Network
          enabled: false
        state: merged

    # After state:
    # ------------
    #
    # interface Ethernet1/1
    #    description Configured by Ansible
    #    no shutdown
    #    mtu 1800
    # interface Ethernet2
    #    description Configured by Ansible Network
    #    shutdown


    # Using replaced

    # Before state:
    # -------------
    #
    # interface Ethernet1/1
    #    description Interface 1/1
    # interface Ethernet1/2

    - name: Replaces device configuration of listed interfaces with provided configuration
      cisco.nxos.nxos_interfaces:
        config:
        - name: Ethernet1/1
          description: Configured by Ansible
          enabled: true
          mtu: 2000
        - name: Ethernet1/2
          description: Configured by Ansible Network
          enabled: false
          mode: layer2
        state: replaced

    # After state:
    # ------------
    #
    # interface Ethernet1/1
    #   description Configured by Ansible
    #   no shutdown
    #   mtu 1500
    # interface Ethernet2/2
    #    description Configured by Ansible Network
    #    shutdown
    #    switchport


    # Using overridden

    # Before state:
    # -------------
    #
    # interface Ethernet1/1
    #    description Interface Ethernet1/1
    # interface Ethernet1/2
    # interface mgmt0
    #    description Management interface
    #    ip address dhcp

    - name: Override device configuration of all interfaces with provided configuration
      cisco.nxos.nxos_interfaces:
        config:
        - name: Ethernet1/1
          enabled: true
        - name: Ethernet1/2
          description: Configured by Ansible Network
          enabled: false
        state: overridden

    # After state:
    # ------------
    #
    # interface Ethernet1/1
    # interface Ethernet1/2
    #    description Configured by Ansible Network
    #    shutdown
    # interface mgmt0
    #    ip address dhcp


    # Using deleted

    # Before state:
    # -------------
    #
    # interface Ethernet1/1
    #    description Interface Ethernet1/1
    # interface Ethernet1/2
    # interface mgmt0
    #    description Management interface
    #    ip address dhcp

    - name: Delete or return interface parameters to default settings
      cisco.nxos.nxos_interfaces:
        config:
        - name: Ethernet1/1
        state: deleted

    # After state:
    # ------------
    #
    # interface Ethernet1/1
    # interface Ethernet1/2
    # interface mgmt0
    #    description Management interface
    #    ip address dhcp

    # Using rendered

    - name: Use rendered state to convert task input to device specific commands
      cisco.nxos.nxos_interfaces:
        config:
        - name: Ethernet1/1
          description: outbound-intf
          mode: layer3
          speed: 100
        - name: Ethernet1/2
          mode: layer2
          enabled: true
          duplex: full
        state: rendered

    # Task Output (redacted)
    # -----------------------

    # rendered:
    #   - "interface Ethernet1/1"
    #   - "description outbound-intf"
    #   - "speed 100"
    #   - "interface Ethernet1/2"
    #   - "switchport"
    #   - "duplex full"
    #   - "no shutdown"

    # Using parsed

    # parsed.cfg
    # ------------
    # interface Ethernet1/800
    #   description test-1
    #   speed 1000
    #   shutdown
    #   no switchport
    #   duplex half
    # interface Ethernet1/801
    #   description test-2
    #   switchport
    #   no shutdown
    #   mtu 1800

    - name: Use parsed state to convert externally supplied config to structured format
      cisco.nxos.nxos_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output (redacted)
    # -----------------------
    #  parsed:
    #    - description: "test-1"
    #      duplex: "half"
    #      enabled: false
    #      mode: "layer3"
    #      name: "Ethernet1/800"
    #      speed: "1000"
    #
    #    - description: "test-2"
    #      enabled: true
    #      mode: "layer2"
    #      mtu: "1800"
    #      name: "Ethernet1/801"

    # Using gathered

    # Existing device config state
    # -----------------------------
    # interface Ethernet1/1
    #   description outbound-intf
    #   switchport
    #   no shutdown
    # interface Ethernet1/2
    #   description intf-l3
    #   speed 1000
    # interface Ethernet1/3
    # interface Ethernet1/4
    # interface Ethernet1/5

    - name: Gather interfaces facts from the device using nxos_interfaces
      cisco.nxos.nxos_interfaces:
        state: gathered

    # Task output (redacted)
    # -----------------------
    # - name: Ethernet1/1
    #   description: outbound-intf
    #   mode: layer2
    #   enabled: True
    # - name: Ethernet1/2
    #   description: intf-l3
    #   speed: "1000"



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/1&#x27;, &#x27;mtu 1800&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Trishna Guha (@trishnaguha)
