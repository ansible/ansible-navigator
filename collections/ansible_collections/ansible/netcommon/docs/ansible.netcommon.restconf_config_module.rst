.. _ansible.netcommon.restconf_config_module:


*********************************
ansible.netcommon.restconf_config
*********************************

**Handles create, update, read and delete of configuration data on RESTCONF enabled devices.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- RESTCONF is a standard mechanisms to allow web applications to configure and manage data. RESTCONF is a IETF standard and documented on RFC 8040.
- This module allows the user to configure data on RESTCONF enabled devices.




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
                </td>
                <td>
                        <div>The configuration data in format as specififed in <code>format</code> option. Required unless <code>method</code> is <em>delete</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>format</b>
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
                        <div>The format of the configuration provided as value of <code>content</code>. Accepted values are <em>xml</em> and <em>json</em> and the given configuration format should be supported by remote RESTCONF server.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>method</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>post</b>&nbsp;&larr;</div></li>
                                    <li>put</li>
                                    <li>patch</li>
                                    <li>delete</li>
                        </ul>
                </td>
                <td>
                        <div>The RESTCONF method to manage the configuration change on device. The value <em>post</em> is used to create a data resource or invoke an operation resource, <em>put</em> is used to replace the target data resource, <em>patch</em> is used to modify the target resource, and <em>delete</em> is used to delete the target resource.</div>
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

    - name: create l3vpn services
      ansible.netcommon.restconf_config:
        path: /config/ietf-l3vpn-svc:l3vpn-svc/vpn-services
        content: |
          {
            "vpn-service":[
                            {
                              "vpn-id": "red_vpn2",
                              "customer-name": "blue",
                              "vpn-service-topology": "ietf-l3vpn-svc:any-to-any"
                            },
                            {
                              "vpn-id": "blue_vpn1",
                              "customer-name": "red",
                              "vpn-service-topology": "ietf-l3vpn-svc:any-to-any"
                            }
                          ]
           }



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
                    <b>candidate</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>When the method is not delete</td>
                <td>
                            <div>The configuration sent to the device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{
        &quot;vpn-service&quot;: [
            {
                &quot;customer-name&quot;: &quot;red&quot;,
                &quot;vpn-id&quot;: &quot;blue_vpn1&quot;,
                &quot;vpn-service-topology&quot;: &quot;ietf-l3vpn-svc:any-to-any&quot;
            }
        ]
    }</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>running</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>When the method is not delete</td>
                <td>
                            <div>The current running configuration on the device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{
        &quot;vpn-service&quot;: [
            {
              &quot;vpn-id&quot;: &quot;red_vpn2&quot;,
              &quot;customer-name&quot;: &quot;blue&quot;,
              &quot;vpn-service-topology&quot;: &quot;ietf-l3vpn-svc:any-to-any&quot;
            },
            {
              &quot;vpn-id&quot;: &quot;blue_vpn1&quot;,
              &quot;customer-name&quot;: &quot;red&quot;,
              &quot;vpn-service-topology&quot;: &quot;ietf-l3vpn-svc:any-to-any&quot;
            }
        ]
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
