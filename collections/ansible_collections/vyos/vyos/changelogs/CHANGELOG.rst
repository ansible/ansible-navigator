=============================
Vyos Collection Release Notes
=============================

.. contents:: Topics


v1.1.0
======

Minor Changes
-------------

- Added ospf_interfaces resource module.

New Modules
-----------

- vyos_ospf_interfaces - OSPF Interfaces Resource Module


v1.0.5
======

Bugfixes
--------

- Added openvpn vtu interface support.
- Update network integration auth timeout for connection local.
- terminal plugin - Overhaul ansi_re to remove more escape sequences

v1.0.4
======

Minor Changes
-------------

- Moved intent testcases from integration suite to unit tests.
- Reformatted files with latest version of Black (20.8b1).

v1.0.3
======

Release Summary
---------------

- Rereleasing 1.0.2 with updated changelog.

v1.0.2
======

Minor Changes
-------------

- Fixed the typo in the modulename of ospfv2 and ospfv3 unit tests.
- Updated docs.
- terminal plugin - Added additional escape sequence to be removed from terminal output.

Bugfixes
--------

- Added workaround to avoid set_fact dynamically assigning value. This behavior seems to have been broken after ansible2.9.
- Make `src`, `backup` and `backup_options` in vyos_config work when module alias is used (https://github.com/ansible-collections/vyos.vyos/pull/67).
- vyos_config - fixed issue where config could be saved while in check mode (https://github.com/ansible-collections/vyos.vyos/pull/53)

v1.0.1
======

Minor Changes
-------------

- Add doc plugin fixes (https://github.com/ansible-collections/vyos.vyos/pull/51)

v1.0.0
======

New Plugins
-----------

Cliconf
~~~~~~~

- vyos - Use vyos cliconf to run command on VyOS platform

New Modules
-----------

- vyos_banner - Manage multiline banners on VyOS devices
- vyos_command - Run one or more commands on VyOS devices
- vyos_config - Manage VyOS configuration on remote device
- vyos_facts - Get facts about vyos devices.
- vyos_firewall_global - FIREWALL global resource module
- vyos_firewall_interfaces - FIREWALL interfaces resource module
- vyos_firewall_rules - FIREWALL rules resource module
- vyos_interface - (deprecated, removed after 2022-06-01) Manage Interface on VyOS network devices
- vyos_interfaces - Interfaces resource module
- vyos_l3_interface - (deprecated, removed after 2022-06-01) Manage L3 interfaces on VyOS network devices
- vyos_l3_interfaces - L3 interfaces resource module
- vyos_lag_interfaces - LAG interfaces resource module
- vyos_linkagg - (deprecated, removed after 2022-06-01) Manage link aggregation groups on VyOS network devices
- vyos_lldp - (deprecated, removed after 2022-06-01) Manage LLDP configuration on VyOS network devices
- vyos_lldp_global - LLDP global resource module
- vyos_lldp_interface - (deprecated, removed after 2022-06-01) Manage LLDP interfaces configuration on VyOS network devices
- vyos_lldp_interfaces - LLDP interfaces resource module
- vyos_logging - Manage logging on network devices
- vyos_ospfv2 - OSPFv2 resource module
- vyos_ospfv3 - OSPFV3 resource module
- vyos_ping - Tests reachability using ping from VyOS network devices
- vyos_static_route - (deprecated, removed after 2022-06-01) Manage static IP routes on Vyatta VyOS network devices
- vyos_static_routes - Static routes resource module
- vyos_system - Run `set system` commands on VyOS devices
- vyos_user - Manage the collection of local users on VyOS device
- vyos_vlan - Manage VLANs on VyOS network devices
