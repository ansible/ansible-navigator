.. _vyos.vyos.vyos_l3_interfaces_module:


****************************
vyos.vyos.vyos_l3_interfaces
****************************

**L3 interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the L3 interface attributes on VyOS network devices.




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
                        <div>The provided L3 interfaces configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv4</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of IPv4 addresses of the interface.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv4 address of the interface.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv6</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of IPv6 addresses of the interface.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv6 address of the interface.</div>
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
                        <div>Full name of the interface, e.g. eth0, eth1.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vifs</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual sub-interfaces L3 configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv4</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of IPv4 addresses of the virtual interface.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv4 address of the virtual interface.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv6</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of IPv6 addresses of the virtual interface.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv6 address of the virtual interface.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vlan_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifier for the virtual sub-interface.</div>
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
                        <div>The value of this option should be the output received from the VyOS device by executing the command <b>show configuration commands | grep -e eth[2,3]</b>.</div>
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
                                    <li><div style="color: blue"><b>merged</b>&nbsp;&larr;</div></li>
                                    <li>replaced</li>
                                    <li>overridden</li>
                                    <li>deleted</li>
                                    <li>parsed</li>
                                    <li>gathered</li>
                                    <li>rendered</li>
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
   - Tested against VyOS 1.1.8 (helium).
   - This module works with connection ``network_cli``. See `the VyOS OS Platform Options <../network/user_guide/platform_vyos.html>`_.



Examples
--------

