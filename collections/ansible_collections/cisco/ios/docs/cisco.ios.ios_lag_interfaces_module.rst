.. _cisco.ios.ios_lag_interfaces_module:


****************************
cisco.ios.ios_lag_interfaces
****************************

**LAG interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages properties of Link Aggregation Group on Cisco IOS devices.




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
                        <div>Interface options for the link aggregation group.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>link</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Assign a link identifier used for load-balancing.</div>
                        <div>Refer to vendor documentation for valid values.</div>
                        <div>NOTE, parameter only supported on Cisco IOS XE platform.</div>
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
                        <div>Interface member of the link aggregation group.</div>
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
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>auto</li>
                                    <li>on</li>
                                    <li>desirable</li>
                                    <li>active</li>
                                    <li>passive</li>
                        </ul>
                </td>
                <td>
                        <div>Etherchannel Mode of the interface for link aggregation.</div>
                        <div>On mode has to be quoted as &#x27;on&#x27; or else pyyaml will convert to True before it gets to Ansible.</div>
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
                        <div>ID of Ethernet Channel of interfaces.</div>
                        <div>Refer to vendor documentation for valid port values.</div>
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
                                    <li>parsed</li>
                                    <li>gathered</li>
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
    #
    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    # interface GigabitEthernet0/1
    #  shutdown
    # interface GigabitEthernet0/2
    #  shutdown
    # interface GigabitEthernet0/3
    #  shutdown
    # interface GigabitEthernet0/4
    #  shutdown

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_lag_interfaces:
        config:
        - name: 10
          members:
          - member: GigabitEthernet0/1
            mode: auto
          - member: GigabitEthernet0/2
            mode: auto
        - name: 20
          members:
          - member: GigabitEthernet0/3
            mode: on
        - name: 30
          members:
          - member: GigabitEthernet0/4
            mode: active
        state: merged

    # After state:
    # ------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    #  channel-group 10 mode auto
    # interface GigabitEthernet0/2
    #  shutdown
    #  channel-group 10 mode auto
    # interface GigabitEthernet0/3
    #  shutdown
    #  channel-group 20 mode on
    # interface GigabitEthernet0/4
    #  shutdown
    #  channel-group 30 mode active

    # Using overridden
    #
    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    #  channel-group 10 mode auto
    # interface GigabitEthernet0/2
    #  shutdown
    #  channel-group 10 mode auto
    # interface GigabitEthernet0/3
    #  shutdown
    #  channel-group 20 mode on
    # interface GigabitEthernet0/4
    #  shutdown
    #  channel-group 30 mode active

    - name: Override device configuration of all interfaces with provided configuration
      cisco.ios.ios_lag_interfaces:
        config:
        - name: 20
          members:
          - member: GigabitEthernet0/2
            mode: auto
          - member: GigabitEthernet0/3
            mode: auto
        state: overridden

    # After state:
    # ------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    # interface GigabitEthernet0/2
    #  shutdown
    #  channel-group 20 mode auto
    # interface GigabitEthernet0/3
    #  shutdown
    #  channel-group 20 mode auto
    # interface GigabitEthernet0/4
    #  shutdown

    # Using replaced
    #
    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    #  channel-group 10 mode auto
    # interface GigabitEthernet0/2
    #  shutdown
    #  channel-group 10 mode auto
    # interface GigabitEthernet0/3
    #  shutdown
    #  channel-group 20 mode on
    # interface GigabitEthernet0/4
    #  shutdown
    #  channel-group 30 mode active

    - name: Replaces device configuration of listed interfaces with provided configuration
      cisco.ios.ios_lag_interfaces:
        config:
        - name: 40
          members:
          - member: GigabitEthernet0/3
            mode: auto
        state: replaced

    # After state:
    # ------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    # interface Port-channel20
    # interface Port-channel30
    # interface Port-channel40
    # interface GigabitEthernet0/1
    #  shutdown
    #  channel-group 10 mode auto
    # interface GigabitEthernet0/2
    #  shutdown
    #  channel-group 10 mode auto
    # interface GigabitEthernet0/3
    #  shutdown
    #  channel-group 40 mode on
    # interface GigabitEthernet0/4
    #  shutdown
    #  channel-group 30 mode active

    # Using Deleted
    #
    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    #  channel-group 10 mode auto
    # interface GigabitEthernet0/2
    #  shutdown
    #  channel-group 10 mode auto
    # interface GigabitEthernet0/3
    #  shutdown
    #  channel-group 20 mode on
    # interface GigabitEthernet0/4
    #  shutdown
    #  channel-group 30 mode active

    - name: "Delete LAG attributes of given interfaces (Note: This won't delete the interface itself)"
      cisco.ios.ios_lag_interfaces:
        config:
        - name: 10
        - name: 20
        state: deleted

    # After state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    # interface GigabitEthernet0/2
    #  shutdown
    # interface GigabitEthernet0/3
    #  shutdown
    # interface GigabitEthernet0/4
    #  shutdown
    #  channel-group 30 mode active

    # Using Deleted without any config passed
    #"(NOTE: This will delete all of configured LLDP module attributes)"

    #
    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    #  channel-group 10 mode auto
    # interface GigabitEthernet0/2
    #  shutdown
    #  channel-group 10 mode auto
    # interface GigabitEthernet0/3
    #  shutdown
    #  channel-group 20 mode on
    # interface GigabitEthernet0/4
    #  shutdown
    #  channel-group 30 mode active

    - name: "Delete all configured LAG attributes for interfaces (Note: This won't delete the interface itself)"
      cisco.ios.ios_lag_interfaces:
        state: deleted

    # After state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    # interface GigabitEthernet0/2
    #  shutdown
    # interface GigabitEthernet0/3
    #  shutdown
    # interface GigabitEthernet0/4
    #  shutdown

    # Using Gathered

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel11
    # interface Port-channel22
    # interface GigabitEthernet0/1
    #  shutdown
    #  channel-group 11 mode active
    # interface GigabitEthernet0/2
    #  shutdown
    #  channel-group 22 mode active

    - name: Gather listed LAG interfaces with provided configurations
      cisco.ios.ios_lag_interfaces:
        config:
        state: gathered

    # Module Execution Result:
    # ------------------------
    #
    # "gathered": [
    #     {
    #         "members": [
    #             {
    #                 "member": "GigabitEthernet0/1",
    #                 "mode": "active"
    #             }
    #         ],
    #         "name": "Port-channel11"
    #     },
    #     {
    #         "members": [
    #             {
    #                 "member": "GigabitEthernet0/2",
    #                 "mode": "active"
    #             }
    #         ],
    #         "name": "Port-channel22"
    #     }
    # ]

    # After state:
    # ------------
    #
    # vios#sh running-config | section ^interface
    # interface Port-channel11
    # interface Port-channel22
    # interface GigabitEthernet0/1
    #  shutdown
    #  channel-group 11 mode active
    # interface GigabitEthernet0/2
    #  shutdown
    #  channel-group 22 mode active

    # Using Rendered

    - name: Render the commands for provided  configuration
      cisco.ios.ios_lag_interfaces:
        config:
          - name: Port-channel11
            members:
              - member: GigabitEthernet0/1
                mode: active
          - name: Port-channel22
            members:
              - member: GigabitEthernet0/2
                mode: passive
        state: rendered

    # Module Execution Result:
    # ------------------------
    #
    # "rendered": [
    #         "interface GigabitEthernet0/1",
    #         "channel-group 11 mode active",
    #         "interface GigabitEthernet0/2",
    #         "channel-group 22 mode passive",
    #     ]

    # Using Parsed

    #  File: parsed.cfg
    # ----------------
    #
    # interface GigabitEthernet0/1
    # channel-group 11 mode active
    # interface GigabitEthernet0/2
    # channel-group 22 mode passive

    - name: Parse the commands for provided configuration
      cisco.ios.ios_lag_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------
    #
    # "parsed": [
    #     {
    #         "members": [
    #             {
    #                 "member": "GigabitEthernet0/1",
    #                 "mode": "active"
    #             }
    #         ],
    #         "name": "Port-channel11"
    #     },
    #     {
    #         "members": [
    #             {
    #                 "member": "GigabitEthernet0/2",
    #                 "mode": "passive"
    #             }
    #         ],
    #         "name": "Port-channel22"
    #     }
    # ]



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet0/1&#x27;, &#x27;channel-group 1 mode active&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sumit Jaiswal (@justjais)
