.. _ansible.netcommon.restconf_get_module:


******************************
ansible.netcommon.restconf_get
******************************

**Fetch configuration/state data from RESTCONF enabled devices.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- RESTCONF is a standard mechanisms to allow web applications to access the configuration data and state data developed and standardized by the IETF. It is documented in RFC 8040.
- This module allows the user to fetch configuration and state data from RESTCONF enabled devices.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>content</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>config</li>
                                    <li>nonconfig</li>
                                    <li>all</li>
                        </ul>
                </td>
                <td>
                        <div>The <code>content</code> is a query parameter that controls how descendant nodes of the requested data nodes in <code>path</code> will be processed in the reply. If value is <em>config</em> return only configuration descendant data nodes of value in <code>path</code>. If value is <em>nonconfig</em> return only non-configuration descendant data nodes of value in <code>path</code>. If value is <em>all</em> return all descendant data nodes of value in <code>path</code></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>output</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>json</b>&nbsp;&larr;</div></li>
                                    <li>xml</li>
                        </ul>
                </td>
                <td>
                        <div>The output of response received.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>URI being used to execute API calls.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: get l3vpn services
      ansible.netcommon.restconf_get:
        path: /config/ietf-l3vpn-svc:l3vpn-svc/vpn-services



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
                    <b>response</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when the device response is valid JSON</td>
                <td>
                            <div>A dictionary representing a JSON-formatted response</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{
        &quot;vpn-services&quot;: {
            &quot;vpn-service&quot;: [
                {
                    &quot;customer-name&quot;: &quot;red&quot;,
                    &quot;vpn-id&quot;: &quot;blue_vpn1&quot;,
                    &quot;vpn-service-topology&quot;: &quot;ietf-l3vpn-svc:any-to-any&quot;
                }
            ]
        }
    }</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ganesh Nalawade (@ganeshrn)
