#!/usr/bin/python

# (c) 2016, Leandro Lisboa Penz <lpenz at lpenz.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: netconf_config
author:
- Leandro Lisboa Penz (@lpenz)
- Ganesh Nalawade (@ganeshrn)
short_description: netconf device configuration
description:
- Netconf is a network management protocol developed and standardized by the IETF.
  It is documented in RFC 6241.
- This module allows the user to send a configuration XML file to a netconf device,
  and detects if there was a configuration change.
version_added: 1.0.0
extends_documentation_fragment:
- ansible.netcommon.netconf
- ansible.netcommon.network_agnostic
options:
  content:
    description:
    - The configuration data as defined by the device's data models, the value can
      be either in xml string format or text format or python dictionary representation of JSON format.
    - In case of json string format it will be converted to the corresponding xml string using
      xmltodict library before pushing onto the remote host.
    - In case the value of this option isn I(text) format the format should be supported by remote Netconf server.
    - If the value of C(content) option is in I(xml) format in that case the xml value should
      have I(config) as root tag.
    type: raw
    aliases:
    - xml
  target:
    description: Name of the configuration datastore to be edited. - auto, uses candidate
      and fallback to running - candidate, edit <candidate/> datastore and then commit
      - running, edit <running/> datastore directly
    default: auto
    type: str
    choices:
    - auto
    - candidate
    - running
    aliases:
    - datastore
  source_datastore:
    description:
    - Name of the configuration datastore to use as the source to copy the configuration
      to the datastore mentioned by C(target) option. The values can be either I(running),
      I(candidate), I(startup) or a remote URL
    type: str
    aliases:
    - source
  format:
    description:
    - The format of the configuration provided as value of C(content).
    - In case of json string format it will be converted to the corresponding xml string using
      xmltodict library before pushing onto the remote host.
    - In case of I(text) format of the configuration should be supported by remote Netconf server.
    - If the value of C(format) options is not given it tries to guess the data format of
      C(content) option as one of I(xml) or I(json) or I(text).
    - If the data format is not identified it is set to I(xml) by default.
    type: str
    choices:
    - xml
    - text
    - json
  lock:
    description:
    - Instructs the module to explicitly lock the datastore specified as C(target).
      By setting the option value I(always) is will explicitly lock the datastore
      mentioned in C(target) option. It the value is I(never) it will not lock the
      C(target) datastore. The value I(if-supported) lock the C(target) datastore
      only if it is supported by the remote Netconf server.
    type: str
    default: always
    choices:
    - never
    - always
    - if-supported
  default_operation:
    description:
    - The default operation for <edit-config> rpc, valid values are I(merge), I(replace)
      and I(none). If the default value is merge, the configuration data in the C(content)
      option is merged at the corresponding level in the C(target) datastore. If the
      value is replace the data in the C(content) option completely replaces the configuration
      in the C(target) datastore. If the value is none the C(target) datastore is
      unaffected by the configuration in the config option, unless and until the incoming
      configuration data uses the C(operation) operation to request a different operation.
    type: str
    choices:
    - merge
    - replace
    - none
  confirm:
    description:
    - This argument will configure a timeout value for the commit to be confirmed
      before it is automatically rolled back. If the C(confirm_commit) argument is
      set to False, this argument is silently ignored. If the value of this argument
      is set to 0, the commit is confirmed immediately. The remote host MUST support
      :candidate and :confirmed-commit capability for this option to .
    type: int
    default: 0
  confirm_commit:
    description:
    - This argument will execute commit operation on remote device. It can be used
      to confirm a previous commit.
    type: bool
    default: no
  error_option:
    description:
    - This option controls the netconf server action after an error occurs while editing
      the configuration.
    - If I(error_option=stop-on-error), abort the config edit on first error.
    - If I(error_option=continue-on-error), continue to process configuration data
      on error. The error is recorded and negative response is generated if any errors
      occur.
    - If I(error_option=rollback-on-error), rollback to the original configuration
      if any error occurs. This requires the remote Netconf server to support the
      I(error_option=rollback-on-error) capability.
    default: stop-on-error
    type: str
    choices:
    - stop-on-error
    - continue-on-error
    - rollback-on-error
  save:
    description:
    - The C(save) argument instructs the module to save the configuration in C(target)
      datastore to the startup-config if changed and if :startup capability is supported
      by Netconf server.
    default: false
    type: bool
  backup:
    description:
    - This argument will cause the module to create a full backup of the current C(running-config)
      from the remote device before any changes are made. If the C(backup_options)
      value is not given, the backup file is written to the C(backup) folder in the
      playbook root directory or role root directory, if playbook is part of an ansible
      role. If the directory does not exist, it is created.
    type: bool
    default: no
  delete:
    description:
    - It instructs the module to delete the configuration from value mentioned in
      C(target) datastore.
    type: bool
    default: no
  commit:
    description:
    - This boolean flag controls if the configuration changes should be committed
      or not after editing the candidate datastore. This option is supported only
      if remote Netconf server supports :candidate capability. If the value is set
      to I(False) commit won't be issued after edit-config operation and user needs
      to handle commit or discard-changes explicitly.
    type: bool
    default: true
  validate:
    description:
    - This boolean flag if set validates the content of datastore given in C(target)
      option. For this option to work remote Netconf server should support :validate
      capability.
    type: bool
    default: false
  src:
    description:
    - Specifies the source path to the xml file that contains the configuration or
      configuration template to load. The path to the source file can either be the
      full path on the Ansible control host or a relative path from the playbook or
      role root directory. This argument is mutually exclusive with I(xml).
    type: path
  backup_options:
    description:
    - This is a dict object containing configurable options related to backup file
      path. The value of this option is read only when C(backup) is set to I(yes),
      if C(backup) is set to I(no) this option will be silently ignored.
    suboptions:
      filename:
        description:
        - The filename to be used to store the backup configuration. If the filename
          is not given it will be generated based on the hostname, current time and
          date in format defined by <hostname>_config.<current-date>@<current-time>
        type: str
      dir_path:
        description:
        - This option provides the path ending with directory name in which the backup
          configuration file will be stored. If the directory does not exist it will
          be first created and the filename is either the value of C(filename) or
          default filename as described in C(filename) options description. If the
          path value is not given in that case a I(backup) directory will be created
          in the current working directory and backup configuration will be copied
          in C(filename) within I(backup) directory.
        type: path
    type: dict
  get_filter:
    description:
    - This argument specifies the XML string which acts as a filter to restrict the
      portions of the data retrieved from the remote device when comparing the before
      and after state of the device following calls to edit_config. When not specified,
      the entire configuration or state data is returned for comparison depending
      on the value of C(source) option. The C(get_filter) value can be either XML
      string or XPath or JSON string or native python dictionary, if the filter is
      in XPath format the NETCONF server running on remote host should support xpath
      capability else it will result in an error.
    type: raw
