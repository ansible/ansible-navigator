.. _ansible.netcommon.net_get_module:


*************************
ansible.netcommon.net_get
*************************

**Copy a file from a network device to Ansible Controller**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides functionality to copy file from network device to ansible controller.



Requirements
------------
The below requirements are needed on the host that executes this module.

- scp


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
                    <b>dest</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">["Same filename as specified in I(src). The path will be playbook root or role root directory if playbook is part of a role."]</div>
                </td>
                <td>
                        <div>Specifies the destination file. The path to the destination file can either be the full path on the Ansible control host or a relative path from the playbook or role root directory.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>protocol</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>scp</b>&nbsp;&larr;</div></li>
                                    <li>sftp</li>
                        </ul>
                </td>
                <td>
                        <div>Protocol used to transfer file.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>src</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies the source file. The path to the source file can either be the full path on the network device or a relative path as per path supported by destination network device.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Some devices need specific configurations to be enabled before scp can work These configuration should be pre-configured before using this module e.g ios - ``ip scp server enable``.
   - User privilege to do scp on network device should be pre-configured e.g. ios - need user privilege 15 by default for allowing scp.
   - Default destination of source file.
   - This module is supported on ``ansible_network_os`` network platforms. See the :ref:`Network Platform Options <platform_options>` for details.



Examples
--------

.. code-block:: yaml

    - name: copy file from the network device to Ansible controller
      ansible.netcommon.net_get:
        src: running_cfg_ios1.txt

    - name: copy file from ios to common location at /tmp
      ansible.netcommon.net_get:
        src: running_cfg_sw1.txt
        dest: /tmp/ios1.txt




Status
------


Authors
~~~~~~~

- Deepak Agrawal (@dagrawal)
