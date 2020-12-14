.. _ansible.netcommon.napalm_connection:


************************
ansible.netcommon.napalm
************************

**Provides persistent connection using NAPALM**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

DEPRECATED
----------
:Removed in collection release after 2022-06-01
:Why: I am pretty sure no one has ever tried to use these modules
:Alternative: None. If anyone actually wants to use this plugin, open an issue and we'll rescind the deprecation



Synopsis
--------
- This connection plugin provides connectivity to network devices using the NAPALM network device abstraction library.  This library requires certain features to be enabled on network devices depending on the destination device operating system.  The connection plugin requires ``napalm`` to be installed locally on the Ansible controller.



Requirements
------------
The below requirements are needed on the local Ansible controller node that executes this connection.

- napalm


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
                    <b>host</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"inventory_hostname"</div>
                </td>
                    <td>
                                <div>var: ansible_host</div>
                    </td>
                <td>
                        <div>Specifies the remote device FQDN or IP address to establish the SSH connection to.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_key_auto_add</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"no"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[paramiko_connection]<br>host_key_auto_add = no</p>
                            </div>
                                <div>env:ANSIBLE_HOST_KEY_AUTO_ADD</div>
                    </td>
                <td>
                        <div>By default, Ansible will prompt the user before adding SSH keys to the known hosts file. By enabling this option, unknown host keys will automatically be added to the known hosts file.</div>
                        <div>Be sure to fully understand the security implications of enabling this option on production systems as it could create a security vulnerability.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>network_os</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>var: ansible_network_os</div>
                    </td>
                <td>
                        <div>Configures the device platform network operating system.  This value is used to load a napalm device abstraction.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>var: ansible_password</div>
                                <div>var: ansible_ssh_pass</div>
                                <div>var: ansible_ssh_password</div>
                    </td>
                <td>
                        <div>Configures the user password used to authenticate to the remote device when first establishing the SSH connection.</div>
                </td>
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
                        <b>Default:</b><br/><div style="color: blue">30</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[persistent_connection]<br>command_timeout = 30</p>
                            </div>
                                <div>env:ANSIBLE_PERSISTENT_COMMAND_TIMEOUT</div>
                                <div>var: ansible_command_timeout</div>
                    </td>
                <td>
                        <div>Configures, in seconds, the amount of time to wait for a command to return from the remote device.  If this timer is exceeded before the command returns, the connection plugin will raise an exception and close.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>persistent_connect_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">30</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[persistent_connection]<br>connect_timeout = 30</p>
                            </div>
                                <div>env:ANSIBLE_PERSISTENT_CONNECT_TIMEOUT</div>
                                <div>var: ansible_connect_timeout</div>
                    </td>
                <td>
                        <div>Configures, in seconds, the amount of time to wait when trying to initially establish a persistent connection.  If this value expires before the connection to the remote device is completed, the connection will fail.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>port</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">22</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[defaults]<br>remote_port = 22</p>
                            </div>
                                <div>env:ANSIBLE_REMOTE_PORT</div>
                                <div>var: ansible_port</div>
                    </td>
                <td>
                        <div>Specifies the port on the remote device that listens for connections when establishing the SSH connection.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>private_key_file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[defaults]<br>private_key_file = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_PRIVATE_KEY_FILE</div>
                                <div>var: ansible_private_key_file</div>
                    </td>
                <td>
                        <div>The private SSH key or certificate file used to authenticate to the remote device when first establishing the SSH connection.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>remote_user</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[defaults]<br>remote_user = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_REMOTE_USER</div>
                                <div>var: ansible_user</div>
                    </td>
                <td>
                        <div>The username used to authenticate to the remote device when the SSH connection is first established.  If the remote_user is not specified, the connection will use the username of the logged in user.</div>
                        <div>Can be configured from the CLI via the <code>--user</code> or <code>-u</code> options.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">120</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Sets the connection time, in seconds, for communicating with the remote device.  This timeout is used as the default timeout value for commands when issuing a command to the network CLI.  If the command does not return in timeout seconds, an error is generated.</div>
                </td>
            </tr>
    </table>
    <br/>








Status
------


- This connection will be removed in version . *[deprecated]*
- For more information see `DEPRECATED`_.


Authors
~~~~~~~

- Ansible Networking Team


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
