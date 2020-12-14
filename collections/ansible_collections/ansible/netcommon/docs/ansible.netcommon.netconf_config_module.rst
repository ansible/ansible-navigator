.. _ansible.netcommon.netconf_config_module:


********************************
ansible.netcommon.netconf_config
********************************

**netconf device configuration**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Netconf is a network management protocol developed and standardized by the IETF. It is documented in RFC 6241.
- This module allows the user to send a configuration XML file to a netconf device, and detects if there was a configuration change.



Requirements
------------
The below requirements are needed on the host that executes this module.

- ncclient


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>backup</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>This argument will cause the module to create a full backup of the current <code>running-config</code> from the remote device before any changes are made. If the <code>backup_options</code> value is not given, the backup file is written to the <code>backup</code> folder in the playbook root directory or role root directory, if playbook is part of an ansible role. If the directory does not exist, it is created.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>backup_options</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This is a dict object containing configurable options related to backup file path. The value of this option is read only when <code>backup</code> is set to <em>yes</em>, if <code>backup</code> is set to <em>no</em> this option will be silently ignored.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dir_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This option provides the path ending with directory name in which the backup configuration file will be stored. If the directory does not exist it will be first created and the filename is either the value of <code>filename</code> or default filename as described in <code>filename</code> options description. If the path value is not given in that case a <em>backup</em> directory will be created in the current working directory and backup configuration will be copied in <code>filename</code> within <em>backup</em> directory.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filename</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The filename to be used to store the backup configuration. If the filename is not given it will be generated based on the hostname, current time and date in format defined by &lt;hostname&gt;_config.&lt;current-date&gt;@&lt;current-time&gt;</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>commit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>This boolean flag controls if the configuration changes should be committed or not after editing the candidate datastore. This option is supported only if remote Netconf server supports :candidate capability. If the value is set to <em>False</em> commit won&#x27;t be issued after edit-config operation and user needs to handle commit or discard-changes explicitly.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>confirm</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">0</div>
                </td>
                <td>
                        <div>This argument will configure a timeout value for the commit to be confirmed before it is automatically rolled back. If the <code>confirm_commit</code> argument is set to False, this argument is silently ignored. If the value of this argument is set to 0, the commit is confirmed immediately. The remote host MUST support :candidate and :confirmed-commit capability for this option to .</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>confirm_commit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>This argument will execute commit operation on remote device. It can be used to confirm a previous commit.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>content</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The configuration data as defined by the device&#x27;s data models, the value can be either in xml string format or text format or python dictionary representation of JSON format.</div>
                        <div>In case of json string format it will be converted to the corresponding xml string using xmltodict library before pushing onto the remote host.</div>
                        <div>In case the value of this option isn <em>text</em> format the format should be supported by remote Netconf server.</div>
                        <div>If the value of <code>content</code> option is in <em>xml</em> format in that case the xml value should have <em>config</em> as root tag.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: xml</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>default_operation</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>merge</li>
                                    <li>replace</li>
                                    <li>none</li>
                        </ul>
                </td>
                <td>
                        <div>The default operation for &lt;edit-config&gt; rpc, valid values are <em>merge</em>, <em>replace</em> and <em>none</em>. If the default value is merge, the configuration data in the <code>content</code> option is merged at the corresponding level in the <code>target</code> datastore. If the value is replace the data in the <code>content</code> option completely replaces the configuration in the <code>target</code> datastore. If the value is none the <code>target</code> datastore is unaffected by the configuration in the config option, unless and until the incoming configuration data uses the <code>operation</code> operation to request a different operation.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>delete</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>It instructs the module to delete the configuration from value mentioned in <code>target</code> datastore.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>error_option</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>stop-on-error</b>&nbsp;&larr;</div></li>
                                    <li>continue-on-error</li>
                                    <li>rollback-on-error</li>
                        </ul>
                </td>
                <td>
                        <div>This option controls the netconf server action after an error occurs while editing the configuration.</div>
                        <div>If <em>error_option=stop-on-error</em>, abort the config edit on first error.</div>
                        <div>If <em>error_option=continue-on-error</em>, continue to process configuration data on error. The error is recorded and negative response is generated if any errors occur.</div>
                        <div>If <em>error_option=rollback-on-error</em>, rollback to the original configuration if any error occurs. This requires the remote Netconf server to support the <em>error_option=rollback-on-error</em> capability.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>format</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>xml</li>
                                    <li>text</li>
                                    <li>json</li>
                        </ul>
                </td>
                <td>
                        <div>The format of the configuration provided as value of <code>content</code>.</div>
                        <div>In case of json string format it will be converted to the corresponding xml string using xmltodict library before pushing onto the remote host.</div>
                        <div>In case of <em>text</em> format of the configuration should be supported by remote Netconf server.</div>
                        <div>If the value of <code>format</code> options is not given it tries to guess the data format of <code>content</code> option as one of <em>xml</em> or <em>json</em> or <em>text</em>.</div>
                        <div>If the data format is not identified it is set to <em>xml</em> by default.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>get_filter</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This argument specifies the XML string which acts as a filter to restrict the portions of the data retrieved from the remote device when comparing the before and after state of the device following calls to edit_config. When not specified, the entire configuration or state data is returned for comparison depending on the value of <code>source</code> option. The <code>get_filter</code> value can be either XML string or XPath or JSON string or native python dictionary, if the filter is in XPath format the NETCONF server running on remote host should support xpath capability else it will result in an error.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies the DNS host name or address for connecting to the remote device over the specified transport.  The value of host is used as the destination address for the transport.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hostkey_verify</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>If set to <code>yes</code>, the ssh host key of the device must match a ssh key present on the host if set to <code>no</code>, the ssh host key of the device is not checked.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lock</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>never</li>
                                    <li><div style="color: blue"><b>always</b>&nbsp;&larr;</div></li>
                                    <li>if-supported</li>
                        </ul>
                </td>
                <td>
                        <div>Instructs the module to explicitly lock the datastore specified as <code>target</code>. By setting the option value <em>always</em> is will explicitly lock the datastore mentioned in <code>target</code> option. It the value is <em>never</em> it will not lock the <code>target</code> datastore. The value <em>if-supported</em> lock the <code>target</code> datastore only if it is supported by the remote Netconf server.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>look_for_keys</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Enables looking in the usual locations for the ssh keys (e.g. :file:`~/.ssh/id_*`)</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies the password to use to authenticate the connection to the remote device.   This value is used to authenticate the SSH session. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_PASSWORD</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
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
                        <div>Specifies the port to use when building the connection to the remote device.  The port value will default to port 830.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>save</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>The <code>save</code> argument instructs the module to save the configuration in <code>target</code> datastore to the startup-config if changed and if :startup capability is supported by Netconf server.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source_datastore</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the configuration datastore to use as the source to copy the configuration to the datastore mentioned by <code>target</code> option. The values can be either <em>running</em>, <em>candidate</em>, <em>startup</em> or a remote URL</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: source</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>src</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies the source path to the xml file that contains the configuration or configuration template to load. The path to the source file can either be the full path on the Ansible control host or a relative path from the playbook or role root directory. This argument is mutually exclusive with <em>xml</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ssh_keyfile</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specifies the SSH key to use to authenticate the connection to the remote device.   This value is the path to the key used to authenticate the SSH session. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>target</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>auto</b>&nbsp;&larr;</div></li>
                                    <li>candidate</li>
                                    <li>running</li>
                        </ul>
                </td>
                <td>
                        <div>Name of the configuration datastore to be edited. - auto, uses candidate and fallback to running - candidate, edit &lt;candidate/&gt; datastore and then commit - running, edit &lt;running/&gt; datastore directly</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: datastore</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">10</div>
                </td>
                <td>
                        <div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>username</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configures the username to use to authenticate the connection to the remote device.  This value is used to authenticate the SSH session. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_USERNAME</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>validate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>This boolean flag if set validates the content of datastore given in <code>target</code> option. For this option to work remote Netconf server should support :validate capability.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module requires the netconf system service be enabled on the remote device being managed.
   - This module supports devices with and without the candidate and confirmed-commit capabilities. It will always use the safer feature.
   - This module supports the use of connection=netconf
   - For information on using netconf see the :ref:`Platform Options guide using Netconf<netconf_enabled_platform_options>`
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - This module is supported on ``ansible_network_os`` network platforms. See the :ref:`Network Platform Options <platform_options>` for details.



