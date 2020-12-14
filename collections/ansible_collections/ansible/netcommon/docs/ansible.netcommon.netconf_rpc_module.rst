.. _ansible.netcommon.netconf_rpc_module:


*****************************
ansible.netcommon.netconf_rpc
*****************************

**Execute operations on NETCONF enabled network devices.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- NETCONF is a network management protocol developed and standardized by the IETF. It is documented in RFC 6241.
- This module allows the user to execute NETCONF RPC requests as defined by IETF RFC standards as well as proprietary requests.



Requirements
------------
The below requirements are needed on the host that executes this module.

- ncclient (>=v0.5.2)
- jxmlease


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
                        <div>This argument specifies the optional request content (all RPC attributes). The <em>content</em> value can either be provided as XML formatted string or as dictionary.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>display</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>json</li>
                                    <li>pretty</li>
                                    <li>xml</li>
                        </ul>
                </td>
                <td>
                        <div>Encoding scheme to use when serializing output from the device. The option <em>json</em> will serialize the output as JSON data. If the option value is <em>json</em> it requires jxmlease to be installed on control node. The option <em>pretty</em> is similar to received XML response but is using human readable format (spaces, new lines). The option value <em>xml</em> is similar to received XML response but removes all XML namespaces.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rpc</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This argument specifies the request (name of the operation) to be executed on the remote NETCONF enabled device.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>xmlns</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>NETCONF operations not defined in rfc6241 typically require the appropriate XML namespace to be set. In the case the <em>request</em> option is not already provided in XML format, the namespace can be defined by the <em>xmlns</em> option.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module requires the NETCONF system service be enabled on the remote device being managed.
   - This module supports the use of connection=netconf
   - To execute ``get-config``, ``get`` or ``edit-config`` requests it is recommended to use the Ansible *netconf_get* and *netconf_config* modules.
   - This module is supported on ``ansible_network_os`` network platforms. See the :ref:`Network Platform Options <platform_options>` for details.



Examples
--------

.. code-block:: yaml

    - name: lock candidate
      ansible.netcommon.netconf_rpc:
        rpc: lock
        content:
          target:
            candidate:

    - name: unlock candidate
      ansible.netcommon.netconf_rpc:
        rpc: unlock
        xmlns: urn:ietf:params:xml:ns:netconf:base:1.0
        content: "{'target': {'candidate': None}}"

    - name: discard changes
      ansible.netcommon.netconf_rpc:
        rpc: discard-changes

    - name: get-schema
      ansible.netcommon.netconf_rpc:
        rpc: get-schema
        xmlns: urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring
        content:
          identifier: ietf-netconf
          version: '2011-06-01'

    - name: copy running to startup
      ansible.netcommon.netconf_rpc:
        rpc: copy-config
        content:
          source:
            running:
          target:
            startup:

    - name: get schema list with JSON output
      ansible.netcommon.netconf_rpc:
        rpc: get
        content: |
          <filter>
            <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
              <schemas/>
            </netconf-state>
          </filter>
        display: json

    - name: get schema using XML request
      ansible.netcommon.netconf_rpc:
        rpc: get-schema
        xmlns: urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring
        content: |
          <identifier>ietf-netconf-monitoring</identifier>
          <version>2010-10-04</version>
        display: json



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>output</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">complex</span>
                    </div>
                </td>
                <td>when the display format is selected as JSON it is returned as dict type, if the display format is xml or pretty pretty it is returned as a string apart from low-level errors (such as action plugin).</td>
                <td>
                            <div>Based on the value of display option will return either the set of transformed XML to JSON format from the RPC response with type dict or pretty XML string response (human-readable) or response with namespace removed from XML string.</div>
                    <br/>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>formatted_output</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td></td>
                <td>
                            <div>Contains formatted response received from remote host as per the value in display format.</div>
                    <br/>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stdout</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>always apart from low-level errors (such as action plugin)</td>
                <td>
                            <div>The raw XML string containing configuration or state data received from the underlying ncclient library.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">...</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stdout_lines</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always apart from low-level errors (such as action plugin)</td>
                <td>
                            <div>The value of stdout split into a list</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;...&#x27;, &#x27;...&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ganesh Nalawade (@ganeshrn)
- Sven Wisotzky (@wisotzky)
