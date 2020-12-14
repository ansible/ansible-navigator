===================================
Cisco Nxos Collection Release Notes
===================================

.. contents:: Topics


v1.3.1
======

Bugfixes
--------

- Add version key to galaxy.yaml to work around ansible-galaxy bug
- Allow nxos_user to run with MDS (https://github.com/ansible-collections/cisco.nxos/issues/163).
- Fix for nxos_lag_interfaces issue (https://github.com/ansible-collections/cisco.nxos/pull/194).
- Make sure that the OSPF modules work properly when process_id is a string (https://github.com/ansible-collections/cisco.nxos/issues/198).

v1.3.0
======

Minor Changes
-------------

- Add nxos_ospf_interfaces resource module.

Deprecated Features
-------------------

- Deprecated `nxos_interface_ospf` in favor of `nxos_ospf_interfaces` Resource Module.

Bugfixes
--------

- Allow `fex-fabric` option for mode key (https://github.com/ansible-collections/cisco.nxos/issues/166).
- Fixes for nxos rpm issue (https://github.com/ansible-collections/cisco.nxos/pull/173).
- Update regex to accept the platform "N77" as supporting fabricpath.
- Vlan config diff was not removing default values

New Modules
-----------

- nxos_ospf_interfaces - OSPF Interfaces Resource Module.

v1.2.0
======

Minor Changes
-------------

- Add nxos_ospfv3 module.
- Allow other transfer protocols than scp to pull files from a NXOS device in nxos_file_copy module. sftp, http, https, tftp and ftp can be choosen as a transfer protocol, when the file_pull parameter is true..

Deprecated Features
-------------------

- Deprecated `nxos_smu` in favour of `nxos_rpm` module.
- The `nxos_ospf_vrf` module is deprecated by `nxos_ospfv2` and `nxos_ospfv3` Resource Modules.

Bugfixes
--------

- Correctly parse facts for lacp interfaces mode information (https://github.com/ansible-collections/cisco.nxos/pull/164).
- Fix for nxos smu issue (https://github.com/ansible-collections/cisco.nxos/pull/160).
- Fix regex for parsing configuration in nxos_lag_interfaces.
- Fix regexes in nxos_acl_interfaces facts and some code cleanup (https://github.com/ansible-collections/cisco.nxos/issues/149).
- Fix rendering of `log-adjacency-changes` commands.
- Preserve whitespaces in banner text (https://github.com/ansible-collections/cisco.nxos/pull/146).

New Modules
-----------

- nxos_ospfv3 - OSPFv3 resource module

v1.1.0
======

Minor Changes
-------------

- Add N9K multisite support(https://github.com/ansible-collections/cisco.nxos/pull/142)

Bugfixes
--------

- Allow facts round trip to work on nxos_vlans (https://github.com/ansible-collections/cisco.nxos/pull/141).

v1.0.2
======

Release Summary
---------------

Rereleased 1.0.1 with updated changelog.

v1.0.1
======

Minor Changes
-------------

- documentation - Use FQCN when refering to modules (https://github.com/ansible-collections/cisco.nxos/pull/116)

Bugfixes
--------

- Element type of `commands` key should be `raw` since it accepts both strings and dicts (https://github.com/ansible-collections/cisco.nxos/pull/126).
- Fix nxos_interfaces states replaced and overridden (https://github.com/ansible-collections/cisco.nxos/pull/102).
- Fixed force option in lag_interfaces.py (https://github.com/ansible-collections/cisco.nxos/pull/111).
- Make `src`, `backup` and `backup_options` in nxos_config work when module alias is used (https://github.com/ansible-collections/cisco.nxos/pull/121).
- Makes sure that docstring and argspec are in sync and removes sanity ignores (https://github.com/ansible-collections/cisco.nxos/pull/112).
- Update docs after sanity fixes to modules.
- nxos_user - do not fail when a custom role is used (https://github.com/ansible-collections/cisco.nxos/pull/130)

v1.0.0
======

New Plugins
-----------

Cliconf
~~~~~~~

- nxos - Use NX-OS cliconf to run commands on Cisco NX-OS platform

Httpapi
~~~~~~~

- nxos - Use NX-API to run commands on Cisco NX-OS platform

New Modules
-----------

- nxos_aaa_server - Manages AAA server global configuration.
- nxos_aaa_server_host - Manages AAA server host-specific configuration.
- nxos_acl - (deprecated, removed after 2022-06-01) Manages access list entries for ACLs.
- nxos_acl_interface - (deprecated, removed after 2022-06-01) Manages applying ACLs to interfaces.
- nxos_acl_interfaces - ACL interfaces resource module
- nxos_acls - ACLs resource module
- nxos_banner - Manage multiline banners on Cisco NXOS devices
- nxos_bfd_global - Bidirectional Forwarding Detection (BFD) global-level configuration
- nxos_bfd_interfaces - BFD interfaces resource module
- nxos_bgp - Manages BGP configuration.
- nxos_bgp_af - Manages BGP Address-family configuration.
- nxos_bgp_neighbor - Manages BGP neighbors configurations.
- nxos_bgp_neighbor_af - Manages BGP address-family's neighbors configuration.
- nxos_command - Run arbitrary command on Cisco NXOS devices
- nxos_config - Manage Cisco NXOS configuration sections
- nxos_evpn_global - Handles the EVPN control plane for VXLAN.
- nxos_evpn_vni - Manages Cisco EVPN VXLAN Network Identifier (VNI).
- nxos_facts - Gets facts about NX-OS switches
- nxos_feature - Manage features in NX-OS switches.
- nxos_file_copy - Copy a file to a remote NXOS device.
- nxos_gir - Trigger a graceful removal or insertion (GIR) of the switch.
- nxos_gir_profile_management - Create a maintenance-mode or normal-mode profile for GIR.
- nxos_hsrp - Manages HSRP configuration on NX-OS switches.
- nxos_hsrp_interfaces - HSRP interfaces resource module
- nxos_igmp - Manages IGMP global configuration.
- nxos_igmp_interface - Manages IGMP interface configuration.
- nxos_igmp_snooping - Manages IGMP snooping global configuration.
- nxos_install_os - Set boot options like boot, kickstart image and issu.
- nxos_interface - (deprecated, removed after 2022-06-01) Manages physical attributes of interfaces.
- nxos_interface_ospf - Manages configuration of an OSPF interface instance.
- nxos_interfaces - Interfaces resource module
- nxos_l2_interface - (deprecated, removed after 2022-06-01) Manage Layer-2 interface on Cisco NXOS devices.
- nxos_l2_interfaces - L2 interfaces resource module
- nxos_l3_interface - (deprecated, removed after 2022-06-01) Manage L3 interfaces on Cisco NXOS network devices
- nxos_l3_interfaces - L3 interfaces resource module
- nxos_lacp - LACP resource module
- nxos_lacp_interfaces - LACP interfaces resource module
- nxos_lag_interfaces - LAG interfaces resource module
- nxos_linkagg - (deprecated, removed after 2022-06-01) Manage link aggregation groups on Cisco NXOS devices.
- nxos_lldp - (deprecated, removed after 2022-06-01) Manage LLDP configuration on Cisco NXOS network devices.
- nxos_lldp_global - LLDP resource module
- nxos_lldp_interfaces - LLDP interfaces resource module
- nxos_logging - Manage logging on network devices
- nxos_ntp - Manages core NTP configuration.
- nxos_ntp_auth - Manages NTP authentication.
- nxos_ntp_options - Manages NTP options.
- nxos_nxapi - Manage NXAPI configuration on an NXOS device.
- nxos_ospf - (deprecated, removed after 2022-06-01) Manages configuration of an ospf instance.
- nxos_ospf_vrf - Manages a VRF for an OSPF router.
- nxos_ospfv2 - OSPFv2 resource module
- nxos_overlay_global - Configures anycast gateway MAC of the switch.
- nxos_pim - Manages configuration of a PIM instance.
- nxos_pim_interface - Manages PIM interface configuration.
- nxos_pim_rp_address - Manages configuration of an PIM static RP address instance.
- nxos_ping - Tests reachability using ping from Nexus switch.
- nxos_reboot - Reboot a network device.
- nxos_rollback - Set a checkpoint or rollback to a checkpoint.
- nxos_rpm - Install patch or feature rpms on Cisco NX-OS devices.
- nxos_smu - Perform SMUs on Cisco NX-OS devices.
- nxos_snapshot - Manage snapshots of the running states of selected features.
- nxos_snmp_community - Manages SNMP community configs.
- nxos_snmp_contact - Manages SNMP contact info.
- nxos_snmp_host - Manages SNMP host configuration.
- nxos_snmp_location - Manages SNMP location information.
- nxos_snmp_traps - Manages SNMP traps.
- nxos_snmp_user - Manages SNMP users for monitoring.
- nxos_static_route - (deprecated, removed after 2022-06-01) Manages static route configuration
- nxos_static_routes - Static routes resource module
- nxos_system - Manage the system attributes on Cisco NXOS devices
- nxos_telemetry - TELEMETRY resource module
- nxos_udld - Manages UDLD global configuration params.
- nxos_udld_interface - Manages UDLD interface configuration params.
- nxos_user - Manage the collection of local users on Nexus devices
- nxos_vlan - (deprecated, removed after 2022-06-01) Manages VLAN resources and attributes.
- nxos_vlans - VLANs resource module
- nxos_vpc - Manages global VPC configuration
- nxos_vpc_interface - Manages interface VPC configuration
- nxos_vrf - Manages global VRF configuration.
- nxos_vrf_af - Manages VRF AF.
- nxos_vrf_interface - Manages interface specific VRF configuration.
- nxos_vrrp - Manages VRRP configuration on NX-OS switches.
- nxos_vtp_domain - Manages VTP domain configuration.
- nxos_vtp_password - Manages VTP password configuration.
- nxos_vtp_version - Manages VTP version configuration.
- nxos_vxlan_vtep - Manages VXLAN Network Virtualization Endpoint (NVE).
- nxos_vxlan_vtep_vni - Creates a Virtual Network Identifier member (VNI)

Storage
~~~~~~~

- nxos_devicealias - Configuration of device alias.
- nxos_vsan - Configuration of vsan.
- nxos_zone_zoneset - Configuration of zone/zoneset.
