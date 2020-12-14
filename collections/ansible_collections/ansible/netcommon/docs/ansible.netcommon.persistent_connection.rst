.. _ansible.netcommon.persistent_connection:


****************************
ansible.netcommon.persistent
****************************

**Use a persistent unix socket for connection**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This is a helper plugin to allow making other connections persistent.




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
                    <b>persistent_command_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">10</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[persistent_connection]<br>command_timeout = 10</p>
                            </div>
                                <div>env:ANSIBLE_PERSISTENT_COMMAND_TIMEOUT</div>
                                <div>var: ansible_command_timeout</div>
                    </td>
                <td>
                        <div>Configures, in seconds, the amount of time to wait for a command to return from the remote device.  If this timer is exceeded before the command returns, the connection plugin will raise an exception and close</div>
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
