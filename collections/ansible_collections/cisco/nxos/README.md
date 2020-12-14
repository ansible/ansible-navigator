

# Cisco NX-OS Collection
[![CI](https://zuul-ci.org/gated.svg)](https://dashboard.zuul.ansible.com/t/ansible/project/github.com/ansible-collections/cisco.nxos) <!--[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/vyos)](https://codecov.io/gh/ansible-collections/cisco.nxos)-->

The Ansible Cisco NX-OS collection includes a variety of Ansible content to help automate the management of Cisco NX-OS network appliances.

The Cisco NX-OS connection plugins combined with Cisco NX-OS resource modules aligns the Cisco NX-OS experience with the other core networking platforms supported by Ansible.

This collection has been tested against Cisco NX-OS 7.0(3)I5(1) on Nexus Switches and NX-OS 8.4(1) on MDS Switches.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10,<2.11**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

### Supported connections
The Cisco NX-OS collection supports ``network_cli``  and ``httpapi`` connections.

## Included content
<!--start collection content-->
### Cliconf plugins
Name | Description
--- | ---
[cisco.nxos.nxos](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_cliconf.rst)|Use NX-OS cliconf to run commands on Cisco NX-OS platform

### Httpapi plugins
Name | Description
--- | ---
[cisco.nxos.nxos](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_httpapi.rst)|Use NX-API to run commands on Cisco NX-OS platform

### Modules
Name | Description
--- | ---
[cisco.nxos.nxos_aaa_server](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_aaa_server_module.rst)|Manages AAA server global configuration.
[cisco.nxos.nxos_aaa_server_host](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_aaa_server_host_module.rst)|Manages AAA server host-specific configuration.
[cisco.nxos.nxos_acl](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_acl_module.rst)|(deprecated, removed after 2022-06-01) Manages access list entries for ACLs.
[cisco.nxos.nxos_acl_interface](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_acl_interface_module.rst)|(deprecated, removed after 2022-06-01) Manages applying ACLs to interfaces.
[cisco.nxos.nxos_acl_interfaces](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_acl_interfaces_module.rst)|ACL interfaces resource module
[cisco.nxos.nxos_acls](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_acls_module.rst)|ACLs resource module
[cisco.nxos.nxos_banner](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_banner_module.rst)|Manage multiline banners on Cisco NXOS devices
[cisco.nxos.nxos_bfd_global](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_bfd_global_module.rst)|Bidirectional Forwarding Detection (BFD) global-level configuration
[cisco.nxos.nxos_bfd_interfaces](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_bfd_interfaces_module.rst)|BFD interfaces resource module
[cisco.nxos.nxos_bgp](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_bgp_module.rst)|Manages BGP configuration.
[cisco.nxos.nxos_bgp_af](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_bgp_af_module.rst)|Manages BGP Address-family configuration.
[cisco.nxos.nxos_bgp_neighbor](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_bgp_neighbor_module.rst)|Manages BGP neighbors configurations.
[cisco.nxos.nxos_bgp_neighbor_af](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_bgp_neighbor_af_module.rst)|Manages BGP address-family's neighbors configuration.
[cisco.nxos.nxos_command](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_command_module.rst)|Run arbitrary command on Cisco NXOS devices
[cisco.nxos.nxos_config](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_config_module.rst)|Manage Cisco NXOS configuration sections
[cisco.nxos.nxos_devicealias](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_devicealias_module.rst)|Configuration of device alias.
[cisco.nxos.nxos_evpn_global](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_evpn_global_module.rst)|Handles the EVPN control plane for VXLAN.
[cisco.nxos.nxos_evpn_vni](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_evpn_vni_module.rst)|Manages Cisco EVPN VXLAN Network Identifier (VNI).
[cisco.nxos.nxos_facts](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_facts_module.rst)|Gets facts about NX-OS switches
[cisco.nxos.nxos_feature](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_feature_module.rst)|Manage features in NX-OS switches.
[cisco.nxos.nxos_file_copy](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_file_copy_module.rst)|Copy a file to a remote NXOS device.
[cisco.nxos.nxos_gir](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_gir_module.rst)|Trigger a graceful removal or insertion (GIR) of the switch.
[cisco.nxos.nxos_gir_profile_management](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_gir_profile_management_module.rst)|Create a maintenance-mode or normal-mode profile for GIR.
[cisco.nxos.nxos_hsrp](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_hsrp_module.rst)|Manages HSRP configuration on NX-OS switches.
[cisco.nxos.nxos_hsrp_interfaces](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_hsrp_interfaces_module.rst)|HSRP interfaces resource module
[cisco.nxos.nxos_igmp](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_igmp_module.rst)|Manages IGMP global configuration.
[cisco.nxos.nxos_igmp_interface](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_igmp_interface_module.rst)|Manages IGMP interface configuration.
[cisco.nxos.nxos_igmp_snooping](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_igmp_snooping_module.rst)|Manages IGMP snooping global configuration.
[cisco.nxos.nxos_install_os](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_install_os_module.rst)|Set boot options like boot, kickstart image and issu.
[cisco.nxos.nxos_interface](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_interface_module.rst)|(deprecated, removed after 2022-06-01) Manages physical attributes of interfaces.
[cisco.nxos.nxos_interface_ospf](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_interface_ospf_module.rst)|(deprecated, removed after 2022-10-26) Manages configuration of an OSPF interface instance.
[cisco.nxos.nxos_interfaces](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_interfaces_module.rst)|Interfaces resource module
[cisco.nxos.nxos_l2_interface](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_l2_interface_module.rst)|(deprecated, removed after 2022-06-01) Manage Layer-2 interface on Cisco NXOS devices.
[cisco.nxos.nxos_l2_interfaces](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_l2_interfaces_module.rst)|L2 interfaces resource module
[cisco.nxos.nxos_l3_interface](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_l3_interface_module.rst)|(deprecated, removed after 2022-06-01) Manage L3 interfaces on Cisco NXOS network devices
[cisco.nxos.nxos_l3_interfaces](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_l3_interfaces_module.rst)|L3 interfaces resource module
[cisco.nxos.nxos_lacp](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_lacp_module.rst)|LACP resource module
[cisco.nxos.nxos_lacp_interfaces](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_lacp_interfaces_module.rst)|LACP interfaces resource module
[cisco.nxos.nxos_lag_interfaces](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_lag_interfaces_module.rst)|LAG interfaces resource module
[cisco.nxos.nxos_linkagg](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_linkagg_module.rst)|(deprecated, removed after 2022-06-01) Manage link aggregation groups on Cisco NXOS devices.
[cisco.nxos.nxos_lldp](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_lldp_module.rst)|(deprecated, removed after 2022-06-01) Manage LLDP configuration on Cisco NXOS network devices.
[cisco.nxos.nxos_lldp_global](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_lldp_global_module.rst)|LLDP resource module
[cisco.nxos.nxos_lldp_interfaces](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_lldp_interfaces_module.rst)|LLDP interfaces resource module
[cisco.nxos.nxos_logging](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_logging_module.rst)|Manage logging on network devices
[cisco.nxos.nxos_ntp](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_ntp_module.rst)|Manages core NTP configuration.
[cisco.nxos.nxos_ntp_auth](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_ntp_auth_module.rst)|Manages NTP authentication.
[cisco.nxos.nxos_ntp_options](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_ntp_options_module.rst)|Manages NTP options.
[cisco.nxos.nxos_nxapi](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_nxapi_module.rst)|Manage NXAPI configuration on an NXOS device.
[cisco.nxos.nxos_ospf](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_ospf_module.rst)|(deprecated, removed after 2022-06-01) Manages configuration of an ospf instance.
[cisco.nxos.nxos_ospf_interfaces](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_ospf_interfaces_module.rst)|OSPF Interfaces Resource Module.
[cisco.nxos.nxos_ospf_vrf](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_ospf_vrf_module.rst)|(deprecated, removed after 2022-10-01)Manages a VRF for an OSPF router.
[cisco.nxos.nxos_ospfv2](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_ospfv2_module.rst)|OSPFv2 resource module
[cisco.nxos.nxos_ospfv3](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_ospfv3_module.rst)|OSPFv3 resource module
[cisco.nxos.nxos_overlay_global](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_overlay_global_module.rst)|Configures anycast gateway MAC of the switch.
[cisco.nxos.nxos_pim](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_pim_module.rst)|Manages configuration of a PIM instance.
[cisco.nxos.nxos_pim_interface](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_pim_interface_module.rst)|Manages PIM interface configuration.
[cisco.nxos.nxos_pim_rp_address](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_pim_rp_address_module.rst)|Manages configuration of an PIM static RP address instance.
[cisco.nxos.nxos_ping](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_ping_module.rst)|Tests reachability using ping from Nexus switch.
[cisco.nxos.nxos_reboot](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_reboot_module.rst)|Reboot a network device.
[cisco.nxos.nxos_rollback](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_rollback_module.rst)|Set a checkpoint or rollback to a checkpoint.
[cisco.nxos.nxos_rpm](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_rpm_module.rst)|Install patch or feature rpms on Cisco NX-OS devices.
[cisco.nxos.nxos_smu](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_smu_module.rst)|(deprecated, removed after 2022-10-01) Perform SMUs on Cisco NX-OS devices.
[cisco.nxos.nxos_snapshot](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_snapshot_module.rst)|Manage snapshots of the running states of selected features.
[cisco.nxos.nxos_snmp_community](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_snmp_community_module.rst)|Manages SNMP community configs.
[cisco.nxos.nxos_snmp_contact](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_snmp_contact_module.rst)|Manages SNMP contact info.
[cisco.nxos.nxos_snmp_host](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_snmp_host_module.rst)|Manages SNMP host configuration.
[cisco.nxos.nxos_snmp_location](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_snmp_location_module.rst)|Manages SNMP location information.
[cisco.nxos.nxos_snmp_traps](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_snmp_traps_module.rst)|Manages SNMP traps.
[cisco.nxos.nxos_snmp_user](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_snmp_user_module.rst)|Manages SNMP users for monitoring.
[cisco.nxos.nxos_static_route](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_static_route_module.rst)|(deprecated, removed after 2022-06-01) Manages static route configuration
[cisco.nxos.nxos_static_routes](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_static_routes_module.rst)|Static routes resource module
[cisco.nxos.nxos_system](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_system_module.rst)|Manage the system attributes on Cisco NXOS devices
[cisco.nxos.nxos_telemetry](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_telemetry_module.rst)|TELEMETRY resource module
[cisco.nxos.nxos_udld](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_udld_module.rst)|Manages UDLD global configuration params.
[cisco.nxos.nxos_udld_interface](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_udld_interface_module.rst)|Manages UDLD interface configuration params.
[cisco.nxos.nxos_user](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_user_module.rst)|Manage the collection of local users on Nexus devices
[cisco.nxos.nxos_vlan](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vlan_module.rst)|(deprecated, removed after 2022-06-01) Manages VLAN resources and attributes.
[cisco.nxos.nxos_vlans](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vlans_module.rst)|VLANs resource module
[cisco.nxos.nxos_vpc](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vpc_module.rst)|Manages global VPC configuration
[cisco.nxos.nxos_vpc_interface](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vpc_interface_module.rst)|Manages interface VPC configuration
[cisco.nxos.nxos_vrf](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vrf_module.rst)|Manages global VRF configuration.
[cisco.nxos.nxos_vrf_af](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vrf_af_module.rst)|Manages VRF AF.
[cisco.nxos.nxos_vrf_interface](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vrf_interface_module.rst)|Manages interface specific VRF configuration.
[cisco.nxos.nxos_vrrp](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vrrp_module.rst)|Manages VRRP configuration on NX-OS switches.
[cisco.nxos.nxos_vsan](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vsan_module.rst)|Configuration of vsan.
[cisco.nxos.nxos_vtp_domain](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vtp_domain_module.rst)|Manages VTP domain configuration.
[cisco.nxos.nxos_vtp_password](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vtp_password_module.rst)|Manages VTP password configuration.
[cisco.nxos.nxos_vtp_version](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vtp_version_module.rst)|Manages VTP version configuration.
[cisco.nxos.nxos_vxlan_vtep](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vxlan_vtep_module.rst)|Manages VXLAN Network Virtualization Endpoint (NVE).
[cisco.nxos.nxos_vxlan_vtep_vni](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_vxlan_vtep_vni_module.rst)|Creates a Virtual Network Identifier member (VNI)
[cisco.nxos.nxos_zone_zoneset](https://github.com/ansible-collections/nxos/blob/main/docs/cisco.nxos.nxos_zone_zoneset_module.rst)|Configuration of zone/zoneset.

<!--end collection content-->

Click the ``Content`` button to see the list of content included in this collection.

## Installing this collection

You can install the Cisco NX-OS collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install cisco.nxos

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: cisco.nxos
```
## Using this collection


This collection includes [network resource modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html).

### Using modules from the Cisco NX-OS collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `cisco.nxos.nxos_l2_interfaces`.
The following example task replaces configuration changes in the existing configuration on a Cisco NX-OS network device, using the FQCN:

```yaml
---
  - name: Replace device configuration of specified L2 interfaces with provided configuration.
    cisco.nxos.nxos_l2_interfaces:
      config:
        - name: Ethernet1/1
          trunk:
            native_vlan: 20
            trunk_vlans: 5-10, 15
      state: replaced

```

**NOTE**: For Ansible 2.9, you may not see deprecation warnings when you run your playbooks with this collection. Use this documentation to track when a module is deprecated.


### See Also:

* [Cisco NX-OS Platform Options](https://docs.ansible.com/ansible/latest/network/user_guide/platform_nxos.html)
* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

Ongoing development efforts and contributions to this collection are solely focused on enhancements to current resource modules, additional resource modules and enhancements to connection plugins.

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Cisco NX-OS collection repository](https://github.com/ansible-collections/cisco.nxos).  See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for complete details.

You can also join us on:

- Freenode IRC - ``#ansible-network`` Freenode channel
- Slack - https://ansiblenetwork.slack.com

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.

### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.


## Release notes

Release notes are available [here](https://github.com/ansible-collections/cisco.nxos/blob/main/changelogs/CHANGELOG.rst).

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
