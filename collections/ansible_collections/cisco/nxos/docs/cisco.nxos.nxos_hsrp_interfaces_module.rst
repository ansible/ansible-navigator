.. _cisco.nxos.nxos_hsrp_interfaces_module:


*******************************
cisco.nxos.nxos_hsrp_interfaces
*******************************

**HSRP interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Manages Hot Standby Router Protocol (HSRP) interface attributes.




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
                        <div>The provided configuration</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bfd</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>enable</li>
                                    <li>disable</li>
                        </ul>
                </td>
                <td>
                        <div>Enable/Disable HSRP Bidirectional Forwarding Detection (BFD) on the interface.</div>
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
                        <div>The name of the interface.</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section &#x27;^interface&#x27;</b>.</div>
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
                        <div>The state the configuration should be left in</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NX-OS 7.0(3)I5(1).
   - Feature bfd should be enabled for this module.



Examples
--------

.. code-block:: yaml

    # Using deleted

    - name: Configure hsrp attributes on interfaces
      cisco.nxos.nxos_hsrp_interfaces:
        config:
        - name: Ethernet1/1
        - name: Ethernet1/2
        operation: deleted


    # Using merged

    - name: Configure hsrp attributes on interfaces
      cisco.nxos.nxos_hsrp_interfaces:
        config:
        - name: Ethernet1/1
          bfd: enable
        - name: Ethernet1/2
          bfd: disable
        operation: merged


    # Using overridden

    - name: Configure hsrp attributes on interfaces
      cisco.nxos.nxos_hsrp_interfaces:
        config:
        - name: Ethernet1/1
          bfd: enable
        - name: Ethernet1/2
          bfd: disable
        operation: overridden


    # Using replaced

    - name: Configure hsrp attributes on interfaces
      cisco.nxos.nxos_hsrp_interfaces:
        config:
        - name: Ethernet1/1
          bfd: enable
        - name: Ethernet1/2
          bfd: disable
        operation: replaced

    # Using rendered

    - name: Use rendered state to convert task input to device specific commands
      cisco.nxos.nxos_hsrp_interfaces:
        config:
        - name: Ethernet1/800
          bfd: enable
        - name: Ethernet1/801
          bfd: enable
        state: rendered

    # Task Output (redacted)
    # -----------------------

    # rendered:
    #   - "interface Ethernet1/800"
    #   - "hsrp bfd"
    #   - "interface Ethernet1/801"
    #   - "hsrp bfd"

    # Using parsed

    # parsed.cfg
    # ------------
    # interface Ethernet1/800
    #   no switchport
    #   hsrp bfd
    # interface Ethernet1/801
    #   no switchport
    #   hsrp bfd

    - name: Use parsed state to convert externally supplied config to structured format
      cisco.nxos.nxos_hsrp_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output (redacted)
    # -----------------------

    # parsed:
    #   - name: Ethernet1/800
    #     bfd: enable
    #   - name: Ethernet1/801
    #     bfd: enable

    # Using gathered

    # Existing device config state
    # -------------------------------

    # interface Ethernet1/1
    #   no switchport
    #   hsrp bfd
    # interface Ethernet1/2
    #   no switchport
    #   hsrp bfd
    # interface Ethernet1/3
    #   no switchport

    - name: Gather hsrp_interfaces facts from the device using nxos_hsrp_interfaces
      cisco.nxos.nxos_hsrp_interfaces:
        state: gathered

    # Task output (redacted)
    # -----------------------

    # gathered:
    #   - name: Ethernet1/1
    #     bfd: enable
    #   - name: Ethernet1/2
    #     bfd: enable



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
                            <div>The resulting configuration model invocation.</div>
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
                            <div>The configuration prior to the model invocation.</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/1&#x27;, &#x27;hsrp bfd&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Chris Van Heuveln (@chrisvanheuveln)
