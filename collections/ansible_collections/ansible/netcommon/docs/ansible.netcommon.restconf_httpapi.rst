.. _ansible.netcommon.restconf_httpapi:


**************************
ansible.netcommon.restconf
**************************

**HttpApi Plugin for devices supporting Restconf API**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This HttpApi plugin provides methods to connect to Restconf API endpoints.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>root_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"/restconf"</div>
                </td>
                    <td>
                                <div>var: ansible_httpapi_restconf_root</div>
                    </td>
                <td>
                        <div>Specifies the location of the Restconf root.</div>
                </td>
            </tr>
    </table>
    <br/>








Status
------


Authors
~~~~~~~

- Ansible Networking Team


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
