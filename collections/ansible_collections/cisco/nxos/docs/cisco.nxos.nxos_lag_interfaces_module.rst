.. _cisco.nxos.nxos_lag_interfaces_module:


******************************
cisco.nxos.nxos_lag_interfaces
******************************

**LAG interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages attributes of link aggregation groups of NX-OS Interfaces.




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
                        <div>A list of link aggregation group configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>members</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The list of interfaces that are part of the group.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>force</b>
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
                        <div>When true it forces link aggregation group members to match what is declared in the members param. This can be used to remove members.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>member</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The interface name.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                                    <li>active</li>
                                    <li>on</li>
                                    <li>passive</li>
                        </ul>
                </td>
                <td>
                        <div>Link aggregation group (LAG).</div>
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
                        <div>Name of the link aggregation group (LAG).</div>
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
   - Tested against NXOS 7.3.(0)D1(1) on VIRL.
   - This module works with connection ``network_cli``.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # interface Ethernet1/4

    - name: Merge provided configuration with device configuration.
      cisco.nxos.nxos_lag_interfaces:
        config:
        - name: port-channel99
          members:
          - member: Ethernet1/4
        state: merged

    # After state:
    # ------------
    #
    # interface Ethernet1/4
    #   channel-group 99


    # Using replaced

    # Before state:
    # -------------
    #
    # interface Ethernet1/4
    #   channel-group 99 mode active

    - name: Replace device configuration of specified LAG attributes of given interfaces
        with provided configuration.
      cisco.nxos.nxos_lag_interfaces:
        config:
        - name: port-channel10
          members:
          - member: Ethernet1/4
        state: replaced

    # After state:
    # ------------
    #
    # interface Ethernet1/4
    #   channel-group 10


    # Using overridden

    # Before state:
    # -------------
    #
    # interface Ethernet1/4
    #   channel-group 10
    # interface Ethernet1/2
    #   channel-group 99 mode passive

    - name: Override device configuration of all LAG attributes of given interfaces on
        device with provided configuration.
      cisco.nxos.nxos_lag_interfaces:
        config:
        - name: port-channel20
          members:
          - member: Ethernet1/6
            force: true
        state: overridden

    # After state:
    # ------------
    # interface Ethernet1/2
    # interface Ethernet1/4
    # interface Ethernet1/6
    #   channel-group 20 force


    # Using deleted

    # Before state:
    # -------------
    #
    # interface Ethernet1/4
    #   channel-group 99 mode active

    - name: Delete LAG attributes of given interface (This won't delete the port-channel
        itself).
      cisco.nxos.nxos_lag_interfaces:
        config:
        - port-channel: port-channel99
        state: deleted

    - name: Delete LAG attributes of all the interfaces
      cisco.nxos.nxos_lag_interfaces:
        state: deleted

    # After state:
    # ------------
    #
    # interface Ethernet1/4
    #   no channel-group 99

    # Using rendered

    - name: Use rendered state to convert task input to device specific commands
      cisco.nxos.nxos_lag_interfaces:
        config:
        - name: port-channel10
          members:
          - member: Ethernet1/800
            mode: active
          - member: Ethernet1/801
        - name: port-channel11
          members:
          - member: Ethernet1/802
            mode: passive
        state: rendered

    # Task Output (redacted)
    # -----------------------

    # rendered:
    #  - "interface Ethernet1/800"
    #  - "channel-group 10 mode active"
    #  - "interface Ethernet1/801"
    #  - "channel-group 10"
    #  - "interface Ethernet1/802"
    #  - "channel-group 11 mode passive"

    # Using parsed

    # parsed.cfg
    # ------------

    # interface port-channel10
    # interface port-channel11
    # interface port-channel12
    # interface Ethernet1/800
    #   channel-group 10 mode active
    # interface Ethernet1/801
    #   channel-group 10 mode active
    # interface Ethernet1/802
    #   channel-group 11 mode passive
    # interface Ethernet1/803
    #   channel-group 11 mode passive

    - name: Use parsed state to convert externally supplied config to structured format
      cisco.nxos.nxos_lag_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output (redacted)
    # -----------------------

    # parsed:
    #  - members:
    #      - member: Ethernet1/800
    #        mode: active
    #      - member: Ethernet1/801
    #        mode: active
    #    name: port-channel10
    #
    #  - members:
    #      - member: Ethernet1/802
    #        mode: passive
    #      - member: Ethernet1/803
    #        mode: passive
    #    name: port-channel11
    #
    #  - name: port-channel12

    # Using gathered

    # Existing device config state
    # -------------------------------
    # interface port-channel10
    # interface port-channel11
    # interface Ethernet1/1
    #   channel-group 10 mode active
    # interface Ethernet1/2
    #   channel-group 11 mode passive
    #

    - name: Gather lag_interfaces facts from the device using nxos_lag_interfaces
      cisco.nxos.nxos_lag_interfaces:
        state: gathered

    # Task output (redacted)
    # -----------------------
    # gathered:
    #  - name: port-channel10
    #    members:
    #      - member: Ethernet1/1
    #        mode: active
    #  - name: port-channel11
    #    members:
    #      - member: Ethernet1/2
    #        mode: passive



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/800&#x27;, &#x27;channel-group 10 mode active&#x27;, &#x27;interface Ethernet1/801&#x27;, &#x27;channel-group 10&#x27;, &#x27;interface Ethernet1/802&#x27;, &#x27;channel-group 11 mode passive&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Trishna Guha (@trishnaguha)
- Nilashish Chakraborty (@NilashishC)
