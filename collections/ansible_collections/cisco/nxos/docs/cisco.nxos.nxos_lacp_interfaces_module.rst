.. _cisco.nxos.nxos_lacp_interfaces_module:


*******************************
cisco.nxos.nxos_lacp_interfaces
*******************************

**LACP interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages Link Aggregation Control Protocol (LACP) attributes of NX-OS Interfaces.




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
                        <div>A dictionary of LACP interfaces options.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>convergence</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This dict contains configurable options related to convergence. Applicable only for Port-channel.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>graceful</b>
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
                        <div>port-channel lacp graceful convergence. Disable this only with lacp ports connected to Non-Nexus peer. Disabling this with Nexus peer can lead to port suspension.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vpc</b>
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
                        <div>Enable lacp convergence for vPC port channels.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>links</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This dict contains configurable options related to max and min port-channel links. Applicable only for Port-channel.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Port-channel max bundle.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>min</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Port-channel min links.</div>
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
                                    <li>delay</li>
                        </ul>
                </td>
                <td>
                        <div>LACP mode. Applicable only for Port-channel.</div>
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
                        <div>Name of the interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>port_priority</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>LACP port priority for the interface. Range 1-65535. Applicable only for Ethernet.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>fast</li>
                                    <li>normal</li>
                        </ul>
                </td>
                <td>
                        <div>Rate at which PDUs are sent by LACP. Applicable only for Ethernet. At fast rate LACP is transmitted once every 1 second. At normal rate LACP is transmitted every 30 seconds after the link is bundled.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>suspend_individual</b>
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
                        <div>port-channel lacp state. Disabling this will cause lacp to put the port to individual state and not suspend the port in case it does not get LACP BPDU from the peer ports in the port-channel.</div>
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

    - name: Merge provided configuration with device configuration.
      cisco.nxos.nxos_lacp_interfaces:
        config:
        - name: Ethernet1/3
          port_priority: 5
          rate: fast
        state: merged

    # After state:
    # ------------
    #
    # interface Ethernet1/3
    # lacp port-priority 5
    # lacp rate fast


    # Using replaced

    # Before state:
    # -------------
    #
    # interface Ethernet1/3
    #   lacp port-priority 5
    # interface port-channel11
    #   lacp mode delay

    - name: Replace device lacp interfaces configuration with the given configuration.
      cisco.nxos.nxos_lacp_interfaces:
        config:
        - name: port-channel11
          links:
            min: 4
        state: replaced

    # After state:
    # ------------
    #
    # interface Ethernet1/3
    #   lacp port-priority 5
    # interface port-channel11
    #   lacp min-links 4


    # Using overridden

    # Before state:
    # -------------
    #
    # interface Ethernet1/3
    #   lacp port-priority 5
    # interface port-channel11
    #   lacp mode delay

    - name: Override device configuration of all LACP interfaces attributes of given interfaces
        on device with provided configuration.
      cisco.nxos.nxos_lacp_interfaces:
        config:
        - name: port-channel11
          links:
            min: 4
        state: overridden

    # After state:
    # ------------
    #
    # interface port-channel11
    # lacp min-links 4


    # Using deleted

    # Before state:
    # -------------
    #
    # interface Ethernet1/3
    #   lacp port-priority 5
    # interface port-channel11
    #   lacp mode delay

    - name: Delete LACP interfaces configurations.
      cisco.nxos.nxos_lacp_interfaces:
        state: deleted

    # After state:
    # ------------
    #

    # Using rendered

    - name: Use rendered state to convert task input to device specific commands
      cisco.nxos.nxos_lacp_interfaces:
        config:
        - name: Ethernet1/800
          rate: fast
        - name: Ethernet1/801
          rate: fast
          port_priority: 32
        - name: port-channel10
          links:
            max: 15
            min: 2
          convergence:
            graceful: true
        state: rendered

    # Task Output (redacted)
    # -----------------------

    # rendered:
    #  - "interface Ethernet1/800"
    #  - "lacp rate fast"
    #  - "interface Ethernet1/801"
    #  - "lacp port-priority 32"
    #  - "lacp rate fast"
    #  - "interface port-channel10"
    #  - "lacp min-links 2"
    #  - "lacp max-bundle 15"
    #  - "lacp graceful-convergence"

    # Using parsed

    # parsed.cfg
    # ------------

    # interface port-channel10
    #   lacp min-links 10
    #   lacp max-bundle 15
    # interface Ethernet1/800
    #   lacp port-priority 100
    #   lacp rate fast

    - name: Use parsed state to convert externally supplied config to structured format
      cisco.nxos.nxos_lacp_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output (redacted)
    # -----------------------

    # parsed:
    #   - name: port-channel10
    #     links:
    #       max: 15
    #       min: 10
    #   - name: Ethernet1/800
    #     port_priority: 100
    #     rate: fast

    # Using gathered

    # Existing device config state
    # -------------------------------
    # interface Ethernet1/1
    #   lacp port-priority 5
    #   lacp rate fast
    # interface port-channel10
    #   lacp mode delay
    # interface port-channel11
    #   lacp max-bundle 10
    #   lacp min-links 5

    - name: Gather lacp_interfaces facts from the device using nxos_lacp_interfaces
      cisco.nxos.nxos_lacp_interfaces:
        state: gathered

    # Task output (redacted)
    # -----------------------
    # gathered:
    #  - name: Ethernet1/1
    #    port_priority: 5
    #    rate: fast
    #  - name: port-channel10
    #    mode: delay
    #  - name: port-channel11
    #    links:
    #      max: 10
    #      min: 5



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface port-channel10&#x27;, &#x27;lacp min-links 5&#x27;, &#x27;lacp mode delay&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Trishna Guha (@trishnaguha)
