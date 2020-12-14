==========================================
Ansible Netcommon Collection Release Notes
==========================================

.. contents:: Topics


v1.4.1
======

Release Summary
---------------

- Change how black config is specified to avoid issues with Automation Hub release process

v1.4.0
======

Minor Changes
-------------

- 'prefix' added to NetworkTemplate class, inorder to handle the negate operation for vyos config commands.
- Add support for json format input format for netconf modules using ``xmltodict``
- Update docs for netconf_get and netconf_config examples using display=native

Bugfixes
--------

- Added support for private key based authentication with libssh transport (https://github.com/ansible-collections/ansible.netcommon/issues/168)
- Fixed ipaddr filter plugins in ansible.netcommon collections is not working with latest Ansible (https://github.com/ansible-collections/ansible.netcommon/issues/157)
- Fixed netconf_rpc task fails due to encoding issue in the response (https://github.com/ansible-collections/ansible.netcommon/issues/151)
- Fixed ssh_type none issue while using net_put and net_get module (https://github.com/ansible-collections/ansible.netcommon/issues/153)
- Fixed unit tests under python3.5
- ipaddr filter - query "address/prefix" (also: "gateway", "gw", "host/prefix", "hostnet", and "router") now handles addresses with /32 prefix or /255.255.255.255 netmask
- network_cli - Update underlying ssh connection's play_context in update_play_context, so that the username or password can be updated

v1.3.0
======

Minor Changes
-------------

- Confirmed commit fails with TypeError in IOS XR netconf plugin (https://github.com/ansible-collections/cisco.iosxr/issues/74)
- The netconf_config module now allows root tag with namespace prefix.
- cli_config: Add new return value diff which is returned when the cliconf plugin supports onbox diff
- cli_config: Clarify when commands is returned when the module is run

Bugfixes
--------

- cli_parse - Ensure only native types are returned to the control node from the parser.
- netconf - Changed log level for message of using default netconf plugin to match the level used when a platform-specific netconf plugin is found

v1.2.1
======

Bugfixes
--------

- Fixed "Object of type Capabilities is not JSON serializable" when using default netconf plugin.

v1.2.0
======

Minor Changes
-------------

- Added description to collection galaxy.yml file.
- NetworkConfig objects now have an optional `comment_tokens` parameter which takes a list of strings which will override the DEFAULT_COMMENT_TOKENS list.
- New cli_parse module for parsing structured text using a variety of parsers. The initial implemetation of cli_parse can be used with json, native, ntc_templates, pyats, textfsm, ttp, and xml.
- The httpapi connection plugin now works with `wait_for_connection`. This will periodically request the root page of the server described by the plugin's options until the request succeeds. This can only test that the server is reachable, the correctness or usability of the API is not guaranteed.

Bugfixes
--------

- cli_config fixes issue when rollback_id = 0 evalutes to False
- sort_list will sort a list of dicts using the sorted method with key as an argument.

New Modules
-----------

- cli_parse - Parse cli output or text using a variety of parsers

v1.1.2
======

Release Summary
---------------

Rereleased 1.1.1 with updated changelog.

v1.1.1
======

Release Summary
---------------

Rereleased 1.1.0 with regenerated documentation.

v1.1.0
======

Major Changes
-------------

- Add libssh connection plugin and refactor network_cli (https://github.com/ansible-collections/ansible.netcommon/pull/30)

Minor Changes
-------------

- Add content option validation for netconf_config module (https://github.com/ansible-collections/ansible.netcommon/pull/66)
- Documentation of module arguments updated to match expected types where missing.
- Resource Modules: changed flag is set to true in check_mode for all ACTION_STATES (https://github.com/ansible-collections/ansible.netcommon/pull/82)

Removed Features (previously deprecated)
----------------------------------------

- module_utils.network.common.utils.ComplexDict has been removed

Bugfixes
--------

- Replace deprecated `getiterator` call with `iter`
- ipaddr - "host" query supports /31 subnets properly
- ipaddr filter - Fixed issue where the first IPv6 address in a subnet was not being considered a valid address.
- ipaddr filter now returns empty list instead of False on empty list input
- net_put - Restore missing function removed when action plugin stopped inheriting NetworkActionBase
- nthhost filter now returns str instead of IPAddress object
- slaac filter now returns str instead of IPAddress object

v1.0.0
======

New Plugins
-----------

Become
~~~~~~

- enable - Switch to elevated permissions on a network device

Connection
~~~~~~~~~~

- httpapi - Use httpapi to run command on network appliances
- napalm - Provides persistent connection using NAPALM
- netconf - Provides a persistent connection using the netconf protocol
- network_cli - Use network_cli to run command on network appliances
- persistent - Use a persistent unix socket for connection

Httpapi
~~~~~~~

- restconf - HttpApi Plugin for devices supporting Restconf API

Netconf
~~~~~~~

- default - Use default netconf plugin to run standard netconf commands as per RFC

New Modules
-----------

- cli_command - Run a cli command on cli-based network devices
- cli_config - Push text based configuration to network devices over network_cli
- net_banner - (deprecated, removed after 2022-06-01) Manage multiline banners on network devices
- net_get - Copy a file from a network device to Ansible Controller
- net_interface - (deprecated, removed after 2022-06-01) Manage Interface on network devices
- net_l2_interface - (deprecated, removed after 2022-06-01) Manage Layer-2 interface on network devices
- net_l3_interface - (deprecated, removed after 2022-06-01) Manage L3 interfaces on network devices
- net_linkagg - (deprecated, removed after 2022-06-01) Manage link aggregation groups on network devices
- net_lldp - (deprecated, removed after 2022-06-01) Manage LLDP service configuration on network devices
- net_lldp_interface - (deprecated, removed after 2022-06-01) Manage LLDP interfaces configuration on network devices
- net_logging - (deprecated, removed after 2022-06-01) Manage logging on network devices
- net_ping - Tests reachability using ping from a network device
- net_put - Copy a file from Ansible Controller to a network device
- net_static_route - (deprecated, removed after 2022-06-01) Manage static IP routes on network appliances (routers, switches et. al.)
- net_system - (deprecated, removed after 2022-06-01) Manage the system attributes on network devices
- net_user - (deprecated, removed after 2022-06-01) Manage the aggregate of local users on network device
- net_vlan - (deprecated, removed after 2022-06-01) Manage VLANs on network devices
- net_vrf - (deprecated, removed after 2022-06-01) Manage VRFs on network devices
- netconf_config - netconf device configuration
- netconf_get - Fetch configuration/state data from NETCONF enabled network devices.
- netconf_rpc - Execute operations on NETCONF enabled network devices.
- restconf_config - Handles create, update, read and delete of configuration data on RESTCONF enabled devices.
- restconf_get - Fetch configuration/state data from RESTCONF enabled devices.
- telnet - Executes a low-down and dirty telnet command
