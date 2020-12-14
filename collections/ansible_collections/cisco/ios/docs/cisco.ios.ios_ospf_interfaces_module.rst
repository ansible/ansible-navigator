.. _cisco.ios.ios_ospf_interfaces_module:


*****************************
cisco.ios.ios_ospf_interfaces
*****************************

**OSPF_Interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module configures and manages the Open Shortest Path First (OSPF) version 2 on IOS platforms.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="6">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="6">
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
                        <div>A dictionary of OSPF interfaces options.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
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
                        <div>OSPF interfaces settings on the interfaces in address-family context.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>adjacency</b>
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
                        <div>Adjacency staggering</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Address Family Identifier (AFI) for OSPF interfaces settings on the interfaces.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Enable authentication</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>Use a key-chain for cryptographic authentication keys</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>Use message-digest authentication</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>null</b>
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
                        <div>Use no authentication</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>BFD configuration commands</div>
                        <div>Enable/Disable BFD on this interface</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cost</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface cost</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dynamic_cost</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify dynamic cost options</div>
                        <div>Valid only with IPv6 OSPF config</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>default</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify default link metric value</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hysteresis</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify hysteresis value for LSA dampening</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>percent</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify hysteresis percent changed. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>threshold</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify hysteresis threshold value. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>weight</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify weight to be placed on individual metrics</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>l2_factor</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify weight to be given to L2-factor metric</div>
                        <div>Percentage weight of L2-factor metric. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>latency</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify weight to be given to latency metric.</div>
                        <div>Percentage weight of latency metric. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>oc</b>
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
                        <div>Specify weight to be given to cdr/mdr for oc</div>
                        <div>Give 100 percent weightage for current data rate(0 for maxdatarate)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>resources</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify weight to be given to resources metric</div>
                        <div>Percentage weight of resources metric. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>throughput</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify weight to be given to throughput metric</div>
                        <div>Percentage weight of throughput metric. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interface_cost</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface cost or Route cost of this interface</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>database_filter</b>
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
                        <div>Filter OSPF LSA during synchronization and flooding</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dead_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interval after which a neighbor is declared dead</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>minimal</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set to 1 second and set multiplier for Hellos</div>
                        <div>Number of Hellos sent within 1 second. Please refer vendor documentation of Valid values.</div>
                        <div>Valid only with IP OSPF config</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>time</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>time in seconds</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>demand_circuit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPF Demand Circuit, enable or disable the demand circuit&#x27;</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disable</b>
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
                        <div>Disable demand circuit on this interface</div>
                        <div>Valid only with IPv6 OSPF config</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>Enable Demand Circuit</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ignore</b>
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
                        <div>Ignore demand circuit auto-negotiation requests</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>flood_reduction</b>
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
                        <div>OSPF Flood Reduction</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Time between HELLO packets</div>
                        <div>Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lls</b>
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
                        <div>Link-local Signaling (LLS) support</div>
                        <div>Valid only with IP OSPF config</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>manet</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Mobile Adhoc Networking options</div>
                        <div>MANET Peering options</div>
                        <div>Valid only with IPv6 OSPF config</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cost</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Redundant path cost improvement required to peer</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>percent</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Relative incremental path cost. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>threshold</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Absolute incremental path cost. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>link_metrics</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Redundant path cost improvement required to peer</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cost_threshold</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Minimum link cost threshold. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>Enable link-metrics</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Ignores the MTU in DBD packets</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multi_area</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set the OSPF multi-area ID</div>
                        <div>Valid only with IP OSPF config</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>Interface cost</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPF multi-area ID as a decimal value. Please refer vendor documentation of Valid values.</div>
                        <div>OSPF multi-area ID in IP address format(e.g. A.B.C.D)</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>neighbor</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPF neighbor link-local IPv6 address (X:X:X:X::X)</div>
                        <div>Valid only with IPv6 OSPF config</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>Neighbor link-local IPv6 address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>OSPF cost for point-to-multipoint neighbor</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>database_filter</b>
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
                        <div>Filter OSPF LSA during synchronization and flooding for point-to-multipoint neighbor</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>poll_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPF dead-router polling interval</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>OSPF priority of non-broadcast neighbor</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>network</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Network type</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>broadcast</b>
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
                        <div>Specify OSPF broadcast multi-access network</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>manet</b>
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
                        <div>Specify MANET OSPF interface type</div>
                        <div>Valid only with IPv6 OSPF config</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>non_broadcast</b>
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
                        <div>Specify OSPF NBMA network</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>point_to_multipoint</b>
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
                        <div>Specify OSPF point-to-multipoint network</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>point_to_point</b>
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
                        <div>Specify OSPF point-to-point network</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefix_suppression</b>
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
                        <div>Enable/Disable OSPF prefix suppression</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Router priority. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>process</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPF interfaces process config</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>area_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPF interfaces area ID as a decimal value. Please refer vendor documentation of Valid values.</div>
                        <div>OSPF interfaces area ID in IP address format(e.g. A.B.C.D)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Address Family Identifier (AFI) for OSPF interfaces settings on the interfaces. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>instance_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set the OSPF instance based on ID</div>
                        <div>Valid only with IPv6 OSPF config</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>Include or exclude secondary IP addresses.</div>
                        <div>Valid only with IPv4 config</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>resync_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interval after which adjacency is reset if oob-resync is not started. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Time between retransmitting lost link state advertisements. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Set OSPF protocol&#x27;s state to disable under current interface</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Link state transmit delay. Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ttl_security</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>TTL security check</div>
                        <div>Valid only with IPV4 OSPF config</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hops</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum number of IP hops allowed</div>
                        <div>Please refer vendor documentation of Valid values.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>Enable TTL Security on all interfaces</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
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
                <td colspan="6">
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
                        <div>The value of this option should be the output received from the IOS device by executing the command <b>sh running-config | section ^interface</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="6">
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
                                    <li>rendered</li>
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

    # Using deleted

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ipv6 ospf 55 area 105
    #  ipv6 ospf priority 20
    #  ipv6 ospf transmit-delay 30
    #  ipv6 ospf adjacency stagger disable
    # interface GigabitEthernet0/2
    #  ip ospf priority 40
    #  ip ospf adjacency stagger disable
    #  ip ospf ttl-security hops 50
    #  ip ospf 10 area 20
    #  ip ospf cost 30

    - name: Delete provided OSPF Interface config
      cisco.ios.ios_ospf_interfaces:
        config:
          - name: GigabitEthernet0/1
        state: deleted

    #  Commands Fired:
    #  ---------------
    #
    #  "commands": [
    #         "interface GigabitEthernet0/1",
    #         "no ipv6 ospf 55 area 105",
    #         "no ipv6 ospf adjacency stagger disable",
    #         "no ipv6 ospf priority 20",
    #         "no ipv6 ospf transmit-delay 30"
    #     ]

    # After state:
    # -------------
    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    # interface GigabitEthernet0/2
    #  ip ospf priority 40
    #  ip ospf adjacency stagger disable
    #  ip ospf ttl-security hops 50
    #  ip ospf 10 area 20
    #  ip ospf cost 30

    # Using deleted without any config passed (NOTE: This will delete all OSPF Interfaces configuration from device)

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ipv6 ospf 55 area 105
    #  ipv6 ospf priority 20
    #  ipv6 ospf transmit-delay 30
    #  ipv6 ospf adjacency stagger disable
    # interface GigabitEthernet0/2
    #  ip ospf priority 40
    #  ip ospf adjacency stagger disable
    #  ip ospf ttl-security hops 50
    #  ip ospf 10 area 20
    #  ip ospf cost 30

    - name: Delete all OSPF config from interfaces
      cisco.ios.ios_ospf_interfaces:
        state: deleted

    # Commands Fired:
    # ---------------
    #
    #  "commands": [
    #         "interface GigabitEthernet0/2",
    #         "no ip ospf 10 area 20",
    #         "no ip ospf adjacency stagger disable",
    #         "no ip ospf cost 30",
    #         "no ip ospf priority 40",
    #         "no ip ospf ttl-security hops 50",
    #         "interface GigabitEthernet0/1",
    #         "no ipv6 ospf 55 area 105",
    #         "no ipv6 ospf adjacency stagger disable",
    #         "no ipv6 ospf priority 20",
    #         "no ipv6 ospf transmit-delay 30"
    #     ]

    # After state:
    # -------------
    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    # interface GigabitEthernet0/2

    # Using merged

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^interface
    # router-ios#

    - name: Merge provided OSPF Interfaces configuration
      cisco.ios.ios_ospf_interfaces:
        config:
          - name: GigabitEthernet0/1
            address_family:
              - afi: ipv4
                process:
                  id: 10
                  area_id: 30
                adjacency: true
                bfd: true
                cost:
                  interface_cost: 5
                dead_interval:
                  time: 5
                demand_circuit:
                  ignore: true
                network:
                  broadcast: true
                priority: 25
                resync_timeout: 10
                shutdown: true
                ttl_security:
                  hops: 50
              - afi: ipv6
                process:
                  id: 35
                  area_id: 45
                adjacency: true
                database_filter: true
                manet:
                  link_metrics:
                    cost_threshold: 10
                priority: 55
                transmit_delay: 45
        state: merged

    #  Commands Fired:
    #  ---------------
    #
    #   "commands": [
    #         "interface GigabitEthernet0/1",
    #         "ip ospf 10 area 30",
    #         "ip ospf adjacency stagger disable",
    #         "ip ospf bfd",
    #         "ip ospf cost 5",
    #         "ip ospf dead-interval 5",
    #         "ip ospf demand-circuit ignore",
    #         "ip ospf network broadcast",
    #         "ip ospf priority 25",
    #         "ip ospf resync-timeout 10",
    #         "ip ospf shutdown",
    #         "ip ospf ttl-security hops 50",
    #         "ipv6 ospf 35 area 45",
    #         "ipv6 ospf adjacency stagger disable",
    #         "ipv6 ospf database-filter all out",
    #         "ipv6 ospf manet peering link-metrics 10",
    #         "ipv6 ospf priority 55",
    #         "ipv6 ospf transmit-delay 45"
    #     ]

    # After state:
    # -------------
    #
    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip ospf network broadcast
    #  ip ospf resync-timeout 10
    #  ip ospf dead-interval 5
    #  ip ospf priority 25
    #  ip ospf demand-circuit ignore
    #  ip ospf bfd
    #  ip ospf adjacency stagger disable
    #  ip ospf ttl-security hops 50
    #  ip ospf shutdown
    #  ip ospf 10 area 30
    #  ip ospf cost 5
    #  ipv6 ospf 35 area 45
    #  ipv6 ospf priority 55
    #  ipv6 ospf transmit-delay 45
    #  ipv6 ospf database-filter all out
    #  ipv6 ospf adjacency stagger disable
    #  ipv6 ospf manet peering link-metrics 10
    # interface GigabitEthernet0/2

    # Using overridden

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip ospf network broadcast
    #  ip ospf resync-timeout 10
    #  ip ospf dead-interval 5
    #  ip ospf priority 25
    #  ip ospf demand-circuit ignore
    #  ip ospf bfd
    #  ip ospf adjacency stagger disable
    #  ip ospf ttl-security hops 50
    #  ip ospf shutdown
    #  ip ospf 10 area 30
    #  ip ospf cost 5
    #  ipv6 ospf 35 area 45
    #  ipv6 ospf priority 55
    #  ipv6 ospf transmit-delay 45
    #  ipv6 ospf database-filter all out
    #  ipv6 ospf adjacency stagger disable
    #  ipv6 ospf manet peering link-metrics 10
    # interface GigabitEthernet0/2

    - name: Override provided OSPF Interfaces configuration
      cisco.ios.ios_ospf_interfaces:
        config:
          - name: GigabitEthernet0/1
            address_family:
              - afi: ipv6
                process:
                  id: 55
                  area_id: 105
                adjacency: true
                priority: 20
                transmit_delay: 30
          - name: GigabitEthernet0/2
            address_family:
              - afi: ipv4
                process:
                  id: 10
                  area_id: 20
                adjacency: true
                cost:
                  interface_cost: 30
                priority: 40
                ttl_security:
                  hops: 50
        state: overridden

    # Commands Fired:
    # ---------------
    #
    #  "commands": [
    #         "interface GigabitEthernet0/2",
    #         "ip ospf 10 area 20",
    #         "ip ospf adjacency stagger disable",
    #         "ip ospf cost 30",
    #         "ip ospf priority 40",
    #         "ip ospf ttl-security hops 50",
    #         "interface GigabitEthernet0/1",
    #         "ipv6 ospf 55 area 105",
    #         "no ipv6 ospf database-filter all out",
    #         "no ipv6 ospf manet peering link-metrics 10",
    #         "ipv6 ospf priority 20",
    #         "ipv6 ospf transmit-delay 30",
    #         "no ip ospf 10 area 30",
    #         "no ip ospf adjacency stagger disable",
    #         "no ip ospf bfd",
    #         "no ip ospf cost 5",
    #         "no ip ospf dead-interval 5",
    #         "no ip ospf demand-circuit ignore",
    #         "no ip ospf network broadcast",
    #         "no ip ospf priority 25",
    #         "no ip ospf resync-timeout 10",
    #         "no ip ospf shutdown",
    #         "no ip ospf ttl-security hops 50"
    #     ]

    # After state:
    # -------------
    #
    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ipv6 ospf 55 area 105
    #  ipv6 ospf priority 20
    #  ipv6 ospf transmit-delay 30
    #  ipv6 ospf adjacency stagger disable
    # interface GigabitEthernet0/2
    #  ip ospf priority 40
    #  ip ospf adjacency stagger disable
    #  ip ospf ttl-security hops 50
    #  ip ospf 10 area 20
    #  ip ospf cost 30

    # Using replaced

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip ospf network broadcast
    #  ip ospf resync-timeout 10
    #  ip ospf dead-interval 5
    #  ip ospf priority 25
    #  ip ospf demand-circuit ignore
    #  ip ospf bfd
    #  ip ospf adjacency stagger disable
    #  ip ospf ttl-security hops 50
    #  ip ospf shutdown
    #  ip ospf 10 area 30
    #  ip ospf cost 5
    #  ipv6 ospf 35 area 45
    #  ipv6 ospf priority 55
    #  ipv6 ospf transmit-delay 45
    #  ipv6 ospf database-filter all out
    #  ipv6 ospf adjacency stagger disable
    #  ipv6 ospf manet peering link-metrics 10
    # interface GigabitEthernet0/2

    - name: Replaced provided OSPF Interfaces configuration
      cisco.ios.ios_ospf_interfaces:
        config:
          - name: GigabitEthernet0/2
            address_family:
              - afi: ipv6
                process:
                  id: 55
                  area_id: 105
                adjacency: true
                priority: 20
                transmit_delay: 30
        state: replaced

    # Commands Fired:
    # ---------------
    #  "commands": [
    #         "interface GigabitEthernet0/2",
    #         "ipv6 ospf 55 area 105",
    #         "ipv6 ospf adjacency stagger disable",
    #         "ipv6 ospf priority 20",
    #         "ipv6 ospf transmit-delay 30"
    #     ]

    # After state:
    # -------------
    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip ospf network broadcast
    #  ip ospf resync-timeout 10
    #  ip ospf dead-interval 5
    #  ip ospf priority 25
    #  ip ospf demand-circuit ignore
    #  ip ospf bfd
    #  ip ospf adjacency stagger disable
    #  ip ospf ttl-security hops 50
    #  ip ospf shutdown
    #  ip ospf 10 area 30
    #  ip ospf cost 5
    #  ipv6 ospf 35 area 45
    #  ipv6 ospf priority 55
    #  ipv6 ospf transmit-delay 45
    #  ipv6 ospf database-filter all out
    #  ipv6 ospf adjacency stagger disable
    #  ipv6 ospf manet peering link-metrics 10
    # interface GigabitEthernet0/2
    #  ipv6 ospf 55 area 105
    #  ipv6 ospf priority 20
    #  ipv6 ospf transmit-delay 30
    #  ipv6 ospf adjacency stagger disable

    # Using Gathered

    # Before state:
    # -------------
    #
    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip ospf network broadcast
    #  ip ospf resync-timeout 10
    #  ip ospf dead-interval 5
    #  ip ospf priority 25
    #  ip ospf demand-circuit ignore
    #  ip ospf bfd
    #  ip ospf adjacency stagger disable
    #  ip ospf ttl-security hops 50
    #  ip ospf shutdown
    #  ip ospf 10 area 30
    #  ip ospf cost 5
    #  ipv6 ospf 35 area 45
    #  ipv6 ospf priority 55
    #  ipv6 ospf transmit-delay 45
    #  ipv6 ospf database-filter all out
    #  ipv6 ospf adjacency stagger disable
    #  ipv6 ospf manet peering link-metrics 10
    # interface GigabitEthernet0/2

    - name: Gather OSPF Interfaces provided configurations
      cisco.ios.ios_ospf_interfaces:
        config:
        state: gathered

    # Module Execution Result:
    # ------------------------
    #
    #  "gathered": [
    #         {
    #             "name": "GigabitEthernet0/2"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "adjacency": true,
    #                     "afi": "ipv4",
    #                     "bfd": true,
    #                     "cost": {
    #                         "interface_cost": 5
    #                     },
    #                     "dead_interval": {
    #                         "time": 5
    #                     },
    #                     "demand_circuit": {
    #                         "ignore": true
    #                     },
    #                     "network": {
    #                         "broadcast": true
    #                     },
    #                     "priority": 25,
    #                     "process": {
    #                         "area_id": "30",
    #                         "id": 10
    #                     },
    #                     "resync_timeout": 10,
    #                     "shutdown": true,
    #                     "ttl_security": {
    #                         "hops": 50
    #                     }
    #                 },
    #                 {
    #                     "adjacency": true,
    #                     "afi": "ipv6",
    #                     "database_filter": true,
    #                     "manet": {
    #                         "link_metrics": {
    #                             "cost_threshold": 10
    #                         }
    #                     },
    #                     "priority": 55,
    #                     "process": {
    #                         "area_id": "45",
    #                         "id": 35
    #                     },
    #                     "transmit_delay": 45
    #                 }
    #             ],
    #             "name": "GigabitEthernet0/1"
    #         },
    #         {
    #             "name": "GigabitEthernet0/0"
    #         }
    #  ]

    # After state:
    # ------------
    #
    # router-ios#sh running-config | section ^interface
    # interface GigabitEthernet0/0
    # interface GigabitEthernet0/1
    #  ip ospf network broadcast
    #  ip ospf resync-timeout 10
    #  ip ospf dead-interval 5
    #  ip ospf priority 25
    #  ip ospf demand-circuit ignore
    #  ip ospf bfd
    #  ip ospf adjacency stagger disable
    #  ip ospf ttl-security hops 50
    #  ip ospf shutdown
    #  ip ospf 10 area 30
    #  ip ospf cost 5
    #  ipv6 ospf 35 area 45
    #  ipv6 ospf priority 55
    #  ipv6 ospf transmit-delay 45
    #  ipv6 ospf database-filter all out
    #  ipv6 ospf adjacency stagger disable
    #  ipv6 ospf manet peering link-metrics 10
    # interface GigabitEthernet0/2

    # Using Rendered

    - name: Render the commands for provided  configuration
      cisco.ios.ios_ospf_interfaces:
        config:
          - name: GigabitEthernet0/1
            address_family:
              - afi: ipv4
                process:
                  id: 10
                  area_id: 30
                adjacency: true
                bfd: true
                cost:
                  interface_cost: 5
                dead_interval:
                  time: 5
                demand_circuit:
                  ignore: true
                network:
                  broadcast: true
                priority: 25
                resync_timeout: 10
                shutdown: true
                ttl_security:
                  hops: 50
              - afi: ipv6
                process:
                  id: 35
                  area_id: 45
                adjacency: true
                database_filter: true
                manet:
                  link_metrics:
                    cost_threshold: 10
                priority: 55
                transmit_delay: 45
        state: rendered

    # Module Execution Result:
    # ------------------------
    #
    #  "rendered": [
    #         "interface GigabitEthernet0/1",
    #         "ip ospf 10 area 30",
    #         "ip ospf adjacency stagger disable",
    #         "ip ospf bfd",
    #         "ip ospf cost 5",
    #         "ip ospf dead-interval 5",
    #         "ip ospf demand-circuit ignore",
    #         "ip ospf network broadcast",
    #         "ip ospf priority 25",
    #         "ip ospf resync-timeout 10",
    #         "ip ospf shutdown",
    #         "ip ospf ttl-security hops 50",
    #         "ipv6 ospf 35 area 45",
    #         "ipv6 ospf adjacency stagger disable",
    #         "ipv6 ospf database-filter all out",
    #         "ipv6 ospf manet peering link-metrics 10",
    #         "ipv6 ospf priority 55",
    #         "ipv6 ospf transmit-delay 45"
    #     ]

    # Using Parsed

    # File: parsed.cfg
    # ----------------
    #
    # interface GigabitEthernet0/2
    # interface GigabitEthernet0/1
    #  ip ospf network broadcast
    #  ip ospf resync-timeout 10
    #  ip ospf dead-interval 5
    #  ip ospf priority 25
    #  ip ospf demand-circuit ignore
    #  ip ospf bfd
    #  ip ospf adjacency stagger disable
    #  ip ospf ttl-security hops 50
    #  ip ospf shutdown
    #  ip ospf 10 area 30
    #  ip ospf cost 5
    #  ipv6 ospf 35 area 45
    #  ipv6 ospf priority 55
    #  ipv6 ospf transmit-delay 45
    #  ipv6 ospf database-filter all out
    #  ipv6 ospf adjacency stagger disable
    #  ipv6 ospf manet peering link-metrics 10
    # interface GigabitEthernet0/0

    - name: Parse the provided configuration with the exisiting running configuration
      cisco.ios.ios_ospf_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Module Execution Result:
    # ------------------------
    #
    #  "parsed": [
    #         },
    #         {
    #             "name": "GigabitEthernet0/2"
    #         },
    #         {
    #             "address_family": [
    #                 {
    #                     "adjacency": true,
    #                     "afi": "ipv4",
    #                     "bfd": true,
    #                     "cost": {
    #                         "interface_cost": 5
    #                     },
    #                     "dead_interval": {
    #                         "time": 5
    #                     },
    #                     "demand_circuit": {
    #                         "ignore": true
    #                     },
    #                     "network": {
    #                         "broadcast": true
    #                     },
    #                     "priority": 25,
    #                     "process": {
    #                         "area_id": "30",
    #                         "id": 10
    #                     },
    #                     "resync_timeout": 10,
    #                     "shutdown": true,
    #                     "ttl_security": {
    #                         "hops": 50
    #                     }
    #                 },
    #                 {
    #                     "adjacency": true,
    #                     "afi": "ipv6",
    #                     "database_filter": true,
    #                     "manet": {
    #                         "link_metrics": {
    #                             "cost_threshold": 10
    #                         }
    #                     },
    #                     "priority": 55,
    #                     "process": {
    #                         "area_id": "45",
    #                         "id": 35
    #                     },
    #                     "transmit_delay": 45
    #                 }
    #             ],
    #             "name": "GigabitEthernet0/1"
    #         },
    #         {
    #             "name": "GigabitEthernet0/0"
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface GigabitEthernet0/1&#x27;, &#x27;ip ospf 10 area 30&#x27;, &#x27;ip ospf cost 5&#x27;, &#x27;ip ospf priority 25&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Sumit Jaiswal (@justjais)
