.. _cisco.ios.ios_interfaces_module:


************************
cisco.ios.ios_interfaces
************************

**Interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the interface attributes of Cisco IOS network devices.




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
                        <div>Interface link status. Applicable for Ethernet interfaces only, either in half duplex, full duplex or in automatic state which negotiates the duplex automatically.</div>
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
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Administrative state of the interface.</div>
                        <div>Set the value to <code>true</code> to administratively enable the interface or <code>false</code> to disable it.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mtu</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>MTU for a specific interface. Applicable for Ethernet interfaces only.</div>
                        <div>Refer to vendor documentation for valid values.</div>
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
                        <div>Full name of interface, e.g. GigabitEthernet0/2, loopback999.</div>
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
   - Tested against Cisco IOSv Version 15.2 on VIRL



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  no ip address
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  no ip address
    #  duplex auto
    #  speed auto

    - name: Merge provided configuration with device configuration
      cisco.ios.ios_interfaces:
        config:
        - name: GigabitEthernet0/2
          description: Configured and Merged by Ansible Network
          enabled: true
        - name: GigabitEthernet0/3
          description: Configured and Merged by Ansible Network
          mtu: 2800
          enabled: false
          speed: 100
          duplex: full
        state: merged

    # After state:
    # ------------
    #
    # vios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description Configured and Merged by Ansible Network
    #  no ip address
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  description Configured and Merged by Ansible Network
    #  mtu 2800
    #  no ip address
    #  shutdown
    #  duplex full
    #  speed 100

    # Using replaced

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description Configured by Ansible Network
    #  no ip address
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  mtu 2000
    #  no ip address
    #  shutdown
    #  duplex full
    #  speed 100

    - name: Replaces device configuration of listed interfaces with provided configuration
      cisco.ios.ios_interfaces:
        config:
        - name: GigabitEthernet0/3
          description: Configured and Replaced by Ansible Network
          enabled: false
          duplex: auto
          mtu: 2500
          speed: 1000
        state: replaced

    # After state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description Configured by Ansible Network
    #  no ip address
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  description Configured and Replaced by Ansible Network
    #  mtu 2500
    #  no ip address
    #  shutdown
    #  duplex full
    #  speed 1000

    # Using overridden

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface#
    # interface GigabitEthernet0/1
    #  description Configured by Ansible
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description This is test
    #  no ip address
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  description Configured by Ansible
    #  mtu 2800
    #  no ip address
    #  shutdown
    #  duplex full
    #  speed 100

    - name: Override device configuration of all interfaces with provided configuration
      cisco.ios.ios_interfaces:
        config:
        - name: GigabitEthernet0/2
          description: Configured and Overridden by Ansible Network
          speed: 1000
        - name: GigabitEthernet0/3
          description: Configured and Overridden by Ansible Network
          enabled: false
          duplex: full
          mtu: 2000
        state: overridden

    # After state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description Configured and Overridden by Ansible Network
    #  no ip address
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  description Configured and Overridden by Ansible Network
    #  mtu 2000
    #  no ip address
    #  shutdown
    #  duplex full
    #  speed 100

    # Using Deleted

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description Configured by Ansible Network
    #  no ip address
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    #  mtu 2500
    #  no ip address
    #  shutdown
    #  duplex full
    #  speed 1000

    - name: "Delete module attributes of given interfaces (Note: This won't delete the interface itself)"
      cisco.ios.ios_interfaces:
        config:
        - name: GigabitEthernet0/2
        state: deleted

    # After state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    #  mtu 2500
    #  no ip address
    #  shutdown
    #  duplex full
    #  speed 1000

    # Using Deleted without any config passed
    #"(NOTE: This will delete all of configured resource module attributes from each configured interface)"

    # Before state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  description Configured by Ansible Network
    #  no ip address
    #  duplex auto
    #  speed 1000
    # interface GigabitEthernet0/3
    #  description Configured by Ansible Network
    #  mtu 2500
    #  no ip address
    #  shutdown
    #  duplex full
    #  speed 1000

    - name: "Delete module attributes of all interfaces (Note: This won't delete the interface itself)"
      cisco.ios.ios_interfaces:
        state: deleted

    # After state:
    # -------------
    #
    # vios#show running-config | section ^interface
    # interface GigabitEthernet0/1
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/2
    #  no ip address
    #  duplex auto
    #  speed auto
    # interface GigabitEthernet0/3
    #  no ip address
    #  duplex auto
    #  speed auto

    # Using Gathered

    # Before state:
    # -------------
    #
    # vios#sh running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description this is interface1
    #  mtu 65
    #  duplex auto
    #  speed 10
    # interface GigabitEthernet0/2
    #  description this is interface2
    #  mtu 110
    #  shutdown
    #  duplex auto
    #  speed 100

    - name: Gather listed interfaces with provided configurations
      cisco.ios.ios_interfaces:
        config:
        state: gathered

    # Module Execution Result:
    # ------------------------
    #
    # "gathered": [
    #         {
    #             "description": "this is interface1",
    #             "duplex": "auto",
    #             "enabled": true,
    #             "mtu": 65,
    #             "name": "GigabitEthernet0/1",
    #             "speed": "10"
    #         },
    #         {
    #             "description": "this is interface2",
    #             "duplex": "auto",
    #             "enabled": false,
    #             "mtu": 110,
    #             "name": "GigabitEthernet0/2",
    #             "speed": "100"
    #         }
    #     ]

    # After state:
    # ------------
    #
    # vios#sh running-config | section ^interface
    # interface GigabitEthernet0/1
    #  description this is interface1
    #  mtu 65
    #  duplex auto
    #  speed 10
    # interface GigabitEthernet0/2
    #  description this is interface2
    #  mtu 110
    #  shutdown
    #  duplex auto
    #  speed 100

    # Using Rendered

    - name: Render the commands for provided  configuration
      cisco.ios.ios_interfaces:
        config:
        - name: GigabitEthernet0/1
          description: Configured by Ansible-Network
          mtu: 110
          enabled: true
          duplex: half
        - name: GigabitEthernet0/2
          description: Configured by Ansible-Network
          mtu: 2800
          enabled: false
          speed: 100
          duplex: full
        state: rendered

    # Module Execution Result:
    # ------------------------
    #
    # "rendered": [
    #         "interface GigabitEthernet0/1",
    #         "description Configured by Ansible-Network",
    #         "mtu 110",
    #         "duplex half",
    #         "no shutdown",
    #         "interface GigabitEthernet0/2",
    #         "description Configured by Ansible-Network",
    #         "mtu 2800",
    #         "speed 100",
    #         "duplex full",
    #         "shutdown"

    # Using Parsed

    # File: parsed.cfg
    # ----------------
    #
    # interface GigabitEthernet0/1
    # description interfaces 0/1
    # mtu 110
    # duplex half
    # no shutdown
    # interface GigabitEthernet0/2
    # description interfaces 0/2
    # mtu 2800
    # speed 100
    # duplex full
    # shutdown

    - name: Parse the commands for provided configuration
      cisco.ios.ios_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------
    #
    # "parsed": [
    #         {
    #             "description": "interfaces 0/1",
    #             "duplex": "half",
    #             "enabled": true,
    #             "mtu": 110,
    #             "name": "GigabitEthernet0/1"
    #         },
    #         {
    #             "description": "interfaces 0/2",
    #             "duplex": "full",
    #             "enabled": true,
    #             "mtu": 2800,
    #             "name": "GigabitEthernet0/2",
    #             "speed": "100"
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet 0/1&#x27;, &#x27;description This is test&#x27;, &#x27;speed 100&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sumit Jaiswal (@justjais)