requirements:
- ncclient
notes:
- This module requires the netconf system service be enabled on the remote device
  being managed.
- This module supports devices with and without the candidate and confirmed-commit
  capabilities. It will always use the safer feature.
- This module supports the use of connection=netconf
"""

EXAMPLES = """
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

"""

RETURN = """
server_capabilities:
    description: list of capabilities of the server
    returned: success
    type: list
    sample: ['urn:ietf:params:netconf:base:1.1','urn:ietf:params:netconf:capability:confirmed-commit:1.0','urn:ietf:params:netconf:capability:candidate:1.0']
backup_path:
  description: The full path to the backup file
  returned: when backup is yes
  type: str
  sample: /playbooks/ansible/backup/config.2016-07-16@22:28:34
diff:
  description: If --diff option in enabled while running, the before and after configuration change are
               returned as part of before and after key.
  returned: when diff is enabled
  type: dict
  sample:
    "after": "<rpc-reply>\n<data>\n<configuration>\n<version>17.3R1.10</version>...<--snip-->"
    "before": "<rpc-reply>\n<data>\n<configuration>\n <version>17.3R1.10</version>...<--snip-->"
"""

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import Connection, ConnectionError
from ansible_collections.ansible.netcommon.plugins.module_utils.utils.data import (
    validate_and_normalize_data,
    dict_to_xml,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.netconf.netconf import (
    get_capabilities,
    get_config,
    sanitize_xml,
)

try:
    from lxml.etree import tostring, fromstring
except ImportError:
    from xml.etree.ElementTree import tostring, fromstring


def validate_config(module, config, format="xml"):
    if format == "xml":
        root = fromstring(config)
        if not root.tag.endswith("config"):
            module.fail_json(
                msg="content value should have XML string with config tag as the root node"
            )


def main():
    """ main entry point for module execution
    """
    backup_spec = dict(filename=dict(), dir_path=dict(type="path"))
    argument_spec = dict(
        content=dict(aliases=["xml"], type="raw"),
        target=dict(
            choices=["auto", "candidate", "running"],
            default="auto",
            aliases=["datastore"],
        ),
        source_datastore=dict(aliases=["source"]),
        format=dict(choices=["xml", "text", "json"]),
        lock=dict(
            choices=["never", "always", "if-supported"], default="always"
        ),
        default_operation=dict(choices=["merge", "replace", "none"]),
        confirm=dict(type="int", default=0),
        confirm_commit=dict(type="bool", default=False),
        error_option=dict(
            choices=[
                "stop-on-error",
                "continue-on-error",
                "rollback-on-error",
            ],
            default="stop-on-error",
        ),
        backup=dict(type="bool", default=False),
        backup_options=dict(type="dict", options=backup_spec),
        save=dict(type="bool", default=False),
        delete=dict(type="bool", default=False),
        commit=dict(type="bool", default=True),
        validate=dict(type="bool", default=False),
        get_filter=dict(type="raw"),
    )

    # deprecated options
    netconf_top_spec = {
        "src": dict(
            type="path",
            removed_at_date="2020-12-01",
            removed_from_collection="ansible.netcommon",
        ),
        "host": dict(
            removed_at_date="2020-12-01",
            removed_from_collection="ansible.netcommon",
        ),
        "port": dict(
            removed_at_date="2020-12-01",
            removed_from_collection="ansible.netcommon",
            type="int",
            default=830,
        ),
        "username": dict(
            fallback=(env_fallback, ["ANSIBLE_NET_USERNAME"]),
            removed_at_date="2020-12-01",
            removed_from_collection="ansible.netcommon",
            no_log=True,
        ),
        "password": dict(
            fallback=(env_fallback, ["ANSIBLE_NET_PASSWORD"]),
            removed_at_date="2020-12-01",
            removed_from_collection="ansible.netcommon",
            no_log=True,
        ),
        "ssh_keyfile": dict(
            fallback=(env_fallback, ["ANSIBLE_NET_SSH_KEYFILE"]),
            removed_at_date="2020-12-01",
            removed_from_collection="ansible.netcommon",
            type="path",
        ),
        "hostkey_verify": dict(
            removed_at_date="2020-12-01",
            removed_from_collection="ansible.netcommon",
            type="bool",
            default=True,
        ),
        "look_for_keys": dict(
            removed_at_date="2020-12-01",
            removed_from_collection="ansible.netcommon",
            type="bool",
            default=True,
        ),
        "timeout": dict(
            removed_at_date="2020-12-01",
            removed_from_collection="ansible.netcommon",
            type="int",
            default=10,
        ),
    }
    argument_spec.update(netconf_top_spec)

    mutually_exclusive = [
        ("content", "src", "source_datastore", "delete", "confirm_commit")
    ]
    required_one_of = [
        ("content", "src", "source_datastore", "delete", "confirm_commit")
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=required_one_of,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )

    config = module.params["content"] or module.params["src"]
    target = module.params["target"]
    lock = module.params["lock"]
    source = module.params["source_datastore"]
    delete = module.params["delete"]
    confirm_commit = module.params["confirm_commit"]
    confirm = module.params["confirm"]
    validate = module.params["validate"]
    save = module.params["save"]
    filter = module.params["get_filter"]
    format = module.params["format"]

    try:
        filter_data, filter_type = validate_and_normalize_data(filter)
    except Exception as exc:
        module.fail_json(msg=to_text(exc))

    if filter_type:
        if filter_type == "xml":
            filter_type = "subtree"
        elif filter_type == "json":
            try:
                filter = dict_to_xml(filter_data)
            except Exception as exc:
                module.fail_json(msg=to_text(exc))
            filter_type = "subtree"
        elif filter_type == "xpath":
            pass
        else:
            module.fail_json(
                msg="Invalid filter type detected %s for get_filter value %s"
                % (filter_type, filter)
            )

    conn = Connection(module._socket_path)
    capabilities = get_capabilities(module)
    operations = capabilities["device_operations"]

    supports_commit = operations.get("supports_commit", False)
    supports_writable_running = operations.get(
        "supports_writable_running", False
    )
    supports_startup = operations.get("supports_startup", False)

    # identify target datastore
    if target == "candidate" and not supports_commit:
        module.fail_json(
            msg=":candidate is not supported by this netconf server"
        )
    elif target == "running" and not supports_writable_running:
        module.fail_json(
            msg=":writable-running is not supported by this netconf server"
        )
    elif target == "auto":
        if supports_commit:
            target = "candidate"
        elif supports_writable_running:
            target = "running"
        else:
            module.fail_json(
                msg="neither :candidate nor :writable-running are supported by this netconf server"
            )

    # Netconf server capability validation against input options
    if save and not supports_startup:
        module.fail_json(
            msg="cannot copy <%s/> to <startup/>, while :startup is not supported"
            % target
        )

    if confirm_commit and not operations.get("supports_confirm_commit", False):
        module.fail_json(
            msg="confirm commit is not supported by Netconf server"
        )

    if (confirm > 0) and not operations.get("supports_confirm_commit", False):
        module.fail_json(
            msg="confirm commit is not supported by this netconf server, given confirm timeout: %d"
            % confirm
        )

    if validate and not operations.get("supports_validate", False):
        module.fail_json(
            msg="validate is not supported by this netconf server"
        )

    if filter_type == "xpath" and not operations.get("supports_xpath", False):
        module.fail_json(
            msg="filter value '%s' of type xpath is not supported on this device"
            % filter
        )

    filter_spec = (filter_type, filter) if filter_type else None

    if lock == "never":
        execute_lock = False
    elif target in operations.get("lock_datastore", []):
        # lock is requested (always/if-support) and supported => lets do it
        execute_lock = True
    else:
        # lock is requested (always/if-supported) but not supported => issue warning
        module.warn(
            "lock operation on '%s' source is not supported on this device"
            % target
        )
        execute_lock = lock == "always"

    result = {
        "changed": False,
        "server_capabilities": capabilities.get("server_capabilities", []),
    }
    before = None
    after = None
    locked = False
    try:
        if module.params["backup"]:
            response = get_config(
                module, target, filter_spec, lock=execute_lock
            )
            before = to_text(
                tostring(response), errors="surrogate_then_replace"
            ).strip()
            result["__backup__"] = before.strip()
        if validate:
            conn.validate(target)
        if source:
            if not module.check_mode:
                conn.copy(source, target)
            result["changed"] = True
        elif delete:
            if not module.check_mode:
                conn.delete(target)
            result["changed"] = True
        elif confirm_commit:
            if not module.check_mode:
                conn.commit()
            result["changed"] = True
        elif config:
            if module.check_mode and not supports_commit:
                module.warn(
                    "check mode not supported as Netconf server doesn't support candidate capability"
                )
                result["changed"] = True
                module.exit_json(**result)

            if execute_lock:
                conn.lock(target=target)
                locked = True
            if before is None:
                before = to_text(
                    conn.get_config(source=target, filter=filter_spec),
                    errors="surrogate_then_replace",
                ).strip()

            if format != "text":
                # check for format of type json/xml/xpath
                try:
                    config_obj, config_format = validate_and_normalize_data(
                        config, format
                    )
                except Exception as exc:
                    module.fail_json(msg=to_text(exc))

                if config_format == "json":
                    try:
                        config = dict_to_xml(config_obj)
                    except Exception as exc:
                        module.fail_json(msg=to_text(exc))
                    format = "xml"
                elif config_format is None:
                    format = "xml"
                else:
                    format = config_format

            validate_config(module, config, format)

            kwargs = {
                "config": config,
                "target": target,
                "default_operation": module.params["default_operation"],
                "error_option": module.params["error_option"],
                "format": format,
            }

            conn.edit_config(**kwargs)

            if supports_commit and module.params["commit"]:
                after = to_text(
                    conn.get_config(source="candidate", filter=filter_spec),
                    errors="surrogate_then_replace",
                ).strip()
                if not module.check_mode:
                    confirm_timeout = confirm if confirm > 0 else None
                    confirmed_commit = True if confirm_timeout else False
                    conn.commit(
                        confirmed=confirmed_commit, timeout=confirm_timeout
                    )
                else:
                    conn.discard_changes()

            if after is None:
                after = to_text(
                    conn.get_config(source="running", filter=filter_spec),
                    errors="surrogate_then_replace",
                ).strip()

            sanitized_before = sanitize_xml(before)
            sanitized_after = sanitize_xml(after)
            if sanitized_before != sanitized_after:
                result["changed"] = True

            if result["changed"]:
                if save and not module.check_mode:
                    conn.copy_config(target, "startup")
                if module._diff:
                    result["diff"] = {
                        "before": sanitized_before,
                        "after": sanitized_after,
                    }

    except ConnectionError as e:
        module.fail_json(
            msg=to_text(e, errors="surrogate_then_replace").strip()
        )
    finally:
        if locked:
            conn.unlock(target=target)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
