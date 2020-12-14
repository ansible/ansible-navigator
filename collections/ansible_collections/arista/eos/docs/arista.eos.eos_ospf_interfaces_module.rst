.. _arista.eos.eos_ospf_interfaces_module:


******************************
arista.eos.eos_ospf_interfaces
******************************

**OSPF Interfaces Resource Module.**


Version added: 1.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages OSPF configuration of interfaces on devices running Arista EOS.




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
                        <div>Valid only when afi = ipv4.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>Valid only when afi = ipv4.</div>
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
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>0 Specifies an UNENCRYPTED authentication key will follow.</div>
                        <div>7 Specifies a proprietry encryption type.`</div>
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
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>password (up to 8 chars).</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authentication_v2</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication settings on the interface.</div>
                        <div>Valid only when afi = ipv4.</div>
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
                    <b>set</b>
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
                        <div>Enable authentication on the interface.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authentication_v3</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication settings on the interface.</div>
                        <div>Valid only when afi = ipv6.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>algorithm</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>md5</li>
                                    <li>sha1</li>
                        </ul>
                </td>
                <td>
                        <div>Encryption alsgorithm.</div>
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
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>128 bit MD5 key or 140 bit SHA1 key.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>keytype</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies if an unencrypted/hidden follows.</div>
                        <div>0 denotes unencrypted key.</div>
                        <div>7 denotes hidden key.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>passphrase</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Passphrase String for deriving keys for authentication and encryption.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>spi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPsec Security Parameter Index.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bfd</b>
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
                        <div>Enable BFD.</div>
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
                        <div>metric associated with interface.</div>
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
                        <div>Time interval to detect a dead router.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>encryption_v3</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication settings on the interface.</div>
                        <div>Valid only when afi = ipv6.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>algorithm</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>md5</li>
                                    <li>sha1</li>
                        </ul>
                </td>
                <td>
                        <div>algorithm.</div>
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
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>3des-cbc</li>
                                    <li>aes-128-cbc</li>
                                    <li>aes-192-cbc</li>
                                    <li>aes-256-cbc</li>
                                    <li>null</li>
                        </ul>
                </td>
                <td>
                        <div>encryption type.</div>
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
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>key</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>keytype</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies if an unencrypted/hidden follows.</div>
                        <div>0 denotes unencrypted key.</div>
                        <div>7 denotes hidden key.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>passphrase</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Passphrase String for deriving keys for authentication and encryption.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>spi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPsec Security Parameter Index.</div>
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
                        <div>Timer interval between transmission of hello packets.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ip_params</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify parameters for IPv4/IPv6.</div>
                        <div>Valid only when afi = ipv6.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>Address Family Identifier (AFI) for OSPF settings on the interfaces.</div>
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
                        <div>Valid only when afi = ipv4.</div>
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
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bfd</b>
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
                        <div>Enable BFD.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>metric associated with interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>Time interval to detect a dead router.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>Timer interval between transmission of hello packets.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>if True, Disable MTU check for Database Description packets.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>network</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface type.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>Suppress routing updates in an interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>Interface priority.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>LSA retransmission interval.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>LSA transmission delay.</div>
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
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>0 Specifies an UNENCRYPTED ospf password (key) will follow.</div>
                        <div>7 Specifies a proprietry encryption type.</div>
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
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication key (upto 16 chars).</div>
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
                        <div>if True, Disable MTU check for Database Description packets.</div>
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
                </td>
                <td>
                        <div>Interface type.</div>
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
                        <div>Suppress routing updates in an interface.</div>
                        <div>Valid only when afi = ipv6.</div>
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
                        <div>Interface priority.</div>
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
                        <div>LSA retransmission interval.</div>
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
                        <div>LSA transmission delay.</div>
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
                        <div>The value of this option should be the output received from the EOS device by executing the command <b>show running-config | section interface</b>.</div>
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

    # Before state

    # veos(config)#show running-config | section interface | ospf
    # veos(config)#

      - name: Merge provided configuration with device configuration
        arista.eos.eos_ospf_interfaces:
          config:
            - name: "Vlan1"
              address_family:
                - afi: "ipv4"
                  area:
                    area_id: "0.0.0.50"
                  cost: 500
                  mtu_ignore: True
                - afi: "ipv6"
                  dead_interval: 44
                  ip_params:
                    - afi: "ipv6"
                      mtu_ignore: True
                      network: "point-to-point"
          state: merged

    # After State

    # veos(config)#show running-config | section interface | ospf
    # interface Vlan1
    #    ip ospf cost 500
    #    ip ospf mtu-ignore
    #    ip ospf area 0.0.0.50
    #    ospfv3 dead-interval 44
    #    ospfv3 ipv6 network point-to-point
    #    ospfv3 ipv6 mtu-ignore
    # veos(config)#
    #
    #
    # Module Execution:
    #
    #   "after": [
    #         {
    #             "name": "Ethernet1"
    #         },
    #         {
    #             "name": "Ethernet2"
    #         },
    #         {
    #             "name": "Management1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "area": {
    #                         "area_id": "0.0.0.50"
    #                     },
    #                     "cost": 500,
    #                     "mtu_ignore": True
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "dead_interval": 44,
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv6",
    #                             "mtu_ignore": True,
    #                             "network": "point-to-point"
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "name": "Vlan1"
    #         }
    #     ],
    #     "before": [
    #         {
    #             "name": "Ethernet1"
    #         },
    #         {
    #             "name": "Ethernet2"
    #         },
    #         {
    #             "name": "Management1"
    #         }
    #     ],
    #     "changed": True,
    #     "commands": [
    #         "interface Vlan1",
    #         "ip ospf area 0.0.0.50",
    #         "ip ospf cost 500",
    #         "ip ospf mtu-ignore",
    #         "ospfv3 dead-interval 44",
    #         "ospfv3 ipv6 mtu-ignore",
    #         "ospfv3 ipv6 network point-to-point"
    #     ],
    #

    # Using replaced
    #---------------

    # Before State:

    # veos(config)#show running-config | section interface | ospf
    # interface Vlan1
    #    ip ospf cost 500
    #    ip ospf dead-interval 29
    #    ip ospf hello-interval 66
    #    ip ospf mtu-ignore
    #    ip ospf area 0.0.0.50
    #    ospfv3 cost 106
    #    ospfv3 hello-interval 77
    #    ospfv3 dead-interval 44
    #    ospfv3 transmit-delay 100
    #    ospfv3 ipv4 priority 45
    #    ospfv3 ipv4 area 0.0.0.5
    #    ospfv3 ipv6 passive-interface
    #    ospfv3 ipv6 retransmit-interval 115
    #    ospfv3 ipv6 network point-to-point
    #    ospfv3 ipv6 mtu-ignore
    # !
    # interface Vlan2
    #    ospfv3 ipv4 hello-interval 45
    #    ospfv3 ipv4 retransmit-interval 100
    #    ospfv3 ipv4 area 0.0.0.6
    # veos(config)#


      - name: Replace device configuration with provided configuration
        arista.eos.eos_ospf_interfaces:
          config:
            - name: "Vlan1"
              address_family:
                - afi: "ipv6"
                  cost: 44
                  bfd: True
                  ip_params:
                    - afi: "ipv6"
                      mtu_ignore: True
                      network: "point-to-point"
                      dead_interval: 56
          state: replaced

    # After State:

    # veos(config)#show running-config | section interface | ospf
    # interface Vlan1
    #    ospfv3 bfd
    #    ospfv3 cost 44
    #    no ospfv3 ipv6 passive-interface
    #    ospfv3 ipv6 network point-to-point
    #    ospfv3 ipv6 mtu-ignore
    # !
    # interface Vlan2
    #    ospfv3 ipv4 hello-interval 45
    #    ospfv3 ipv4 retransmit-interval 100
    #    ospfv3 ipv4 area 0.0.0.6
    # veos(config)#
    #
    # Module Execution:
    #
    # "after": [
    #         {
    #             "name": "Ethernet1"
    #         },
    #         {
    #             "name": "Ethernet2"
    #         },
    #         {
    #             "name": "Management1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv6",
    #                     "bfd": True,
    #                     "cost": 44,
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv6",
    #                             "mtu_ignore": True,
    #                             "network": "point-to-point"
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "name": "Vlan1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv6",
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv4",
    #                             "area": {
    #                                 "area_id": "0.0.0.6"
    #                             },
    #                             "hello_interval": 45,
    #                             "retransmit_interval": 100
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "name": "Vlan2"
    #         }
    #     ],
    #     "before": [
    #         {
    #             "name": "Ethernet1"
    #         },
    #         {
    #             "name": "Ethernet2"
    #         },
    #         {
    #             "name": "Management1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "area": {
    #                         "area_id": "0.0.0.50"
    #                     },
    #                     "cost": 500,
    #                     "dead_interval": 29,
    #                     "hello_interval": 66,
    #                     "mtu_ignore": True
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "cost": 106,
    #                     "dead_interval": 44,
    #                     "hello_interval": 77,
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv4",
    #                             "area": {
    #                                 "area_id": "0.0.0.5"
    #                             },
    #                             "priority": 45
    #                         },
    #                         {
    #                             "afi": "ipv6",
    #                             "mtu_ignore": True,
    #                             "network": "point-to-point",
    #                             "passive_interface": True,
    #                             "retransmit_interval": 115
    #                         }
    #                     ],
    #                     "transmit_delay": 100
    #                 }
    #             ],
    #             "name": "Vlan1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv6",
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv4",
    #                             "area": {
    #                                 "area_id": "0.0.0.6"
    #                             },
    #                             "hello_interval": 45,
    #                             "retransmit_interval": 100
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "name": "Vlan2"
    #         }
    #     ],
    #     "changed": True,
    #     "commands": [
    #         "interface Vlan1",
    #         "no ip ospf cost 500",
    #         "no ip ospf dead-interval 29",
    #         "no ip ospf hello-interval 66",
    #         "no ip ospf mtu-ignore",
    #         "no ip ospf area 0.0.0.50",
    #         "ospfv3 cost 44",
    #         "ospfv3 bfd",
    #         "ospfv3 authentication ipsec spi 30 md5 passphrase 7 7hl8FV3lZ6H1mAKpjL47hQ==",
    #         "no ospfv3 ipv4 priority 45",
    #         "no ospfv3 ipv4 area 0.0.0.5",
    #         "ospfv3 ipv6 dead-interval 56",
    #         "no ospfv3 ipv6 passive-interface",
    #         "no ospfv3 ipv6 retransmit-interval 115",
    #         "no ospfv3 hello-interval 77",
    #         "no ospfv3 dead-interval 44",
    #         "no ospfv3 transmit-delay 100"
    #     ],
    #

    # Using overidden:
    # ----------------

    # Before State:
    # veos(config)#show running-config | section interface | ospf
    # interface Vlan1
    #    ip ospf dead-interval 29
    #    ip ospf hello-interval 66
    #    ip ospf mtu-ignore
    #    ospfv3 bfd
    #    ospfv3 cost 106
    #    ospfv3 hello-interval 77
    #    ospfv3 transmit-delay 100
    #    ospfv3 ipv4 priority 45
    #    ospfv3 ipv4 area 0.0.0.5
    #    ospfv3 ipv6 passive-interface
    #    ospfv3 ipv6 dead-interval 56
    #    ospfv3 ipv6 retransmit-interval 115
    #    ospfv3 ipv6 network point-to-point
    #    ospfv3 ipv6 mtu-ignore
    # !
    # interface Vlan2
    #    ospfv3 ipv4 hello-interval 45
    #    ospfv3 ipv4 retransmit-interval 100
    #    ospfv3 ipv4 area 0.0.0.6
    # veos(config)#

      - name: Override device configuration with provided configuration
        arista.eos.eos_ospf_interfaces:
          config:
            - name: "Vlan1"
              address_family:
                - afi: "ipv6"
                  cost: 44
                  bfd: True
                  ip_params:
                    - afi: "ipv6"
                      mtu_ignore: True
                      network: "point-to-point"
                      dead_interval: 56
          state: overridden

    # After State:

    # veos(config)#show running-config | section interface | ospf
    # interface Vlan1
    #    ospfv3 bfd
    #    ospfv3 cost 44
    #    no ospfv3 ipv6 passive-interface
    #    ospfv3 ipv6 dead-interval 56
    #    ospfv3 ipv6 network point-to-point
    #    ospfv3 ipv6 mtu-ignore
    # veos(config)#
    #
    #
    # Module Execution:
    #
    #  "after": [
    #         {
    #             "name": "Ethernet1"
    #         },
    #         {
    #             "name": "Ethernet2"
    #         },
    #         {
    #             "name": "Management1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv6",
    #                     "bfd": True,
    #                     "cost": 44,
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv6",
    #                             "dead_interval": 56,
    #                             "mtu_ignore": True,
    #                             "network": "point-to-point"
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "name": "Vlan1"
    #         },
    #         {
    #             "name": "Vlan2"
    #         }
    #     ],
    #     "before": [
    #         {
    #             "name": "Ethernet1"
    #         },
    #         {
    #             "name": "Ethernet2"
    #         },
    #         {
    #             "name": "Management1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "dead_interval": 29,
    #                     "hello_interval": 66,
    #                     "mtu_ignore": True
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "bfd": True,
    #                     "cost": 106,
    #                     "hello_interval": 77,
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv4",
    #                             "area": {
    #                                 "area_id": "0.0.0.5"
    #                             },
    #                             "priority": 45
    #                         },
    #                         {
    #                             "afi": "ipv6",
    #                             "dead_interval": 56,
    #                             "mtu_ignore": True,
    #                             "network": "point-to-point",
    #                             "passive_interface": True,
    #                             "retransmit_interval": 115
    #                         }
    #                     ],
    #                     "transmit_delay": 100
    #                 }
    #             ],
    #             "name": "Vlan1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv6",
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv4",
    #                             "area": {
    #                                 "area_id": "0.0.0.6"
    #                             },
    #                             "hello_interval": 45,
    #                             "retransmit_interval": 100
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "name": "Vlan2"
    #         }
    #     ],
    #     "changed": True,
    #     "commands": [
    #         "interface Vlan2",
    #         "no ospfv3 ipv4 hello-interval 45",
    #         "no ospfv3 ipv4 retransmit-interval 100",
    #         "no ospfv3 ipv4 area 0.0.0.6",
    #         "interface Vlan1",
    #         "no ip ospf dead-interval 29",
    #         "no ip ospf hello-interval 66",
    #         "no ip ospf mtu-ignore",
    #         "ospfv3 cost 44",
    #         "ospfv3 authentication ipsec spi 30 md5 passphrase 7 7hl8FV3lZ6H1mAKpjL47hQ==",
    #         "no ospfv3 ipv4 priority 45",
    #         "no ospfv3 ipv4 area 0.0.0.5",
    #         "no ospfv3 ipv6 passive-interface",
    #         "no ospfv3 ipv6 retransmit-interval 115",
    #         "no ospfv3 hello-interval 77",
    #         "no ospfv3 transmit-delay 100"
    #     ],
    #

    # Using deleted:
    #--------------

    # before State:

    # veos(config)#show running-config | section interface | ospf
    # interface Vlan1
    #    ip ospf dead-interval 29
    #    ip ospf hello-interval 66
    #    ip ospf mtu-ignore
    #    ospfv3 bfd
    #    ospfv3 cost 106
    #    ospfv3 hello-interval 77
    #    ospfv3 transmit-delay 100
    #    ospfv3 ipv4 priority 45
    #    ospfv3 ipv4 area 0.0.0.5
    #    ospfv3 ipv6 passive-interface
    #    ospfv3 ipv6 dead-interval 56
    #    ospfv3 ipv6 retransmit-interval 115
    #    ospfv3 ipv6 network point-to-point
    #    ospfv3 ipv6 mtu-ignore
    # !
    # interface Vlan2
    #    ospfv3 ipv4 hello-interval 45
    #    ospfv3 ipv4 retransmit-interval 100
    #    ospfv3 ipv4 area 0.0.0.6
    # veos(config)#

      - name: Delete device configuration
        arista.eos.eos_ospf_interfaces:
          config:
            - name: "Vlan1"
          state: deleted

    # After State:

    # veos#show running-config | section interface | ospf
    # interface Vlan2
    #    ospfv3 ipv4 hello-interval 45
    #    ospfv3 ipv4 retransmit-interval 100
    #    ospfv3 ipv4 area 0.0.0.6
    #
    # Module Execution:
    #
    # "after": [
    #         {
    #             "name": "Ethernet1"
    #         },
    #         {
    #             "name": "Ethernet2"
    #         },
    #         {
    #             "name": "Management1"
    #         },
    #         {
    #             "name": "Vlan1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv6",
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv4",
    #                             "area": {
    #                                 "area_id": "0.0.0.6"
    #                             },
    #                             "hello_interval": 45,
    #                             "retransmit_interval": 100
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "name": "Vlan2"
    #         }
    #     ],
    #     "before": [
    #         {
    #             "name": "Ethernet1"
    #         },
    #         {
    #             "name": "Ethernet2"
    #         },
    #         {
    #             "name": "Management1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "dead_interval": 29,
    #                     "hello_interval": 66,
    #                     "mtu_ignore": True
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "bfd": True,
    #                     "cost": 106,
    #                     "hello_interval": 77,
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv4",
    #                             "area": {
    #                                 "area_id": "0.0.0.5"
    #                             },
    #                             "priority": 45
    #                         },
    #                         {
    #                             "afi": "ipv6",
    #                             "dead_interval": 56,
    #                             "mtu_ignore": True,
    #                             "network": "point-to-point",
    #                             "passive_interface": True,
    #                             "retransmit_interval": 115
    #                         }
    #                     ],
    #                     "transmit_delay": 100
    #                 }
    #             ],
    #             "name": "Vlan1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv6",
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv4",
    #                             "area": {
    #                                 "area_id": "0.0.0.6"
    #                             },
    #                             "hello_interval": 45,
    #                             "retransmit_interval": 100
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "name": "Vlan2"
    #         }
    #     ],
    #     "changed": True,
    #     "commands": [
    #         "interface Vlan1",
    #         "no ip ospf dead-interval 29",
    #         "no ip ospf hello-interval 66",
    #         "no ip ospf mtu-ignore",
    #         "no ospfv3 bfd",
    #         "no ospfv3 cost 106",
    #         "no ospfv3 hello-interval 77",
    #         "no ospfv3 transmit-delay 100",
    #         "no ospfv3 ipv4 priority 45",
    #         "no ospfv3 ipv4 area 0.0.0.5",
    #         "no ospfv3 ipv6 passive-interface",
    #         "no ospfv3 ipv6 dead-interval 56",
    #         "no ospfv3 ipv6 retransmit-interval 115",
    #         "no ospfv3 ipv6 network point-to-point",
    #         "no ospfv3 ipv6 mtu-ignore"
    #     ],
    #

    # Using parsed:
    # ------------

    # parsed.cfg:
    # ----------

    # interface Vlan1
    #    ip ospf dead-interval 29
    #    ip ospf hello-interval 66
    #    ip ospf mtu-ignore
    #    ip ospf cost 500
    #    ospfv3 bfd
    #    ospfv3 cost 106
    #    ospfv3 hello-interval 77
    #    ospfv3 transmit-delay 100
    #    ospfv3 ipv4 priority 45
    #    ospfv3 ipv4 area 0.0.0.5
    #    ospfv3 ipv6 passive-interface
    #    ospfv3 ipv6 dead-interval 56
    #    ospfv3 ipv6 retransmit-interval 115
    #    ospfv3 ipv6 network point-to-point
    #    ospfv3 ipv6 mtu-ignore
    # !
    # interface Vlan2
    #    ospfv3 ipv4 hello-interval 45
    #    ospfv3 ipv4 retransmit-interval 100
    #    ospfv3 ipv4 area 0.0.0.6
    #

      - name: parse configs
        arista.eos.eos_ospf_interfaces:
          running_config: "{{ lookup('file', './parsed.cfg') }}"
          state: parsed

    # Module Execution:
    # "parsed": [
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "cost": 500,
    #                     "dead_interval": 29,
    #                     "hello_interval": 66,
    #                     "mtu_ignore": True
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "bfd": True,
    #                     "cost": 106,
    #                     "hello_interval": 77,
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv4",
    #                             "area": {
    #                                 "area_id": "0.0.0.5"
    #                             },
    #                             "priority": 45
    #                         },
    #                         {
    #                             "afi": "ipv6",
    #                             "dead_interval": 56,
    #                             "mtu_ignore": True,
    #                             "network": "point-to-point",
    #                             "passive_interface": True,
    #                             "retransmit_interval": 115
    #                         }
    #                     ],
    #                     "transmit_delay": 100
    #                 }
    #             ],
    #             "name": "Vlan1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv6",
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv4",
    #                             "area": {
    #                                 "area_id": "0.0.0.6"
    #                             },
    #                             "hello_interval": 45,
    #                             "retransmit_interval": 100
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "name": "Vlan2"
    #         }
    #     ]

    # Using gathered:

    # Device COnfig:

    # veos#show running-config | section interface | ospf
    # interface Vlan1
    #    ip ospf cost 500
    #    ip ospf dead-interval 29
    #    ip ospf hello-interval 66
    #    ip ospf mtu-ignore
    #    ip ospf area 0.0.0.50
    #    ospfv3 cost 106
    #    ospfv3 hello-interval 77
    #    ospfv3 transmit-delay 100
    #    ospfv3 ipv4 priority 45
    #    ospfv3 ipv4 area 0.0.0.5
    #    ospfv3 ipv6 passive-interface
    #    ospfv3 ipv6 dead-interval 56
    #    ospfv3 ipv6 retransmit-interval 115
    #    ospfv3 ipv6 network point-to-point
    #    ospfv3 ipv6 mtu-ignore
    # !
    # interface Vlan2
    #    ospfv3 ipv4 hello-interval 45
    #    ospfv3 ipv4 retransmit-interval 100
    #    ospfv3 ipv4 area 0.0.0.6
    # veos#

      - name: gather configs
        arista.eos.eos_ospf_interfaces:
          state: gathered

    # Module Execution:
    #
    #  "gathered": [
    #         {
    #             "name": "Ethernet1"
    #         },
    #         {
    #             "name": "Ethernet2"
    #         },
    #         {
    #             "name": "Management1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv4",
    #                     "area": {
    #                         "area_id": "0.0.0.50"
    #                     },
    #                     "cost": 500,
    #                     "dead_interval": 29,
    #                     "hello_interval": 66,
    #                     "mtu_ignore": True
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "cost": 106,
    #                     "hello_interval": 77,
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv4",
    #                             "area": {
    #                                 "area_id": "0.0.0.5"
    #                             },
    #                             "priority": 45
    #                         },
    #                         {
    #                             "afi": "ipv6",
    #                             "dead_interval": 56,
    #                             "mtu_ignore": True,
    #                             "network": "point-to-point",
    #                             "passive_interface": True,
    #                             "retransmit_interval": 115
    #                         }
    #                     ],
    #                     "transmit_delay": 100
    #                 }
    #             ],
    #             "name": "Vlan1"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "afi": "ipv6",
    #                     "ip_params": [
    #                         {
    #                             "afi": "ipv4",
    #                             "area": {
    #                                 "area_id": "0.0.0.6"
    #                             },
    #                             "hello_interval": 45,
    #                             "retransmit_interval": 100
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "name": "Vlan2"
    #         }
    #     ],
    #


    # Using rendered:
    # --------------

      - name: Render provided configuration
        arista.eos.eos_ospf_interfaces:
          config:
            - name: "Vlan1"
              address_family:
                - afi: "ipv4"
                  dead_interval: 29
                  mtu_ignore: True
                  hello_interval: 66
                - afi: "ipv6"
                  hello_interval: 77
                  cost : 106
                  transmit_delay: 100
                  ip_params:
                    - afi: "ipv6"
                      retransmit_interval: 115
                      dead_interval: 56
                      passive_interface: True
                    - afi: "ipv4"
                      area:
                        area_id: "0.0.0.5"
                      priority: 45
            - name: "Vlan2"
              address_family:
                - afi: "ipv6"
                  ip_params:
                    - afi: "ipv4"
                      area:
                        area_id: "0.0.0.6"
                      hello_interval: 45
                      retransmit_interval: 100
                - afi: "ipv4"
                  message_digest_key:
                    key_id: 200
                    encryption: 7
                    key: "hkdfhtu=="

          state: rendered

    # Module Execution:
    #
    # "rendered": [
    #         "interface Vlan1",
    #         "ip ospf dead-interval 29",
    #         "ip ospf mtu-ignore",
    #         "ip ospf hello-interval 66",
    #         "ospfv3 hello-interval 77",
    #         "ospfv3 cost 106",
    #         "ospfv3 transmit-delay 100",
    #         "ospfv3 ipv4 area 0.0.0.5",
    #         "ospfv3 ipv4 priority 45",
    #         "ospfv3 ipv6 retransmit-interval 115",
    #         "ospfv3 ipv6 dead-interval 56",
    #         "ospfv3 ipv6 passive-interface",
    #         "interface Vlan2",
    #         "ip ospf message-digest-key 200 md5 7 hkdfhtu==",
    #         "ospfv3 ipv4 area 0.0.0.6",
    #         "ospfv3 ipv4 hello-interval 45",
    #         "ospfv3 ipv4 retransmit-interval 100"
    #     ]
    #




Status
------


Authors
~~~~~~~

- Gomathi Selvi Srinivasan (@GomathiselviS)