Examples
--------

.. code-block:: yaml

    - name: use lookup filter to provide xml configuration
      ansible.netcommon.netconf_config:
        content: "{{ lookup('file', './config.xml') }}"

    - name: set ntp server in the device
      ansible.netcommon.netconf_config:
        content: |
          <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
              <system xmlns="urn:ietf:params:xml:ns:yang:ietf-system">
                  <ntp>
                      <enabled>true</enabled>
                      <server>
                          <name>ntp1</name>
                          <udp><address>127.0.0.1</address></udp>
                      </server>
                  </ntp>
              </system>
          </config>

    - name: wipe ntp configuration
      ansible.netcommon.netconf_config:
        content: |
          <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
              <system xmlns="urn:ietf:params:xml:ns:yang:ietf-system">
                  <ntp>
                      <enabled>false</enabled>
                      <server operation="remove">
                          <name>ntp1</name>
                      </server>
                  </ntp>
              </system>
          </config>

    - name: configure interface while providing different private key file path (for connection=netconf)
      ansible.netcommon.netconf_config:
        backup: yes
      register: backup_junos_location
      vars:
        ansible_private_key_file: /home/admin/.ssh/newprivatekeyfile

    - name: configurable backup path
      ansible.netcommon.netconf_config:
        backup: yes
        backup_options:
          filename: backup.cfg
          dir_path: /home/user

    - name: "configure using direct native format configuration (cisco iosxr)"
      ansible.netcommon.netconf_config:
        content: {
                    "config": {
                        "interface-configurations": {
                            "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
                            "interface-configuration": {
                                "active": "act",
                                "description": "test for ansible Loopback999",
                                "interface-name": "Loopback999"
                            }
                        }
                    }
                }
        get_filter: {
                      "interface-configurations": {
                          "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
                          "interface-configuration": null
                      }
                  }

    - name: "configure using json string format configuration (cisco iosxr)"
      ansible.netcommon.netconf_config:
        content: |
                {
                    "config": {
                        "interface-configurations": {
                            "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
                            "interface-configuration": {
                                "active": "act",
                                "description": "test for ansible Loopback999",
                                "interface-name": "Loopback999"
                            }
                        }
                    }
                }
        get_filter: |
                {
                      "interface-configurations": {
                          "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
                          "interface-configuration": null
                      }
                  }


    # Make a round-trip interface description change, diff the before and after
    # this demonstrates the use of the native display format and several utilities
    # from the ansible.utils collection

    - name: Define the openconfig interface filter
      set_fact:
        filter:
          interfaces:
            "@xmlns": "http://openconfig.net/yang/interfaces"
            interface:
              name: Ethernet2

    - name: Get the pre-change config using the filter
      ansible.netcommon.netconf_get:
        source: running
        filter: "{{ filter }}"
        display: native
      register: pre

    - name: Update the description
      ansible.utils.update_fact:
        updates:
        - path: pre.output.data.interfaces.interface.config.description
          value: "Configured by ansible {{ 100 | random }}"
      register: updated

    - name: Apply the new configuration
      ansible.netcommon.netconf_config:
        content:
          config:
            interfaces: "{{ updated.pre.output.data.interfaces }}"

    - name: Get the post-change config using the filter
      ansible.netcommon.netconf_get:
        source: running
        filter: "{{ filter }}"
        display: native
      register: post

    - name: Show the differences between the pre and post configurations
      ansible.utils.fact_diff:
        before: "{{ pre.output.data|ansible.utils.to_paths }}"
        after: "{{ post.output.data|ansible.utils.to_paths }}"

    # TASK [Show the differences between the pre and post configurations] ********
    # --- before
    # +++ after
    # @@ -1,11 +1,11 @@
    #  {
    # -    "@time-modified": "2020-10-23T12:27:17.462332477Z",
    # +    "@time-modified": "2020-10-23T12:27:21.744541708Z",
    #      "@xmlns": "urn:ietf:params:xml:ns:netconf:base:1.0",
    #      "interfaces.interface.aggregation.config['fallback-timeout']['#text']": "90",
    #      "interfaces.interface.aggregation.config['fallback-timeout']['@xmlns']": "http://arista.com/yang/openconfig/interfaces/augments",
    #      "interfaces.interface.aggregation.config['min-links']": "0",
    #      "interfaces.interface.aggregation['@xmlns']": "http://openconfig.net/yang/interfaces/aggregate",
    # -    "interfaces.interface.config.description": "Configured by ansible 56",
    # +    "interfaces.interface.config.description": "Configured by ansible 67",
    #      "interfaces.interface.config.enabled": "true",
    #      "interfaces.interface.config.mtu": "0",
    #      "interfaces.interface.config.name": "Ethernet2",



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
                    <b>backup_path</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when backup is yes</td>
                <td>
                            <div>The full path to the backup file</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/playbooks/ansible/backup/config.2016-07-16@22:28:34</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>diff</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when diff is enabled</td>
                <td>
                            <div>If --diff option in enabled while running, the before and after configuration change are returned as part of before and after key.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;after&#x27;: &#x27;&lt;rpc-reply&gt; &lt;data&gt; &lt;configuration&gt; &lt;version&gt;17.3R1.10&lt;/version&gt;...&lt;--snip--&gt;&#x27;, &#x27;before&#x27;: &#x27;&lt;rpc-reply&gt; &lt;data&gt; &lt;configuration&gt; &lt;version&gt;17.3R1.10&lt;/version&gt;...&lt;--snip--&gt;&#x27;}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>server_capabilities</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>list of capabilities of the server</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;urn:ietf:params:netconf:base:1.1&#x27;, &#x27;urn:ietf:params:netconf:capability:confirmed-commit:1.0&#x27;, &#x27;urn:ietf:params:netconf:capability:candidate:1.0&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Leandro Lisboa Penz (@lpenz)
- Ganesh Nalawade (@ganeshrn)
