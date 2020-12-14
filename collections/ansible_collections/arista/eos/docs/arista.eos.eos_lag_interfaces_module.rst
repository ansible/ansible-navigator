.. _arista.eos.eos_lag_interfaces_module:


*****************************
arista.eos.eos_lag_interfaces
*****************************

**LAG interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages attributes of link aggregation groups on Arista EOS devices.




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
                        <div>Ethernet interfaces that are part of the group.</div>
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
                        <div>Name of ethernet interface that is a member of the LAG.</div>
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
                        <div>LAG mode for this interface.</div>
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
                        <div>Name of the port-channel interface of the link aggregation group (LAG) e.g., Port-Channel5.</div>
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
                        <div>The value of this option should be the output received from the EOS device by executing the command <b>show running-config | section interfaces</b>.</div>
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

    # Before state:
    # -------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    #   channel-group 5 mode on
    # interface Ethernet2

    - name: Merge provided LAG attributes with existing device configuration
      arista.eos.eos_lag_interfaces:
        config:
        - name: 5
          members:
          - member: Ethernet2
            mode: on
        state: merged

    # After state:
    # ------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    #   channel-group 5 mode on
    # interface Ethernet2
    #   channel-group 5 mode on


    # Using replaced

    # Before state:
    # -------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    #   channel-group 5 mode on
    # interface Ethernet2

    - name: Replace all device configuration of specified LAGs with provided configuration
      arista.eos.eos_lag_interfaces:
        config:
        - name: 5
          members:
          - member: Ethernet2
            mode: on
        state: replaced

    # After state:
    # ------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    # interface Ethernet2
    #   channel-group 5 mode on


    # Using overridden

    # Before state:
    # -------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    #   channel-group 5 mode on
    # interface Ethernet2

    - name: Override all device configuration of all LAG attributes with provided configuration
      arista.eos.eos_lag_interfaces:
        config:
        - name: 10
          members:
          - member: Ethernet2
            mode: on
        state: overridden

    # After state:
    # ------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    # interface Ethernet2
    #   channel-group 10 mode on


    # Using deleted

    # Before state:
    # -------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    #   channel-group 5 mode on
    # interface Ethernet2
    #   channel-group 5 mode on

    - name: Delete LAG attributes of the given interfaces.
      arista.eos.eos_lag_interfaces:
        config:
        - name: 5
          members:
          - member: Ethernet1
        state: deleted

    # After state:
    # ------------
    #
    # veos#show running-config | section interface
    # interface Ethernet1
    # interface Ethernet2
    #   channel-group 5 mode on

    # Using parsed:

    # parsed.cfg
    # interface Ethernet1
    #   channel-group 5 mode on
    # interface Ethernet2
    #   channel-group 5 mode on

    - name: Use parsed to convert native configs to structured data
      arista.eos.lag_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Output:
    #   parsed:
    #     - name: 5
    #       members:
    #         - member: Ethernet2
    #           mode: on
    #         - member: Ethernet1
    #           mode: on

    # using rendered:

    - name: Use Rendered to convert the structured data to native config
      arista.eos.eos_lag_interfaces:
        config:
        - name: 5
          members:
          - member: Ethernet2
            mode: on
          - member: Ethernet1
            mode: on
        state: rendered
    # -----------
    # Output
    # -----------
    #
    # rendered:

    # interface Ethernet1
    #   channel-group 5 mode on
    # interface Ethernet2
    #   channel-group 5 mode on


    # Using gathered:

    # native config:
    # interface Ethernet1
    #   channel-group 5 mode on
    # interface Ethernet2
    #   channel-group 5 mode on

    - name: Gather lldp_global facts from the device
      arista.eos.lldp_global:
        state: gathered

    # Output:
    #   gathered:
    #     - name: 5
    #       members:
    #         - member: Ethernet2
    #           mode: on
    #         - member: Ethernet1
    #           mode: on



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;command 1&#x27;, &#x27;command 2&#x27;, &#x27;command 3&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Nathaniel Case (@Qalthos)
