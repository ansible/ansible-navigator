.. _arista.eos.eos_acl_interfaces_module:


*****************************
arista.eos.eos_acl_interfaces
*****************************

**ACL interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages adding and removing Access Control Lists (ACLs) from interfaces on devices running EOS software.




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
                        <div>A dictionary of ACL options for interfaces.</div>
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
                        <div>Specifies ACLs attached to the interfaces.</div>
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
                        <div>Specifies the AFI for the ACL(s) to be configured on this interface.</div>
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
                        <div>Name/Identifier for the interface.</div>
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
                        <div>The module, by default, will connect to the remote device and retrieve the current running-config to use as a base for comparing against the contents of source. There are times when it is not desirable to have the task get the current running-config for every task in a playbook.  The <em>running_config</em> argument allows the implementer to pass in the configuration to use as the base config for comparison. This value of this option should be the output received from device by executing command</div>
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
                        <div>The state the configuration should be left in.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    # Using Merged

    # Before state:
    # -------------
    #
    # eos#sh running-config | include interface|access-group
    # interface Ethernet1
    # interface Ethernet2
    # interface Ethernet3

    - name: Merge module attributes of given access-groups
      arista.eos.eos_acl_interfaces:
        config:
        - name: Ethernet2
          access_groups:
          - afi: ipv4
            acls:
              name: acl01
              direction: in
          - afi: ipv6
            acls:
              name: acl03
              direction: out
        state: merged

    # Commands Fired:
    # ---------------
    #
    # interface Ethernet2
    # ip access-group acl01 in
    # ipv6 access-group acl03 out

    # After state:
    # -------------
    #
    # eos#sh running-config | include interface| access-group
    # interface Loopback888
    # interface Ethernet1
    # interface Ethernet2
    #  ip access-group acl01 in
    #  ipv6 access-group acl03 out
    # interface Ethernet3


    # Using Replaced

    # Before state:
    # -------------
    #
    # eos#sh running-config | include interface|access-group
    # interface Ethernet1
    # interface Ethernet2
    #  ip access-group acl01 in
    #  ipv6 access-group acl03 out
    # interface Ethernet3
    #  ip access-group acl01 in

    - name: Replace module attributes of given access-groups
      arista.eos.eos_acl_interfaces:
        config:
        - name: Ethernet2
          access_groups:
          - afi: ipv4
            acls:
              name: acl01
              direction: out
        state: replaced

    # Commands Fired:
    # ---------------
    #
    # interface Ethernet2
    # no ip access-group acl01 in
    # no ipv6 access-group acl03 out
    # ip access-group acl01 out

    # After state:
    # -------------
    #
    # eos#sh running-config | include interface| access-group
    # interface Loopback888
    # interface Ethernet1
    # interface Ethernet2
    #  ip access-group acl01 out
    # interface Ethernet3
    #  ip access-group acl01 in


    # Using Overridden

    # Before state:
    # -------------
    #
    # eos#sh running-config | include interface|access-group
    # interface Ethernet1
    # interface Ethernet2
    #  ip access-group acl01 in
    #  ipv6 access-group acl03 out
    # interface Ethernet3
    #  ip access-group acl01 in

    - name: Override module attributes of given access-groups
      arista.eos.eos_acl_interfaces:
        config:
        - name: Ethernet2
          access_groups:
          - afi: ipv4
            acls:
              name: acl01
              direction: out
        state: overridden

    # Commands Fired:
    # ---------------
    #
    # interface Ethernet2
    # no ip access-group acl01 in
    # no ipv6 access-group acl03 out
    # ip access-group acl01 out
    # interface Ethernet3
    # no ip access-group acl01 in

    # After state:
    # -------------
    #
    # eos#sh running-config | include interface| access-group
    # interface Loopback888
    # interface Ethernet1
    # interface Ethernet2
    #  ip access-group acl01 out
    # interface Ethernet3


    # Using Deleted

    # Before state:
    # -------------
    #
    # eos#sh running-config | include interface|access-group
    # interface Ethernet1
    # interface Ethernet2
    #  ip access-group acl01 in
    #  ipv6 access-group acl03 out
    # interface Ethernet3
    #  ip access-group acl01 out

    - name: Delete module attributes of given access-groups
      arista.eos.eos_acl_interfaces:
        config:
        - name: Ethernet2
          access_groups:
          - afi: ipv4
            acls:
              name: acl01
              direction: in
          - afi: ipv6
            acls:
              name: acl03
              direction: out
        state: deleted

    # Commands Fired:
    # ---------------
    #
    # interface Ethernet2
    # no ip access-group acl01 in
    # no ipv6 access-group acl03 out

    # After state:
    # -------------
    #
    # eos#sh running-config | include interface| access-group
    # interface Loopback888
    # interface Ethernet1
    # interface Ethernet2
    # interface Ethernet3
    #  ip access-group acl01 out


    # Before state:
    # -------------
    #
    # eos#sh running-config | include interface| access-group
    # interface Ethernet1
    # interface Ethernet2
    #  ip access-group acl01 in
    #  ipv6 access-group acl03 out
    # interface Ethernet3
    #  ip access-group acl01 out

    - name: Delete module attributes of given access-groups from ALL Interfaces
      arista.eos.eos_acl_interfaces:
        config:
        state: deleted

    # Commands Fired:
    # ---------------
    #
    # interface Ethernet2
    # no ip access-group acl01 in
    # no ipv6 access-group acl03 out
    # interface Ethernet3
    # no ip access-group acl01 out

    # After state:
    # -------------
    #
    # eos#sh running-config | include interface| access-group
    # interface Loopback888
    # interface Ethernet1
    # interface Ethernet2
    # interface Ethernet3

    # Before state:
    # -------------
    #
    # eos#sh running-config | include interface| access-group
    # interface Ethernet1
    # interface Ethernet2
    #  ip access-group acl01 in
    #  ipv6 access-group acl03 out
    # interface Ethernet3
    #  ip access-group acl01 out

    - name: Delete acls under afi
      arista.eos.eos_acl_interfaces:
        config:
        - name: Ethernet3
          access_groups:
          - afi: ipv4
        - name: Ethernet2
          access_groups:
          - afi: ipv6
        state: deleted

    # Commands Fired:
    # ---------------
    #
    # interface Ethernet2
    # no ipv6 access-group acl03 out
    # interface Ethernet3
    # no ip access-group acl01 out

    # After state:
    # -------------
    #
    # eos#sh running-config | include interface| access-group
    # interface Loopback888
    # interface Ethernet1
    # interface Ethernet2
    #   ip access-group acl01 in
    # interface Ethernet3



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet2&#x27;, &#x27;ip access-group acl01 in&#x27;, &#x27;ipv6 access-group acl03 out&#x27;, &#x27;interface Ethernet3&#x27;, &#x27;ip access-group acl01 out&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- GomathiSelvi S (@GomathiselviS)
