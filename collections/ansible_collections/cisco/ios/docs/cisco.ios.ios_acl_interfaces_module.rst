.. _cisco.ios.ios_acl_interfaces_module:


****************************
cisco.ios.ios_acl_interfaces
****************************

**ACL interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module configures and manages the access-control (ACL) attributes of interfaces on IOS platforms.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="4">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="4">
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
                        <div>A dictionary of ACL interfaces options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>access_groups</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify access-group for IP access list (standard or extended).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>acls</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies the ACLs for the provided AFI.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>direction</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>in</li>
                                    <li>out</li>
                        </ul>
                </td>
                <td>
                        <div>Specifies the direction of packets that the ACL will be applied on.</div>
                        <div>With one direction already assigned, other acl direction cannot be same.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
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
                        <div>Specifies the name of the IPv4/IPv4 ACL for the interface.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>afi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ipv4</li>
                                    <li>ipv6</li>
                        </ul>
                </td>
                <td>
                        <div>Specifies the AFI for the ACLs to be configured on this interface.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>Full name of the interface excluding any logical unit number, i.e. GigabitEthernet0/1.</div>
                </td>
            </tr>

            <tr>
                <td colspan="4">
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
                        <div>The module, by default, will connect to the remote device and retrieve the current running-config to use as a base for comparing against the contents of source. There are times when it is not desirable to have the task get the current running-config for every task in a playbook.  The <em>running_config</em> argument allows the implementer to pass in the configuration to use as the base config for comparison. This value of this option should be the output received from device by executing command.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
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
                                    <li>parsed</li>
                                    <li>rendered</li>
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

    # Using Merged

    # Before state:
    # -------------
    #
    # vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
    # interface Loopback888
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    # interface GigabitEthernet0/2
    #  ip access-group 123 out

    - name: Merge module attributes of given access-groups
      cisco.ios.ios_acl_interfaces:
        config:
        - name: GigabitEthernet0/1
          access_groups:
          - afi: ipv4
            acls:
            - name: 110
              direction: in
            - name: 123
              direction: out
          - afi: ipv6
            acls:
            - name: test_v6
              direction: out
            - name: temp_v6
              direction: in
        - name: GigabitEthernet0/2
          access_groups:
          - afi: ipv4
            acls:
            - name: 100
              direction: in
        state: merged

    # Commands Fired:
    # ---------------
    #
    # interface GigabitEthernet0/1
    #  ip access-group 110 in
    #  ip access-group 123 out
    #  ipv6 traffic-filter test_v6 out
    #  ipv6 traffic-filter temp_v6 in
    # interface GigabitEthernet0/2
    #  ip access-group 100 in
    #  ip access-group 123 out


    # After state:
    # -------------
    #
    # vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
    # interface Loopback888
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip access-group 110 in
    #  ip access-group 123 out
    #  ipv6 traffic-filter test_v6 out
    #  ipv6 traffic-filter temp_v6 in
    # interface GigabitEthernet0/2
    #  ip access-group 110 in
    #  ip access-group 123 out

    # Using Replaced

    # Before state:
    # -------------
    #
    # vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
    # interface Loopback888
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip access-group 110 in
    #  ip access-group 123 out
    #  ipv6 traffic-filter test_v6 out
    #  ipv6 traffic-filter temp_v6 in
    # interface GigabitEthernet0/2
    #  ip access-group 110 in
    #  ip access-group 123 out

    - name: Replace module attributes of given access-groups
      cisco.ios.ios_acl_interfaces:
        config:
        - name: GigabitEthernet0/1
          access_groups:
          - afi: ipv4
            acls:
            - name: 100
              direction: out
            - name: 110
              direction: in
        state: replaced

    # Commands Fired:
    # ---------------
    #
    # interface GigabitEthernet0/1
    # no ip access-group 123 out
    # no ipv6 traffic-filter temp_v6 in
    # no ipv6 traffic-filter test_v6 out
    # ip access-group 100 out

    # After state:
    # -------------
    #
    # vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
    # interface Loopback888
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip access-group 100 out
    #  ip access-group 110 in
    # interface GigabitEthernet0/2
    #  ip access-group 110 in
    #  ip access-group 123 out

    # Using Overridden

    # Before state:
    # -------------
    #
    # vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
    # interface Loopback888
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip access-group 110 in
    #  ip access-group 123 out
    #  ipv6 traffic-filter test_v6 out
    #  ipv6 traffic-filter temp_v6 in
    # interface GigabitEthernet0/2
    #  ip access-group 110 in
    #  ip access-group 123 out

    - name: Overridden module attributes of given access-groups
      cisco.ios.ios_acl_interfaces:
        config:
        - name: GigabitEthernet0/1
          access_groups:
          - afi: ipv4
            acls:
            - name: 100
              direction: out
            - name: 110
              direction: in
        state: overridden

    # Commands Fired:
    # ---------------
    #
    # interface GigabitEthernet0/1
    # no ip access-group 123 out
    # no ipv6 traffic-filter test_v6 out
    # no ipv6 traffic-filter temp_v6 in
    # ip access-group 100 out
    # interface GigabitEthernet0/2
    # no ip access-group 110 in
    # no ip access-group 123 out

    # After state:
    # -------------
    #
    # vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
    # interface Loopback888
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip access-group 100 out
    #  ip access-group 110 in
    # interface GigabitEthernet0/2

    # Using Deleted

    # Before state:
    # -------------
    #
    # vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
    # interface Loopback888
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip access-group 110 in
    #  ip access-group 123 out
    #  ipv6 traffic-filter test_v6 out
    #  ipv6 traffic-filter temp_v6 in
    # interface GigabitEthernet0/2
    #  ip access-group 110 in
    #  ip access-group 123 out

    - name: Delete module attributes of given Interface
      cisco.ios.ios_acl_interfaces:
        config:
        - name: GigabitEthernet0/1
        state: deleted

    # Commands Fired:
    # ---------------
    #
    # interface GigabitEthernet0/1
    # no ip access-group 110 in
    # no ip access-group 123 out
    # no ipv6 traffic-filter test_v6 out
    # no ipv6 traffic-filter temp_v6 in

    # After state:
    # -------------
    #
    # vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
    # interface Loopback888
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    # interface GigabitEthernet0/2
    #  ip access-group 110 in
    #  ip access-group 123 out

    # Using DELETED without any config passed
    #"(NOTE: This will delete all of configured resource module attributes from each configured interface)"

    # Before state:
    # -------------
    #
    # vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
    # interface Loopback888
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip access-group 110 in
    #  ip access-group 123 out
    #  ipv6 traffic-filter test_v6 out
    #  ipv6 traffic-filter temp_v6 in
    # interface GigabitEthernet0/2
    #  ip access-group 110 in
    #  ip access-group 123 out

    - name: Delete module attributes of given access-groups from ALL Interfaces
      cisco.ios.ios_acl_interfaces:
        config:
        state: deleted

    # Commands Fired:
    # ---------------
    #
    # interface GigabitEthernet0/1
    # no ip access-group 110 in
    # no ip access-group 123 out
    # no ipv6 traffic-filter test_v6 out
    # no ipv6 traffic-filter temp_v6 in
    # interface GigabitEthernet0/2
    # no ip access-group 110 out
    # no ip access-group 123 out

    # After state:
    # -------------
    #
    # vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
    # interface Loopback888
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    # interface GigabitEthernet0/2

    # Using Gathered

    # Before state:
    # -------------
    #
    # vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
    # interface Loopback888
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip access-group 110 in
    #  ip access-group 123 out
    #  ipv6 traffic-filter test_v6 out
    #  ipv6 traffic-filter temp_v6 in
    # interface GigabitEthernet0/2
    #  ip access-group 110 in
    #  ip access-group 123 out

    - name: Gather listed acl interfaces with provided configurations
      cisco.ios.ios_acl_interfaces:
        config:
        state: gathered

    # Module Execution Result:
    # ------------------------
    #
    # "gathered": [
    #         {
    #             "name": "Loopback888"
    #         },
    #         {
    #             "name": "GigabitEthernet0/0"
    #         },
    #         {
    #             "access_groups": [
    #                 {
    #                     "acls": [
    #                         {
    #                             "direction": "in",
    #                             "name": "110"
    #                         },
    #                         {
    #                             "direction": "out",
    #                             "name": "123"
    #                         }
    #                     ],
    #                     "afi": "ipv4"
    #                 },
    #                 {
    #                     "acls": [
    #                         {
    #                             "direction": "in",
    #                             "name": "temp_v6"
    #                         },
    #                         {
    #                             "direction": "out",
    #                             "name": "test_v6"
    #                         }
    #                     ],
    #                     "afi": "ipv6"
    #                 }
    #             ],
    #             "name": "GigabitEthernet0/1"
    #         },
    #         {
    #             "access_groups": [
    #                 {
    #                     "acls": [
    #                         {
    #                             "direction": "in",
    #                             "name": "100"
    #                         },
    #                         {
    #                             "direction": "out",
    #                             "name": "123"
    #                         }
    #                     ],
    #                     "afi": "ipv4"
    #                 }
    #             ],
    #             "name": "GigabitEthernet0/2"
    #         }
    #     ]

    # After state:
    # ------------
    #
    # vios#sh running-config | include interface|ip access-group|ipv6 traffic-filter
    # interface Loopback888
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip access-group 110 in
    #  ip access-group 123 out
    #  ipv6 traffic-filter test_v6 out
    #  ipv6 traffic-filter temp_v6 in
    # interface GigabitEthernet0/2
    #  ip access-group 110 in
    #  ip access-group 123 out

    # Using Rendered

    - name: Render the commands for provided  configuration
      cisco.ios.ios_acl_interfaces:
        config:
        - name: GigabitEthernet0/1
          access_groups:
          - afi: ipv4
            acls:
            - name: 110
              direction: in
            - name: 123
              direction: out
          - afi: ipv6
            acls:
            - name: test_v6
              direction: out
            - name: temp_v6
              direction: in
        state: rendered

    # Module Execution Result:
    # ------------------------
    #
    # "rendered": [
    #         "interface GigabitEthernet0/1",
    #         "ip access-group 110 in",
    #         "ip access-group 123 out",
    #         "ipv6 traffic-filter temp_v6 in",
    #         "ipv6 traffic-filter test_v6 out"
    #     ]

    # Using Parsed

    # File: parsed.cfg
    # ----------------
    #
    # interface GigabitEthernet0/1
    # ip access-group 110 in
    # ip access-group 123 out
    # ipv6 traffic-filter temp_v6 in
    # ipv6 traffic-filter test_v6 out

    - name: Parse the commands for provided configuration
      cisco.ios.ios_acl_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------
    #
    # "parsed": [
    #         {
    #             "access_groups": [
    #                 {
    #                     "acls": [
    #                         {
    #                             "direction": "in",
    #                             "name": "110"
    #                         }
    #                     ],
    #                     "afi": "ipv4"
    #                 },
    #                 {
    #                     "acls": [
    #                         {
    #                             "direction": "in",
    #                             "name": "temp_v6"
    #                         }
    #                     ],
    #                     "afi": "ipv6"
    #                 }
    #             ],
    #             "name": "GigabitEthernet0/1"
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet0/1&#x27;, &#x27;ip access-group 110 in&#x27;, &#x27;ipv6 traffic-filter test_v6 out&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sumit Jaiswal (@justjais)
