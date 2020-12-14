

# Ansible Network Collection for Common Code (netcommon)
[![CI](https://zuul-ci.org/gated.svg)](https://dashboard.zuul.ansible.com/t/ansible/builds?project=ansible-collections%2Fansible.netcommon) <!--[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/ansible.netcommon)](https://codecov.io/gh/ansible-collections/ansible.netcommon)-->

The Ansible ``ansible.netcommon`` collection includes common content to help automate the management of network, security, and cloud devices.
This includes  connection plugins, such as ``network_cli``, ``httpapi``, and ``netconf``.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10,<2.11**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## Included content

<!--start collection content-->
### Become plugins
Name | Description
--- | ---
[ansible.netcommon.enable](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.enable_become.rst)|Switch to elevated permissions on a network device

### Connection plugins
Name | Description
--- | ---
[ansible.netcommon.httpapi](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.httpapi_connection.rst)|Use httpapi to run command on network appliances
[ansible.netcommon.libssh](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.libssh_connection.rst)|(Tech preview) Run tasks using libssh for ssh connection
[ansible.netcommon.napalm](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.napalm_connection.rst)|Provides persistent connection using NAPALM
[ansible.netcommon.netconf](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.netconf_connection.rst)|Provides a persistent connection using the netconf protocol
[ansible.netcommon.network_cli](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.network_cli_connection.rst)|Use network_cli to run command on network appliances
[ansible.netcommon.persistent](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.persistent_connection.rst)|Use a persistent unix socket for connection

### Filter plugins
Name | Description
--- | ---
ansible.netcommon.cidr_merge|ansible.netcommon cidr_merge filter plugin
ansible.netcommon.comp_type5|ansible.netcommon comp_type5 filter plugin
ansible.netcommon.hash_salt|ansible.netcommon hash_salt filter plugin
ansible.netcommon.hwaddr|Check if string is a HW/MAC address and filter it
ansible.netcommon.ip4_hex|Convert an IPv4 address to Hexadecimal notation
ansible.netcommon.ipaddr|Check if string is an IP address or network and filter it
ansible.netcommon.ipmath|ansible.netcommon ipmath filter plugin
ansible.netcommon.ipsubnet|Manipulate IPv4/IPv6 subnets
ansible.netcommon.ipv4|ansible.netcommon ipv4 filter plugin
ansible.netcommon.ipv6|ansible.netcommon ipv6 filter plugin
ansible.netcommon.ipwrap|ansible.netcommon ipwrap filter plugin
ansible.netcommon.macaddr|ansible.netcommon macaddr filter plugin
ansible.netcommon.network_in_network|Checks whether the 'test' address or addresses are in 'value', including broadcast and network
ansible.netcommon.network_in_usable|Checks whether 'test' is a useable address or addresses in 'value'
ansible.netcommon.next_nth_usable|ansible.netcommon next_nth_usable filter plugin
ansible.netcommon.nthhost|Get the nth host within a given network
ansible.netcommon.parse_cli|ansible.netcommon parse_cli filter plugin
ansible.netcommon.parse_cli_textfsm|ansible.netcommon parse_cli_textfsm filter plugin
ansible.netcommon.parse_xml|ansible.netcommon parse_xml filter plugin
ansible.netcommon.previous_nth_usable|ansible.netcommon previous_nth_usable filter plugin
ansible.netcommon.reduce_on_network|Reduces a list of addresses to only the addresses that match a given network.
ansible.netcommon.slaac|Get the SLAAC address within given network
ansible.netcommon.type5_pw|ansible.netcommon type5_pw filter plugin
ansible.netcommon.vlan_parser|Input: Unsorted list of vlan integers

### Httpapi plugins
Name | Description
--- | ---
[ansible.netcommon.restconf](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.restconf_httpapi.rst)|HttpApi Plugin for devices supporting Restconf API

### Netconf plugins
Name | Description
--- | ---
[ansible.netcommon.default](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.default_netconf.rst)|Use default netconf plugin to run standard netconf commands as per RFC

### Modules
Name | Description
--- | ---
[ansible.netcommon.cli_command](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.cli_command_module.rst)|Run a cli command on cli-based network devices
[ansible.netcommon.cli_config](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.cli_config_module.rst)|Push text based configuration to network devices over network_cli
[ansible.netcommon.cli_parse](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.cli_parse_module.rst)|Parse cli output or text using a variety of parsers
[ansible.netcommon.net_banner](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_banner_module.rst)|(deprecated, removed after 2022-06-01) Manage multiline banners on network devices
[ansible.netcommon.net_get](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_get_module.rst)|Copy a file from a network device to Ansible Controller
[ansible.netcommon.net_interface](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_interface_module.rst)|(deprecated, removed after 2022-06-01) Manage Interface on network devices
[ansible.netcommon.net_l2_interface](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_l2_interface_module.rst)|(deprecated, removed after 2022-06-01) Manage Layer-2 interface on network devices
[ansible.netcommon.net_l3_interface](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_l3_interface_module.rst)|(deprecated, removed after 2022-06-01) Manage L3 interfaces on network devices
[ansible.netcommon.net_linkagg](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_linkagg_module.rst)|(deprecated, removed after 2022-06-01) Manage link aggregation groups on network devices
[ansible.netcommon.net_lldp](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_lldp_module.rst)|(deprecated, removed after 2022-06-01) Manage LLDP service configuration on network devices
[ansible.netcommon.net_lldp_interface](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_lldp_interface_module.rst)|(deprecated, removed after 2022-06-01) Manage LLDP interfaces configuration on network devices
[ansible.netcommon.net_logging](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_logging_module.rst)|(deprecated, removed after 2022-06-01) Manage logging on network devices
[ansible.netcommon.net_ping](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_ping_module.rst)|Tests reachability using ping from a network device
[ansible.netcommon.net_put](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_put_module.rst)|Copy a file from Ansible Controller to a network device
[ansible.netcommon.net_static_route](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_static_route_module.rst)|(deprecated, removed after 2022-06-01) Manage static IP routes on network appliances (routers, switches et. al.)
[ansible.netcommon.net_system](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_system_module.rst)|(deprecated, removed after 2022-06-01) Manage the system attributes on network devices
[ansible.netcommon.net_user](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_user_module.rst)|(deprecated, removed after 2022-06-01) Manage the aggregate of local users on network device
[ansible.netcommon.net_vlan](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_vlan_module.rst)|(deprecated, removed after 2022-06-01) Manage VLANs on network devices
[ansible.netcommon.net_vrf](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.net_vrf_module.rst)|(deprecated, removed after 2022-06-01) Manage VRFs on network devices
[ansible.netcommon.netconf_config](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.netconf_config_module.rst)|netconf device configuration
[ansible.netcommon.netconf_get](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.netconf_get_module.rst)|Fetch configuration/state data from NETCONF enabled network devices.
[ansible.netcommon.netconf_rpc](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.netconf_rpc_module.rst)|Execute operations on NETCONF enabled network devices.
[ansible.netcommon.restconf_config](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.restconf_config_module.rst)|Handles create, update, read and delete of configuration data on RESTCONF enabled devices.
[ansible.netcommon.restconf_get](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.restconf_get_module.rst)|Fetch configuration/state data from RESTCONF enabled devices.
[ansible.netcommon.telnet](https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.telnet_module.rst)|Executes a low-down and dirty telnet command

<!--end collection content-->


## Installing this collection

You can install the ``ansible.netcommon`` collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install ansible.netcommon

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: ansible.netcommon
```
## Using this collection

The most common use case for this collection is to include it as a dependency in a network device-specific collection. Use the Fully Qualified Collection Name (FQCN) when referring to content in this collection (for example, `ansible.netcommon.network_cli`).

See the [Vyos collection](https://github.com/ansible-collections/vyos) for an example of this.


**NOTE**: For Ansible 2.9, you may not see deprecation warnings when you run your playbooks with this collection. Use this documentation to track when a module is deprecated.

### See Also:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [ansible.netcommon collection repository](https://github.com/ansible-collections/ansible.netcommon). See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for complete details.

You can also join us on:

- Freenode IRC - ``#ansible-network`` Freenode channel
- Slack - https://ansiblenetwork.slack.com

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.

### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.


## Release notes
<!--Add a link to a changelog.md file or an external docsite to cover this information. -->
Release notes are available [here](https://github.com/ansible-collections/ansible.netcommon/blob/main/changelogs/CHANGELOG.rst)

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

- [Developing network resource modules](https://docs.ansible.com/ansible/latest/network/dev_guide/developing_resource_modules_network.html#developing-resource-modules)
- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
