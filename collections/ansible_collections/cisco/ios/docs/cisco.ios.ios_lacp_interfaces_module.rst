.. _cisco.ios.ios_lacp_interfaces_module:


*****************************
cisco.ios.ios_lacp_interfaces
*****************************

**LACP interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of LACP on Cisco IOS network devices lacp_interfaces.




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
                        <div>A dictionary of LACP lacp_interfaces option</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>fast_switchover</b>
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
                        <div>LACP fast switchover supported on this port channel.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_bundle</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>LACP maximum number of ports to bundle in this port channel.</div>
                        <div>Refer to vendor documentation for valid port values.</div>
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
                        <div>Name of the Interface for configuring LACP.</div>
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
                        <div>LACP priority on this interface.</div>
                        <div>Refer to vendor documentation for valid port values.</div>
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>show running-config | section ^interface</b>.</div>
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
                                    <li>rendered</li>
                                    <li>gathered</li>
                                    <li>parsed</li>
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
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    # interface GigabitEthernet0/2
    #  shutdown
    # interface GigabitEthernet0/3
    #  shutdown

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_lacp_interfaces:
        config:
        - name: GigabitEthernet0/1
          port_priority: 10
        - name: GigabitEthernet0/2
          port_priority: 20
        - name: GigabitEthernet0/3
          port_priority: 30
        - name: Port-channel10
          fast_switchover: true
          max_bundle: 5
        state: merged

    # After state:
    # ------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    #  lacp fast-switchover
    #  lacp max-bundle 5
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    #  lacp port-priority 10
    # interface GigabitEthernet0/2
    #  shutdown
    #  lacp port-priority 20
    # interface GigabitEthernet0/3
    #  shutdown
    #  lacp port-priority 30

    # Using overridden
    #
    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    #  lacp fast-switchover
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    #  lacp port-priority 10
    # interface GigabitEthernet0/2
    #  shutdown
    #  lacp port-priority 20
    # interface GigabitEthernet0/3
    #  shutdown
    #  lacp port-priority 30

    - name: Override device configuration of all lacp_interfaces with provided configuration
      cisco.ios.ios_lacp_interfaces:
        config:
        - name: GigabitEthernet0/1
          port_priority: 20
        - name: Port-channel10
          max_bundle: 2
        state: overridden

    # After state:
    # ------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    #  lacp max-bundle 2
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    #  lacp port-priority 20
    # interface GigabitEthernet0/2
    #  shutdown
    # interface GigabitEthernet0/3
    #  shutdown

    # Using replaced
    #
    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    #  lacp max-bundle 5
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    #  lacp port-priority 10
    # interface GigabitEthernet0/2
    #  shutdown
    #  lacp port-priority 20
    # interface GigabitEthernet0/3
    #  shutdown
    #  lacp port-priority 30

    - name: Replaces device configuration of listed lacp_interfaces with provided configuration
      cisco.ios.ios_lacp_interfaces:
        config:
        - name: GigabitEthernet0/3
          port_priority: 40
        - name: Port-channel10
          fast_switchover: true
          max_bundle: 2
        state: replaced

    # After state:
    # ------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    #  lacp fast-switchover
    #  lacp max-bundle 2
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    #  lacp port-priority 10
    # interface GigabitEthernet0/2
    #  shutdown
    #  lacp port-priority 20
    # interface GigabitEthernet0/3
    #  shutdown
    #  lacp port-priority 40

    # Using Deleted
    #
    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    #  flowcontrol receive on
    # interface Port-channel20
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    #  lacp port-priority 10
    # interface GigabitEthernet0/2
    #  shutdown
    #  lacp port-priority 20
    # interface GigabitEthernet0/3
    #  shutdown
    #  lacp port-priority 30

    - name: "Delete LACP attributes of given interfaces (Note: This won't delete the interface itself)"
      cisco.ios.ios_lacp_interfaces:
        config:
        - name: GigabitEthernet0/1
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
    #  lacp port-priority 20
    # interface GigabitEthernet0/3
    #  shutdown
    #  lacp port-priority 30

    # Using Deleted without any config passed
    # "(NOTE: This will delete all of configured LLDP module attributes)"
    #
    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface Port-channel10
    #  lacp fast-switchover
    # interface Port-channel20
    #  lacp max-bundle 2
    # interface Port-channel30
    # interface GigabitEthernet0/1
    #  shutdown
    #  lacp port-priority 10
    # interface GigabitEthernet0/2
    #  shutdown
    #  lacp port-priority 20
    # interface GigabitEthernet0/3
    #  shutdown
    #  lacp port-priority 30

    - name: "Delete LACP attributes for all configured interfaces (Note: This won't delete the interface itself)"
      cisco.ios.ios_lacp_interfaces:
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

    # Using Gathered

    # Before state:
    # -------------
    #
    # vios#sh running-config | section ^interface
    # interface Port-channel10
    #  lacp fast-switchover
    #  lacp max-bundle 2
    # interface Port-channel40
    #  lacp max-bundle 5
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  lacp port-priority 30
    # interface GigabitEthernet0/2
    #  lacp port-priority 20

    - name: Gather listed LACP interfaces with provided configurations
      cisco.ios.ios_lacp_interfaces:
        config:
        state: gathered

    # Module Execution Result:
    # ------------------------
    #
    # "gathered": [
    #         {
    #             "fast_switchover": true,
    #             "max_bundle": 2,
    #             "name": "Port-channel10"
    #         },
    #         {
    #             "max_bundle": 5,
    #             "name": "Port-channel40"
    #         },
    #         {
    #             "name": "GigabitEthernet0/0"
    #         },
    #         {
    #             "name": "GigabitEthernet0/1",
    #             "port_priority": 30
    #         },
    #         {
    #             "name": "GigabitEthernet0/2",
    #             "port_priority": 20
    #         }
    #     ]

    # After state:
    # ------------
    #
    # vios#sh running-config | section ^interface
    # interface Port-channel10
    #  lacp fast-switchover
    #  lacp max-bundle 2
    # interface Port-channel40
    #  lacp max-bundle 5
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  lacp port-priority 30
    # interface GigabitEthernet0/2
    #  lacp port-priority 20

    # Using Rendered

    - name: Render the commands for provided  configuration
      cisco.ios.ios_lacp_interfaces:
        config:
        - name: GigabitEthernet0/1
          port_priority: 10
        - name: GigabitEthernet0/2
          port_priority: 20
        - name: Port-channel10
          fast_switchover: true
          max_bundle: 2
        state: rendered

    # Module Execution Result:
    # ------------------------
    #
    # "rendered": [
    #         "interface GigabitEthernet0/1",
    #         "lacp port-priority 10",
    #         "interface GigabitEthernet0/2",
    #         "lacp port-priority 20",
    #         "interface Port-channel10",
    #         "lacp max-bundle 2",
    #         "lacp fast-switchover"
    #     ]

    # Using Parsed

    # File: parsed.cfg
    # ----------------
    #
    # interface GigabitEthernet0/1
    # lacp port-priority 10
    # interface GigabitEthernet0/2
    # lacp port-priority 20
    # interface Port-channel10
    # lacp max-bundle 2 fast-switchover

    - name: Parse the commands for provided configuration
      cisco.ios.ios_lacp_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------
    #
    # "parsed": [
    #         {
    #             "name": "GigabitEthernet0/1",
    #             "port_priority": 10
    #         },
    #         {
    #             "name": "GigabitEthernet0/2",
    #             "port_priority": 20
    #         },
    #         {
    #             "fast_switchover": true,
    #             "max_bundle": 2,
    #             "name": "Port-channel10"
    #         }
    #     ]



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet 0/1&#x27;, &#x27;lacp port-priority 30&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sumit Jaiswal (@justjais)
