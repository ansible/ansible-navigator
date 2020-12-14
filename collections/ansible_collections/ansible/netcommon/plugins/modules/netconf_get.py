#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2018, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: netconf_get
author:
- Ganesh Nalawade (@ganeshrn)
- Sven Wisotzky (@wisotzky)
short_description: Fetch configuration/state data from NETCONF enabled network devices.
description:
- NETCONF is a network management protocol developed and standardized by the IETF.
  It is documented in RFC 6241.
- This module allows the user to fetch configuration and state data from NETCONF enabled
  network devices.
version_added: 1.0.0
extends_documentation_fragment:
- ansible.netcommon.network_agnostic
options:
  source:
    description:
    - This argument specifies the datastore from which configuration data should be
      fetched. Valid values are I(running), I(candidate) and I(startup). If the C(source)
      value is not set both configuration and state information are returned in response
      from running datastore.
    type: str
    choices:
    - running
    - candidate
    - startup
  filter:
    description:
    - This argument specifies the string which acts as a filter to restrict the
      portions of the data to be are retrieved from the remote device. If this option
      is not specified entire configuration or state data is returned in result depending
      on the value of C(source) option. The C(filter) value can be either XML string
      or XPath or JSON string or native python dictionary, if the filter is in XPath
      format the NETCONF server running on remote host should support xpath capability
      else it will result in an error. If the filter is in JSON format the xmltodict library
      should be installed on the control node for JSON to XML conversion.
    type: raw
  display:
    description:
    - Encoding scheme to use when serializing output from the device. The option I(json)
      will serialize the output as JSON data. If the option value is I(json) it requires
      jxmlease to be installed on control node. The option I(pretty) is similar to
      received XML response but is using human readable format (spaces, new lines).
      The option value I(xml) is similar to received XML response but removes all
      XML namespaces.
    type: str
    choices:
    - json
    - pretty
    - xml
    - native
  lock:
    description:
    - Instructs the module to explicitly lock the datastore specified as C(source).
      If no I(source) is defined, the I(running) datastore will be locked. By setting
      the option value I(always) is will explicitly lock the datastore mentioned in
      C(source) option. By setting the option value I(never) it will not lock the
      C(source) datastore. The value I(if-supported) allows better interworking with
      NETCONF servers, which do not support the (un)lock operation for all supported
      datastores.
    type: str
    default: never
    choices:
    - never
    - always
    - if-supported
requirements:
- ncclient (>=v0.5.2)
- jxmlease (for display=json)
- xmltodict (for display=native)
notes:
- This module requires the NETCONF system service be enabled on the remote device
  being managed.
- This module supports the use of connection=netconf
"""

EXAMPLES = """
- name: Get running configuration and state data
  ansible.netcommon.netconf_get:

- name: Get configuration and state data from startup datastore
  ansible.netcommon.netconf_get:
    source: startup

- name: Get system configuration data from running datastore state (junos)
  ansible.netcommon.netconf_get:
    source: running
    filter: <configuration><system></system></configuration>

- name: Get configuration and state data in JSON format
  ansible.netcommon.netconf_get:
    display: json

- name: get schema list using subtree w/ namespaces
  ansible.netcommon.netconf_get:
    display: json
    filter: <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring"><schemas><schema/></schemas></netconf-state>
    lock: never

- name: get schema list using xpath
  ansible.netcommon.netconf_get:
    display: xml
    filter: /netconf-state/schemas/schema

- name: get interface configuration with filter (iosxr)
  ansible.netcommon.netconf_get:
    display: pretty
    filter: <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"></interface-configurations>
    lock: if-supported

- name: Get system configuration data from running datastore state (junos)
  ansible.netcommon.netconf_get:
    source: running
    filter: <configuration><system></system></configuration>
    lock: if-supported

- name: Get complete configuration data from running datastore (SROS)
  ansible.netcommon.netconf_get:
    source: running
    filter: <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf"/>

- name: Get complete state data (SROS)
  ansible.netcommon.netconf_get:
    filter: <state xmlns="urn:nokia.com:sros:ns:yang:sr:state"/>

- name: "get configuration with json filter string and native output (using xmltodict)"
  netconf_get:
    filter: |
              {
                  "interface-configurations": {
                      "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
                      "interface-configuration": null
                  }
              }
    display: native

- name: Define the Cisco IOSXR interface filter
  set_fact:
    filter:
      interface-configurations:
        "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"
        interface-configuration: null

- name: "get configuration with native filter type using set_facts"
  ansible.netcommon.netconf_get:
    filter: "{{ filter }}"
    display: native
  register: result

