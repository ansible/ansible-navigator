.. _ansible.netcommon.netconf_connection:


*************************
ansible.netcommon.netconf
*************************

**Provides a persistent connection using the netconf protocol**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This connection plugin provides a connection to remote devices over the SSH NETCONF subsystem.  This connection plugin is typically used by network devices for sending and receiving RPC calls over NETCONF.
- Note this connection plugin requires ncclient to be installed on the local Ansible controller.



Requirements
------------
The below requirements are needed on the local Ansible controller node that executes this connection.

- ncclient


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
                    <b>host_key_checking</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"yes"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[defaults]<br>host_key_checking = yes</p>
                                    <p>[paramiko_connection]<br>host_key_checking = yes</p>
                            </div>
                                <div>env:ANSIBLE_HOST_KEY_CHECKING</div>
                                <div>env:ANSIBLE_SSH_HOST_KEY_CHECKING</div>
                                <div>env:ANSIBLE_NETCONF_HOST_KEY_CHECKING</div>
                                <div>var: ansible_host_key_checking</div>
                                <div>var: ansible_ssh_host_key_checking</div>
                                <div>var: ansible_netconf_host_key_checking</div>
                    </td>
                <td>
                        <div>Set this to &quot;False&quot; if you want to avoid host key checking by the underlying tools Ansible uses to connect to the host</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>look_for_keys</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"yes"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[paramiko_connection]<br>look_for_keys = yes</p>
                            </div>
                                <div>env:ANSIBLE_PARAMIKO_LOOK_FOR_KEYS</div>
                    </td>
                <td>
                        <div>Enables looking for ssh keys in the usual locations for ssh keys (e.g. :file:`~/.ssh/id_*`).</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>netconf_ssh_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[netconf_connection]<br>ssh_config = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_NETCONF_SSH_CONFIG</div>
                                <div>var: ansible_netconf_ssh_config</div>
                    </td>
                <td>
                        <div>This variable is used to enable bastion/jump host with netconf connection. If set to True the bastion/jump host ssh settings should be present in ~/.ssh/config file, alternatively it can be set to custom ssh configuration file path to read the bastion/jump host settings.</div>
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
                        <div>Configures the device platform network operating system.  This value is used to load a device specific netconf plugin.  If this option is not configured (or set to <code>auto</code>), then Ansible will attempt to guess the correct network_os to use. If it can not guess a network_os correctly it will use <code>default</code>.</div>
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
                                <div>var: ansible_netconf_password</div>
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
                    <b>persistent_log_messages</b>
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
                                    <p>[persistent_connection]<br>log_messages = no</p>
                            </div>
                                <div>env:ANSIBLE_PERSISTENT_LOG_MESSAGES</div>
                                <div>var: ansible_persistent_log_messages</div>
                    </td>
                <td>
                        <div>This flag will enable logging the command executed and response received from target device in the ansible log file. For this option to work &#x27;log_path&#x27; ansible configuration option is required to be set to a file path with write access.</div>
                        <div>Be sure to fully understand the security implications of enabling this option as it could create a security vulnerability by logging sensitive information in log file.</div>
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
                        <b>Default:</b><br/><div style="color: blue">830</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[defaults]<br>remote_port = 830</p>
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
    </table>
    <br/>








Status
------


Authors
~~~~~~~

- Ansible Networking Team


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
