.. _ansible.netcommon.libssh_connection:


************************
ansible.netcommon.libssh
************************

**(Tech preview) Run tasks using libssh for ssh connection**


Version added: 2.10

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Use the ansible-pylibssh python bindings to connect to targets
- The python bindings use libssh C library (https://www.libssh.org/) to connect to targets
- This plugin borrows a lot of settings from the ssh plugin as they both cover the same protocol.




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
                    <b>host_key_auto_add</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[libssh_connection]<br>host_key_auto_add = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_LIBSSH_HOST_KEY_AUTO_ADD</div>
                    </td>
                <td>
                        <div>TODO: write it</div>
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
                                    <p>[libssh_connection]<br>host_key_checking = yes</p>
                            </div>
                                <div>env:ANSIBLE_HOST_KEY_CHECKING</div>
                                <div>env:ANSIBLE_SSH_HOST_KEY_CHECKING</div>
                                <div>env:ANSIBLE_LIBSSH_HOST_KEY_CHECKING</div>
                                <div>var: ansible_host_key_checking</div>
                                <div>var: ansible_ssh_host_key_checking</div>
                                <div>var: ansible_libssh_host_key_checking</div>
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
                                    <p>[libssh_connection]<br>look_for_keys = yes</p>
                            </div>
                                <div>env:ANSIBLE_LIBSSH_LOOK_FOR_KEYS</div>
                    </td>
                <td>
                        <div>TODO: write it</div>
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
                                <div>var: ansible_libssh_pass</div>
                                <div>var: ansible_libssh_password</div>
                    </td>
                <td>
                        <div>Secret used to either login the ssh server or as a passphrase for ssh keys that require it</div>
                        <div>Can be set from the CLI via the <code>--ask-pass</code> option.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>proxy_command</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">""</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[libssh_connection]<br>proxy_command = </p>
                            </div>
                                <div>env:ANSIBLE_LIBSSH_PROXY_COMMAND</div>
                    </td>
                <td>
                        <div>Proxy information for running the connection via a jumphost</div>
                        <div>Also this plugin will scan &#x27;ssh_args&#x27;, &#x27;ssh_extra_args&#x27; and &#x27;ssh_common_args&#x27; from the &#x27;ssh&#x27; plugin settings for proxy information if set.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>pty</b>
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
                                    <p>[libssh_connection]<br>pty = yes</p>
                            </div>
                                <div>env:ANSIBLE_LIBSSH_PTY</div>
                    </td>
                <td>
                        <div>TODO: write it</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>remote_addr</b>
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
                                <div>var: ansible_ssh_host</div>
                                <div>var: ansible_libssh_host</div>
                    </td>
                <td>
                        <div>Address of the remote target</div>
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
                                    <p>[libssh_connection]<br>remote_user = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_REMOTE_USER</div>
                                <div>env:ANSIBLE_LIBSSH_REMOTE_USER</div>
                                <div>var: ansible_user</div>
                                <div>var: ansible_ssh_user</div>
                                <div>var: ansible_libssh_user</div>
                    </td>
                <td>
                        <div>User to login/authenticate as</div>
                        <div>Can be set from the CLI via the <code>--user</code> or <code>-u</code> options.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_persistent_connections</b>
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
                                    <p>[defaults]<br>use_persistent_connections = no</p>
                            </div>
                                <div>env:ANSIBLE_USE_PERSISTENT_CONNECTIONS</div>
                    </td>
                <td>
                        <div>Toggles the use of persistence for connections</div>
                </td>
            </tr>
    </table>
    <br/>








Status
------


Authors
~~~~~~~

- Ansible Team


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
