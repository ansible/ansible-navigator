.. _arista.eos.eos_httpapi:


**************
arista.eos.eos
**************

**Use eAPI to run command on eos platform**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This eos plugin provides low level abstraction api's for sending and receiving CLI commands with eos network devices.




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
                    <b>eos_use_sessions</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">1</div>
                </td>
                    <td>
                                <div>env:ANSIBLE_EOS_USE_SESSIONS</div>
                                <div>var: ansible_eos_use_sessions</div>
                    </td>
                <td>
                        <div>Specifies if sessions should be used on remote host or not</div>
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
