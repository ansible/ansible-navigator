

# Arista EOS Collection
[![CI](https://zuul-ci.org/gated.svg)](https://dashboard.zuul.ansible.com/t/ansible/project/github.com/ansible-collections/arista.eos) <!--[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/vyos)](https://codecov.io/gh/ansible-collections/arista.eos)-->

The Ansible Arista EOS collection includes a variety of Ansible content to help automate the management of Arista EOS network appliances.

This collection has been tested against Arista EOS 4.20.10M.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10,<2.11**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

### Supported connections
The Arista EOS collection supports ``network_cli``  and ``httpapi`` connections.

## Included content

<!--start collection content-->
### Cliconf plugins
Name | Description
--- | ---
[arista.eos.eos](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_cliconf.rst)|Use eos cliconf to run command on Arista EOS platform

### Filter plugins
Name | Description
--- | ---

### Httpapi plugins
Name | Description
--- | ---
[arista.eos.eos](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_httpapi.rst)|Use eAPI to run command on eos platform

### Inventory plugins
Name | Description
--- | ---

### Modules
Name | Description
--- | ---
[arista.eos.eos_acl_interfaces](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_acl_interfaces_module.rst)|ACL interfaces resource module
[arista.eos.eos_acls](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_acls_module.rst)|ACLs resource module
[arista.eos.eos_banner](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_banner_module.rst)|Manage multiline banners on Arista EOS devices
[arista.eos.eos_bgp](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_bgp_module.rst)|Configure global BGP protocol settings on Arista EOS.
[arista.eos.eos_command](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_command_module.rst)|Run arbitrary commands on an Arista EOS device
[arista.eos.eos_config](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_config_module.rst)|Manage Arista EOS configuration sections
[arista.eos.eos_eapi](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_eapi_module.rst)|Manage and configure Arista EOS eAPI.
[arista.eos.eos_facts](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_facts_module.rst)|Collect facts from remote devices running Arista EOS
[arista.eos.eos_interface](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_interface_module.rst)|(deprecated, removed after 2022-06-01) Manage Interface on Arista EOS network devices
[arista.eos.eos_interfaces](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_interfaces_module.rst)|Interfaces resource module
[arista.eos.eos_l2_interface](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_l2_interface_module.rst)|(deprecated, removed after 2022-06-01) Manage L2 interfaces on Arista EOS network devices.
[arista.eos.eos_l2_interfaces](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_l2_interfaces_module.rst)|L2 interfaces resource module
[arista.eos.eos_l3_interface](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_l3_interface_module.rst)|(deprecated, removed after 2022-06-01) Manage L3 interfaces on Arista EOS network devices.
[arista.eos.eos_l3_interfaces](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_l3_interfaces_module.rst)|L3 interfaces resource module
[arista.eos.eos_lacp](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_lacp_module.rst)|LACP resource module
[arista.eos.eos_lacp_interfaces](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_lacp_interfaces_module.rst)|LACP interfaces resource module
[arista.eos.eos_lag_interfaces](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_lag_interfaces_module.rst)|LAG interfaces resource module
[arista.eos.eos_linkagg](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_linkagg_module.rst)|(deprecated, removed after 2022-06-01) Manage link aggregation groups on Arista EOS network devices
[arista.eos.eos_lldp](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_lldp_module.rst)|Manage LLDP configuration on Arista EOS network devices
[arista.eos.eos_lldp_global](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_lldp_global_module.rst)|LLDP resource module
[arista.eos.eos_lldp_interfaces](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_lldp_interfaces_module.rst)|LLDP interfaces resource module
[arista.eos.eos_logging](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_logging_module.rst)|Manage logging on network devices
[arista.eos.eos_ospf_interfaces](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_ospf_interfaces_module.rst)|OSPF Interfaces Resource Module.
[arista.eos.eos_ospfv2](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_ospfv2_module.rst)|OSPFv2 resource module
[arista.eos.eos_ospfv3](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_ospfv3_module.rst)|OSPFv3 resource module
[arista.eos.eos_static_route](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_static_route_module.rst)|(deprecated, removed after 2022-06-01) Manage static IP routes on Arista EOS network devices
[arista.eos.eos_static_routes](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_static_routes_module.rst)|Static routes resource module
[arista.eos.eos_system](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_system_module.rst)|Manage the system attributes on Arista EOS devices
[arista.eos.eos_user](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_user_module.rst)|Manage the collection of local users on EOS devices
[arista.eos.eos_vlan](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_vlan_module.rst)|(deprecated, removed after 2022-06-01) Manage VLANs on Arista EOS network devices
[arista.eos.eos_vlans](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_vlans_module.rst)|VLANs resource module
[arista.eos.eos_vrf](https://github.com/ansible-collections/arista.eos/blob/main/docs/arista.eos.eos_vrf_module.rst)|Manage VRFs on Arista EOS network devices

<!--end collection content-->

Click the ``Content`` button to see the list of content included in this collection.

## Installing this collection

You can install the Arista EOS collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install arista.eos

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: arista.eos
```
## Using this collection


This collection includes [network resource modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html).

### Using modules from the Arista EOS collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `arista.eos.eos_l2_interfaces`.
The following example task replaces configuration changes in the existing configuration on a Arista EOS network device, using the FQCN:

```yaml
---
  - name: Replace device configuration of specified L2 interfaces with provided configuration.
    arista.eos.eos_l2_interfaces:
      config:
        - name: Ethernet1
          trunk:
            native_vlan: 20
            trunk_vlans: 5-10, 15
      state: replaced
```

**NOTE**: For Ansible 2.9, you may not see deprecation warnings when you run your playbooks with this collection. Use this documentation to track when a module is deprecated.

### See Also:

* [Arista EOS Platform Options](https://docs.ansible.com/ansible/latest/network/user_guide/platform_eos.html)
* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Arista EOS collection repository](https://github.com/ansible-collections/arista.eos). See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for complete details.

You can also join us on:

- Freenode IRC - ``#ansible-network`` Freenode channel
- Slack - https://ansiblenetwork.slack.com

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.

### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Changelogs
<!--Add a link to a changelog.md file or an external docsite to cover this information. -->
## Release notes

Release notes are available [here](https://github.com/ansible-collections/arista.eos/blob/main/changelogs/CHANGELOG.rst).

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
