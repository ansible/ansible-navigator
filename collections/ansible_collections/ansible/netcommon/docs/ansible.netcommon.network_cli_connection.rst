.. _ansible.netcommon.network_cli_connection:


*****************************
ansible.netcommon.network_cli
*****************************

**Use network_cli to run command on network appliances**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This connection plugin provides a connection to remote devices over the SSH and implements a CLI shell.  This connection plugin is typically used by network devices for sending and receiving CLi commands to network devices.




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
                    <b>become</b>
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
                                    <p>[privilege_escalation]<br>become = no</p>
                            </div>
                                <div>env:ANSIBLE_BECOME</div>
                                <div>var: ansible_become</div>
                    </td>
                <td>
                        <div>The become option will instruct the CLI session to attempt privilege escalation on platforms that support it.  Normally this means transitioning from user mode to <code>enable</code> mode in the CLI session. If become is set to True and the remote device does not support privilege escalation or the privilege has already been elevated, then this option is silently ignored.</div>
                        <div>Can be configured from the CLI via the <code>--become</code> or <code>-b</code> options.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>become_method</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"sudo"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[privilege_escalation]<br>become_method = sudo</p>
                            </div>
                                <div>env:ANSIBLE_BECOME_METHOD</div>
                                <div>var: ansible_become_method</div>
                    </td>
                <td>
                        <div>This option allows the become method to be specified in for handling privilege escalation.  Typically the become_method value is set to <code>enable</code> but could be defined as other values.</div>
                </td>
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
                        <div>By default, Ansible will prompt the user before adding SSH keys to the known hosts file.  Since persistent connections such as network_cli run in background processes, the user will never be prompted.  By enabling this option, unknown host keys will automatically be added to the known hosts file.</div>
                        <div>Be sure to fully understand the security implications of enabling this option on production systems as it could create a security vulnerability.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>network_cli_retries</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">3</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[persistent_connection]<br>network_cli_retries = 3</p>
                            </div>
                                <div>env:ANSIBLE_NETWORK_CLI_RETRIES</div>
                                <div>var: ansible_network_cli_retries</div>
                    </td>
                <td>
                        <div>Number of attempts to connect to remote host. The delay time between the retires increases after every attempt by power of 2 in seconds till either the maximum attempts are exhausted or any of the <code>persistent_command_timeout</code> or <code>persistent_connect_timeout</code> timers are triggered.</div>
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
                        <div>Configures the device platform network operating system.  This value is used to load the correct terminal and cliconf plugins to communicate with the remote device.</div>
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
                    <b>persistent_buffer_read_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">float</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">0.1</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[persistent_connection]<br>buffer_read_timeout = 0.1</p>
                            </div>
                                <div>env:ANSIBLE_PERSISTENT_BUFFER_READ_TIMEOUT</div>
                                <div>var: ansible_buffer_read_timeout</div>
                    </td>
                <td>
                        <div>Configures, in seconds, the amount of time to wait for the data to be read from Paramiko channel after the command prompt is matched. This timeout value ensures that command prompt matched is correct and there is no more data left to be received from remote host.</div>
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
                    <b>ssh_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"paramiko"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[persistent_connection]<br>ssh_type = paramiko</p>
                            </div>
                                <div>env:ANSIBLE_NETWORK_CLI_SSH_TYPE</div>
                                <div>var: ansible_network_cli_ssh_type</div>
                    </td>
                <td>
                        <div>The type of the transport used by <code>network_cli</code> connection plugin to connection to remote host. Valid value is either <em>paramiko</em> or <em>libssh</em></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>terminal_inital_prompt_newline</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"yes"</div>
                </td>
                    <td>
                                <div>var: ansible_terminal_initial_prompt_newline</div>
                    </td>
                <td>
                        <div>This boolean flag, that when set to <em>True</em> will send newline in the response if any of values in <em>terminal_initial_prompt</em> is matched.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>terminal_initial_answer</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>var: ansible_terminal_initial_answer</div>
                    </td>
                <td>
                        <div>The answer to reply with if the <code>terminal_initial_prompt</code> is matched. The value can be a single answer or a list of answers for multiple terminal_initial_prompt. In case the login menu has multiple prompts the sequence of the prompt and excepted answer should be in same order and the value of <em>terminal_prompt_checkall</em> should be set to <em>True</em> if all the values in <code>terminal_initial_prompt</code> are expected to be matched and set to <em>False</em> if any one login prompt is to be matched.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>terminal_initial_prompt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>var: ansible_terminal_initial_prompt</div>
                    </td>
                <td>
                        <div>A single regex pattern or a sequence of patterns to evaluate the expected prompt at the time of initial login to the remote host.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>terminal_initial_prompt_checkall</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"no"</div>
                </td>
                    <td>
                                <div>var: ansible_terminal_initial_prompt_checkall</div>
                    </td>
                <td>
                        <div>By default the value is set to <em>False</em> and any one of the prompts mentioned in <code>terminal_initial_prompt</code> option is matched it won&#x27;t check for other prompts. When set to <em>True</em> it will check for all the prompts mentioned in <code>terminal_initial_prompt</code> option in the given order and all the prompts should be received from remote host if not it will result in timeout.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>terminal_stderr_re</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>var: ansible_terminal_stderr_re</div>
                    </td>
                <td>
                        <div>This option provides the regex pattern and optional flags to match the error string from the received response chunk. This option accepts <code>pattern</code> and <code>flags</code> keys. The value of <code>pattern</code> is a python regex pattern to match the response and the value of <code>flags</code> is the value accepted by <em>flags</em> argument of <em>re.compile</em> python method to control the way regex is matched with the response, for example <em>&#x27;re.I&#x27;</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>terminal_stdout_re</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>var: ansible_terminal_stdout_re</div>
                    </td>
                <td>
                        <div>A single regex pattern or a sequence of patterns along with optional flags to match the command prompt from the received response chunk. This option accepts <code>pattern</code> and <code>flags</code> keys. The value of <code>pattern</code> is a python regex pattern to match the response and the value of <code>flags</code> is the value accepted by <em>flags</em> argument of <em>re.compile</em> python method to control the way regex is matched with the response, for example <em>&#x27;re.I&#x27;</em>.</div>
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
