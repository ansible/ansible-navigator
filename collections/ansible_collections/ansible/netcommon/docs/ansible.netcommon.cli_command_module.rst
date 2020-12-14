.. _ansible.netcommon.cli_command_module:


*****************************
ansible.netcommon.cli_command
*****************************

**Run a cli command on cli-based network devices**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Sends a command to a network device and returns the result read from the device.




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
                    <b>answer</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The answer to reply with if <em>prompt</em> is matched. The value can be a single answer or a list of answer for multiple prompts. In case the command execution results in multiple prompts the sequence of the prompt and excepted answer should be in same order.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>check_all</b>
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
                        <div>By default if any one of the prompts mentioned in <code>prompt</code> option is matched it won&#x27;t check for other prompts. This boolean flag, that when set to <em>True</em> will check for all the prompts mentioned in <code>prompt</code> option in the given order. If the option is set to <em>True</em> all the prompts should be received from remote host if not it will result in timeout.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>command</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The command to send to the remote network device.  The resulting output from the command is returned, unless <em>sendonly</em> is set.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>newline</b>
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
                        <div>The boolean value, that when set to false will send <em>answer</em> to the device without a trailing newline.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prompt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A single regex pattern or a sequence of patterns to evaluate the expected prompt from <em>command</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sendonly</b>
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
                        <div>The boolean value, that when set to true will send <em>command</em> to the device but not wait for a result.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module is supported on ``ansible_network_os`` network platforms. See the :ref:`Network Platform Options <platform_options>` for details.



Examples
--------

.. code-block:: yaml

    - name: run show version on remote devices
      ansible.netcommon.cli_command:
        command: show version

    - name: run command with json formatted output
      ansible.netcommon.cli_command:
        command: show version | json

    - name: run command expecting user confirmation
      ansible.netcommon.cli_command:
        command: commit replace
        prompt: This commit will replace or remove the entire running configuration
        answer: yes

    - name: run command expecting user confirmation
      ansible.netcommon.cli_command:
        command: show interface summary
        prompt: Press any key to continue
        answer: y
        newline: false

    - name: run config mode command and handle prompt/answer
      ansible.netcommon.cli_command:
        command: '{{ item }}'
        prompt:
        - Exit with uncommitted changes
        answer: y
      loop:
      - configure
      - set system syslog file test any any
      - exit

    - name: multiple prompt, multiple answer (mandatory check for all prompts)
      ansible.netcommon.cli_command:
        command: copy sftp sftp://user@host//user/test.img
        check_all: true
        prompt:
        - Confirm download operation
        - Password
        - Do you want to change that to the standby image
        answer:
        - y
        - <password>
        - y



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
                    <b>json</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when the device response is valid JSON</td>
                <td>
                            <div>A dictionary representing a JSON-formatted response</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{
      &quot;architecture&quot;: &quot;i386&quot;,
      &quot;bootupTimestamp&quot;: 1532649700.56,
      &quot;modelName&quot;: &quot;vEOS&quot;,
      &quot;version&quot;: &quot;4.15.9M&quot;
      [...]
    }</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stdout</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when sendonly is false</td>
                <td>
                            <div>The response from the command</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Version:      VyOS 1.1.7[...]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Nathaniel Case (@Qalthos)