- name: "get configuration with direct native filter type"
  ansible.netcommon.netconf_get:
    filter: {
            "interface-configurations": {
            "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
            "interface-configuration": null
      }
    }
    display: native
  register: result


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
stdout:
  description: The raw XML string containing configuration or state data
               received from the underlying ncclient library.
  returned: always apart from low-level errors (such as action plugin)
  type: str
  sample: '...'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low-level errors (such as action plugin)
  type: list
  sample: ['...', '...']
output:
  description: Based on the value of display option will return either the set of
               transformed XML to JSON format from the RPC response with type dict
               or pretty XML string response (human-readable) or response with
               namespace removed from XML string.
  returned: If the display format is selected as I(json) it is returned as dict type
            and the conversion is done using jxmlease python library. If the display
            format is selected as I(native) it is returned as dict type and the conversion
            is done using xmltodict python library. If the display format is xml or pretty
            it is returned as a string apart from low-level errors (such as action plugin).
  type: complex
  contains:
    formatted_output:
      description:
        - Contains formatted response received from remote host as per the value in display format.
      type: str
"""
try:
    from lxml.etree import tostring
except ImportError:
    from xml.etree.ElementTree import tostring

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.netconf.netconf import (
    get_capabilities,
    get_config,
    get,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.netconf import (
    remove_namespaces,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.utils.data import (
    validate_and_normalize_data,
    xml_to_dict,
    dict_to_xml,
)
from ansible.module_utils._text import to_text

try:
    import jxmlease

    HAS_JXMLEASE = True
except ImportError:
    HAS_JXMLEASE = False


def main():
    """entry point for module execution
    """
    argument_spec = dict(
        source=dict(choices=["running", "candidate", "startup"]),
        filter=dict(type="raw"),
        display=dict(choices=["json", "pretty", "xml", "native"]),
        lock=dict(
            default="never", choices=["never", "always", "if-supported"]
        ),
    )

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    capabilities = get_capabilities(module)
    operations = capabilities["device_operations"]

    source = module.params["source"]
    filter = module.params["filter"]

    try:
        filter_data, filter_type = validate_and_normalize_data(filter)
    except Exception as exc:
        module.fail_json(msg=to_text(exc))

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
    elif (filter_type is None) and (filter_data is not None):
        # to maintain backward compatibility for ansible 2.9 which
        # defaults to "subtree" filter type
        filter_type = "subtree"
    elif filter_type:
        module.fail_json(
            msg="Invalid filter type detected %s for filter value %s"
            % (filter_type, filter)
        )

    lock = module.params["lock"]
    display = module.params["display"]

    if source == "candidate" and not operations.get("supports_commit", False):
        module.fail_json(
            msg="candidate source is not supported on this device"
        )

    if source == "startup" and not operations.get("supports_startup", False):
        module.fail_json(msg="startup source is not supported on this device")

    if filter_type == "xpath" and not operations.get("supports_xpath", False):
        module.fail_json(
            msg="filter value '%s' of type xpath is not supported on this device"
            % filter
        )

    # If source is None, NETCONF <get> operation is issued, reading config/state data
    # from the running datastore. The python expression "(source or 'running')" results
    # in the value of source (if not None) or the value 'running' (if source is None).

    if lock == "never":
        execute_lock = False
    elif (source or "running") in operations.get("lock_datastore", []):
        # lock is requested (always/if-support) and supported => lets do it
        execute_lock = True
    else:
        # lock is requested (always/if-supported) but not supported => issue warning
        module.warn(
            "lock operation on '%s' source is not supported on this device"
            % (source or "running")
        )
        execute_lock = lock == "always"

    if display == "json" and not HAS_JXMLEASE:
        module.fail_json(
            msg="jxmlease is required to display response in json format"
            "but does not appear to be installed. "
            "It can be installed using `pip install jxmlease`"
        )

    filter_spec = (filter_type, filter) if filter_type else None

    if source is not None:
        response = get_config(module, source, filter_spec, execute_lock)
    else:
        response = get(module, filter_spec, execute_lock)

    xml_resp = to_text(tostring(response))
    output = None

    if display == "xml":
        output = remove_namespaces(xml_resp)
    elif display == "json":
        try:
            output = jxmlease.parse(xml_resp)
        except Exception:
            raise ValueError(xml_resp)
    elif display == "pretty":
        output = to_text(tostring(response, pretty_print=True))
    elif display == "native":
        try:
            output = xml_to_dict(xml_resp)
        except Exception as exc:
            module.fail_json(msg=to_text(exc))

    result = {"stdout": xml_resp, "output": output}

    module.exit_json(**result)


if __name__ == "__main__":
    main()
