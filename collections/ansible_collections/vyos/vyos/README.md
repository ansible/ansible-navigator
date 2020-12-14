

# VyOS Collection
[![CI](https://zuul-ci.org/gated.svg)](https://dashboard.zuul.ansible.com/t/ansible/project/github.com/ansible-collections/vyos) <!--[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/vyos)](https://codecov.io/gh/ansible-collections/vyos)-->

The Ansible VyOS collection includes a variety of Ansible content to help automate the management of VyOS network appliances.

This collection has been tested against VyOS 1.1.8 (helium).

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10,<2.11**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->


### Supported connections
The VyOS collection supports ``network_cli`` connections.

## Included content

<!--start collection content-->
### Cliconf plugins
Name | Description
--- | ---
[vyos.vyos.vyos](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_cliconf.rst)|Use vyos cliconf to run command on VyOS platform

### Filter plugins
Name | Description
--- | ---

### Inventory plugins
Name | Description
--- | ---

### Modules
Name | Description
--- | ---
[vyos.vyos.vyos_banner](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_banner_module.rst)|Manage multiline banners on VyOS devices
[vyos.vyos.vyos_command](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_command_module.rst)|Run one or more commands on VyOS devices
[vyos.vyos.vyos_config](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_config_module.rst)|Manage VyOS configuration on remote device
[vyos.vyos.vyos_facts](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_facts_module.rst)|Get facts about vyos devices.
[vyos.vyos.vyos_firewall_global](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_firewall_global_module.rst)|FIREWALL global resource module
[vyos.vyos.vyos_firewall_interfaces](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_firewall_interfaces_module.rst)|FIREWALL interfaces resource module
[vyos.vyos.vyos_firewall_rules](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_firewall_rules_module.rst)|FIREWALL rules resource module
[vyos.vyos.vyos_interface](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_interface_module.rst)|(deprecated, removed after 2022-06-01) Manage Interface on VyOS network devices
[vyos.vyos.vyos_interfaces](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_interfaces_module.rst)|Interfaces resource module
[vyos.vyos.vyos_l3_interface](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_l3_interface_module.rst)|(deprecated, removed after 2022-06-01) Manage L3 interfaces on VyOS network devices
[vyos.vyos.vyos_l3_interfaces](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_l3_interfaces_module.rst)|L3 interfaces resource module
[vyos.vyos.vyos_lag_interfaces](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_lag_interfaces_module.rst)|LAG interfaces resource module
[vyos.vyos.vyos_linkagg](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_linkagg_module.rst)|(deprecated, removed after 2022-06-01) Manage link aggregation groups on VyOS network devices
[vyos.vyos.vyos_lldp](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_lldp_module.rst)|(deprecated, removed after 2022-06-01) Manage LLDP configuration on VyOS network devices
[vyos.vyos.vyos_lldp_global](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_lldp_global_module.rst)|LLDP global resource module
[vyos.vyos.vyos_lldp_interface](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_lldp_interface_module.rst)|(deprecated, removed after 2022-06-01) Manage LLDP interfaces configuration on VyOS network devices
[vyos.vyos.vyos_lldp_interfaces](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_lldp_interfaces_module.rst)|LLDP interfaces resource module
[vyos.vyos.vyos_logging](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_logging_module.rst)|Manage logging on network devices
[vyos.vyos.vyos_ospf_interfaces](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_ospf_interfaces_module.rst)|OSPF Interfaces Resource Module.
[vyos.vyos.vyos_ospfv2](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_ospfv2_module.rst)|OSPFv2 resource module
[vyos.vyos.vyos_ospfv3](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_ospfv3_module.rst)|OSPFV3 resource module
[vyos.vyos.vyos_ping](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_ping_module.rst)|Tests reachability using ping from VyOS network devices
[vyos.vyos.vyos_static_route](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_static_route_module.rst)|(deprecated, removed after 2022-06-01) Manage static IP routes on Vyatta VyOS network devices
[vyos.vyos.vyos_static_routes](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_static_routes_module.rst)|Static routes resource module
[vyos.vyos.vyos_system](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_system_module.rst)|Run `set system` commands on VyOS devices
[vyos.vyos.vyos_user](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_user_module.rst)|Manage the collection of local users on VyOS device
[vyos.vyos.vyos_vlan](https://github.com/ansible-collections/vyos.vyos/blob/main/docs/vyos.vyos.vyos_vlan_module.rst)|Manage VLANs on VyOS network devices

<!--end collection content-->

Click the ``Content`` button to see the list of content included in this collection.

## Installing this collection

You can install the VyOS collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install vyos.vyos

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: vyos.vyos
```
## Using this collection


This collection includes [network resource modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html).

### Using modules from the VyOS collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `vyos.vyos.vyos_static_routes`.
The following example task replaces configuration changes in the existing configuration on a VyOS network device, using the FQCN:

```yaml
---
  - name: Replace device configurations of listed static routes with provided
      configurations
    register: result
    vyos.vyos.vyos_static_routes: &id001
      config:

        - address_families:

            - afi: ipv4
              routes:

                - dest: 192.0.2.32/28
                  blackhole_config:
                    distance: 2
                  next_hops:

                    - forward_router_address: 192.0.2.7

                    - forward_router_address: 192.0.2.8

                    - forward_router_address: 192.0.2.9
      state: replaced
```

**NOTE**: For Ansible 2.9, you may not see deprecation warnings when you run your playbooks with this collection. Use this documentation to track when a module is deprecated.



### See Also:

* [VyOS Platform Options](https://docs.ansible.com/ansible/latest/network/user_guide/platform_vyos.html)
* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [VyOS collection repository](https://github.com/ansible-collections/vyos). See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for complete details.

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

Release notes are available [here](https://github.com/ansible-collections/vyos.vyos/blob/main/changelogs/CHANGELOG.rst).

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