.. code-block:: yaml

    # Using merged
    #
    # Before state:
    # -------------
    #
    # vyos:~$ show configuration commands | grep -e eth[2,3]
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces ethernet eth3 vif 101
    # set interfaces ethernet eth3 vif 102

    - name: Merge provided configuration with device configuration
      vyos.vyos.vyos_l3_interfaces:
        config:
        - name: eth2
          ipv4:
          - address: 192.0.2.10/28
          - address: 198.51.100.40/27
          ipv6:
          - address: 2001:db8:100::2/32
          - address: 2001:db8:400::10/32

        - name: eth3
          ipv4:
          - address: 203.0.113.65/26
          vifs:
          - vlan_id: 101
            ipv4:
            - address: 192.0.2.71/28
            - address: 198.51.100.131/25
          - vlan_id: 102
            ipv6:
            - address: 2001:db8:1000::5/38
            - address: 2001:db8:1400::3/38
        state: merged

    # After state:
    # -------------
    #
    # vyos:~$ show configuration commands | grep -e eth[2,3]
    # set interfaces ethernet eth2 address '192.0.2.10/28'
    # set interfaces ethernet eth2 address '198.51.100.40/27'
    # set interfaces ethernet eth2 address '2001:db8:100::2/32'
    # set interfaces ethernet eth2 address '2001:db8:400::10/32'
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth3 address '203.0.113.65/26'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces ethernet eth3 vif 101 address '192.0.2.71/28'
    # set interfaces ethernet eth3 vif 101 address '198.51.100.131/25'
    # set interfaces ethernet eth3 vif 102 address '2001:db8:1000::5/38'
    # set interfaces ethernet eth3 vif 102 address '2001:db8:1400::3/38'
    # set interfaces ethernet eth3 vif 102 address '2001:db8:4000::2/34'


    # Using replaced
    #
    # Before state:
    # -------------
    #
    # vyos:~$ show configuration commands | grep eth
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:30:f0:22'
    # set interfaces ethernet eth0 smp-affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 hw-id '08:00:27:EA:0F:B9'
    # set interfaces ethernet eth1 address '192.0.2.14/24'
    # set interfaces ethernet eth2 address '192.0.2.10/24'
    # set interfaces ethernet eth2 address '192.0.2.11/24'
    # set interfaces ethernet eth2 address '2001:db8::10/32'
    # set interfaces ethernet eth2 address '2001:db8::11/32'
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth3 address '198.51.100.10/24'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces ethernet eth3 vif 101 address '198.51.100.130/25'
    # set interfaces ethernet eth3 vif 101 address '198.51.100.131/25'
    # set interfaces ethernet eth3 vif 102 address '2001:db8:4000::3/34'
    # set interfaces ethernet eth3 vif 102 address '2001:db8:4000::2/34'
    #
    - name: Replace device configurations of listed interfaces with provided configurations
      vyos.vyos.vyos_l3_interfaces:
        config:
        - name: eth2
          ipv4:
          - address: 192.0.2.10/24

        - name: eth3
          ipv6:
          - address: 2001:db8::11/32
        state: replaced

    # After state:
    # -------------
    #
    # vyos:~$ show configuration commands | grep eth
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:30:f0:22'
    # set interfaces ethernet eth0 smp-affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 hw-id '08:00:27:EA:0F:B9'
    # set interfaces ethernet eth1 address '192.0.2.14/24'
    # set interfaces ethernet eth2 address '192.0.2.10/24'
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces ethernet eth3 address '2001:db8::11/32'
    # set interfaces ethernet eth3 vif 101
    # set interfaces ethernet eth3 vif 102


    # Using overridden
    #
    # Before state
    # --------------
    #
    # vyos@vyos-appliance:~$ show configuration commands | grep eth
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:30:f0:22'
    # set interfaces ethernet eth0 smp-affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 hw-id '08:00:27:EA:0F:B9'
    # set interfaces ethernet eth1 address '192.0.2.14/24'
    # set interfaces ethernet eth2 address '192.0.2.10/24'
    # set interfaces ethernet eth2 address '192.0.2.11/24'
    # set interfaces ethernet eth2 address '2001:db8::10/32'
    # set interfaces ethernet eth2 address '2001:db8::11/32'
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth3 address '198.51.100.10/24'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces ethernet eth3 vif 101 address '198.51.100.130/25'
    # set interfaces ethernet eth3 vif 101 address '198.51.100.131/25'
    # set interfaces ethernet eth3 vif 102 address '2001:db8:4000::3/34'
    # set interfaces ethernet eth3 vif 102 address '2001:db8:4000::2/34'

    - name: Overrides all device configuration with provided configuration
      vyos.vyos.vyos_l3_interfaces:
        config:
        - name: eth0
          ipv4:
          - address: dhcp
          ipv6:
          - address: dhcpv6
        state: overridden

    # After state
    # ------------
    #
    # vyos@vyos-appliance:~$ show configuration commands | grep eth
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 address 'dhcpv6'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:30:f0:22'
    # set interfaces ethernet eth0 smp-affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 hw-id '08:00:27:EA:0F:B9'
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces ethernet eth3 vif 101
    # set interfaces ethernet eth3 vif 102


    # Using deleted
    #
    # Before state
    # -------------
    # vyos@vyos-appliance:~$ show configuration commands | grep eth
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:30:f0:22'
    # set interfaces ethernet eth0 smp-affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 hw-id '08:00:27:EA:0F:B9'
    # set interfaces ethernet eth1 address '192.0.2.14/24'
    # set interfaces ethernet eth2 address '192.0.2.10/24'
    # set interfaces ethernet eth2 address '192.0.2.11/24'
    # set interfaces ethernet eth2 address '2001:db8::10/32'
    # set interfaces ethernet eth2 address '2001:db8::11/32'
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth3 address '198.51.100.10/24'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces ethernet eth3 vif 101 address '198.51.100.130/25'
    # set interfaces ethernet eth3 vif 101 address '198.51.100.131/25'
    # set interfaces ethernet eth3 vif 102 address '2001:db8:4000::3/34'
    # set interfaces ethernet eth3 vif 102 address '2001:db8:4000::2/34'

    - name: Delete L3 attributes of given interfaces (Note - This won't delete the interface
        itself)
      vyos.vyos.vyos_l3_interfaces:
        config:
        - name: eth1
        - name: eth2
        - name: eth3
        state: deleted

    # After state
    # ------------
    # vyos@vyos-appliance:~$ show configuration commands | grep eth
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:f3:6c:b5'
    # set interfaces ethernet eth0 smp_affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 hw-id '08:00:27:ad:ef:65'
    # set interfaces ethernet eth1 smp_affinity 'auto'
    # set interfaces ethernet eth2 hw-id '08:00:27:ab:4e:79'
    # set interfaces ethernet eth2 smp_affinity 'auto'
    # set interfaces ethernet eth3 hw-id '08:00:27:17:3c:85'
    # set interfaces ethernet eth3 smp_affinity 'auto'


    # Using gathered
    #
    # Before state:
    # -------------
    #
    # vyos:~$ show configuration commands | grep -e eth[2,3,0]
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:50:5e:19'
    # set interfaces ethernet eth0 smp_affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 address '192.0.2.14/24'
    # set interfaces ethernet eth2 address '192.0.2.11/24'
    # set interfaces ethernet eth2 address '192.0.2.10/24'
    # set interfaces ethernet eth2 address '2001:db8::10/32'
    # set interfaces ethernet eth2 address '2001:db8::12/32'
    #
    - name: Gather listed l3 interfaces with provided configurations
      vyos.vyos.vyos_l3_interfaces:
        config:
        state: gathered
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #    "gathered": [
    #         {
    #             "ipv4": [
    #                 {
    #                     "address": "192.0.2.11/24"
    #                 },
    #                 {
    #                     "address": "192.0.2.10/24"
    #                 }
    #             ],
    #             "ipv6": [
    #                 {
    #                     "address": "2001:db8::10/32"
    #                 },
    #                 {
    #                     "address": "2001:db8::12/32"
    #                 }
    #             ],
    #             "name": "eth2"
    #         },
    #         {
    #             "ipv4": [
    #                 {
    #                     "address": "192.0.2.14/24"
    #                 }
    #             ],
    #             "name": "eth1"
    #         },
    #         {
    #             "ipv4": [
    #                 {
    #                     "address": "dhcp"
    #                 }
    #             ],
    #             "name": "eth0"
    #         }
    #     ]
    #
    #
    # After state:
    # -------------
    #
    # vyos:~$ show configuration commands | grep -e eth[2,3]
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:50:5e:19'
    # set interfaces ethernet eth0 smp_affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 address '192.0.2.14/24'
    # set interfaces ethernet eth2 address '192.0.2.11/24'
    # set interfaces ethernet eth2 address '192.0.2.10/24'
    # set interfaces ethernet eth2 address '2001:db8::10/32'
    # set interfaces ethernet eth2 address '2001:db8::12/32'


    # Using rendered
    #
    #
    - name: Render the commands for provided  configuration
      vyos.vyos.vyos_l3_interfaces:
        config:
        - name: eth1
          ipv4:
          - address: 192.0.2.14/24
        - name: eth2
          ipv4:
          - address: 192.0.2.10/24
          - address: 192.0.2.11/24
          ipv6:
          - address: 2001:db8::10/32
          - address: 2001:db8::12/32
        state: rendered
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #
    # "rendered": [
    #         "set interfaces ethernet eth1 address '192.0.2.14/24'",
    #         "set interfaces ethernet eth2 address '192.0.2.11/24'",
    #         "set interfaces ethernet eth2 address '192.0.2.10/24'",
    #         "set interfaces ethernet eth2 address '2001:db8::10/32'",
    #         "set interfaces ethernet eth2 address '2001:db8::12/32'"
    #     ]


    # Using parsed
    #
    #
    - name: parse the provided running configuration
      vyos.vyos.vyos_l3_interfaces:
        running_config:
          "set interfaces ethernet eth0 address 'dhcp'
           set interfaces ethernet eth1 address '192.0.2.14/24'
           set interfaces ethernet eth2 address '192.0.2.10/24'
           set interfaces ethernet eth2 address '192.0.2.11/24'
           set interfaces ethernet eth2 address '2001:db8::10/32'
           set interfaces ethernet eth2 address '2001:db8::12/32'"
        state: parsed
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #
    # "parsed": [
    #         {
    #             "ipv4": [
    #                 {
    #                     "address": "192.0.2.10/24"
    #                 },
    #                 {
    #                     "address": "192.0.2.11/24"
    #                 }
    #             ],
    #             "ipv6": [
    #                 {
    #                     "address": "2001:db8::10/32"
    #                 },
    #                 {
    #                     "address": "2001:db8::12/32"
    #                 }
    #             ],
    #             "name": "eth2"
    #         },
    #         {
    #             "ipv4": [
    #                 {
    #                     "address": "192.0.2.14/24"
    #                 }
    #             ],
    #             "name": "eth1"
    #         },
    #         {
    #             "ipv4": [
    #                 {
    #                     "address": "dhcp"
    #                 }
    #             ],
    #             "name": "eth0"
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;set interfaces ethernet eth1 192.0.2.14/2&#x27;, &#x27;set interfaces ethernet eth3 vif 101 address 198.51.100.130/25&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Nilashish Chakraborty (@NilashishC)
- Rohit Thakur (@rohitthakur2590)
