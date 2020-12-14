.. _vyos.vyos.vyos_interfaces_module:


*************************
vyos.vyos.vyos_interfaces
*************************

**Interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the interface attributes on VyOS network devices.
- This module supports managing base attributes of Ethernet, Bonding, VXLAN, Loopback and Virtual Tunnel Interfaces.




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
                        <div>The provided interfaces configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                <td colspan="2">
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
                        <div>Interface duplex mode.</div>
                        <div>Applicable for Ethernet interfaces only.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                <td colspan="2">
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
                        <div>MTU for a specific interface. Refer to vendor documentation for valid values.</div>
                        <div>Applicable for Ethernet, Bonding, VXLAN and Virtual Tunnel interfaces.</div>
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
                        <div>Full name of the interface, e.g. eth0, eth1, bond0, vti1, vxlan2.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>speed</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>auto</li>
                                    <li>10</li>
                                    <li>100</li>
                                    <li>1000</li>
                                    <li>2500</li>
                                    <li>10000</li>
                        </ul>
                </td>
                <td>
                        <div>Interface link speed.</div>
                        <div>Applicable for Ethernet interfaces only.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>Virtual sub-interfaces related configuration.</div>
                        <div>802.1Q VLAN interfaces are represented as virtual sub-interfaces in VyOS.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>Virtual sub-interface description.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>Administrative state of the virtual sub-interface.</div>
                        <div>Set the value to <code>true</code> to administratively enable the interface or <code>false</code> to disable it.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>MTU for the virtual sub-interface.</div>
                        <div>Refer to vendor documentation for valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>The value of this option should be the output received from the VyOS device by executing the command <b>show configuration commands | grep interfaces</b>.</div>
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
   - Tested against VyOS 1.1.8 (helium).
   - This module works with connection ``network_cli``. See `the VyOS OS Platform Options <../network/user_guide/platform_vyos.html>`_.



Examples
--------

