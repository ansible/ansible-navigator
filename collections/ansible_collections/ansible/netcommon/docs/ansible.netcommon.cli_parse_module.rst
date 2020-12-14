.. _ansible.netcommon.cli_parse_module:


***************************
ansible.netcommon.cli_parse
***************************

**Parse cli output or text using a variety of parsers**


Version added: 1.2.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Parse cli output or text using a variety of parsers




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
                    <b>command</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The command to run on the host</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parser</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Parser specific parameters</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>command</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The command used to locate the parser&#x27;s template</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name of the parser to use</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>os</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Provide an operating system value to the parser</div>
                        <div>For `ntc_templates` parser, this should be in the supported `&lt;vendor&gt;_&lt;os&gt;` format.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>template_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Path of the parser template on the Ansible controller</div>
                        <div>This can be a relative or an absolute path</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vars</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Additional parser specific parameters</div>
                        <div>See the cli_parse user guide for examples of parser specific variables</div>
                        <div>https://docs.ansible.com/ansible/latest/network/user_guide/cli_parsing.html</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set_fact</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set the resulting parsed data as a fact</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>text</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Text to be parsed</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - The default search path for a parser template is templates/{{ short_os }}_{{ command }}.{{ extension }}
   - => short_os derived from ansible_network_os or ansible_distribution and set to lower case
   - => command is the command passed to the module with spaces replaced with _
   - => extension is specific to the parser used (native=yaml, textfsm=textfsm, ttp=ttp)
   - The default Ansible search path for the templates directory is used for parser templates as well
   - Some parsers may have additional configuration options available. See the parsers/vars key and the parser's documentation
   - Some parsers require third-party python libraries be installed on the Ansible control node and a specific python version
   - e.g. Pyats requires pyats and genie and requires Python 3
   - e.g. ntc_templates requires ntc_templates
   - e.g. textfsm requires textfsm
   - e.g. ttp requires ttp
   - e.g. xml requires xml_to_dict
   - Support of 3rd party python libraries is limited to the use of their public APIs as documented
   - Additional information and examples can be found in the parsing user guide:
   - https://docs.ansible.com/ansible/latest/network/user_guide/cli_parsing.html



Examples
--------

