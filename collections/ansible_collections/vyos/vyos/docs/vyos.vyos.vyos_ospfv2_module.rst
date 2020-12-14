.. _vyos.vyos.vyos_ospfv2_module:


*********************
vyos.vyos.vyos_ospfv2
*********************

**OSPFv2 resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This resource module configures and manages attributes of OSPFv2 routes on VyOS network devices.




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
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A provided OSPFv2 route configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>areas</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv2 area.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>OSPFv2 area identity.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>area_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Area type.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>normal</b>
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
                        <div>Normal OSPFv2 area.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nssa</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>NSSA OSPFv2 area.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>default_cost</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Summary-default cost of NSSA area.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>no_summary</b>
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
                        <div>Do not inject inter-area routes into stub.</div>
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
                        <div>Enabling NSSA.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>translate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>always</li>
                                    <li>candidate</li>
                                    <li>never</li>
                        </ul>
                </td>
                <td>
                        <div>NSSA-ABR.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>stub</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Stub OSPFv2 area.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>default_cost</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Summary-default cost of stub area.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>no_summary</b>
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
                        <div>Do not inject inter-area routes into stub.</div>
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
                        <div>Enabling stub.</div>
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
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>plaintext-password</li>
                                    <li>md5</li>
                        </ul>
                </td>
                <td>
                        <div>OSPFv2 area authentication type.</div>
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
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv2 network.</div>
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
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv2 IPv4 network address.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>range</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Summarize routes matching prefix (border routers only).</div>
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
                        <div>border router IPv4 address.</div>
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
                        <div>Metric for this range.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>not_advertise</b>
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
                        <div>Don&#x27;t advertise this range.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>substitute</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Announce area range (IPv4 address) as another prefix.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>shortcut</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>default</li>
                                    <li>disable</li>
                                    <li>enable</li>
                        </ul>
                </td>
                <td>
                        <div>Area&#x27;s shortcut mode.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>virtual_link</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual link address.</div>
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
                        <div>virtual link address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>OSPFv2 area authentication type.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>md5</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>MD5 key id based authentication.</div>
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
                    <b>key_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>MD5 key id.</div>
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
                    <b>md5_key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>MD5 key.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>plaintext_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Plain text password.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>Interval after which a neighbor is declared dead.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>Interval between hello packets.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>Interval between retransmitting lost link state advertisements.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                        <div>Link state transmit delay.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>auto_cost</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Calculate OSPFv2 interface cost according to bandwidth.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>reference_bandwidth</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Reference bandwidth cost in Mbits/sec.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>default_information</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Control distribution of default information.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>originate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Distribute a default route.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>always</b>
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
                        <div>Always advertise default route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>metric</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv2 default metric.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>metric_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv2 Metric types for default routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route map references.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>default_metric</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Metric of redistributed routes</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>distance</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Administrative distance.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>global</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Global OSPFv2 administrative distance.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ospf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv2 administrative distance.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>external</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Distance for external routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>inter_area</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Distance for inter-area routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>intra_area</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Distance for intra-area routes.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>log_adjacency_changes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>detail</li>
                        </ul>
                </td>
                <td>
                        <div>Log changes in adjacency state.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_metric</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv2 maximum/infinite-distance metric.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>router_lsa</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Advertise own Router-LSA with infinite distance (stub router).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>administrative</b>
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
                        <div>Administratively apply, for an indefinite period.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>on_shutdown</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Time to advertise self as stub-router.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>on_startup</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Time to advertise self as stub-router</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mpls_te</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>MultiProtocol Label Switching-Traffic Engineering (MPLS-TE) parameters.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Enable MPLS-TE functionality.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>router_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Stable IP address of the advertising router.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>neighbor</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Neighbor IP address.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>neighbor_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identity (number/IP address) of neighbor.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Seconds between dead neighbor polling interval.</div>
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
                        <div>Neighbor priority.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parameters</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv2 specific parameters.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>abr_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>cisco</li>
                                    <li>ibm</li>
                                    <li>shortcut</li>
                                    <li>standard</li>
                        </ul>
                </td>
                <td>
                        <div>OSPFv2 ABR Type.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>opaque_lsa</b>
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
                        <div>Enable the Opaque-LSA capability (rfc2370).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rfc1583_compatibility</b>
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
                        <div>Enable rfc1583 criteria for handling AS external routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>router_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Override the default router identifier.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>passive_interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Suppress routing updates on an interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>passive_interface_exclude</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface to exclude when using passive-interface default.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>redistribute</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Redistribute information from another routing protocol.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>metric</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Metric for redistribution routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>metric_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv2 Metric types.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route map references.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>bgp</li>
                                    <li>connected</li>
                                    <li>kernel</li>
                                    <li>rip</li>
                                    <li>static</li>
                        </ul>
                </td>
                <td>
                        <div>Route type to redistribute.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Filter routes installed in local route map.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timers</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Adjust routing timers.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>refresh</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Adjust refresh parameters.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timers</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>refresh timer.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>throttle</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Throttling adaptive timers.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>spf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OSPFv2 SPF timers.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>delay</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Delay (msec) from first change received till SPF calculation.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>initial_holdtime</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Initial hold time(msec) between consecutive SPF calculations.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_holdtime</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>maximum hold time (sec).</div>
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
                        <div>The value of this option should be the output received from the VyOS device by executing the command <b>show configuration commands | grep ospf</b>.</div>
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
                                    <li>deleted</li>
                                    <li>parsed</li>
                                    <li>gathered</li>
                                    <li>rendered</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in.</div>
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
    # vyos@vyos# run show  configuration commands | grep ospf
    #
    #
    - name: Merge the provided configuration with the existing running configuration
      vyos.vyos.vyos_ospfv2:
        config:
          log_adjacency_changes: detail
          max_metric:
            router_lsa:
              administrative: true
              on_shutdown: 10
              on_startup: 10
            default_information:
              originate:
                always: true
                metric: 10
                metric_type: 2
                route_map: ingress
            mpls_te:
              enabled: true
              router_address: 192.0.11.11
            auto_cost:
              reference_bandwidth: 2
            neighbor:
            - neighbor_id: 192.0.11.12
              poll_interval: 10
              priority: 2
            redistribute:
            - route_type: bgp
              metric: 10
              metric_type: 2
            passive_interface:
            - eth1
            - eth2
            parameters:
              router_id: 192.0.1.1
              opaque_lsa: true
              rfc1583_compatibility: true
              abr_type: cisco
            areas:
            - area_id: '2'
              area_type:
                normal: true
                authentication: plaintext-password
                shortcut: enable
            - area_id: '3'
              area_type:
                nssa:
                  set: true
            - area_id: '4'
              area_type:
                stub:
                  default_cost: 20
              network:
              - address: 192.0.2.0/24
              range:
              - address: 192.0.3.0/24
                cost: 10
              - address: 192.0.4.0/24
              cost: 12
        state: merged
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    # before": {}
    #
    #    "commands": [
    #       "set protocols ospf mpls-te enable",
    #       "set protocols ospf mpls-te router-address '192.0.11.11'",
    #       "set protocols ospf redistribute bgp",
    #       "set protocols ospf redistribute bgp metric-type 2",
    #       "set protocols ospf redistribute bgp metric 10",
    #       "set protocols ospf default-information originate metric-type 2",
    #       "set protocols ospf default-information originate always",
    #       "set protocols ospf default-information originate metric 10",
    #       "set protocols ospf default-information originate route-map ingress",
    #       "set protocols ospf auto-cost reference-bandwidth '2'",
    #       "set protocols ospf parameters router-id '192.0.1.1'",
    #       "set protocols ospf parameters opaque-lsa",
    #       "set protocols ospf parameters abr-type 'cisco'",
    #       "set protocols ospf parameters rfc1583-compatibility",
    #       "set protocols ospf passive-interface eth1",
    #       "set protocols ospf passive-interface eth2",
    #       "set protocols ospf max-metric router-lsa on-shutdown 10",
    #       "set protocols ospf max-metric router-lsa administrative",
    #       "set protocols ospf max-metric router-lsa on-startup 10",
    #       "set protocols ospf log-adjacency-changes 'detail'",
    #       "set protocols ospf neighbor 192.0.11.12 priority 2",
    #       "set protocols ospf neighbor 192.0.11.12 poll-interval 10",
    #       "set protocols ospf neighbor 192.0.11.12",
    #       "set protocols ospf area '2'",
    #       "set protocols ospf area 2 authentication plaintext-password",
    #       "set protocols ospf area 2 shortcut enable",
    #       "set protocols ospf area 2 area-type normal",
    #       "set protocols ospf area '3'",
    #       "set protocols ospf area 3 area-type nssa",
    #       "set protocols ospf area 4 range 192.0.3.0/24 cost 10",
    #       "set protocols ospf area 4 range 192.0.3.0/24",
    #       "set protocols ospf area 4 range 192.0.4.0/24 cost 12",
    #       "set protocols ospf area 4 range 192.0.4.0/24",
    #       "set protocols ospf area 4 area-type stub default-cost 20",
    #       "set protocols ospf area '4'",
    #       "set protocols ospf area 4 network 192.0.2.0/24"
    #    ]
    #
    # "after": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "area_type": {
    #                    "normal": true
    #                },
    #                "authentication": "plaintext-password",
    #                "shortcut": "enable"
    #            },
    #            {
    #                "area_id": "3",
    #                "area_type": {
    #                    "nssa": {
    #                        "set": true
    #                    }
    #                }
    #            },
    #            {
    #                "area_id": "4",
    #                "area_type": {
    #                    "stub": {
    #                        "default_cost": 20,
    #                        "set": true
    #                    }
    #                },
    #                "network": [
    #                    {
    #                        "address": "192.0.2.0/24"
    #                    }
    #                ],
    #                "range": [
    #                    {
    #                        "address": "192.0.3.0/24",
    #                        "cost": 10
    #                    },
    #                    {
    #                        "address": "192.0.4.0/24",
    #                        "cost": 12
    #                    }
    #                ]
    #            }
    #        ],
    #        "auto_cost": {
    #            "reference_bandwidth": 2
    #        },
    #        "default_information": {
    #            "originate": {
    #                "always": true,
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_map": "ingress"
    #            }
    #        },
    #        "log_adjacency_changes": "detail",
    #        "max_metric": {
    #            "router_lsa": {
    #                "administrative": true,
    #                "on_shutdown": 10,
    #                "on_startup": 10
    #            }
    #        },
    #        "mpls_te": {
    #            "enabled": true,
    #            "router_address": "192.0.11.11"
    #        },
    #        "neighbor": [
    #            {
    #                "neighbor_id": "192.0.11.12",
    #                "poll_interval": 10,
    #                "priority": 2
    #            }
    #        ],
    #        "parameters": {
    #            "abr_type": "cisco",
    #            "opaque_lsa": true,
    #            "rfc1583_compatibility": true,
    #            "router_id": "192.0.1.1"
    #        },
    #        "passive_interface": [
    #            "eth2",
    #            "eth1"
    #        ],
    #        "redistribute": [
    #            {
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    #
    # After state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospf
    # set protocols ospf area 2 area-type 'normal'
    # set protocols ospf area 2 authentication 'plaintext-password'
    # set protocols ospf area 2 shortcut 'enable'
    # set protocols ospf area 3 area-type 'nssa'
    # set protocols ospf area 4 area-type stub default-cost '20'
    # set protocols ospf area 4 network '192.0.2.0/24'
    # set protocols ospf area 4 range 192.0.3.0/24 cost '10'
    # set protocols ospf area 4 range 192.0.4.0/24 cost '12'
    # set protocols ospf auto-cost reference-bandwidth '2'
    # set protocols ospf default-information originate 'always'
    # set protocols ospf default-information originate metric '10'
    # set protocols ospf default-information originate metric-type '2'
    # set protocols ospf default-information originate route-map 'ingress'
    # set protocols ospf log-adjacency-changes 'detail'
    # set protocols ospf max-metric router-lsa 'administrative'
    # set protocols ospf max-metric router-lsa on-shutdown '10'
    # set protocols ospf max-metric router-lsa on-startup '10'
    # set protocols ospf mpls-te 'enable'
    # set protocols ospf mpls-te router-address '192.0.11.11'
    # set protocols ospf neighbor 192.0.11.12 poll-interval '10'
    # set protocols ospf neighbor 192.0.11.12 priority '2'
    # set protocols ospf parameters abr-type 'cisco'
    # set protocols ospf parameters 'opaque-lsa'
    # set protocols ospf parameters 'rfc1583-compatibility'
    # set protocols ospf parameters router-id '192.0.1.1'
    # set protocols ospf passive-interface 'eth1'
    # set protocols ospf passive-interface 'eth2'
    # set protocols ospf redistribute bgp metric '10'
    # set protocols ospf redistribute bgp metric-type '2'


    # Using merged
    #
    # Before state:
    # -------------
    #
    # vyos@vyos# run show  configuration commands | grep ospf
    #
    #
    - name: Merge the provided configuration to update existing running configuration
      vyos.vyos.vyos_ospfv2:
        config:
          areas:
          - area_id: '2'
            area_type:
              normal: true
            authentication: plaintext-password
            shortcut: enable
          - area_id: '3'
            area_type:
              nssa:
                set: false
          - area_id: '4'
            area_type:
              stub:
                default_cost: 20
            network:
            - address: 192.0.2.0/24
            - address: 192.0.22.0/24
            - address: 192.0.32.0/24
        state: merged
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    # "before": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "area_type": {
    #                    "normal": true
    #                },
    #                "authentication": "plaintext-password",
    #                "shortcut": "enable"
    #            },
    #            {
    #                "area_id": "3",
    #                "area_type": {
    #                    "nssa": {
    #                        "set": true
    #                    }
    #                }
    #            },
    #            {
    #                "area_id": "4",
    #                "area_type": {
    #                    "stub": {
    #                        "default_cost": 20,
    #                        "set": true
    #                    }
    #                },
    #                "network": [
    #                    {
    #                        "address": "192.0.2.0/24"
    #                    }
    #                ],
    #                "range": [
    #                    {
    #                        "address": "192.0.3.0/24",
    #                        "cost": 10
    #                    },
    #                    {
    #                        "address": "192.0.4.0/24",
    #                        "cost": 12
    #                    }
    #                ]
    #            }
    #        ],
    #        "auto_cost": {
    #            "reference_bandwidth": 2
    #        },
    #        "default_information": {
    #            "originate": {
    #                "always": true,
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_map": "ingress"
    #            }
    #        },
    #        "log_adjacency_changes": "detail",
    #        "max_metric": {
    #            "router_lsa": {
    #                "administrative": true,
    #                "on_shutdown": 10,
    #                "on_startup": 10
    #            }
    #        },
    #        "mpls_te": {
    #            "enabled": true,
    #            "router_address": "192.0.11.11"
    #        },
    #        "neighbor": [
    #            {
    #                "neighbor_id": "192.0.11.12",
    #                "poll_interval": 10,
    #                "priority": 2
    #            }
    #        ],
    #        "parameters": {
    #            "abr_type": "cisco",
    #            "opaque_lsa": true,
    #            "rfc1583_compatibility": true,
    #            "router_id": "192.0.1.1"
    #        },
    #        "passive_interface": [
    #            "eth2",
    #            "eth1"
    #        ],
    #        "redistribute": [
    #            {
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    #
    #    "commands": [
    #       "delete protocols ospf area 4 area-type stub",
    #       "set protocols ospf area 4 network 192.0.22.0/24"
    #       "set protocols ospf area 4 network 192.0.32.0/24"
    #    ]
    #
    # "after": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "area_type": {
    #                    "normal": true
    #                },
    #                "authentication": "plaintext-password",
    #                "shortcut": "enable"
    #            },
    #            {
    #                "area_id": "3",
    #                "area_type": {
    #                    "nssa": {
    #                        "set": true
    #                    }
    #                }
    #            },
    #            {
    #                "area_id": "4",
    #                },
    #                "network": [
    #                    {
    #                        "address": "192.0.2.0/24"
    #                    },
    #                    {
    #                        "address": "192.0.22.0/24"
    #                    },
    #                    {
    #                        "address": "192.0.32.0/24"
    #                    }
    #                ],
    #                "range": [
    #                    {
    #                        "address": "192.0.3.0/24",
    #                        "cost": 10
    #                    },
    #                    {
    #                        "address": "192.0.4.0/24",
    #                        "cost": 12
    #                    }
    #                ]
    #            }
    #        ],
    #        "auto_cost": {
    #            "reference_bandwidth": 2
    #        },
    #        "default_information": {
    #            "originate": {
    #                "always": true,
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_map": "ingress"
    #            }
    #        },
    #        "log_adjacency_changes": "detail",
    #        "max_metric": {
    #            "router_lsa": {
    #                "administrative": true,
    #                "on_shutdown": 10,
    #                "on_startup": 10
    #            }
    #        },
    #        "mpls_te": {
    #            "enabled": true,
    #            "router_address": "192.0.11.11"
    #        },
    #        "neighbor": [
    #            {
    #                "neighbor_id": "192.0.11.12",
    #                "poll_interval": 10,
    #                "priority": 2
    #            }
    #        ],
    #        "parameters": {
    #            "abr_type": "cisco",
    #            "opaque_lsa": true,
    #            "rfc1583_compatibility": true,
    #            "router_id": "192.0.1.1"
    #        },
    #        "passive_interface": [
    #            "eth2",
    #            "eth1"
    #        ],
    #        "redistribute": [
    #            {
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    #
    # After state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospf
    # set protocols ospf area 2 area-type 'normal'
    # set protocols ospf area 2 authentication 'plaintext-password'
    # set protocols ospf area 2 shortcut 'enable'
    # set protocols ospf area 3 area-type 'nssa'
    # set protocols ospf area 4 network '192.0.2.0/24'
    # set protocols ospf area 4 network '192.0.22.0/24'
    # set protocols ospf area 4 network '192.0.32.0/24'
    # set protocols ospf area 4 range 192.0.3.0/24 cost '10'
    # set protocols ospf area 4 range 192.0.4.0/24 cost '12'
    # set protocols ospf auto-cost reference-bandwidth '2'
    # set protocols ospf default-information originate 'always'
    # set protocols ospf default-information originate metric '10'
    # set protocols ospf default-information originate metric-type '2'
    # set protocols ospf default-information originate route-map 'ingress'
    # set protocols ospf log-adjacency-changes 'detail'
    # set protocols ospf max-metric router-lsa 'administrative'
    # set protocols ospf max-metric router-lsa on-shutdown '10'
    # set protocols ospf max-metric router-lsa on-startup '10'
    # set protocols ospf mpls-te 'enable'
    # set protocols ospf mpls-te router-address '192.0.11.11'
    # set protocols ospf neighbor 192.0.11.12 poll-interval '10'
    # set protocols ospf neighbor 192.0.11.12 priority '2'
    # set protocols ospf parameters abr-type 'cisco'
    # set protocols ospf parameters 'opaque-lsa'
    # set protocols ospf parameters 'rfc1583-compatibility'
    # set protocols ospf parameters router-id '192.0.1.1'
    # set protocols ospf passive-interface 'eth1'
    # set protocols ospf passive-interface 'eth2'
    # set protocols ospf redistribute bgp metric '10'
    # set protocols ospf redistribute bgp metric-type '2'


    # Using replaced
    #
    # Before state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospf
    # set protocols ospf area 2 area-type 'normal'
    # set protocols ospf area 2 authentication 'plaintext-password'
    # set protocols ospf area 2 shortcut 'enable'
    # set protocols ospf area 3 area-type 'nssa'
    # set protocols ospf area 4 area-type stub default-cost '20'
    # set protocols ospf area 4 network '192.0.2.0/24'
    # set protocols ospf area 4 range 192.0.3.0/24 cost '10'
    # set protocols ospf area 4 range 192.0.4.0/24 cost '12'
    # set protocols ospf auto-cost reference-bandwidth '2'
    # set protocols ospf default-information originate 'always'
    # set protocols ospf default-information originate metric '10'
    # set protocols ospf default-information originate metric-type '2'
    # set protocols ospf default-information originate route-map 'ingress'
    # set protocols ospf log-adjacency-changes 'detail'
    # set protocols ospf max-metric router-lsa 'administrative'
    # set protocols ospf max-metric router-lsa on-shutdown '10'
    # set protocols ospf max-metric router-lsa on-startup '10'
    # set protocols ospf mpls-te 'enable'
    # set protocols ospf mpls-te router-address '192.0.11.11'
    # set protocols ospf neighbor 192.0.11.12 poll-interval '10'
    # set protocols ospf neighbor 192.0.11.12 priority '2'
    # set protocols ospf parameters abr-type 'cisco'
    # set protocols ospf parameters 'opaque-lsa'
    # set protocols ospf parameters 'rfc1583-compatibility'
    # set protocols ospf parameters router-id '192.0.1.1'
    # set protocols ospf passive-interface 'eth1'
    # set protocols ospf passive-interface 'eth2'
    # set protocols ospf redistribute bgp metric '10'
    # set protocols ospf redistribute bgp metric-type '2'
    #
    - name: Replace ospfv2 routes attributes configuration.
      vyos.vyos.vyos_ospfv2:
        config:
          log_adjacency_changes: detail
          max_metric:
            router_lsa:
              administrative: true
              on_shutdown: 10
              on_startup: 10
            default_information:
              originate:
                always: true
                metric: 10
                metric_type: 2
                route_map: ingress
            mpls_te:
              enabled: true
              router_address: 192.0.22.22
            auto_cost:
              reference_bandwidth: 2
            neighbor:
            - neighbor_id: 192.0.11.12
              poll_interval: 10
              priority: 2
            redistribute:
            - route_type: bgp
              metric: 10
              metric_type: 2
            passive_interface:
            - eth1
            parameters:
              router_id: 192.0.1.1
              opaque_lsa: true
              rfc1583_compatibility: true
              abr_type: cisco
            areas:
            - area_id: '2'
              area_type:
                normal: true
              authentication: plaintext-password
              shortcut: enable
            - area_id: '4'
              area_type:
                stub:
                  default_cost: 20
              network:
              - address: 192.0.2.0/24
              - address: 192.0.12.0/24
              - address: 192.0.22.0/24
              - address: 192.0.32.0/24
              range:
              - address: 192.0.42.0/24
                cost: 10
        state: replaced
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #    "before": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "area_type": {
    #                    "normal": true
    #                },
    #                "authentication": "plaintext-password",
    #                "shortcut": "enable"
    #            },
    #            {
    #                "area_id": "3",
    #                "area_type": {
    #                    "nssa": {
    #                        "set": true
    #                    }
    #                }
    #            },
    #            {
    #                "area_id": "4",
    #                "area_type": {
    #                    "stub": {
    #                        "default_cost": 20,
    #                        "set": true
    #                    }
    #                },
    #                "network": [
    #                    {
    #                        "address": "192.0.2.0/24"
    #                    }
    #                ],
    #                "range": [
    #                    {
    #                        "address": "192.0.3.0/24",
    #                        "cost": 10
    #                    },
    #                    {
    #                        "address": "192.0.4.0/24",
    #                        "cost": 12
    #                    }
    #                ]
    #            }
    #        ],
    #        "auto_cost": {
    #            "reference_bandwidth": 2
    #        },
    #        "default_information": {
    #            "originate": {
    #                "always": true,
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_map": "ingress"
    #            }
    #        },
    #        "log_adjacency_changes": "detail",
    #        "max_metric": {
    #            "router_lsa": {
    #                "administrative": true,
    #                "on_shutdown": 10,
    #                "on_startup": 10
    #            }
    #        },
    #        "mpls_te": {
    #            "enabled": true,
    #            "router_address": "192.0.11.11"
    #        },
    #        "neighbor": [
    #            {
    #                "neighbor_id": "192.0.11.12",
    #                "poll_interval": 10,
    #                "priority": 2
    #            }
    #        ],
    #        "parameters": {
    #            "abr_type": "cisco",
    #            "opaque_lsa": true,
    #            "rfc1583_compatibility": true,
    #            "router_id": "192.0.1.1"
    #        },
    #        "passive_interface": [
    #            "eth2",
    #            "eth1"
    #        ],
    #        "redistribute": [
    #            {
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    #
    # "commands": [
    #     "delete protocols ospf passive-interface eth2",
    #     "delete protocols ospf area 3",
    #     "delete protocols ospf area 4 range 192.0.3.0/24 cost",
    #     "delete protocols ospf area 4 range 192.0.3.0/24",
    #     "delete protocols ospf area 4 range 192.0.4.0/24 cost",
    #     "delete protocols ospf area 4 range 192.0.4.0/24",
    #     "set protocols ospf mpls-te router-address '192.0.22.22'",
    #     "set protocols ospf area 4 range 192.0.42.0/24 cost 10",
    #     "set protocols ospf area 4 range 192.0.42.0/24",
    #     "set protocols ospf area 4 network 192.0.12.0/24",
    #     "set protocols ospf area 4 network 192.0.22.0/24",
    #     "set protocols ospf area 4 network 192.0.32.0/24"
    #    ]
    #
    #    "after": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "area_type": {
    #                    "normal": true
    #                },
    #                "authentication": "plaintext-password",
    #                "shortcut": "enable"
    #            },
    #            {
    #                "area_id": "4",
    #                "area_type": {
    #                    "stub": {
    #                        "default_cost": 20,
    #                        "set": true
    #                    }
    #                },
    #                "network": [
    #                    {
    #                        "address": "192.0.12.0/24"
    #                    },
    #                    {
    #                        "address": "192.0.2.0/24"
    #                    },
    #                    {
    #                        "address": "192.0.22.0/24"
    #                    },
    #                    {
    #                        "address": "192.0.32.0/24"
    #                    }
    #                ],
    #                "range": [
    #                    {
    #                        "address": "192.0.42.0/24",
    #                        "cost": 10
    #                    }
    #                ]
    #            }
    #        ],
    #        "auto_cost": {
    #            "reference_bandwidth": 2
    #        },
    #        "default_information": {
    #            "originate": {
    #                "always": true,
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_map": "ingress"
    #            }
    #        },
    #        "log_adjacency_changes": "detail",
    #        "max_metric": {
    #            "router_lsa": {
    #                "administrative": true,
    #                "on_shutdown": 10,
    #                "on_startup": 10
    #            }
    #        },
    #        "mpls_te": {
    #            "enabled": true,
    #            "router_address": "192.0.22.22"
    #        },
    #        "neighbor": [
    #            {
    #                "neighbor_id": "192.0.11.12",
    #                "poll_interval": 10,
    #                "priority": 2
    #            }
    #        ],
    #        "parameters": {
    #            "abr_type": "cisco",
    #            "opaque_lsa": true,
    #            "rfc1583_compatibility": true,
    #            "router_id": "192.0.1.1"
    #        },
    #        "passive_interface": [
    #            "eth1"
    #        ],
    #        "redistribute": [
    #            {
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    #
    # After state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospf
    # set protocols ospf area 2 area-type 'normal'
    # set protocols ospf area 2 authentication 'plaintext-password'
    # set protocols ospf area 2 shortcut 'enable'
    # set protocols ospf area 4 area-type stub default-cost '20'
    # set protocols ospf area 4 network '192.0.2.0/24'
    # set protocols ospf area 4 network '192.0.12.0/24'
    # set protocols ospf area 4 network '192.0.22.0/24'
    # set protocols ospf area 4 network '192.0.32.0/24'
    # set protocols ospf area 4 range 192.0.42.0/24 cost '10'
    # set protocols ospf auto-cost reference-bandwidth '2'
    # set protocols ospf default-information originate 'always'
    # set protocols ospf default-information originate metric '10'
    # set protocols ospf default-information originate metric-type '2'
    # set protocols ospf default-information originate route-map 'ingress'
    # set protocols ospf log-adjacency-changes 'detail'
    # set protocols ospf max-metric router-lsa 'administrative'
    # set protocols ospf max-metric router-lsa on-shutdown '10'
    # set protocols ospf max-metric router-lsa on-startup '10'
    # set protocols ospf mpls-te 'enable'
    # set protocols ospf mpls-te router-address '192.0.22.22'
    # set protocols ospf neighbor 192.0.11.12 poll-interval '10'
    # set protocols ospf neighbor 192.0.11.12 priority '2'
    # set protocols ospf parameters abr-type 'cisco'
    # set protocols ospf parameters 'opaque-lsa'
    # set protocols ospf parameters 'rfc1583-compatibility'
    # set protocols ospf parameters router-id '192.0.1.1'
    # set protocols ospf passive-interface 'eth1'
    # set protocols ospf redistribute bgp metric '10'
    # set protocols ospf redistribute bgp metric-type '2'


    # Using rendered
    #
    #
    - name: Render the commands for provided  configuration
      vyos.vyos.vyos_ospfv2:
        config:
          log_adjacency_changes: detail
          max_metric:
            router_lsa:
              administrative: true
              on_shutdown: 10
              on_startup: 10
            default_information:
              originate:
                always: true
                metric: 10
                metric_type: 2
                route_map: ingress
            mpls_te:
              enabled: true
              router_address: 192.0.11.11
            auto_cost:
              reference_bandwidth: 2
            neighbor:
            - neighbor_id: 192.0.11.12
              poll_interval: 10
              priority: 2
            redistribute:
            - route_type: bgp
              metric: 10
              metric_type: 2
            passive_interface:
            - eth1
            - eth2
            parameters:
              router_id: 192.0.1.1
              opaque_lsa: true
              rfc1583_compatibility: true
              abr_type: cisco
            areas:
            - area_id: '2'
              area_type:
                normal: true
              authentication: plaintext-password
              shortcut: enable
            - area_id: '3'
              area_type:
                nssa:
                  set: true
            - area_id: '4'
              area_type:
                stub:
                  default_cost: 20
              network:
              - address: 192.0.2.0/24
              range:
              - address: 192.0.3.0/24
                cost: 10
              - address: 192.0.4.0/24
                cost: 12
        state: rendered
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #
    # "rendered": [
    #        [
    #       "set protocols ospf mpls-te enable",
    #       "set protocols ospf mpls-te router-address '192.0.11.11'",
    #       "set protocols ospf redistribute bgp",
    #       "set protocols ospf redistribute bgp metric-type 2",
    #       "set protocols ospf redistribute bgp metric 10",
    #       "set protocols ospf default-information originate metric-type 2",
    #       "set protocols ospf default-information originate always",
    #       "set protocols ospf default-information originate metric 10",
    #       "set protocols ospf default-information originate route-map ingress",
    #       "set protocols ospf auto-cost reference-bandwidth '2'",
    #       "set protocols ospf parameters router-id '192.0.1.1'",
    #       "set protocols ospf parameters opaque-lsa",
    #       "set protocols ospf parameters abr-type 'cisco'",
    #       "set protocols ospf parameters rfc1583-compatibility",
    #       "set protocols ospf passive-interface eth1",
    #       "set protocols ospf passive-interface eth2",
    #       "set protocols ospf max-metric router-lsa on-shutdown 10",
    #       "set protocols ospf max-metric router-lsa administrative",
    #       "set protocols ospf max-metric router-lsa on-startup 10",
    #       "set protocols ospf log-adjacency-changes 'detail'",
    #       "set protocols ospf neighbor 192.0.11.12 priority 2",
    #       "set protocols ospf neighbor 192.0.11.12 poll-interval 10",
    #       "set protocols ospf neighbor 192.0.11.12",
    #       "set protocols ospf area '2'",
    #       "set protocols ospf area 2 authentication plaintext-password",
    #       "set protocols ospf area 2 shortcut enable",
    #       "set protocols ospf area 2 area-type normal",
    #       "set protocols ospf area '3'",
    #       "set protocols ospf area 3 area-type nssa",
    #       "set protocols ospf area 4 range 192.0.3.0/24 cost 10",
    #       "set protocols ospf area 4 range 192.0.3.0/24",
    #       "set protocols ospf area 4 range 192.0.4.0/24 cost 12",
    #       "set protocols ospf area 4 range 192.0.4.0/24",
    #       "set protocols ospf area 4 area-type stub default-cost 20",
    #       "set protocols ospf area '4'",
    #       "set protocols ospf area 4 network 192.0.2.0/24"
    #    ]


    # Using parsed
    #
    #
    - name: Parse the commands for provided  structured configuration
      vyos.vyos.vyos_ospfv2:
        running_config:
          "set protocols ospf area 2 area-type 'normal'
           set protocols ospf area 2 authentication 'plaintext-password'
           set protocols ospf area 2 shortcut 'enable'
           set protocols ospf area 3 area-type 'nssa'
           set protocols ospf area 4 area-type stub default-cost '20'
           set protocols ospf area 4 network '192.0.2.0/24'
           set protocols ospf area 4 range 192.0.3.0/24 cost '10'
           set protocols ospf area 4 range 192.0.4.0/24 cost '12'
           set protocols ospf auto-cost reference-bandwidth '2'
           set protocols ospf default-information originate 'always'
           set protocols ospf default-information originate metric '10'
           set protocols ospf default-information originate metric-type '2'
           set protocols ospf default-information originate route-map 'ingress'
           set protocols ospf log-adjacency-changes 'detail'
           set protocols ospf max-metric router-lsa 'administrative'
           set protocols ospf max-metric router-lsa on-shutdown '10'
           set protocols ospf max-metric router-lsa on-startup '10'
           set protocols ospf mpls-te 'enable'
           set protocols ospf mpls-te router-address '192.0.11.11'
           set protocols ospf neighbor 192.0.11.12 poll-interval '10'
           set protocols ospf neighbor 192.0.11.12 priority '2'
           set protocols ospf parameters abr-type 'cisco'
           set protocols ospf parameters 'opaque-lsa'
           set protocols ospf parameters 'rfc1583-compatibility'
           set protocols ospf parameters router-id '192.0.1.1'
           set protocols ospf passive-interface 'eth1'
           set protocols ospf passive-interface 'eth2'
           set protocols ospf redistribute bgp metric '10'
           set protocols ospf redistribute bgp metric-type '2'"
        state: parsed
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #
    # "parsed": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "area_type": {
    #                    "normal": true
    #                },
    #                "authentication": "plaintext-password",
    #                "shortcut": "enable"
    #            },
    #            {
    #                "area_id": "3",
    #                "area_type": {
    #                    "nssa": {
    #                        "set": true
    #                    }
    #                }
    #            },
    #            {
    #                "area_id": "4",
    #                "area_type": {
    #                    "stub": {
    #                        "default_cost": 20,
    #                        "set": true
    #                    }
    #                },
    #                "network": [
    #                    {
    #                        "address": "192.0.2.0/24"
    #                    }
    #                ],
    #                "range": [
    #                    {
    #                        "address": "192.0.3.0/24",
    #                        "cost": 10
    #                    },
    #                    {
    #                        "address": "192.0.4.0/24",
    #                        "cost": 12
    #                    }
    #                ]
    #            }
    #        ],
    #        "auto_cost": {
    #            "reference_bandwidth": 2
    #        },
    #        "default_information": {
    #            "originate": {
    #                "always": true,
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_map": "ingress"
    #            }
    #        },
    #        "log_adjacency_changes": "detail",
    #        "max_metric": {
    #            "router_lsa": {
    #                "administrative": true,
    #                "on_shutdown": 10,
    #                "on_startup": 10
    #            }
    #        },
    #        "mpls_te": {
    #            "enabled": true,
    #            "router_address": "192.0.11.11"
    #        },
    #        "neighbor": [
    #            {
    #                "neighbor_id": "192.0.11.12",
    #                "poll_interval": 10,
    #                "priority": 2
    #            }
    #        ],
    #        "parameters": {
    #            "abr_type": "cisco",
    #            "opaque_lsa": true,
    #            "rfc1583_compatibility": true,
    #            "router_id": "192.0.1.1"
    #        },
    #        "passive_interface": [
    #            "eth2",
    #            "eth1"
    #        ],
    #        "redistribute": [
    #            {
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    # }


    # Using gathered
    #
    # Before state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospf
    # set protocols ospf area 2 area-type 'normal'
    # set protocols ospf area 2 authentication 'plaintext-password'
    # set protocols ospf area 2 shortcut 'enable'
    # set protocols ospf area 3 area-type 'nssa'
    # set protocols ospf area 4 area-type stub default-cost '20'
    # set protocols ospf area 4 network '192.0.2.0/24'
    # set protocols ospf area 4 range 192.0.3.0/24 cost '10'
    # set protocols ospf area 4 range 192.0.4.0/24 cost '12'
    # set protocols ospf auto-cost reference-bandwidth '2'
    # set protocols ospf default-information originate 'always'
    # set protocols ospf default-information originate metric '10'
    # set protocols ospf default-information originate metric-type '2'
    # set protocols ospf default-information originate route-map 'ingress'
    # set protocols ospf log-adjacency-changes 'detail'
    # set protocols ospf max-metric router-lsa 'administrative'
    # set protocols ospf max-metric router-lsa on-shutdown '10'
    # set protocols ospf max-metric router-lsa on-startup '10'
    # set protocols ospf mpls-te 'enable'
    # set protocols ospf mpls-te router-address '192.0.11.11'
    # set protocols ospf neighbor 192.0.11.12 poll-interval '10'
    # set protocols ospf neighbor 192.0.11.12 priority '2'
    # set protocols ospf parameters abr-type 'cisco'
    # set protocols ospf parameters 'opaque-lsa'
    # set protocols ospf parameters 'rfc1583-compatibility'
    # set protocols ospf parameters router-id '192.0.1.1'
    # set protocols ospf passive-interface 'eth1'
    # set protocols ospf passive-interface 'eth2'
    # set protocols ospf redistribute bgp metric '10'
    # set protocols ospf redistribute bgp metric-type '2'
    #
    - name: Gather ospfv2 routes config with provided configurations
      vyos.vyos.vyos_ospfv2:
        config:
        state: gathered
    #
    #
    # -------------------------
    # Module Execution Result
    # -------------------------
    #
    #    "gathered": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "area_type": {
    #                    "normal": true
    #                },
    #                "authentication": "plaintext-password",
    #                "shortcut": "enable"
    #            },
    #            {
    #                "area_id": "3",
    #                "area_type": {
    #                    "nssa": {
    #                        "set": true
    #                    }
    #                }
    #            },
    #            {
    #                "area_id": "4",
    #                "area_type": {
    #                    "stub": {
    #                        "default_cost": 20,
    #                        "set": true
    #                    }
    #                },
    #                "network": [
    #                    {
    #                        "address": "192.0.2.0/24"
    #                    }
    #                ],
    #                "range": [
    #                    {
    #                        "address": "192.0.3.0/24",
    #                        "cost": 10
    #                    },
    #                    {
    #                        "address": "192.0.4.0/24",
    #                        "cost": 12
    #                    }
    #                ]
    #            }
    #        ],
    #        "auto_cost": {
    #            "reference_bandwidth": 2
    #        },
    #        "default_information": {
    #            "originate": {
    #                "always": true,
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_map": "ingress"
    #            }
    #        },
    #        "log_adjacency_changes": "detail",
    #        "max_metric": {
    #            "router_lsa": {
    #                "administrative": true,
    #                "on_shutdown": 10,
    #                "on_startup": 10
    #            }
    #        },
    #        "mpls_te": {
    #            "enabled": true,
    #            "router_address": "192.0.11.11"
    #        },
    #        "neighbor": [
    #            {
    #                "neighbor_id": "192.0.11.12",
    #                "poll_interval": 10,
    #                "priority": 2
    #            }
    #        ],
    #        "parameters": {
    #            "abr_type": "cisco",
    #            "opaque_lsa": true,
    #            "rfc1583_compatibility": true,
    #            "router_id": "192.0.1.1"
    #        },
    #        "passive_interface": [
    #            "eth2",
    #            "eth1"
    #        ],
    #        "redistribute": [
    #            {
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    #
    # After state:
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospf
    # set protocols ospf area 2 area-type 'normal'
    # set protocols ospf area 2 authentication 'plaintext-password'
    # set protocols ospf area 2 shortcut 'enable'
    # set protocols ospf area 3 area-type 'nssa'
    # set protocols ospf area 4 area-type stub default-cost '20'
    # set protocols ospf area 4 network '192.0.2.0/24'
    # set protocols ospf area 4 range 192.0.3.0/24 cost '10'
    # set protocols ospf area 4 range 192.0.4.0/24 cost '12'
    # set protocols ospf auto-cost reference-bandwidth '2'
    # set protocols ospf default-information originate 'always'
    # set protocols ospf default-information originate metric '10'
    # set protocols ospf default-information originate metric-type '2'
    # set protocols ospf default-information originate route-map 'ingress'
    # set protocols ospf log-adjacency-changes 'detail'
    # set protocols ospf max-metric router-lsa 'administrative'
    # set protocols ospf max-metric router-lsa on-shutdown '10'
    # set protocols ospf max-metric router-lsa on-startup '10'
    # set protocols ospf mpls-te 'enable'
    # set protocols ospf mpls-te router-address '192.0.11.11'
    # set protocols ospf neighbor 192.0.11.12 poll-interval '10'
    # set protocols ospf neighbor 192.0.11.12 priority '2'
    # set protocols ospf parameters abr-type 'cisco'
    # set protocols ospf parameters 'opaque-lsa'
    # set protocols ospf parameters 'rfc1583-compatibility'
    # set protocols ospf parameters router-id '192.0.1.1'
    # set protocols ospf passive-interface 'eth1'
    # set protocols ospf passive-interface 'eth2'
    # set protocols ospf redistribute bgp metric '10'
    # set protocols ospf redistribute bgp metric-type '2'


    # Using deleted
    #
    # Before state
    # -------------
    #
    # vyos@192# run show configuration commands | grep ospf
    # set protocols ospf area 2 area-type 'normal'
    # set protocols ospf area 2 authentication 'plaintext-password'
    # set protocols ospf area 2 shortcut 'enable'
    # set protocols ospf area 3 area-type 'nssa'
    # set protocols ospf area 4 area-type stub default-cost '20'
    # set protocols ospf area 4 network '192.0.2.0/24'
    # set protocols ospf area 4 range 192.0.3.0/24 cost '10'
    # set protocols ospf area 4 range 192.0.4.0/24 cost '12'
    # set protocols ospf auto-cost reference-bandwidth '2'
    # set protocols ospf default-information originate 'always'
    # set protocols ospf default-information originate metric '10'
    # set protocols ospf default-information originate metric-type '2'
    # set protocols ospf default-information originate route-map 'ingress'
    # set protocols ospf log-adjacency-changes 'detail'
    # set protocols ospf max-metric router-lsa 'administrative'
    # set protocols ospf max-metric router-lsa on-shutdown '10'
    # set protocols ospf max-metric router-lsa on-startup '10'
    # set protocols ospf mpls-te 'enable'
    # set protocols ospf mpls-te router-address '192.0.11.11'
    # set protocols ospf neighbor 192.0.11.12 poll-interval '10'
    # set protocols ospf neighbor 192.0.11.12 priority '2'
    # set protocols ospf parameters abr-type 'cisco'
    # set protocols ospf parameters 'opaque-lsa'
    # set protocols ospf parameters 'rfc1583-compatibility'
    # set protocols ospf parameters router-id '192.0.1.1'
    # set protocols ospf passive-interface 'eth1'
    # set protocols ospf passive-interface 'eth2'
    # set protocols ospf redistribute bgp metric '10'
    # set protocols ospf redistribute bgp metric-type '2'
    #
    - name: Delete attributes of ospfv2 routes.
      vyos.vyos.vyos_ospfv2:
        config:
        state: deleted
    #
    #
    # ------------------------
    # Module Execution Results
    # ------------------------
    #
    #    "before": {
    #        "areas": [
    #            {
    #                "area_id": "2",
    #                "area_type": {
    #                    "normal": true
    #                },
    #                "authentication": "plaintext-password",
    #                "shortcut": "enable"
    #            },
    #            {
    #                "area_id": "3",
    #                "area_type": {
    #                    "nssa": {
    #                        "set": true
    #                    }
    #                }
    #            },
    #            {
    #                "area_id": "4",
    #                "area_type": {
    #                    "stub": {
    #                        "default_cost": 20,
    #                        "set": true
    #                    }
    #                },
    #                "network": [
    #                    {
    #                        "address": "192.0.2.0/24"
    #                    }
    #                ],
    #                "range": [
    #                    {
    #                        "address": "192.0.3.0/24",
    #                        "cost": 10
    #                    },
    #                    {
    #                        "address": "192.0.4.0/24",
    #                        "cost": 12
    #                    }
    #                ]
    #            }
    #        ],
    #        "auto_cost": {
    #            "reference_bandwidth": 2
    #        },
    #        "default_information": {
    #            "originate": {
    #                "always": true,
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_map": "ingress"
    #            }
    #        },
    #        "log_adjacency_changes": "detail",
    #        "max_metric": {
    #            "router_lsa": {
    #                "administrative": true,
    #                "on_shutdown": 10,
    #                "on_startup": 10
    #            }
    #        },
    #        "mpls_te": {
    #            "enabled": true,
    #            "router_address": "192.0.11.11"
    #        },
    #        "neighbor": [
    #            {
    #                "neighbor_id": "192.0.11.12",
    #                "poll_interval": 10,
    #                "priority": 2
    #            }
    #        ],
    #        "parameters": {
    #            "abr_type": "cisco",
    #            "opaque_lsa": true,
    #            "rfc1583_compatibility": true,
    #            "router_id": "192.0.1.1"
    #        },
    #        "passive_interface": [
    #            "eth2",
    #            "eth1"
    #        ],
    #        "redistribute": [
    #            {
    #                "metric": 10,
    #                "metric_type": 2,
    #                "route_type": "bgp"
    #            }
    #        ]
    #    }
    # "commands": [
    #        "delete protocols ospf"
    #    ]
    #
    # "after": {}
    # After state
    # ------------
    # vyos@192# run show configuration commands | grep ospf
    #



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;set protocols ospf parameters router-id 192.0.1.1&#x27;, &quot;set protocols ospf passive-interface &#x27;eth1&#x27;&quot;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Rohit Thakur (@rohitthakur2590)
