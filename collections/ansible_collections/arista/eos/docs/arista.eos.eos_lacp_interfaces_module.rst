.. _arista.eos.eos_lacp_interfaces_module:


******************************
arista.eos.eos_lacp_interfaces
******************************

**LACP interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages Link Aggregation Control Protocol (LACP) attributes of interfaces on Arista EOS devices.




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
                        <div>A dictionary of LACP interfaces options.</div>
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
                        <div>Full name of the interface (i.e. Ethernet1).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>LACP port priority for the interface. Range 1-65535.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Rate at which PDUs are sent by LACP. At fast rate LACP is transmitted once every 1 second. At normal rate LACP is transmitted every 30 seconds after the link is bundled.</div>
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
                        <div>The value of this option should be the output received from the EOS device by executing the command <b>show running-config | section ^interfaces</b>.</div>
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
                                    <li>parsed</li>
                                    <li>rendered</li>
                                    <li>gathered</li>
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
   - Tested against Arista EOS 4.20.10M
   - This module works with connection ``network_cli``. See the `EOS Platform Options <../network/user_guide/platform_eos.html>`_.



Examples
--------

.. code-block:: yaml

    # Using merged
    #
    #
    # ------------
    # Before state
    # ------------
    #
    #
    # veos#show run | section ^interface
    # interface Ethernet1
    #    lacp port-priority 30
    # interface Ethernet2
    #    lacp rate fast

    - name: Merge provided configuration with device configuration
      arista.eos.eos_lacp_interfaces:
        config:
        - name: Ethernet1
          rate: fast
        - name: Ethernet2
          rate: normal
        state: merged

    #
    # -----------
    # After state
    # -----------
    #
    # veos#show run | section ^interface
    # interface Ethernet1
    #    lacp port-priority 30
    #    lacp rate fast
    # interface Ethernet2


    # Using replaced
    #
    #
    # ------------
    # Before state
    # ------------
    #
    #
    # veos#show run | section ^interface
    # interface Ethernet1
    #    lacp port-priority 30
    # interface Ethernet2
    #    lacp rate fast

    - name: Replace existing LACP configuration of specified interfaces with provided
        configuration
      arista.eos.eos_lacp_interfaces:
        config:
        - name: Ethernet1
          rate: fast
        state: replaced

    #
    # -----------
    # After state
    # -----------
    #
    # veos#show run | section ^interface
    # interface Ethernet1
    #    lacp rate fast
    # interface Ethernet2
    #    lacp rate fast


    # Using overridden
    #
    #
    # ------------
    # Before state
    # ------------
    #
    #
    # veos#show run | section ^interface
    # interface Ethernet1
    #    lacp port-priority 30
    # interface Ethernet2
    #    lacp rate fast

    - name: Override the LACP configuration of all the interfaces with provided configuration
      arista.eos.eos_lacp_interfaces:
        config:
        - name: Ethernet1
          rate: fast
        state: overridden

    #
    # -----------
    # After state
    #
    #
    # veos#show run | section ^interface
    # interface Ethernet1
    #    lacp rate fast
    # interface Ethernet2


    # Using deleted
    #
    #
    # ------------
    # Before state
    # ------------
    #
    #
    # veos#show run | section ^interface
    # interface Ethernet1
    #    lacp port-priority 30
    # interface Ethernet2
    #    lacp rate fast

    - name: Delete LACP attributes of given interfaces (or all interfaces if none specified).
      arista.eos.eos_lacp_interfaces:
        state: deleted

    #
    # -----------
    # After state
    # -----------
    #
    # veos#show run | section ^interface
    # interface Ethernet1
    # interface Ethernet2

    # using rendered:

    - name: Use Rendered to convert the structured data to native config
      arista.eos.eos_lacp_interfaces:
        config:
        - name: Ethernet1
          rate: fast
        - name: Ethernet2
          rate: normal
        state: rendered

    #
    # -----------
    # Output
    # -----------
    # rendered:
    #   - "interface Ethernet1"
    #   - "lacp rate fast"

    # Using parsed:

    # parsed.cfg:
    #    "interface Ethernet1"
    #    "lacp rate fast"
    #    "interface Ethernet2"

    - name: Use parsed to convert native configs to structured data
      arista.eos.eos_lacp_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Output:
    # parsed:
    #   - name: Ethernet1
    #     rate: fast
    #   - name: Ethernet2
    #     rate: normal

    # Using gathered:
    # native config:
    #  veos#show run | section ^interface
    # interface Ethernet1
    #    lacp port-priority 30
    # interface Ethernet2
    #    lacp rate fast

    - name: Gather LACP facts from the device
      arista.eos.eos_lacp_interfaces:
        state: gathered

    # Output:
    # gathered:
    #   - name: Ethernet1
    #   - name: Ethernet2
    #     rate: fast



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1&#x27;, &#x27;lacp rate fast&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Nathaniel Case (@Qalthos)
