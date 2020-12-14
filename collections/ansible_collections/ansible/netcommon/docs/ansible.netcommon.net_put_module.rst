.. _ansible.netcommon.net_put_module:


*************************
ansible.netcommon.net_put
*************************

**Copy a file from Ansible Controller to a network device**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides functionality to copy file from Ansible controller to network devices.



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
                        <b>Default:</b><br/><div style="color: blue">["Filename from src and at default directory of user shell on network_os."]</div>
                </td>
                <td>
                        <div>Specifies the destination file. The path to destination file can either be the full path or relative path as supported by network_os.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mode</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>binary</b>&nbsp;&larr;</div></li>
                                    <li>text</li>
                        </ul>
                </td>
                <td>
                        <div>Set the file transfer mode. If mode is set to <em>text</em> then <em>src</em> file will go through Jinja2 template engine to replace any vars if present in the src file. If mode is set to <em>binary</em> then file will be copied as it is to destination device.</div>
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
                        <div>Specifies the source file. The path to the source file can either be the full path on the Ansible control host or a relative path from the playbook or role root directory.</div>
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

    - name: copy file from ansible controller to a network device
      ansible.netcommon.net_put:
        src: running_cfg_ios1.txt

    - name: copy file at root dir of flash in slot 3 of sw1(ios)
      ansible.netcommon.net_put:
        src: running_cfg_sw1.txt
        protocol: sftp
        dest: flash3:/running_cfg_sw1.txt




Status
------


Authors
~~~~~~~

- Deepak Agrawal (@dagrawal)