.. code-block:: yaml

    # Using merged
    #
    # -------------
    # Before state:
    # -------------
    #
    # vyos@vyos:~$ show configuration commands | grep interfaces
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 address 'dhcpv6'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:30:f0:22'
    # set interfaces ethernet eth0 smp-affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 hw-id '08:00:27:ea:0f:b9'
    # set interfaces ethernet eth1 smp-affinity 'auto'
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth2 smp-affinity 'auto'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces loopback lo

    - name: Merge provided configuration with device configuration
      vyos.vyos.vyos_interfaces:
        config:
        - name: eth2
          description: Configured by Ansible
          enabled: true
          vifs:
          - vlan_id: 200
            description: VIF 200 - ETH2

        - name: eth3
          description: Configured by Ansible
          mtu: 1500

        - name: bond1
          description: Bond - 1
          mtu: 1200

        - name: vti2
          description: VTI - 2
          enabled: false
        state: merged
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    # "before": [
    #      	{
    #            "enabled": true,
    #            "name": "lo"
    #      	},
    #       {
    #            "enabled": true,
    #            "name": "eth3"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "eth2"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "eth1"
    #        },
    #        {
    #            "duplex": "auto",
    #            "enabled": true,
    #            "name": "eth0",
    #            "speed": "auto"
    #        }
    #    ]
    #
    # "commands": [
    #        "set interfaces ethernet eth2 description 'Configured by Ansible'",
    #        "set interfaces ethernet eth2 vif 200",
    #        "set interfaces ethernet eth2 vif 200 description 'VIF 200 - ETH2'",
    #        "set interfaces ethernet eth3 description 'Configured by Ansible'",
    #        "set interfaces ethernet eth3 mtu '1500'",
    #        "set interfaces bonding bond1",
    #        "set interfaces bonding bond1 description 'Bond - 1'",
    #        "set interfaces bonding bond1 mtu '1200'",
    #        "set interfaces vti vti2",
    #        "set interfaces vti vti2 description 'VTI - 2'",
    #        "set interfaces vti vti2 disable"
    #    ]
    #
    # "after": [
    #        {
    #            "description": "Bond - 1",
    #            "enabled": true,
    #            "mtu": 1200,
    #            "name": "bond1"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "lo"
    #        },
    #        {
    #            "description": "VTI - 2",
    #            "enabled": false,
    #            "name": "vti2"
    #        },
    #        {
    #            "description": "Configured by Ansible",
    #            "enabled": true,
    #            "mtu": 1500,
    #            "name": "eth3"
    #        },
    #        {
    #            "description": "Configured by Ansible",
    #            "enabled": true,
    #            "name": "eth2",
    #            "vifs": [
    #                {
    #                    "description": "VIF 200 - ETH2",
    #                    "enabled": true,
    #                    "vlan_id": "200"
    #                }
    #            ]
    #        },
    #        {
    #            "enabled": true,
    #            "name": "eth1"
    #        },
    #        {
    #            "duplex": "auto",
    #            "enabled": true,
    #            "name": "eth0",
    #            "speed": "auto"
    #        }
    #    ]
    #
    #
    # -------------
    # After state:
    # -------------
    #
    # vyos@vyos:~$ show configuration commands | grep interfaces
    # set interfaces bonding bond1 description 'Bond - 1'
    # set interfaces bonding bond1 mtu '1200'
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 address 'dhcpv6'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:30:f0:22'
    # set interfaces ethernet eth0 smp-affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 hw-id '08:00:27:ea:0f:b9'
    # set interfaces ethernet eth1 smp-affinity 'auto'
    # set interfaces ethernet eth2 description 'Configured by Ansible'
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth2 smp-affinity 'auto'
    # set interfaces ethernet eth2 vif 200 description 'VIF 200 - ETH2'
    # set interfaces ethernet eth3 description 'Configured by Ansible'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces ethernet eth3 mtu '1500'
    # set interfaces loopback lo
    # set interfaces vti vti2 description 'VTI - 2'
    # set interfaces vti vti2 disable
    #


    # Using replaced
    #
    # -------------
    # Before state:
    # -------------
    #
    # vyos:~$ show configuration commands | grep eth
    # set interfaces bonding bond1 description 'Bond - 1'
    # set interfaces bonding bond1 mtu '1400'
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 description 'Management Interface for the Appliance'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:f3:6c:b5'
    # set interfaces ethernet eth0 smp_affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 description 'Configured by Ansible Eng Team'
    # set interfaces ethernet eth1 duplex 'full'
    # set interfaces ethernet eth1 hw-id '08:00:27:ad:ef:65'
    # set interfaces ethernet eth1 smp_affinity 'auto'
    # set interfaces ethernet eth1 speed '100'
    # set interfaces ethernet eth2 description 'Configured by Ansible'
    # set interfaces ethernet eth2 duplex 'full'
    # set interfaces ethernet eth2 hw-id '08:00:27:ab:4e:79'
    # set interfaces ethernet eth2 mtu '500'
    # set interfaces ethernet eth2 smp_affinity 'auto'
    # set interfaces ethernet eth2 speed '100'
    # set interfaces ethernet eth2 vif 200 description 'Configured by Ansible'
    # set interfaces ethernet eth3 description 'Configured by Ansible'
    # set interfaces ethernet eth3 duplex 'full'
    # set interfaces ethernet eth3 hw-id '08:00:27:17:3c:85'
    # set interfaces ethernet eth3 mtu '1500'
    # set interfaces ethernet eth3 smp_affinity 'auto'
    # set interfaces ethernet eth3 speed '100'
    # set interfaces loopback lo
    #
    #
    - name: Replace device configurations of listed interfaces with provided configurations
      vyos.vyos.vyos_interfaces:
        config:
        - name: eth2
          description: Replaced by Ansible

        - name: eth3
          description: Replaced by Ansible

        - name: eth1
          description: Replaced by Ansible
        state: replaced
    #
    #
    # -----------------------
    # Module Execution Result
    # -----------------------
    #
    # "before": [
    #        {
    #            "description": "Bond - 1",
    #            "enabled": true,
    #            "mtu": 1400,
    #            "name": "bond1"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "lo"
    #        },
    #        {
    #            "description": "Configured by Ansible",
    #            "duplex": "full",
    #            "enabled": true,
    #            "mtu": 1500,
    #            "name": "eth3",
    #            "speed": "100"
    #        },
    #        {
    #            "description": "Configured by Ansible",
    #            "duplex": "full",
    #            "enabled": true,
    #            "mtu": 500,
    #            "name": "eth2",
    #            "speed": "100",
    #            "vifs": [
    #                {
    #                    "description": "VIF 200 - ETH2",
    #                    "enabled": true,
    #                    "vlan_id": "200"
    #                }
    #            ]
    #        },
    #        {
    #            "description": "Configured by Ansible Eng Team",
    #            "duplex": "full",
    #            "enabled": true,
    #            "name": "eth1",
    #            "speed": "100"
    #        },
    #        {
    #            "description": "Management Interface for the Appliance",
    #            "duplex": "auto",
    #            "enabled": true,
    #            "name": "eth0",
    #            "speed": "auto"
    #        }
    #    ]
    #
    # "commands": [
    #        "delete interfaces ethernet eth2 speed",
    #        "delete interfaces ethernet eth2 duplex",
    #        "delete interfaces ethernet eth2 mtu",
    #        "delete interfaces ethernet eth2 vif 200 description",
    #        "set interfaces ethernet eth2 description 'Replaced by Ansible'",
    #        "delete interfaces ethernet eth3 speed",
    #        "delete interfaces ethernet eth3 duplex",
    #        "delete interfaces ethernet eth3 mtu",
    #        "set interfaces ethernet eth3 description 'Replaced by Ansible'",
    #        "delete interfaces ethernet eth1 speed",
    #        "delete interfaces ethernet eth1 duplex",
    #        "set interfaces ethernet eth1 description 'Replaced by Ansible'"
    #    ]
    #
    # "after": [
    #        {
    #            "description": "Bond - 1",
    #            "enabled": true,
    #            "mtu": 1400,
    #            "name": "bond1"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "lo"
    #        },
    #        {
    #            "description": "Replaced by Ansible",
    #            "enabled": true,
    #            "name": "eth3"
    #        },
    #        {
    #            "description": "Replaced by Ansible",
    #            "enabled": true,
    #            "name": "eth2",
    #            "vifs": [
    #                {
    #                    "enabled": true,
    #                    "vlan_id": "200"
    #                }
    #            ]
    #        },
    #        {
    #            "description": "Replaced by Ansible",
    #            "enabled": true,
    #            "name": "eth1"
    #        },
    #        {
    #            "description": "Management Interface for the Appliance",
    #            "duplex": "auto",
    #            "enabled": true,
    #            "name": "eth0",
    #            "speed": "auto"
    #        }
    #    ]
    #
    #
    # -------------
    # After state:
    # -------------
    #
    # vyos@vyos:~$ show configuration commands | grep interfaces
    # set interfaces bonding bond1 description 'Bond - 1'
    # set interfaces bonding bond1 mtu '1400'
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 address 'dhcpv6'
    # set interfaces ethernet eth0 description 'Management Interface for the Appliance'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:30:f0:22'
    # set interfaces ethernet eth0 smp-affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 description 'Replaced by Ansible'
    # set interfaces ethernet eth1 hw-id '08:00:27:ea:0f:b9'
    # set interfaces ethernet eth1 smp-affinity 'auto'
    # set interfaces ethernet eth2 description 'Replaced by Ansible'
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth2 smp-affinity 'auto'
    # set interfaces ethernet eth2 vif 200
    # set interfaces ethernet eth3 description 'Replaced by Ansible'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces loopback lo
    #
    #
    # Using overridden
    #
    #
    # --------------
    # Before state
    # --------------
    #
    # vyos@vyos:~$ show configuration commands | grep interfaces
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 address 'dhcpv6'
    # set interfaces ethernet eth0 description 'Ethernet Interface - 0'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:30:f0:22'
    # set interfaces ethernet eth0 mtu '1200'
    # set interfaces ethernet eth0 smp-affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 description 'Configured by Ansible Eng Team'
    # set interfaces ethernet eth1 hw-id '08:00:27:ea:0f:b9'
    # set interfaces ethernet eth1 mtu '100'
    # set interfaces ethernet eth1 smp-affinity 'auto'
    # set interfaces ethernet eth1 vif 100 description 'VIF 100 - ETH1'
    # set interfaces ethernet eth1 vif 100 disable
    # set interfaces ethernet eth2 description 'Configured by Ansible Team (Admin Down)'
    # set interfaces ethernet eth2 disable
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth2 mtu '600'
    # set interfaces ethernet eth2 smp-affinity 'auto'
    # set interfaces ethernet eth3 description 'Configured by Ansible Network'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces loopback lo
    # set interfaces vti vti1 description 'Virtual Tunnel Interface - 1'
    # set interfaces vti vti1 mtu '68'
    #
    #
    - name: Overrides all device configuration with provided configuration
      vyos.vyos.vyos_interfaces:
        config:
        - name: eth0
          description: Outbound Interface For The Appliance
          speed: auto
          duplex: auto

        - name: eth2
          speed: auto
          duplex: auto

        - name: eth3
          mtu: 1200
        state: overridden
    #
    #
    # ------------------------
    # Module Execution Result
    # ------------------------
    #
    # "before": [
    #        {
    #            "enabled": true,
    #            "name": "lo"
    #        },
    #        {
    #            "description": "Virtual Tunnel Interface - 1",
    #            "enabled": true,
    #            "mtu": 68,
    #            "name": "vti1"
    #        },
    #        {
    #            "description": "Configured by Ansible Network",
    #            "enabled": true,
    #            "name": "eth3"
    #        },
    #        {
    #            "description": "Configured by Ansible Team (Admin Down)",
    #            "enabled": false,
    #            "mtu": 600,
    #            "name": "eth2"
    #        },
    #        {
    #            "description": "Configured by Ansible Eng Team",
    #            "enabled": true,
    #            "mtu": 100,
    #            "name": "eth1",
    #            "vifs": [
    #                {
    #                    "description": "VIF 100 - ETH1",
    #                    "enabled": false,
    #                    "vlan_id": "100"
    #                }
    #            ]
    #        },
    #        {
    #            "description": "Ethernet Interface - 0",
    #            "duplex": "auto",
    #            "enabled": true,
    #            "mtu": 1200,
    #            "name": "eth0",
    #            "speed": "auto"
    #        }
    #    ]
    #
    # "commands": [
    #        "delete interfaces vti vti1 description",
    #        "delete interfaces vti vti1 mtu",
    #        "delete interfaces ethernet eth1 description",
    #        "delete interfaces ethernet eth1 mtu",
    #        "delete interfaces ethernet eth1 vif 100 description",
    #        "delete interfaces ethernet eth1 vif 100 disable",
    #        "delete interfaces ethernet eth0 mtu",
    #        "set interfaces ethernet eth0 description 'Outbound Interface For The Appliance'",
    #        "delete interfaces ethernet eth2 description",
    #        "delete interfaces ethernet eth2 mtu",
    #        "set interfaces ethernet eth2 duplex 'auto'",
    #        "delete interfaces ethernet eth2 disable",
    #        "set interfaces ethernet eth2 speed 'auto'",
    #        "delete interfaces ethernet eth3 description",
    #        "set interfaces ethernet eth3 mtu '1200'"
    #    ],
    #
    # "after": [
    #        {
    #            "enabled": true,
    #            "name": "lo"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "vti1"
    #        },
    #        {
    #            "enabled": true,
    #            "mtu": 1200,
    #            "name": "eth3"
    #        },
    #        {
    #            "duplex": "auto",
    #            "enabled": true,
    #            "name": "eth2",
    #            "speed": "auto"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "eth1",
    #            "vifs": [
    #                {
    #                    "enabled": true,
    #                    "vlan_id": "100"
    #                }
    #            ]
    #        },
    #        {
    #            "description": "Outbound Interface For The Appliance",
    #            "duplex": "auto",
    #            "enabled": true,
    #            "name": "eth0",
    #            "speed": "auto"
    #        }
    #    ]
    #
    #
    # ------------
    # After state
    # ------------
    #
    # vyos@vyos:~$ show configuration commands | grep interfaces
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 address 'dhcpv6'
    # set interfaces ethernet eth0 description 'Outbound Interface For The Appliance'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:30:f0:22'
    # set interfaces ethernet eth0 smp-affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 hw-id '08:00:27:ea:0f:b9'
    # set interfaces ethernet eth1 smp-affinity 'auto'
    # set interfaces ethernet eth1 vif 100
    # set interfaces ethernet eth2 duplex 'auto'
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth2 smp-affinity 'auto'
    # set interfaces ethernet eth2 speed 'auto'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces ethernet eth3 mtu '1200'
    # set interfaces loopback lo
    # set interfaces vti vti1
    #
    #
    # Using deleted
    #
    #
    # -------------
    # Before state
    # -------------
    #
    # vyos@vyos:~$ show configuration commands | grep interfaces
    # set interfaces bonding bond0 mtu '1300'
    # set interfaces bonding bond1 description 'LAG - 1'
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 address 'dhcpv6'
    # set interfaces ethernet eth0 description 'Outbound Interface for this appliance'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:30:f0:22'
    # set interfaces ethernet eth0 smp-affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 description 'Configured by Ansible Network'
    # set interfaces ethernet eth1 duplex 'full'
    # set interfaces ethernet eth1 hw-id '08:00:27:ea:0f:b9'
    # set interfaces ethernet eth1 smp-affinity 'auto'
    # set interfaces ethernet eth1 speed '100'
    # set interfaces ethernet eth2 description 'Configured by Ansible'
    # set interfaces ethernet eth2 disable
    # set interfaces ethernet eth2 duplex 'full'
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth2 mtu '600'
    # set interfaces ethernet eth2 smp-affinity 'auto'
    # set interfaces ethernet eth2 speed '100'
    # set interfaces ethernet eth3 description 'Configured by Ansible Network'
    # set interfaces ethernet eth3 duplex 'full'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces ethernet eth3 speed '100'
    # set interfaces loopback lo
    #
    #
    - name: Delete attributes of given interfaces (Note - This won't delete the interfaces
        themselves)
      vyos.vyos.vyos_interfaces:
        config:
        - name: bond1

        - name: eth1

        - name: eth2

        - name: eth3
        state: deleted
    #
    #
    # ------------------------
    # Module Execution Results
    # ------------------------
    #
    # "before": [
    #        {
    #            "enabled": true,
    #            "mtu": 1300,
    #            "name": "bond0"
    #        },
    #        {
    #            "description": "LAG - 1",
    #            "enabled": true,
    #            "name": "bond1"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "lo"
    #        },
    #        {
    #            "description": "Configured by Ansible Network",
    #            "duplex": "full",
    #            "enabled": true,
    #            "name": "eth3",
    #            "speed": "100"
    #        },
    #        {
    #            "description": "Configured by Ansible",
    #            "duplex": "full",
    #            "enabled": false,
    #            "mtu": 600,
    #            "name": "eth2",
    #            "speed": "100"
    #        },
    #        {
    #            "description": "Configured by Ansible Network",
    #            "duplex": "full",
    #            "enabled": true,
    #            "name": "eth1",
    #            "speed": "100"
    #        },
    #        {
    #            "description": "Outbound Interface for this appliance",
    #            "duplex": "auto",
    #            "enabled": true,
    #            "name": "eth0",
    #            "speed": "auto"
    #        }
    #    ]
    #
    # "commands": [
    #        "delete interfaces bonding bond1 description",
    #        "delete interfaces ethernet eth1 speed",
    #        "delete interfaces ethernet eth1 duplex",
    #        "delete interfaces ethernet eth1 description",
    #        "delete interfaces ethernet eth2 speed",
    #        "delete interfaces ethernet eth2 disable",
    #        "delete interfaces ethernet eth2 duplex",
    #        "delete interfaces ethernet eth2 disable",
    #        "delete interfaces ethernet eth2 description",
    #        "delete interfaces ethernet eth2 disable",
    #        "delete interfaces ethernet eth2 mtu",
    #        "delete interfaces ethernet eth2 disable",
    #        "delete interfaces ethernet eth3 speed",
    #        "delete interfaces ethernet eth3 duplex",
    #        "delete interfaces ethernet eth3 description"
    #    ]
    #
    # "after": [
    #        {
    #            "enabled": true,
    #            "mtu": 1300,
    #            "name": "bond0"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "bond1"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "lo"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "eth3"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "eth2"
    #        },
    #        {
    #            "enabled": true,
    #            "name": "eth1"
    #        },
    #        {
    #            "description": "Outbound Interface for this appliance",
    #            "duplex": "auto",
    #            "enabled": true,
    #            "name": "eth0",
    #            "speed": "auto"
    #        }
    #    ]
    #
    #
    # ------------
    # After state
    # ------------
    #
    # vyos@vyos:~$ show configuration commands | grep interfaces
    # set interfaces bonding bond0 mtu '1300'
    # set interfaces bonding bond1
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 address 'dhcpv6'
    # set interfaces ethernet eth0 description 'Outbound Interface for this appliance'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:30:f0:22'
    # set interfaces ethernet eth0 smp-affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 hw-id '08:00:27:ea:0f:b9'
    # set interfaces ethernet eth1 smp-affinity 'auto'
    # set interfaces ethernet eth2 hw-id '08:00:27:c2:98:23'
    # set interfaces ethernet eth2 smp-affinity 'auto'
    # set interfaces ethernet eth3 hw-id '08:00:27:43:70:8c'
    # set interfaces loopback lo
    #
    #


    # Using gathered
    #
    # Before state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep interfaces
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:50:5e:19'
    # set interfaces ethernet eth0 smp_affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 description 'Configured by Ansible'
    # set interfaces ethernet eth1 duplex 'auto'
    # set interfaces ethernet eth1 mtu '1500'
    # set interfaces ethernet eth1 speed 'auto'
    # set interfaces ethernet eth1 vif 200 description 'VIF - 200'
    # set interfaces ethernet eth2 description 'Configured by Ansible'
    # set interfaces ethernet eth2 duplex 'auto'
    # set interfaces ethernet eth2 mtu '1500'
    # set interfaces ethernet eth2 speed 'auto'
    # set interfaces ethernet eth2 vif 200 description 'VIF - 200'
    #
    - name: Gather listed interfaces with provided configurations
      vyos.vyos.vyos_interfaces:
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
    #             "description": "Configured by Ansible",
    #             "duplex": "auto",
    #             "enabled": true,
    #             "mtu": 1500,
    #             "name": "eth2",
    #             "speed": "auto",
    #             "vifs": [
    #                 {
    #                     "description": "VIF - 200",
    #                     "enabled": true,
    #                     "vlan_id": 200
    #                 }
    #             ]
    #         },
    #         {
    #             "description": "Configured by Ansible",
    #             "duplex": "auto",
    #             "enabled": true,
    #             "mtu": 1500,
    #             "name": "eth1",
    #             "speed": "auto",
    #             "vifs": [
    #                 {
    #                     "description": "VIF - 200",
    #                     "enabled": true,
    #                     "vlan_id": 200
    #                 }
    #             ]
    #         },
    #         {
    #             "duplex": "auto",
    #             "enabled": true,
    #             "name": "eth0",
    #             "speed": "auto"
    #         }
    #     ]
    #
    #
    # After state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep interfaces
    # set interfaces ethernet eth0 address 'dhcp'
    # set interfaces ethernet eth0 duplex 'auto'
    # set interfaces ethernet eth0 hw-id '08:00:27:50:5e:19'
    # set interfaces ethernet eth0 smp_affinity 'auto'
    # set interfaces ethernet eth0 speed 'auto'
    # set interfaces ethernet eth1 description 'Configured by Ansible'
    # set interfaces ethernet eth1 duplex 'auto'
    # set interfaces ethernet eth1 mtu '1500'
    # set interfaces ethernet eth1 speed 'auto'
    # set interfaces ethernet eth1 vif 200 description 'VIF - 200'
    # set interfaces ethernet eth2 description 'Configured by Ansible'
    # set interfaces ethernet eth2 duplex 'auto'
    # set interfaces ethernet eth2 mtu '1500'
    # set interfaces ethernet eth2 speed 'auto'
    # set interfaces ethernet eth2 vif 200 description 'VIF - 200'


    # Using rendered
    #
    #
    - name: Render the commands for provided  configuration
      vyos.vyos.vyos_interfaces:
        config:
        - name: eth0
          enabled: true
          duplex: auto
          speed: auto
        - name: eth1
          description: Configured by Ansible - Interface 1
          mtu: 1500
          speed: auto
          duplex: auto
          enabled: true
          vifs:
          - vlan_id: 100
            description: Eth1 - VIF 100
            mtu: 400
            enabled: true
          - vlan_id: 101
            description: Eth1 - VIF 101
            enabled: true
        - name: eth2
          description: Configured by Ansible - Interface 2 (ADMIN DOWN)
          mtu: 600
          enabled: false
        state: rendered
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #
    # "rendered": [
    #         "set interfaces ethernet eth0 duplex 'auto'",
    #         "set interfaces ethernet eth0 speed 'auto'",
    #         "delete interfaces ethernet eth0 disable",
    #         "set interfaces ethernet eth1 duplex 'auto'",
    #         "delete interfaces ethernet eth1 disable",
    #         "set interfaces ethernet eth1 speed 'auto'",
    #         "set interfaces ethernet eth1 description 'Configured by Ansible - Interface 1'",
    #         "set interfaces ethernet eth1 mtu '1500'",
    #         "set interfaces ethernet eth1 vif 100 description 'Eth1 - VIF 100'",
    #         "set interfaces ethernet eth1 vif 100 mtu '400'",
    #         "set interfaces ethernet eth1 vif 101 description 'Eth1 - VIF 101'",
    #         "set interfaces ethernet eth2 disable",
    #         "set interfaces ethernet eth2 description 'Configured by Ansible - Interface 2 (ADMIN DOWN)'",
    #         "set interfaces ethernet eth2 mtu '600'"
    #     ]


    # Using parsed
    #
    #
    - name: Parse the configuration.
      vyos.vyos.vyos_interfaces:
        running_config:
          "set interfaces ethernet eth0 address 'dhcp'
           set interfaces ethernet eth0 duplex 'auto'
           set interfaces ethernet eth0 hw-id '08:00:27:50:5e:19'
           set interfaces ethernet eth0 smp_affinity 'auto'
           set interfaces ethernet eth0 speed 'auto'
           set interfaces ethernet eth1 description 'Configured by Ansible'
           set interfaces ethernet eth1 duplex 'auto'
           set interfaces ethernet eth1 mtu '1500'
           set interfaces ethernet eth1 speed 'auto'
           set interfaces ethernet eth1 vif 200 description 'VIF - 200'
           set interfaces ethernet eth2 description 'Configured by Ansible'
           set interfaces ethernet eth2 duplex 'auto'
           set interfaces ethernet eth2 mtu '1500'
           set interfaces ethernet eth2 speed 'auto'
           set interfaces ethernet eth2 vif 200 description 'VIF - 200'"
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
    #             "description": "Configured by Ansible",
    #             "duplex": "auto",
    #             "enabled": true,
    #             "mtu": 1500,
    #             "name": "eth2",
    #             "speed": "auto",
    #             "vifs": [
    #                 {
    #                     "description": "VIF - 200",
    #                     "enabled": true,
    #                     "vlan_id": 200
    #                 }
    #             ]
    #         },
    #         {
    #             "description": "Configured by Ansible",
    #             "duplex": "auto",
    #             "enabled": true,
    #             "mtu": 1500,
    #             "name": "eth1",
    #             "speed": "auto",
    #             "vifs": [
    #                 {
    #                     "description": "VIF - 200",
    #                     "enabled": true,
    #                     "vlan_id": 200
    #                 }
    #             ]
    #         },
    #         {
    #             "duplex": "auto",
    #             "enabled": true,
    #             "name": "eth0",
    #             "speed": "auto"
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;set interfaces ethernet eth1 mtu 1200&#x27;, &#x27;set interfaces ethernet eth2 vif 100 description VIF 100&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Nilashish Chakraborty (@nilashishc)
- Rohit Thakur (@rohitthakur2590)