.. code-block:: yaml

    # Using the native parser

    # -------------
    # templates/nxos_show_interface.yaml
    # - example: Ethernet1/1 is up
    #   getval: '(?P<name>\S+) is (?P<oper_state>\S+)'
    #   result:
    #     "{{ name }}":
    #         name: "{{ name }}"
    #         state:
    #         operating: "{{ oper_state }}"
    #   shared: True
    #
    # - example: admin state is up, Dedicated Interface
    #   getval: 'admin state is (?P<admin_state>\S+)'
    #   result:
    #     "{{ name }}":
    #         name: "{{ name }}"
    #         state:
    #         admin: "{{ admin_state }}"
    #
    # - example: "  Hardware: Ethernet, address: 0000.5E00.5301 (bia 0000.5E00.5301)"
    #   getval: '\s+Hardware: (?P<hardware>.*), address: (?P<mac>\S+)'
    #   result:
    #     "{{ name }}":
    #         hardware: "{{ hardware }}"
    #         mac_address: "{{ mac }}"

    - name: Run command and parse with native
      ansible.netcommon.cli_parse:
        command: "show interface"
        parser:
          name: ansible.netcommon.native
        set_fact: interfaces_fact


    - name: Pass text and template_path
      ansible.netcommon.cli_parse:
        text: "{{ previous_command['stdout'] }}"
        parser:
          name: ansible.netcommon.native
          template_path: "{{ role_path }}/templates/nxos_show_interface.yaml"


    # Using the ntc_templates parser

    # -------------
    # The ntc_templates use 'vendor_platform' for the file name
    # it will be derived from ansible_network_os if not provided
    # e.g. cisco.ios.ios => cisco_ios

    - name: Run command and parse with ntc_templates
      ansible.netcommon.cli_parse:
        command: "show interface"
        parser:
          name: ansible.netcommon.ntc_templates
      register: parser_output

    - name: Pass text and command
      ansible.netcommon.cli_parse:
        text: "{{ previous_command['stdout'] }}"
        parser:
          name: ansible.netcommon.ntc_templates
          command: show interface
      register: parser_output


    # Using the pyats parser

    # -------------
    # The pyats parser uses 'os' to locate the appropriate parser
    # it will be derived from ansible_network_os if not provided
    # in the case of pyats: cisco.ios.ios => iosxe

    - name: Run command and parse with pyats
      ansible.netcommon.cli_parse:
        command: "show interface"
        parser:
            name: ansible.netcommon.pyats
      register: parser_output

    - name: Pass text and command
      ansible.netcommon.cli_parse:
        text: "{{ previous_command['stdout'] }}"
        parser:
            name: ansible.netcommon.pyats
            command: show interface
      register: parser_output

    - name: Provide an OS to pyats to use an ios parser
      ansible.netcommon.cli_parse:
        text: "{{ previous_command['stdout'] }}"
        parser:
            name: ansible.netcommon.pyats
            command: show interface
            os: ios
      register: parser_output


    # Using the textfsm parser

    # -------------
    # templates/nxos_show_version.textfsm
    #
    # Value UPTIME ((\d+\s\w+.s.,?\s?){4})
    # Value LAST_REBOOT_REASON (.+)
    # Value OS (\d+.\d+(.+)?)
    # Value BOOT_IMAGE (.*)
    # Value PLATFORM (\w+)
    #
    # Start
    #   ^\s+(NXOS: version|system:\s+version)\s+${OS}\s*$$
    #   ^\s+(NXOS|kickstart)\s+image\s+file\s+is:\s+${BOOT_IMAGE}\s*$$
    #   ^\s+cisco\s+${PLATFORM}\s+[cC]hassis
    #   ^\s+cisco\s+Nexus\d+\s+${PLATFORM}
    #   # Cisco N5K platform
    #   ^\s+cisco\s+Nexus\s+${PLATFORM}\s+[cC]hassis
    #   ^\s+cisco\s+.+-${PLATFORM}\s*
    #   ^Kernel\s+uptime\s+is\s+${UPTIME}
    #   ^\s+Reason:\s${LAST_REBOOT_REASON} -> Record

    - name: Run command and parse with textfsm
      ansible.netcommon.cli_parse:
        command: "show version"
        parser:
          name: ansible.netcommon.textfsm
      register: parser_output

    - name: Pass text and command
      ansible.netcommon.cli_parse:
        text: "{{ previous_command['stdout'] }}"
        parser:
          name: ansible.netcommon.textfsm
          command: show version
      register: parser_output

    # Using the ttp parser

    # -------------
    # templates/nxos_show_interface.ttp
    #
    # {{ interface }} is {{ state }}
    # admin state is {{ admin_state }}{{ ignore(".*") }}

    - name: Run command and parse with ttp
      ansible.netcommon.cli_parse:
        command: "show interface"
        parser:
          name: ansible.netcommon.ttp
        set_fact: new_fact_key

    - name: Pass text and template_path
      ansible.netcommon.cli_parse:
        text: "{{ previous_command['stdout'] }}"
        parser:
          name: ansible.netcommon.ttp
          template_path: "{{ role_path }}/templates/nxos_show_interface.ttp"
      register: parser_output

    # Using the XML parser

    # -------------
    - name: Run command and parse with xml
      ansible.netcommon.cli_parse:
        command: "show interface | xml"
        parser:
          name: ansible.netcommon.xml
      register: parser_output

    - name: Pass text and parse with xml
      ansible.netcommon.cli_parse:
        text: "{{ previous_command['stdout'] }}"
        parser:
          name: ansible.netcommon.xml
      register: parser_output



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
                    <b>parsed</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The structured data resulting from the parsing of the text</div>
                    <br/>
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
                <td>when provided a command</td>
                <td>
                            <div>The output from the command run</div>
                    <br/>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stdout_lines</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when provided a command</td>
                <td>
                            <div>The output of the command run split into lines</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Bradley Thornton (@cidrblock)
