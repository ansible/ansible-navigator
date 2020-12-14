.. _cisco.nxos.nxos_acl_interfaces_module:


******************************
cisco.nxos.nxos_acl_interfaces
******************************

**ACL interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Add and remove Access Control Lists on interfaces in NX-OS platform




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
                        <div>A list of interfaces to be configured with ACLs</div>
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
                        <div>List of address family indicators with ACLs to be configured on the interface</div>
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
                        <div>List of Access Control Lists for the interface</div>
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
                        <div>Direction to be applied for the ACL</div>
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
                        <div>Name of the ACL to be added/removed</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>port</b>
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
                        <div>Use ACL as port policy.</div>
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
                        <div>Address Family Indicator of the ACLs to be configured</div>
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
                        <div>Name of the interface</div>
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
                        <div>This option is used only with state <em>parsed</em>.</div>
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section &#x27;^interface&#x27;</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
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
                                    <li>deleted</li>
                                    <li>gathered</li>
                                    <li><div style="color: blue"><b>merged</b>&nbsp;&larr;</div></li>
                                    <li>overridden</li>
                                    <li>rendered</li>
                                    <li>replaced</li>
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
   - Tested against NX-OS 7.3.(0)D1(1) on VIRL



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # ------------
    #

    - name: Merge ACL interfaces configuration
      cisco.nxos.nxos_acl_interfaces:
        config:
        - name: Ethernet1/2
          access_groups:
          - afi: ipv6
            acls:
            - name: ACL1v6
              direction: in

        - name: Eth1/5
          access_groups:
          - afi: ipv4
            acls:
            - name: PortACL
              direction: in
              port: true

            - name: ACL1v4
              direction: out

          - afi: ipv6
            acls:
            - name: ACL1v6
              direction: in
        state: merged

    # After state:
    # ------------
    # interface Ethernet1/2
    #   ipv6 traffic-filter ACL1v6 in
    # interface Ethernet1/5
    #   ip port access-group PortACL in
    #   ip access-group ACL1v4 out
    #   ipv6 traffic-filter ACL1v6 in

    # Using replaced

    # Before state:
    # ------------
    # interface Ethernet1/2
    #   ipv6 traffic-filter ACL1v6 in
    # interface Ethernet1/5
    #   ip port access-group PortACL in
    #   ip access-group ACL1v4 out
    #   ipv6 traffic-filter ACL1v6 in

    - name: Replace interface configuration with given configuration
      cisco.nxos.nxos_acl_interfaces:
        config:
        - name: Eth1/5
          access_groups:
          - afi: ipv4
            acls:
            - name: NewACLv4
              direction: out

        - name: Ethernet1/3
          access_groups:
          - afi: ipv6
            acls:
            - name: NewACLv6
              direction: in
              port: true
        state: replaced

    # After state:
    # ------------
    # interface Ethernet1/2
    #   ipv6 traffic-filter ACL1v6 in
    # interface Ethernet1/3
    #   ipv6 port traffic-filter NewACLv6 in
    # interface Ethernet1/5
    #   ip access-group NewACLv4 out

    # Using overridden

    # Before state:
    # ------------
    # interface Ethernet1/2
    #   ipv6 traffic-filter ACL1v6 in
    # interface Ethernet1/5
    #   ip port access-group PortACL in
    #   ip access-group ACL1v4 out
    #   ipv6 traffic-filter ACL1v6 in

    - name: Override interface configuration with given configuration
      cisco.nxos.nxos_acl_interfaces:
        config:
        - name: Ethernet1/3
          access_groups:
          - afi: ipv4
            acls:
            - name: ACL1v4
              direction: out

            - name: PortACL
              port: true
              direction: in
          - afi: ipv6
            acls:
            - name: NewACLv6
              direction: in
              port: true
        state: overridden

    # After state:
    # ------------
    # interface Ethernet1/3
    #   ip access-group ACL1v4 out
    #   ip port access-group PortACL in
    #   ipv6 port traffic-filter NewACLv6 in

    # Using deleted to remove ACL config from specified interfaces

    # Before state:
    # -------------
    # interface Ethernet1/1
    #   ip access-group ACL2v4 in
    # interface Ethernet1/2
    #   ipv6 traffic-filter ACL1v6 in
    # interface Ethernet1/5
    #   ip port access-group PortACL in
    #   ip access-group ACL1v4 out
    #   ipv6 traffic-filter ACL1v6 in

    - name: Delete ACL configuration on interfaces
      cisco.nxos.nxos_acl_interfaces:
        config:
        - name: Ethernet1/5
        - name: Ethernet1/2
        state: deleted

    # After state:
    # -------------
    # interface Ethernet1/1
    #   ip access-group ACL2v4 in
    # interface Ethernet1/2
    # interface Ethernet1/5

    # Using deleted to remove ACL config from all interfaces

    # Before state:
    # -------------
    # interface Ethernet1/1
    #   ip access-group ACL2v4 in
    # interface Ethernet1/2
    #   ipv6 traffic-filter ACL1v6 in
    # interface Ethernet1/5
    #   ip port access-group PortACL in
    #   ip access-group ACL1v4 out
    #   ipv6 traffic-filter ACL1v6 in

    - name: Delete ACL configuration from all interfaces
      cisco.nxos.nxos_acl_interfaces:
        state: deleted

    # After state:
    # -------------
    # interface Ethernet1/1
    # interface Ethernet1/2
    # interface Ethernet1/5

    # Using parsed

    - name: Parse given configuration into structured format
      cisco.nxos.nxos_acl_interfaces:
        running_config: |
          interface Ethernet1/2
          ipv6 traffic-filter ACL1v6 in
          interface Ethernet1/5
          ipv6 traffic-filter ACL1v6 in
          ip access-group ACL1v4 out
          ip port access-group PortACL in
        state: parsed

    # returns
    # parsed:
    #   - name: Ethernet1/2
    #     access_groups:
    #       - afi: ipv6
    #         acls:
    #           - name: ACL1v6
    #             direction: in
    #  - name: Ethernet1/5
    #    access_groups:
    #      - afi: ipv4
    #        acls:
    #          - name: PortACL
    #            direction: in
    #            port: True
    #          - name: ACL1v4
    #            direction: out
    #      - afi: ipv6
    #        acls:
    #          - name: ACL1v6
    #             direction: in


    # Using gathered:

    # Before state:
    # ------------
    # interface Ethernet1/2
    #   ipv6 traffic-filter ACL1v6 in
    # interface Ethernet1/5
    #   ipv6 traffic-filter ACL1v6 in
    #   ip access-group ACL1v4 out
    #   ip port access-group PortACL in

    - name: Gather existing configuration from device
      cisco.nxos.nxos_acl_interfaces:
        config:
        state: gathered

    # returns
    # gathered:
    #   - name: Ethernet1/2
    #     access_groups:
    #       - afi: ipv6
    #         acls:
    #           - name: ACL1v6
    #             direction: in
    #  - name: Ethernet1/5
    #    access_groups:
    #      - afi: ipv4
    #        acls:
    #          - name: PortACL
    #            direction: in
    #            port: True
    #          - name: ACL1v4
    #            direction: out
    #      - afi: ipv6
    #        acls:
    #          - name: ACL1v6
    #             direction: in


    # Using rendered

    - name: Render required configuration to be pushed to the device
      cisco.nxos.nxos_acl_interfaces:
        config:
        - name: Ethernet1/2
          access_groups:
          - afi: ipv6
            acls:
            - name: ACL1v6
              direction: in

        - name: Ethernet1/5
          access_groups:
          - afi: ipv4
            acls:
            - name: PortACL
              direction: in
              port: true
            - name: ACL1v4
              direction: out
          - afi: ipv6
            acls:
            - name: ACL1v6
              direction: in
        state: rendered

    # returns
    # rendered:
    #   interface Ethernet1/2
    #   ipv6 traffic-filter ACL1v6 in
    #   interface Ethernet1/5
    #   ipv6 traffic-filter ACL1v6 in
    #   ip access-group ACL1v4 out
    #   ip port access-group PortACL in



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
                      <span style="color: purple">dictionary</span>
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
                      <span style="color: purple">dictionary</span>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/2&#x27;, &#x27;ipv6 traffic-filter ACL1v6 out&#x27;, &#x27;ip port access-group PortACL in&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Adharsh Srivats Rangarajan (@adharshsrivatsr)
