.. _ansible.netcommon.cli_config_module:


****************************
ansible.netcommon.cli_config
****************************

**Push text based configuration to network devices over network_cli**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides platform agnostic way of pushing text based configuration to network devices over network_cli connection plugin.




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
                        <div>This argument will cause the module to create a full backup of the current running config from the remote device before any changes are made. If the <code>backup_options</code> value is not given, the backup file is written to the <code>backup</code> folder in the playbook root directory or role root directory, if playbook is part of an ansible role. If the directory does not exist, it is created.</div>
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
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>The <code>commit</code> argument instructs the module to push the configuration to the device. This is mapped to module check mode.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>commit_comment</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The <code>commit_comment</code> argument specifies a text string to be used when committing the configuration. If the <code>commit</code> argument is set to False, this argument is silently ignored. This argument is only valid for the platforms that support commit operation with comment.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The config to be pushed to the network device. This argument is mutually exclusive with <code>rollback</code> and either one of the option should be given as input. The config should have indentation that the device uses.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>defaults</b>
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
                        <div>The <em>defaults</em> argument will influence how the running-config is collected from the device.  When the value is set to true, the command used to collect the running-config is append with the all keyword.  When the value is set to false, the command is issued without the all keyword.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>diff_ignore_lines</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Use this argument to specify one or more lines that should be ignored during the diff. This is used for lines in the configuration that are automatically updated by the system. This argument takes a list of regular expressions or exact line matches. Note that this parameter will be ignored if the platform has onbox diff support.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>diff_match</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>line</li>
                                    <li>strict</li>
                                    <li>exact</li>
                                    <li>none</li>
                        </ul>
                </td>
                <td>
                        <div>Instructs the module on the way to perform the matching of the set of commands against the current device config. If <code>diff_match</code> is set to <em>line</em>, commands are matched line by line. If <code>diff_match</code> is set to <em>strict</em>, command lines are matched with respect to position. If <code>diff_match</code> is set to <em>exact</em>, command lines must be an equal match. Finally, if <code>diff_match</code> is set to <em>none</em>, the module will not attempt to compare the source configuration with the running configuration on the remote device. Note that this parameter will be ignored if the platform has onbox diff support.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>diff_replace</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>line</li>
                                    <li>block</li>
                                    <li>config</li>
                        </ul>
                </td>
                <td>
                        <div>Instructs the module on the way to perform the configuration on the device. If the <code>diff_replace</code> argument is set to <em>line</em> then the modified lines are pushed to the device in configuration mode. If the argument is set to <em>block</em> then the entire command block is pushed to the device in configuration mode if any line is not correct. Note that this parameter will be ignored if the platform has onbox diff support.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multiline_delimiter</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This argument is used when pushing a multiline configuration element to the device. It specifies the character to use as the delimiting character. This only applies to the configuration action.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>replace</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>If the <code>replace</code> argument is set to <code>yes</code>, it will replace the entire running-config of the device with the <code>config</code> argument value. For devices that support replacing running configuration from file on device like NXOS/JUNOS, the <code>replace</code> argument takes path to the file on the device that will be used for replacing the entire running-config. The value of <code>config</code> option should be <em>None</em> for such devices. Nexus 9K devices only support replace. Use <em>net_put</em> or <em>nxos_file_copy</em> in case of NXOS module to copy the flat file to remote device and then use set the fullpath to this argument.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rollback</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The <code>rollback</code> argument instructs the module to rollback the current configuration to the identifier specified in the argument.  If the specified rollback identifier does not exist on the remote device, the module will fail. To rollback to the most recent commit, set the <code>rollback</code> argument to 0. This option is mutually exclusive with <code>config</code>.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - The commands will be returned only for platforms that do not support onbox diff. The ``--diff`` option with the playbook will return the difference in configuration for devices that has support for onbox diff
   - This module is supported on ``ansible_network_os`` network platforms. See the :ref:`Network Platform Options <platform_options>` for details.



Examples
--------

.. code-block:: yaml

    - name: configure device with config
      ansible.netcommon.cli_config:
        config: "{{ lookup('template', 'basic/config.j2') }}"

    - name: multiline config
      ansible.netcommon.cli_config:
        config: |
          hostname foo
          feature nxapi

    - name: configure device with config with defaults enabled
      ansible.netcommon.cli_config:
        config: "{{ lookup('template', 'basic/config.j2') }}"
        defaults: yes

    - name: Use diff_match
      ansible.netcommon.cli_config:
        config: "{{ lookup('file', 'interface_config') }}"
        diff_match: none

    - name: nxos replace config
      ansible.netcommon.cli_config:
        replace: bootflash:nxoscfg

    - name: junos replace config
      ansible.netcommon.cli_config:
        replace: /var/home/ansible/junos01.cfg

    - name: commit with comment
      ansible.netcommon.cli_config:
        config: set system host-name foo
        commit_comment: this is a test

    - name: configurable backup path
      ansible.netcommon.cli_config:
        config: "{{ lookup('template', 'basic/config.j2') }}"
        backup: yes
        backup_options:
          filename: backup.cfg
          dir_path: /home/user



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/playbooks/ansible/backup/hostname_config.2016-07-16@22:28:34</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>commands</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>When <em>supports_generated_diff=True</em> and <em>supports_onbox_diff=False</em> in the platform&#x27;s cliconf plugin</td>
                <td>
                            <div>The set of commands that will be pushed to the remote device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Loopback999&#x27;, &#x27;no shutdown&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>diff</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>When <em>supports_onbox_diff=True</em> in the platform&#x27;s cliconf plugin</td>
                <td>
                            <div>The diff generated on the device when the commands were applied</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">--- system:/running-config
    +++ session:/ansible_1599745461-session-config
    @@ -4,7 +4,7 @@
     !
     transceiver qsfp default-mode 4x10G
     !
    -hostname veos
    +hostname veos3
     !
     spanning-tree mode mstp</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Trishna Guha (@trishnaguha)
