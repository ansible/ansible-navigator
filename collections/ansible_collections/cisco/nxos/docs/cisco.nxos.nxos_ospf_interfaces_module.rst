.. _cisco.nxos.nxos_ospf_interfaces_module:


*******************************
cisco.nxos.nxos_ospf_interfaces
*******************************

**OSPF Interfaces Resource Module.**


Version added: 1.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages OSPF(v2/v3) configuration of interfaces on devices running Cisco NX-OS.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="5">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="5">
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
                        <div>A list of OSPF configuration for interfaces.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address_family</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPF settings on the interfaces in address-family context.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>Address Family Identifier (AFI) for OSPF settings on the interfaces.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authentication</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication settings on the interface.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enable</b>
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
                        <div>Enable/disable authentication on the interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_chain</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication password key-chain.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>message_digest</b>
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
                        <div>Use message-digest authentication.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>null_auth</b>
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
                        <div>Use null(disable) authentication.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authentication_key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure the authentication key for the interface.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>encryption</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>0 Specifies an UNENCRYPTED authentication key will follow.</div>
                        <div>3 Specifies an 3DES ENCRYPTED authentication key will follow.</div>
                        <div>7 Specifies a Cisco type 7  ENCRYPTED authentication key will follow.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication key.</div>
                        <div>Valid values are Cisco type 7 ENCRYPTED password, 3DES ENCRYPTED password and UNENCRYPTED (cleartext) password based on the value of encryption key.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cost</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Cost associated with interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dead_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Dead interval value (in seconds).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hello_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Hello interval value (in seconds).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>instance</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Instance identifier.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>message_digest_key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Message digest authentication password (key) settings.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>encryption</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>0 Specifies an UNENCRYPTED ospf password (key) will follow.</div>
                        <div>3 Specifies an 3DES ENCRYPTED ospf password (key) will follow.</div>
                        <div>7 Specifies a Cisco type 7 ENCRYPTED the ospf password (key) will follow.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication key.</div>
                        <div>Valid values are Cisco type 7 ENCRYPTED password, 3DES ENCRYPTED password and UNENCRYPTED (cleartext) password based on the value of encryption key.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Key ID.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mtu_ignore</b>
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
                        <div>Enable/disable OSPF MTU mismatch detection.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multi_areas</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Multi-Areas associated with interface (not tied to OSPF process).</div>
                        <div>Valid values are Area Ids as an integer or IP address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>network</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>broadcast</li>
                                    <li>point-to-point</li>
                        </ul>
                </td>
                <td>
                        <div>Network type.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>passive_interface</b>
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
                        <div>Suppress routing updates on the interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>priority</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Router priority.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>processes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interfaces configuration for an OSPF process.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>area</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Area associated with interface.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>area_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Area ID as a decimal or IP address format.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>secondaries</b>
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
                        <div>Do not include secondary IPv4/IPv6 addresses.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multi_areas</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Multi-Areas associated with interface.</div>
                        <div>Valid values are Area Ids as an integer or IP address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>process_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPF process tag.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>retransmit_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Packet retransmission interval.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>shutdown</b>
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
                        <div>Shutdown OSPF on this interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>transmit_delay</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Packet transmission delay.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Name/Identifier of the interface.</div>
                </td>
            </tr>

            <tr>
                <td colspan="5">
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section &quot;^interface&quot;</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="5">
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

    # Using merged

    # Before state:
    # -------------
    # NXOS# show running-config | section ^interface
    # interface Ethernet1/1
    #   no switchport
    # interface Ethernet1/2
    #   no switchport
    # interface Ethernet1/3
    #   no switchport

    - name: Merge the provided configuration with the exisiting running configuration
      cisco.nxos.nxos_ospf_interfaces:
        config:
          - name: Ethernet1/1
            address_family:
            - afi: ipv4
              processes:
              - process_id: "100"
                area:
                  area_id: 1.1.1.1
                  secondaries: False
              multi_areas:
              - 11.11.11.11
            - afi: ipv6
              processes:
              - process_id: "200"
                area:
                  area_id: 2.2.2.2
                multi_areas:
                - 21.0.0.0
              - process_id: "300"
                multi_areas:
                - 50.50.50.50
              multi_areas:
              - 16.10.10.10
          - name: Ethernet1/2
            address_family:
            - afi: ipv4
              authentication:
                enable: True
                key_chain: test-1
              message_digest_key:
                key_id: 10
                encryption: 3
                key: abc01d272be25d29
              cost: 100
            - afi: ipv6
              network: broadcast
              shutdown: True
          - name: Ethernet1/3
            address_family:
            - afi: ipv4
              authentication_key:
                encryption: 7
                key: 12090404011C03162E
        state: merged

    # Task output
    # -------------
    # "before": [
    #        {
    #            "name": "Ethernet1/1"
    #        },
    #        {
    #            "name": "Ethernet1/2"
    #        },
    #        {
    #            "name": "Ethernet1/3"
    #        },
    # ]
    #
    # "commands": [
    #        "interface Ethernet1/1",
    #        "ip router ospf multi-area 11.11.11.11",
    #        "ip router ospf 100 area 1.1.1.1 secondaries none",
    #        "ipv6 router ospfv3 multi-area 16.10.10.10",
    #        "ipv6 router ospfv3 200 area 2.2.2.2",
    #        "ipv6 router ospfv3 200 multi-area 21.0.0.0",
    #        "ipv6 router ospfv3 300 multi-area 50.50.50.50",
    #        "interface Ethernet1/2",
    #        "ip ospf authentication key-chain test-1",
    #        "ip ospf authentication",
    #        "ip ospf message-digest-key 10 md5 3 abc01d272be25d29",
    #        "ip ospf cost 100",
    #        "ospfv3 network broadcast",
    #        "ospfv3 shutdown",
    #        "interface Ethernet1/3",
    #        "ip ospf authentication-key 7 12090404011C03162E"
    # ]
    #
    # "after": [
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "multi_areas": [
    #                        "11.11.11.11"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "1.1.1.1",
    #                                "secondaries": false
    #                            },
    #                            "process_id": "100"
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "multi_areas": [
    #                        "16.10.10.10"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "2.2.2.2"
    #                            },
    #                            "multi_areas": [
    #                                "21.0.0.0"
    #                            ],
    #                            "process_id": "200"
    #                        },
    #                        {
    #                            "multi_areas": [
    #                                "50.50.50.50"
    #                            ],
    #                            "process_id": "300"
    #                        }
    #                    ]
    #                }
    #            ],
    #            "name": "Ethernet1/1"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication": {
    #                       "enable": true,
    #                       "key_chain": "test-1"
    #                    },
    #                    "cost": 100,
    #                    "message_digest_key": {
    #                        "encryption": 3,
    #                        "key": "abc01d272be25d29",
    #                        "key_id": 10
    #                    }
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "network": "broadcast",
    #                    "shutdown": true
    #                }
    #            ],
    #            "name": "Ethernet1/2"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication_key": {
    #                        "encryption": 7,
    #                        "key": "12090404011C03162E"
    #                    }
    #                }
    #            ],
    #            "name": "Ethernet1/3"
    #        },
    # ]

    # After state:
    # -------------
    # NXOS# show running-config | section ^interface
    # interface Ethernet1/1
    #   no switchport
    #   ip router ospf 100 area 1.1.1.1 secondaries none
    #   ip router ospf multi-area 11.11.11.11
    #   ipv6 router ospfv3 200 area 2.2.2.2
    #   ipv6 router ospfv3 multi-area 16.10.10.10
    #   ipv6 router ospfv3 200 multi-area 21.0.0.0
    #   ipv6 router ospfv3 300 multi-area 50.50.50.50
    # interface Ethernet1/2
    #   no switchport
    #   ip ospf authentication
    #   ip ospf authentication key-chain test-1
    #   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
    #   ip ospf cost 100
    #   ospfv3 network broadcast
    #   ospfv3 shutdown
    # interface Ethernet1/3
    #   no switchport
    #   ip ospf authentication-key 7 12090404011C03162E


    # Using replaced

    # Before state:
    # ------------
    # NXOS# show running-config | section ^interface
    # interface Ethernet1/1
    #   no switchport
    #   ip router ospf 100 area 1.1.1.1 secondaries none
    #   ip router ospf multi-area 11.11.11.11
    #   ipv6 router ospfv3 200 area 2.2.2.2
    #   ipv6 router ospfv3 multi-area 16.10.10.10
    #   ipv6 router ospfv3 200 multi-area 21.0.0.0
    #   ipv6 router ospfv3 300 multi-area 50.50.50.50
    # interface Ethernet1/2
    #   no switchport
    #   ip ospf authentication
    #   ip ospf authentication key-chain test-1
    #   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
    #   ip ospf cost 100
    #   ospfv3 network broadcast
    #   ospfv3 shutdown
    # interface Ethernet1/3
    #   no switchport
    #   ip ospf authentication-key 7 12090404011C03162E

    - name: Replace OSPF configurations of listed interfaces with provided configurations
      cisco.nxos.nxos_ospf_interfaces:
        config:
        - name: Ethernet1/1
          address_family:
          - afi: ipv4
            processes:
            - process_id: "100"
              area:
                area_id: 1.1.1.1
                secondaries: False
            multi_areas:
            - 11.11.11.12
        - name: Ethernet1/3
        state: replaced

    # Task output
    # -------------
    # "before": [
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "multi_areas": [
    #                        "11.11.11.11"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "1.1.1.1",
    #                                "secondaries": false
    #                            },
    #                            "process_id": "100"
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "multi_areas": [
    #                        "16.10.10.10"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "2.2.2.2"
    #                            },
    #                            "multi_areas": [
    #                                "21.0.0.0"
    #                            ],
    #                            "process_id": "200"
    #                        },
    #                        {
    #                            "multi_areas": [
    #                                "50.50.50.50"
    #                            ],
    #                            "process_id": "300"
    #                        }
    #                    ]
    #                }
    #            ],
    #            "name": "Ethernet1/1"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication": {
    #                       "enable": true,
    #                       "key_chain": "test-1"
    #                    },
    #                    "cost": 100,
    #                    "message_digest_key": {
    #                        "encryption": 3,
    #                        "key": "abc01d272be25d29",
    #                        "key_id": 10
    #                    }
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "network": "broadcast",
    #                    "shutdown": true
    #                }
    #            ],
    #            "name": "Ethernet1/2"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication_key": {
    #                        "encryption": 7,
    #                        "key": "12090404011C03162E"
    #                    }
    #                }
    #            ],
    #            "name": "Ethernet1/3"
    #        },
    # ]
    #
    # "commands": [
    #        "interface Ethernet1/1",
    #        "ip router ospf multi-area 11.11.11.12",
    #        "no ip router ospf multi-area 11.11.11.11",
    #        "no ipv6 router ospfv3 multi-area 16.10.10.10",
    #        "no ipv6 router ospfv3 200 area 2.2.2.2",
    #        "no ipv6 router ospfv3 200 multi-area 21.0.0.0",
    #        "no ipv6 router ospfv3 300 multi-area 50.50.50.50",
    #        "interface Ethernet1/3",
    #        "no ip ospf authentication-key 7 12090404011C03162E"
    # ]
    #
    # "after": [
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "multi_areas": [
    #                        "11.11.11.12"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "1.1.1.1",
    #                                "secondaries": false
    #                            },
    #                            "process_id": "100"
    #                        }
    #                    ]
    #                }
    #            ],
    #            "name": "Ethernet1/1"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication": {
    #                        "enable": true,
    #                        "key_chain": "test-1"
    #                    },
    #                    "cost": 100,
    #                    "message_digest_key": {
    #                        "encryption": 3,
    #                        "key": "abc01d272be25d29",
    #                        "key_id": 10
    #                    }
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "network": "broadcast",
    #                    "shutdown": true
    #                }
    #            ],
    #            "name": "Ethernet1/2"
    #        },
    #        {
    #            "name": "Ethernet1/3"
    #        },
    #
    # After state:
    # -------------
    # NXOS# show running-config | section ^interface
    # interface Ethernet1/1
    #   no switchport
    #   ip router ospf 100 area 1.1.1.1 secondaries none
    #   ip router ospf multi-area 11.11.11.12
    # interface Ethernet1/2
    #   no switchport
    #   ip ospf authentication
    #   ip ospf authentication key-chain test-1
    #   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
    #   ip ospf cost 100
    #   ospfv3 network broadcast
    #   ospfv3 shutdown
    # interface Ethernet1/3
    #   no switchport


    # Using overridden

    # Before state:
    # ------------
    # NXOS# show running-config | section ^interface
    # interface Ethernet1/1
    #   no switchport
    #   ip router ospf 100 area 1.1.1.1 secondaries none
    #   ip router ospf multi-area 11.11.11.11
    #   ipv6 router ospfv3 200 area 2.2.2.2
    #   ipv6 router ospfv3 multi-area 16.10.10.10
    #   ipv6 router ospfv3 200 multi-area 21.0.0.0
    #   ipv6 router ospfv3 300 multi-area 50.50.50.50
    # interface Ethernet1/2
    #   no switchport
    #   ip ospf authentication
    #   ip ospf authentication key-chain test-1
    #   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
    #   ip ospf cost 100
    #   ospfv3 network broadcast
    #   ospfv3 shutdown
    # interface Ethernet1/3
    #   no switchport
    #   ip ospf authentication-key 7 12090404011C03162E

    - name: Overridde all OSPF interfaces configuration with provided configuration
      cisco.nxos.nxos_ospf_interfaces:
        config:
        - name: Ethernet1/1
          address_family:
          - afi: ipv4
            processes:
            - process_id: "100"
              area:
                area_id: 1.1.1.1
                secondaries: False
            multi_areas:
            - 11.11.11.12
        state: overridden

    # Task output
    # -------------
    # "before": [
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "multi_areas": [
    #                        "11.11.11.11"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "1.1.1.1",
    #                                "secondaries": false
    #                            },
    #                            "process_id": "100"
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "multi_areas": [
    #                        "16.10.10.10"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "2.2.2.2"
    #                            },
    #                            "multi_areas": [
    #                                "21.0.0.0"
    #                            ],
    #                            "process_id": "200"
    #                        },
    #                        {
    #                            "multi_areas": [
    #                                "50.50.50.50"
    #                            ],
    #                            "process_id": "300"
    #                        }
    #                    ]
    #                }
    #            ],
    #            "name": "Ethernet1/1"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication": {
    #                       "enable": true,
    #                       "key_chain": "test-1"
    #                    },
    #                    "cost": 100,
    #                    "message_digest_key": {
    #                        "encryption": 3,
    #                        "key": "abc01d272be25d29",
    #                        "key_id": 10
    #                    }
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "network": "broadcast",
    #                    "shutdown": true
    #                }
    #            ],
    #            "name": "Ethernet1/2"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication_key": {
    #                        "encryption": 7,
    #                        "key": "12090404011C03162E"
    #                    }
    #                }
    #            ],
    #            "name": "Ethernet1/3"
    #        },
    # ]
    #
    # "commands": [
    #        "interface Ethernet1/2",
    #        "no ip ospf authentication key-chain test-1",
    #        "no ip ospf authentication",
    #        "no ip ospf message-digest-key 10 md5 3 abc01d272be25d29",
    #        "no ip ospf cost 100",
    #        "no ospfv3 network broadcast",
    #        "no ospfv3 shutdown",
    #        "interface Ethernet1/3",
    #        "no ip ospf authentication-key 7 12090404011C03162E",
    #        "interface Ethernet1/1",
    #        "ip router ospf multi-area 11.11.11.12",
    #        "no ip router ospf multi-area 11.11.11.11",
    #        "no ipv6 router ospfv3 multi-area 16.10.10.10",
    #        "no ipv6 router ospfv3 200 area 2.2.2.2",
    #        "no ipv6 router ospfv3 200 multi-area 21.0.0.0",
    #        "no ipv6 router ospfv3 300 multi-area 50.50.50.50"
    # ]
    #
    # "after": [
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "multi_areas": [
    #                        "11.11.11.12"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "1.1.1.1",
    #                                "secondaries": false
    #                            },
    #                            "process_id": "100"
    #                        }
    #                    ]
    #                }
    #            ],
    #            "name": "Ethernet1/1"
    #        },
    #        {
    #            "name": "Ethernet1/2"
    #        },
    #        {
    #            "name": "Ethernet1/3"
    #        },
    # ]

    # After state:
    # -------------
    # NXOS# show running-config | section ^interface
    # interface Ethernet1/1
    #   no switchport
    #   ip router ospf 100 area 1.1.1.1 secondaries none
    #   ip router ospf multi-area 11.11.11.12
    # interface Ethernet1/2
    #   no switchport
    # interface Ethernet1/3
    #   no switchport

    # Using deleted to delete OSPF config of a single interface

    # Before state:
    # ------------
    # NXOS# show running-config | section ^interface
    # interface Ethernet1/1
    #   no switchport
    #   ip router ospf 100 area 1.1.1.1 secondaries none
    #   ip router ospf multi-area 11.11.11.11
    #   ipv6 router ospfv3 200 area 2.2.2.2
    #   ipv6 router ospfv3 multi-area 16.10.10.10
    #   ipv6 router ospfv3 200 multi-area 21.0.0.0
    #   ipv6 router ospfv3 300 multi-area 50.50.50.50
    # interface Ethernet1/2
    #   no switchport
    #   ip ospf authentication
    #   ip ospf authentication key-chain test-1
    #   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
    #   ip ospf cost 100
    #   ospfv3 network broadcast
    #   ospfv3 shutdown
    # interface Ethernet1/3
    #   no switchport
    #   ip ospf authentication-key 7 12090404011C03162E

    - name: Delete OSPF config from a single interface
      cisco.nxos.nxos_ospf_interfaces:
        config:
          - name: Ethernet1/1
        state: deleted

    # Task output
    # -------------
    # "before": [
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "multi_areas": [
    #                        "11.11.11.11"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "1.1.1.1",
    #                                "secondaries": false
    #                            },
    #                            "process_id": "100"
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "multi_areas": [
    #                        "16.10.10.10"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "2.2.2.2"
    #                            },
    #                            "multi_areas": [
    #                                "21.0.0.0"
    #                            ],
    #                            "process_id": "200"
    #                        },
    #                        {
    #                            "multi_areas": [
    #                                "50.50.50.50"
    #                            ],
    #                            "process_id": "300"
    #                        }
    #                    ]
    #                }
    #            ],
    #            "name": "Ethernet1/1"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication": {
    #                       "enable": true,
    #                       "key_chain": "test-1"
    #                    },
    #                    "cost": 100,
    #                    "message_digest_key": {
    #                        "encryption": 3,
    #                        "key": "abc01d272be25d29",
    #                        "key_id": 10
    #                    }
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "network": "broadcast",
    #                    "shutdown": true
    #                }
    #            ],
    #            "name": "Ethernet1/2"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication_key": {
    #                        "encryption": 7,
    #                        "key": "12090404011C03162E"
    #                    }
    #                }
    #            ],
    #            "name": "Ethernet1/3"
    #        },
    # ]
    #
    # "commands": [
    #        "interface Ethernet1/1",
    #        "no ip router ospf multi-area 11.11.11.11",
    #        "no ip router ospf 100 area 1.1.1.1 secondaries none",
    #        "no ipv6 router ospfv3 multi-area 16.10.10.10",
    #        "no ipv6 router ospfv3 200 area 2.2.2.2",
    #        "no ipv6 router ospfv3 200 multi-area 21.0.0.0",
    #        "no ipv6 router ospfv3 300 multi-area 50.50.50.50"
    # ]
    #
    # "before": [
    #        {
    #            "name": "Ethernet1/1"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication": {
    #                       "enable": true,
    #                       "key_chain": "test-1"
    #                    },
    #                    "cost": 100,
    #                    "message_digest_key": {
    #                        "encryption": 3,
    #                        "key": "abc01d272be25d29",
    #                        "key_id": 10
    #                    }
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "network": "broadcast",
    #                    "shutdown": true
    #                }
    #            ],
    #            "name": "Ethernet1/2"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication_key": {
    #                        "encryption": 7,
    #                        "key": "12090404011C03162E"
    #                    }
    #                }
    #            ],
    #            "name": "Ethernet1/3"
    #        },
    # ]

    # After state:
    # ------------
    # NXOS# show running-config | section ^interface
    # interface Ethernet1/1
    #   no switchport
    # interface Ethernet1/2
    #   no switchport
    #   ip ospf authentication
    #   ip ospf authentication key-chain test-1
    #   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
    #   ip ospf cost 100
    #   ospfv3 network broadcast
    #   ospfv3 shutdown
    # interface Ethernet1/3
    #   no switchport
    #   ip ospf authentication-key 7 12090404011C03162E

    # Using deleted to delete OSPF config from all interfaces

    # Before state:
    # ------------
    # NXOS# show running-config | section ^interface
    # interface Ethernet1/1
    #   no switchport
    #   ip router ospf 100 area 1.1.1.1 secondaries none
    #   ip router ospf multi-area 11.11.11.11
    #   ipv6 router ospfv3 200 area 2.2.2.2
    #   ipv6 router ospfv3 multi-area 16.10.10.10
    #   ipv6 router ospfv3 200 multi-area 21.0.0.0
    #   ipv6 router ospfv3 300 multi-area 50.50.50.50
    # interface Ethernet1/2
    #   no switchport
    #   ip ospf authentication
    #   ip ospf authentication key-chain test-1
    #   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
    #   ip ospf cost 100
    #   ospfv3 network broadcast
    #   ospfv3 shutdown
    # interface Ethernet1/3
    #   no switchport
    #   ip ospf authentication-key 7 12090404011C03162E

    - name: Delete OSPF config from all interfaces
      cisco.nxos.nxos_ospf_interfaces:
        state: deleted

    # Task output
    # -------------
    # "before": [
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "multi_areas": [
    #                        "11.11.11.11"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "1.1.1.1",
    #                                "secondaries": false
    #                            },
    #                            "process_id": "100"
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "multi_areas": [
    #                        "16.10.10.10"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "2.2.2.2"
    #                            },
    #                            "multi_areas": [
    #                                "21.0.0.0"
    #                            ],
    #                            "process_id": "200"
    #                        },
    #                        {
    #                            "multi_areas": [
    #                                "50.50.50.50"
    #                            ],
    #                            "process_id": "300"
    #                        }
    #                    ]
    #                }
    #            ],
    #            "name": "Ethernet1/1"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication": {
    #                       "enable": true,
    #                       "key_chain": "test-1"
    #                    },
    #                    "cost": 100,
    #                    "message_digest_key": {
    #                        "encryption": 3,
    #                        "key": "abc01d272be25d29",
    #                        "key_id": 10
    #                    }
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "network": "broadcast",
    #                    "shutdown": true
    #                }
    #            ],
    #            "name": "Ethernet1/2"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication_key": {
    #                        "encryption": 7,
    #                        "key": "12090404011C03162E"
    #                    }
    #                }
    #            ],
    #            "name": "Ethernet1/3"
    #        },
    # ]
    #
    # "commands": [
    #        "interface Ethernet1/1",
    #        "no ip router ospf multi-area 11.11.11.11",
    #        "no ip router ospf 100 area 1.1.1.1 secondaries none",
    #        "no ipv6 router ospfv3 multi-area 16.10.10.10",
    #        "no ipv6 router ospfv3 200 area 2.2.2.2",
    #        "no ipv6 router ospfv3 200 multi-area 21.0.0.0",
    #        "no ipv6 router ospfv3 300 multi-area 50.50.50.50",
    #        "interface Ethernet1/2",
    #        "no ip ospf authentication key-chain test-1",
    #        "no ip ospf authentication",
    #        "no ip ospf message-digest-key 10 md5 3 abc01d272be25d29",
    #        "no ip ospf cost 100",
    #        "no ospfv3 network broadcast",
    #        "no ospfv3 shutdown",
    #        "interface Ethernet1/3",
    #        "no ip ospf authentication-key 7 12090404011C03162E"
    # ]
    #
    # "after": [
    #        {
    #            "name": "Ethernet1/1"
    #        },
    #        {
    #            "name": "Ethernet1/2"
    #        },
    #        {
    #            "name": "Ethernet1/3"
    #        },
    # ]

    # After state:
    # ------------
    # NXOS# show running-config | section ^interface
    # interface Ethernet1/1
    #   no switchport
    # interface Ethernet1/2
    #   no switchport
    # interface Ethernet1/3
    #   no switchport

    # Using rendered

    - name: Render platform specific configuration lines with state rendered (without connecting to the device)
      cisco.nxos.nxos_ospf_interfaces:
        config:
          - name: Ethernet1/1
            address_family:
            - afi: ipv4
              processes:
              - process_id: "100"
                area:
                  area_id: 1.1.1.1
                  secondaries: False
              multi_areas:
              - 11.11.11.11
            - afi: ipv6
              processes:
              - process_id: "200"
                area:
                  area_id: 2.2.2.2
                multi_areas:
                - 21.0.0.0
              - process_id: "300"
                multi_areas:
                - 50.50.50.50
              multi_areas:
              - 16.10.10.10
          - name: Ethernet1/2
            address_family:
            - afi: ipv4
              authentication:
                enable: True
                key_chain: test-1
              message_digest_key:
                key_id: 10
                encryption: 3
                key: abc01d272be25d29
              cost: 100
            - afi: ipv6
              network: broadcast
              shutdown: True
          - name: Ethernet1/3
            address_family:
            - afi: ipv4
              authentication_key:
                encryption: 7
                key: 12090404011C03162E
        state: rendered

    # Task Output (redacted)
    # -----------------------
    # "rendered": [
    #        "interface Ethernet1/1",
    #        "ip router ospf multi-area 11.11.11.11",
    #        "ip router ospf 100 area 1.1.1.1 secondaries none",
    #        "ipv6 router ospfv3 multi-area 16.10.10.10",
    #        "ipv6 router ospfv3 200 area 2.2.2.2",
    #        "ipv6 router ospfv3 200 multi-area 21.0.0.0",
    #        "ipv6 router ospfv3 300 multi-area 50.50.50.50",
    #        "interface Ethernet1/2",
    #        "ip ospf authentication key-chain test-1",
    #        "ip ospf authentication",
    #        "ip ospf message-digest-key 10 md5 3 abc01d272be25d29",
    #        "ip ospf cost 100",
    #        "ospfv3 network broadcast",
    #        "ospfv3 shutdown",
    #        "interface Ethernet1/3",
    #        "ip ospf authentication-key 7 12090404011C03162E"
    # ]

    # Using parsed

    # parsed.cfg
    # ------------
    # interface Ethernet1/1
    #   ip router ospf 100 area 1.1.1.1 secondaries none
    #   ip router ospf multi-area 11.11.11.11
    #   ipv6 router ospfv3 200 area 2.2.2.2
    #   ipv6 router ospfv3 200 multi-area 21.0.0.0
    #   ipv6 router ospfv3 300 multi-area 50.50.50.50
    #   ipv6 router ospfv3 multi-area 16.10.10.10
    # interface Ethernet1/2
    #   ip ospf authentication
    #   ip ospf authentication key-chain test-1
    #   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
    #   ip ospf cost 100
    #   ospfv3 network broadcast
    #   ospfv3 shutdown
    # interface Ethernet1/3
    #   ip ospf authentication-key 7 12090404011C03162E

    - name: arse externally provided OSPF interfaces config
      cisco.nxos.nxos_ospf_interfaces:
        running_config: "{{ lookup('file', 'ospf_interfaces.cfg') }}"
        state: parsed

    # Task output (redacted)
    # -----------------------
    # "parsed": [
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "multi_areas": [
    #                        "11.11.11.11"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "1.1.1.1",
    #                                "secondaries": false
    #                            },
    #                            "process_id": "100"
    #                        }
    #                    ]
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "multi_areas": [
    #                        "16.10.10.10"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "2.2.2.2"
    #                            },
    #                            "multi_areas": [
    #                                "21.0.0.0"
    #                            ],
    #                            "process_id": "200"
    #                        },
    #                        {
    #                            "multi_areas": [
    #                                "50.50.50.50"
    #                            ],
    #                            "process_id": "300"
    #                        }
    #                    ]
    #                }
    #            ],
    #            "name": "Ethernet1/1"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication": {
    #                       "enable": true,
    #                       "key_chain": "test-1"
    #                    },
    #                    "cost": 100,
    #                    "message_digest_key": {
    #                        "encryption": 3,
    #                        "key": "abc01d272be25d29",
    #                        "key_id": 10
    #                    }
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "network": "broadcast",
    #                    "shutdown": true
    #                }
    #            ],
    #            "name": "Ethernet1/2"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication_key": {
    #                        "encryption": 7,
    #                        "key": "12090404011C03162E"
    #                    }
    #                }
    #            ],
    #            "name": "Ethernet1/3"
    #        },
    # ]

    # Using gathered

    # On-box config

    # NXOS# show running-config | section ^interface
    # interface Ethernet1/1
    #   no switchport
    #   ip router ospf 100 area 1.1.1.1 secondaries none
    #   ip router ospf multi-area 11.11.11.12
    # interface Ethernet1/2
    #   no switchport
    #   ip ospf authentication
    #   ip ospf authentication key-chain test-1
    #   ip ospf message-digest-key 10 md5 3 abc01d272be25d29
    #   ip ospf cost 100
    #   ospfv3 network broadcast
    #   ospfv3 shutdown
    # interface Ethernet1/3
    #   no switchport

    # Task output (redacted)
    # -----------------------
    # "gathered": [
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "multi_areas": [
    #                        "11.11.11.12"
    #                    ],
    #                    "processes": [
    #                        {
    #                            "area": {
    #                                "area_id": "1.1.1.1",
    #                                "secondaries": false
    #                            },
    #                            "process_id": "100"
    #                        }
    #                    ]
    #                }
    #            ],
    #            "name": "Ethernet1/1"
    #        },
    #        {
    #            "address_family": [
    #                {
    #                    "afi": "ipv4",
    #                    "authentication": {
    #                        "enable": true,
    #                        "key_chain": "test-1"
    #                    },
    #                    "cost": 100,
    #                    "message_digest_key": {
    #                        "encryption": 3,
    #                        "key": "abc01d272be25d29",
    #                        "key_id": 10
    #                    }
    #                },
    #                {
    #                    "afi": "ipv6",
    #                    "network": "broadcast",
    #                    "shutdown": true
    #                }
    #            ],
    #            "name": "Ethernet1/2"
    #        },
    #        {
    #            "name": "Ethernet1/3"
    #        },



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/1&#x27;, &#x27;ip router ospf multi-area 11.11.11.11&#x27;, &#x27;ip router ospf 100 area 1.1.1.1 secondaries none&#x27;, &#x27;no ipv6 router ospfv3 multi-area 16.10.10.10&#x27;, &#x27;ipv6 router ospfv3 200 area 2.2.2.2&#x27;, &#x27;ipv6 router ospfv3 200 multi-area 21.0.0.0&#x27;, &#x27;ipv6 router ospfv3 300 multi-area 50.50.50.50&#x27;, &#x27;interface Ethernet1/2&#x27;, &#x27;no ip ospf authentication key-chain test-1&#x27;, &#x27;ip ospf authentication&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Nilashish Chakraborty (@NilashishC)
