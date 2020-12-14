.. _ansible.netcommon.net_banner_module:


****************************
ansible.netcommon.net_banner
****************************

**(deprecated, removed after 2022-06-01) Manage multiline banners on network devices**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

DEPRECATED
----------
:Removed in collection release after 2022-06-01
:Why: Updated modules released with more functionality
:Alternative: Use platform-specific "[netos]_banner" module



Synopsis
--------
- This will configure both login and motd banners on network devices. It allows playbooks to add or remove banner text from the active running configuration.




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
                    <b>banner</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>login</li>
                                    <li>motd</li>
                        </ul>
                </td>
                <td>
                        <div>Specifies which banner that should be configured on the remote device.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>absent</li>
                        </ul>
                </td>
                <td>
                        <div>Specifies whether or not the configuration is present in the current devices active running configuration.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>text</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The banner text that should be present in the remote device running configuration.  This argument accepts a multiline string, with no empty lines. Requires <em>state=present</em>.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module is supported on ``ansible_network_os`` network platforms. See the :ref:`Network Platform Options <platform_options>` for details.



Examples
--------

.. code-block:: yaml

    - name: configure the login banner
      ansible.netcommon.net_banner:
        banner: login
        text: |
          this is my login banner
          that contains a multiline
          string
        state: present

    - name: remove the motd banner
      ansible.netcommon.net_banner:
        banner: motd
        state: absent

    - name: Configure banner from file
      ansible.netcommon.net_banner:
        banner: motd
        text: "{{ lookup('file', './config_partial/raw_banner.cfg') }}"
        state: present



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
                    <b>commands</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always, except for the platforms that use Netconf transport to manage the device.</td>
                <td>
                            <div>The list of configuration mode commands to send to the device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;banner login&#x27;, &#x27;this is my login banner&#x27;, &#x27;that contains a multiline&#x27;, &#x27;string&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


- This module will be removed in version . *[deprecated]*
- For more information see `DEPRECATED`_.


Authors
~~~~~~~

- Ricardo Carrillo Cruz (@rcarrillocruz)
