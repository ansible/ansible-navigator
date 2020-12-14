#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
"""
The module file for ios_acls
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = """
module: ios_acls
short_description: ACLs resource module
description: This module configures and manages the named or numbered ACLs on IOS
  platforms.
version_added: 1.0.0
author: Sumit Jaiswal (@justjais)
notes:
- Tested against Cisco IOSv Version 15.2 on VIRL
options:
  config:
    description: A dictionary of ACL options.
    type: list
    elements: dict
    suboptions:
      afi:
        description:
        - The Address Family Indicator (AFI) for the Access Control Lists (ACL).
        required: true
        type: str
        choices:
        - ipv4
        - ipv6
      acls:
        description:
        - A list of Access Control Lists (ACL).
        type: list
        elements: dict
        suboptions:
          name:
            description: The name or the number of the ACL.
            required: true
            type: str
          acl_type:
            description:
            - ACL type
            - Note, it's mandatory and required for Named ACL, but for Numbered ACL
              it's not mandatory.
            type: str
            choices:
            - extended
            - standard
          aces:
            description: The entries within the ACL.
            elements: dict
            type: list
            suboptions:
              grant:
                description: Specify the action.
                type: str
                choices:
                - permit
                - deny
              sequence:
                description:
                - Sequence Number for the Access Control Entry(ACE).
                - Refer to vendor documentation for valid values.
                type: int
              protocol:
                description:
                - Specify the protocol to match.
                - Refer to vendor documentation for valid values.
                type: str
              protocol_options:
                description: protocol type.
                type: dict
                suboptions:
                  protocol_number:
                    description: An IP protocol number
                    type: int
                  ahp:
                    description: Authentication Header Protocol.
                    type: bool
                  eigrp:
                    description: Cisco's EIGRP routing protocol.
                    type: bool
                  esp:
                    description: Encapsulation Security Payload.
                    type: bool
                  gre:
                    description: Cisco's GRE tunneling.
                    type: bool
                  hbh:
                    description: Hop by Hop options header. Valid for IPV6
                    type: bool
                  icmp:
                    description: Internet Control Message Protocol.
                    type: dict
                    suboptions:
                      administratively_prohibited:
                        description: Administratively prohibited
                        type: bool
                      alternate_address:
                        description: Alternate address
                        type: bool
                      conversion_error:
                        description: Datagram conversion
                        type: bool
                      dod_host_prohibited:
                        description: Host prohibited
                        type: bool
                      dod_net_prohibited:
                        description: Net prohibited
                        type: bool
                      echo:
                        description: Echo (ping)
                        type: bool
                      echo_reply:
                        description: Echo reply
                        type: bool
                      general_parameter_problem:
                        description: Parameter problem
                        type: bool
                      host_isolated:
                        description: Host isolated
                        type: bool
                      host_precedence_unreachable:
                        description: Host unreachable for precedence
                        type: bool
                      host_redirect:
                        description: Host redirect
                        type: bool
                      host_tos_redirect:
                        description: Host redirect for TOS
                        type: bool
                      host_tos_unreachable:
                        description: Host unreachable for TOS
                        type: bool
                      host_unknown:
                        description: Host unknown
                        type: bool
                      host_unreachable:
                        description: Host unreachable
                        type: bool
                      information_reply:
                        description: Information replies
                        type: bool
                      information_request:
                        description: Information requests
                        type: bool
                      mask_reply:
                        description: Mask replies
                        type: bool
                      mask_request:
                        description: mask_request
                        type: bool
                      mobile_redirect:
                        description: Mobile host redirect
                        type: bool
                      net_redirect:
                        description: Network redirect
                        type: bool
                      net_tos_redirect:
                        description: Net redirect for TOS
                        type: bool
                      net_tos_unreachable:
                        description: Network unreachable for TOS
                        type: bool
                      net_unreachable:
                        description: Net unreachable
                        type: bool
                      network_unknown:
                        description: Network unknown
                        type: bool
                      no_room_for_option:
                        description: Parameter required but no room
                        type: bool
                      option_missing:
                        description: Parameter required but not present
                        type: bool
                      packet_too_big:
                        description: Fragmentation needed and DF set
                        type: bool
                      parameter_problem:
                        description: All parameter problems
                        type: bool
                      port_unreachable:
                        description: Port unreachable
                        type: bool
                      precedence_unreachable:
                        description: Precedence cutoff
                        type: bool
                      protocol_unreachable:
                        description: Protocol unreachable
                        type: bool
                      reassembly_timeout:
                        description: Reassembly timeout
                        type: bool
                      redirect:
                        description: All redirects
                        type: bool
                      router_advertisement:
                        description: Router discovery advertisements
                        type: bool
                      router_solicitation:
                        description: Router discovery solicitations
                        type: bool
                      source_quench:
                        description: Source quenches
                        type: bool
                      source_route_failed:
                        description: Source route failed
                        type: bool
                      time_exceeded:
                        description: All time exceededs
                        type: bool
                      timestamp_reply:
                        description: Timestamp replies
                        type: bool
                      timestamp_request:
                        description: Timestamp requests
                        type: bool
                      traceroute:
                        description: Traceroute
                        type: bool
                      ttl_exceeded:
                        description: TTL exceeded
                        type: bool
                      unreachable:
                        description: All unreachables
                        type: bool
                  igmp:
                    description: Internet Gateway Message Protocol.
                    type: dict
                    suboptions:
                      dvmrp:
                        description: Distance Vector Multicast Routing Protocol(2)
                        type: bool
                      host_query:
                        description: IGMP Membership Query(0)
                        type: bool
                      mtrace_resp:
                        description: Multicast Traceroute Response(7)
                        type: bool
                      mtrace_route:
                        description: Multicast Traceroute(8)
                        type: bool
                      pim:
                        description: Protocol Independent Multicast(3)
                        type: bool
                      trace:
                        description: Multicast trace(4)
                        type: bool
                      v1host_report:
                        description: IGMPv1 Membership Report(1)
                        type: bool
                      v2host_report:
                        description: IGMPv2 Membership Report(5)
                        type: bool
                      v2leave_group:
                        description: IGMPv2 Leave Group(6)
                        type: bool
                      v3host_report:
                        description: IGMPv3 Membership Report(9)
                        type: bool
                  ip:
                    description: Any Internet Protocol.
                    type: bool
                  ipv6:
                    description: Any IPv6.
                    type: bool
                  ipinip:
                    description: IP in IP tunneling.
                    type: bool
                  nos:
                    description: KA9Q NOS compatible IP over IP tunneling.
                    type: bool
                  ospf:
                    description: OSPF routing protocol.
                    type: bool
                  pcp:
                    description: Payload Compression Protocol.
                    type: bool
                  pim:
                    description: Protocol Independent Multicast.
                    type: bool
                  sctp:
                    description: Stream Control Transmission Protocol.
                    type: bool
                  udp:
                    description: User Datagram Protocol.
                    type: bool
                  tcp:
                    description: Match TCP packet flags
                    type: dict
                    suboptions:
                      ack:
                        description: Match on the ACK bit
                        type: bool
                      established:
                        description: Match established connections
                        type: bool
                      fin:
                        description: Match on the FIN bit
                        type: bool
                      psh:
                        description: Match on the PSH bit
                        type: bool
                      rst:
                        description: Match on the RST bit
                        type: bool
                      syn:
                        description: Match on the SYN bit
                        type: bool
                      urg:
                        description: Match on the URG bit
                        type: bool
              source:
                description: Specify the packet source.
                type: dict
                suboptions:
                  address:
                    description: Source network address.
                    type: str
                  wildcard_bits:
                    description: Destination wildcard bits, valid with IPV4 address.
                    type: str
                  any:
                    description: Match any source address.
                    type: bool
                  host:
                    description: A single source host
                    type: str
                  port_protocol:
                    description:
                    - Specify the destination port along with protocol.
                    - Note, Valid with TCP/UDP protocol_options
                    type: dict
                    suboptions:
                      eq:
                        description: Match only packets on a given port number.
                        type: str
                      gt:
                        description: Match only packets with a greater port number.
                        type: str
                      lt:
                        description: Match only packets with a lower port number.
                        type: str
                      neq:
                        description: Match only packets not on a given port number.
                        type: str
                      range:
                        description: Port group.
                        type: dict
                        suboptions:
                          start:
                            description: Specify the start of the port range.
                            type: int
                          end:
                            description: Specify the end of the port range.
                            type: int
              destination:
                description: Specify the packet destination.
                type: dict
                suboptions:
                  address:
                    description: Host address to match, or any single host address.
                    type: str
                  wildcard_bits:
                    description: Destination wildcard bits, valid with IPV4 address.
                    type: str
                  any:
                    description: Match any source address.
                    type: bool
                  host:
                    description: A single destination host
                    type: str
                  port_protocol:
                    description:
                    - Specify the destination port along with protocol.
                    - Note, Valid with TCP/UDP protocol_options
                    type: dict
                    suboptions:
                      eq:
                        description: Match only packets on a given port number.
                        type: str
                      gt:
                        description: Match only packets with a greater port number.
                        type: str
                      lt:
                        description: Match only packets with a lower port number.
                        type: str
                      neq:
                        description: Match only packets not on a given port number.
                        type: str
                      range:
                        description: Port group.
                        type: dict
                        suboptions:
                          start:
                            description: Specify the start of the port range.
                            type: int
                          end:
                            description: Specify the end of the port range.
                            type: int
              dscp:
                description: Match packets with given dscp value.
                type: str
              fragments:
                description: Check non-initial fragments.
                type: str
              log:
                description: Log matches against this entry.
                type: str
              log_input:
                description: Log matches against this entry, including input interface.
                type: str
              option:
                description:
                - Match packets with given IP Options value.
                - Valid only for named acls.
                type: dict
                suboptions:
                  add_ext:
                    description: Match packets with Address Extension Option (147).
                    type: bool
                  any_options:
                    description: Match packets with ANY Option.
                    type: bool
                  com_security:
                    description: Match packets with Commercial Security Option (134).
                    type: bool
                  dps:
                    description: Match packets with Dynamic Packet State Option (151).
                    type: bool
                  encode:
                    description: Match packets with Encode Option (15).
                    type: bool
                  eool:
                    description: Match packets with End of Options (0).
                    type: bool
                  ext_ip:
                    description: Match packets with Extended IP Option (145).
                    type: bool
                  ext_security:
                    description: Match packets with Extended Security Option (133).
                    type: bool
                  finn:
                    description: Match packets with Experimental Flow Control Option
                      (205).
                    type: bool
                  imitd:
                    description: Match packets with IMI Traffic Desriptor Option (144).
                    type: bool
                  lsr:
                    description: Match packets with Loose Source Route Option (131).
                    type: bool
                  mtup:
                    description: Match packets with MTU Probe Option (11).
                    type: bool
                  mtur:
                    description: Match packets with MTU Reply Option (12).
                    type: bool
                  no_op:
                    description: Match packets with No Operation Option (1).
                    type: bool
                  nsapa:
                    description: Match packets with NSAP Addresses Option (150).
                    type: bool
                  record_route:
                    description: Match packets with Record Route Option (7).
                    type: bool
                  router_alert:
                    description: Match packets with Router Alert Option (148).
                    type: bool
                  sdb:
                    description: Match packets with Selective Directed Broadcast Option
                      (149).
                    type: bool
                  security:
                    description: Match packets with Basic Security Option (130).
                    type: bool
                  ssr:
                    description: Match packets with Strict Source Routing Option (137).
                    type: bool
                  stream_id:
                    description: Match packets with Stream ID Option (136).
                    type: bool
                  timestamp:
                    description: Match packets with Time Stamp Option (68).
                    type: bool
                  traceroute:
                    description: Match packets with Trace Route Option (82).
                    type: bool
                  ump:
                    description: Match packets with Upstream Multicast Packet Option
                      (152).
                    type: bool
                  visa:
                    description: Match packets with Experimental Access Control Option
                      (142).
                    type: bool
                  zsu:
                    description: Match packets with Experimental Measurement Option
                      (10).
                    type: bool
              precedence:
                description: Match packets with given precedence value.
                type: int
              time_range:
                description: Specify a time-range.
                type: str
              tos:
                description:
                - Match packets with given TOS value.
                - Note, DSCP and TOS are mutually exclusive
                type: dict
                suboptions:
                  service_value:
                    description: Type of service value
                    type: int
                  max_reliability:
                    description: Match packets with max reliable TOS (2).
                    type: bool
                  max_throughput:
                    description: Match packets with max throughput TOS (4).
                    type: bool
                  min_delay:
                    description: Match packets with min delay TOS (8).
                    type: bool
                  min_monetary_cost:
                    description: Match packets with min monetary cost TOS (1).
                    type: bool
                  normal:
                    description: Match packets with normal TOS (0).
                    type: bool
              ttl:
                description: Match packets with given TTL value.
                type: dict
                suboptions:
                  eq:
                    description: Match only packets on a given TTL number.
                    type: int
                  gt:
                    description: Match only packets with a greater TTL number.
                    type: int
                  lt:
                    description: Match only packets with a lower TTL number.
                    type: int
                  neq:
                    description: Match only packets not on a given TTL number.
                    type: int
                  range:
                    description: Match only packets in the range of TTLs.
                    type: dict
                    suboptions:
                      start:
                        description: Specify the start of the port range.
                        type: int
                      end:
                        description: Specify the end of the port range.
                        type: int
  running_config:
    description:
      - The module, by default, will connect to the remote device and retrieve the current
        running-config to use as a base for comparing against the contents of source.
        There are times when it is not desirable to have the task get the current running-config
        for every task in a playbook.  The I(running_config) argument allows the implementer
        to pass in the configuration to use as the base config for comparison.
    type: str
  state:
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - gathered
    - rendered
    - parsed
    default: merged
    description:
      - The state the configuration should be left in
      - The states I(rendered), I(gathered) and I(parsed) does not perform any change
        on the device.
      - The state I(rendered) will transform the configuration in C(config) option to
        platform specific CLI commands which will be returned in the I(rendered) key
        within the result. For state I(rendered) active connection to remote host is
        not required.
      - The state I(gathered) will fetch the running configuration from device and transform
        it into structured data in the format as per the resource module argspec and
        the value is returned in the I(gathered) key within the result.
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into JSON format as per the resource module parameters and the
        value is returned in the I(parsed) key within the result. The value of C(running_config)
        option should be the same format as the output of command I(show running-config
        | include ip route|ipv6 route) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
"""
EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# vios#sh access-lists
# Extended IP access list 110
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10

- name: Merge provided configuration with device configuration
  cisco.ios.ios_acls:
    config:
    - afi: ipv4
      acls:
      - name: std_acl
        acl_type: standard
        aces:
        - grant: deny
          source:
            address: 192.168.1.200
        - grant: deny
          source:
            address: 192.168.2.0
            wildcard_bits: 0.0.0.255
      - name: 110
        aces:
        - sequence: 10
          protocol_options:
            icmp:
              traceroute: true
        - grant: deny
          protocol_options:
            tcp:
              ack: true
          source:
            host: 198.51.100.0
          destination:
            host: 198.51.110.0
            port_protocol:
              eq: telnet
      - name: test
        acl_type: extended
        aces:
        - grant: deny
          protocol_options:
            tcp:
              fin: true
          source:
            address: 192.0.2.0
            wildcard_bits: 0.0.0.255
          destination:
            address: 192.0.3.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: www
          option:
            traceroute: true
          ttl:
            eq: 10
      - name: 123
        aces:
        - grant: deny
          protocol_options:
            tcp:
              ack: true
          source:
            address: 198.51.100.0
            wildcard_bits: 0.0.0.255
          destination:
            address: 198.51.101.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: telnet
          tos:
            service_value: 12
        - grant: deny
          protocol_options:
            tcp:
              ack: true
          source:
            address: 192.0.3.0
            wildcard_bits: 0.0.0.255
          destination:
            address: 192.0.4.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: www
          dscp: ef
          ttl:
            lt: 20
    - afi: ipv6
      acls:
      - name: R1_TRAFFIC
        aces:
        - grant: deny
          protocol_options:
            tcp:
              ack: true
          source:
            any: true
            port_protocol:
              eq: www
          destination:
            any: true
            port_protocol:
              eq: telnet
          dscp: af11
    state: merged

# Commands fired:
# ---------------
#
# - ip access-list standard std_acl
# - deny 192.168.1.200
# - deny 192.168.2.0 0.0.0.255
# - ip access-list extended 110
# - no 10
# - 10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
# - deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# - ip access-list extended test
# - deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# - ip access-list extended 123
# - deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
# - deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# - ipv6 access-list R1_TRAFFIC
# - deny tcp any eq www any eq telnet ack dscp af11

# After state:
# ------------
#
# vios#sh access-lists
# Standard IP access list std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0, wildcard bits 0.0.0.255
# Extended IP access list 110
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#    20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# Extended IP access list 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# Extended IP access list test
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# IPv6 access list R1_TRAFFIC
#    deny tcp any eq www any eq telnet ack dscp af11 sequence 10


# Using replaced

# Before state:
# -------------
#
# vios#sh access-lists
# Standard IP access list std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0, wildcard bits 0.0.0.255
# Extended IP access list 110
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#    20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# Extended IP access list 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# Extended IP access list test
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# IPv6 access list R1_TRAFFIC
#    deny tcp any eq www any eq telnet ack dscp af11 sequence 10


- name: Replaces device configuration of listed acls with provided configuration
  cisco.ios.ios_acls:
    config:
    - afi: ipv4
      acls:
      - name: 110
        aces:
        - grant: deny
          protocol_options:
            tcp:
              syn: true
          source:
            address: 192.0.2.0
            wildcard_bits: 0.0.0.255
          destination:
            address: 192.0.3.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: www
          dscp: ef
          ttl:
            eq: 10
      - name: 150
        aces:
        - grant: deny
          sequence: 20
          protocol_options:
            tcp:
              syn: true
          source:
            address: 198.51.100.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: telnet
          destination:
            address: 198.51.110.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: telnet
          dscp: ef
          ttl:
            eq: 10
    state: replaced

# Commands fired:
# ---------------
#
# - no ip access-list extended 110
# - ip access-list extended 110
# - deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www syn dscp ef ttl eq 10
# - ip access-list extended 150
# - 20 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10

# After state:
# -------------
#
# vios#sh access-lists
# Standard IP access list std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0, wildcard bits 0.0.0.255
# Extended IP access list 110
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www syn dscp ef ttl eq 10
# Extended IP access list 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# Extended IP access list 150
#    20 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10
# Extended IP access list test
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# IPv6 access list R1_TRAFFIC
#    deny tcp any eq www any eq telnet ack dscp af11 sequence 10

# Using overridden

# Before state:
# -------------
#
# vios#sh access-lists
# Standard IP access list std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0, wildcard bits 0.0.0.255
# Extended IP access list 110
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#    20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# Extended IP access list 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# Extended IP access list test
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# IPv6 access list R1_TRAFFIC
#    deny tcp any eq www any eq telnet ack dscp af11 sequence 10

- name: Override device configuration of all acls with provided configuration
  cisco.ios.ios_acls:
    config:
    - afi: ipv4
      acls:
      - name: 110
        aces:
        - grant: deny
          sequence: 20
          protocol_options:
            tcp:
              ack: true
          source:
            address: 198.51.100.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: telnet
          destination:
            address: 198.51.110.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: www
          dscp: ef
          ttl:
            eq: 10
      - name: 150
        aces:
        - grant: deny
          sequence: 10
          protocol_options:
            tcp:
              syn: true
          source:
            address: 198.51.100.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: telnet
          destination:
            address: 198.51.110.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: telnet
          dscp: ef
          ttl:
            eq: 10
    state: overridden

# Commands fired:
# ---------------
#
# - no ip access-list standard std_acl
# - no ip access-list extended 110
# - no ip access-list extended 123
# - no ip access-list extended 150
# - no ip access-list extended test
# - no ipv6 access-list R1_TRAFFIC
# - ip access-list extended 150
# - 10 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10
# - ip access-list extended 110
# - 20 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq www ack dscp ef ttl eq 10

# After state:
# -------------
#
# vios#sh access-lists
# Extended IP access list 110
#    20 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq www ack dscp ef ttl eq 10
# Extended IP access list 150
#    10 deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10

# Using Deleted

# Before state:
# -------------
#
# vios#sh access-lists
# Standard IP access list std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0, wildcard bits 0.0.0.255
# Extended IP access list 110
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#    20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# Extended IP access list 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# Extended IP access list test
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# IPv6 access list R1_TRAFFIC
#    deny tcp any eq www any eq telnet ack dscp af11 sequence 10

- name: "Delete ACLs (Note: This won't delete the all configured ACLs)"
  cisco.ios.ios_acls:
    config:
    - afi: ipv4
      acls:
      - name: test
        acl_type: extended
      - name: 110
    - afi: ipv6
      acls:
      - name: R1_TRAFFIC
    state: deleted

# Commands fired:
# ---------------
#
# - no ip access-list extended test
# - no ip access-list extended 110
# - no ipv6 access-list R1_TRAFFIC

# After state:
# -------------
#
# vios#sh access-lists
# Standard IP access list std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0, wildcard bits 0.0.0.255
# Extended IP access list 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20

# Before state:
# -------------
#
# vios#sh access-lists
# Standard IP access list std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0, wildcard bits 0.0.0.255
# Extended IP access list 110
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#    20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# Extended IP access list 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# Extended IP access list test
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# IPv6 access list R1_TRAFFIC
#    deny tcp any eq www any eq telnet ack dscp af11 sequence 10

- name: "Delete ACLs based on AFI (Note: This won't delete the all configured ACLs)"
  cisco.ios.ios_acls:
    config:
    - afi: ipv4
    state: deleted

# Commands fired:
# ---------------
#
# - no ip access-list standard std_acl
# - no ip access-list extended test
# - no ip access-list extended 110
# - no ip access-list extended 123

# After state:
# -------------
#
# vios#sh access-lists
# IPv6 access list R1_TRAFFIC
#    deny tcp any eq www any eq telnet ack dscp af11 sequence 10

# Using Deleted without any config passed
#"(NOTE: This will delete all of configured ACLs)"

# Before state:
# -------------
#
# vios#sh access-lists
# Standard IP access list std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0, wildcard bits 0.0.0.255
# Extended IP access list 110
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#    20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# Extended IP access list 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# Extended IP access list test
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# IPv6 access list R1_TRAFFIC
#    deny tcp any eq www any eq telnet ack dscp af11 sequence 10

- name: 'Delete ALL of configured ACLs (Note: This WILL delete the all configured
    ACLs)'
  cisco.ios.ios_acls:
    state: deleted

# Commands fired:
# ---------------
#
# - no ip access-list extended test
# - no ip access-list extended 110
# - no ip access-list extended 123
# - no ip access-list extended test
# - no ipv6 access-list R1_TRAFFIC

# After state:
# -------------
#
# vios#sh access-lists

# Using Gathered

# Before state:
# -------------
#
# vios#sh access-lists
# Standard IP access list std_acl
#    10 deny   192.168.1.200
#    20 deny   192.168.2.0, wildcard bits 0.0.0.255
# Extended IP access list 110
#    10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
#    20 deny tcp host 198.51.100.0 host 198.51.110.0 eq telnet ack
# Extended IP access list 123
#    10 deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos 12
#    20 deny tcp 192.0.3.0 0.0.0.255 192.0.4.0 0.0.0.255 eq www ack dscp ef ttl lt 20
# Extended IP access list test
#    10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www fin option traceroute ttl eq 10
# IPv6 access list R1_TRAFFIC
#    deny tcp any eq www any eq telnet ack dscp af11 sequence 10

- name: Gather listed acls with provided configurations
  cisco.ios.ios_acls:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": [
#         {
#             "acls": [
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "address": "192.0.3.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "dscp": "ef",
#                             "grant": "deny",
#                             "protocol_options": {
#                                 "icmp": {
#                                     "echo": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "address": "192.0.2.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "ttl": {
#                                 "eq": 10
#                             }
#                         }
#                     ],
#                     "acl_type": "extended",
#                     "name": "110"
#                 },
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "address": "198.51.101.0",
#                                 "port_protocol": {
#                                     "eq": "telnet"
#                                 },
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "grant": "deny",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "address": "198.51.100.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "tos": {
#                                 "service_value": 12
#                             }
#                         },
#                         {
#                             "destination": {
#                                 "address": "192.0.4.0",
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 },
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "dscp": "ef",
#                             "grant": "deny",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 20,
#                             "source": {
#                                 "address": "192.0.3.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "ttl": {
#                                 "lt": 20
#                             }
#                         }
#                     ],
#                     "acl_type": "extended",
#                     "name": "123"
#                 },
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "address": "192.0.3.0",
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 },
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "grant": "deny",
#                             "option": {
#                                 "traceroute": true
#                             },
#                             "protocol_options": {
#                                 "tcp": {
#                                     "fin": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "address": "192.0.2.0",
#                                 "wildcard_bits": "0.0.0.255"
#                             },
#                             "ttl": {
#                                 "eq": 10
#                             }
#                         }
#                     ],
#                     "acl_type": "extended",
#                     "name": "test_acl"
#                 }
#             ],
#             "afi": "ipv4"
#         },
#         {
#             "acls": [
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "any": true,
#                                 "port_protocol": {
#                                     "eq": "telnet"
#                                 }
#                             },
#                             "dscp": "af11",
#                             "grant": "deny",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "sequence": 10,
#                             "source": {
#                                 "any": true,
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 }
#                             }
#                         }
#                     ],
#                     "name": "R1_TRAFFIC"
#                 }
#             ],
#             "afi": "ipv6"
#         }
#     ]

# Using Rendered

- name: Rendered the provided configuration with the exisiting running configuration
  cisco.ios.ios_acls:
    config:
    - afi: ipv4
      acls:
      - name: 110
        aces:
        - grant: deny
          sequence: 10
          protocol_options:
            tcp:
              syn: true
          source:
            address: 192.0.2.0
            wildcard_bits: 0.0.0.255
          destination:
            address: 192.0.3.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: www
          dscp: ef
          ttl:
            eq: 10
      - name: 150
        aces:
        - grant: deny
          protocol_options:
            tcp:
              syn: true
          source:
            address: 198.51.100.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: telnet
          destination:
            address: 198.51.110.0
            wildcard_bits: 0.0.0.255
            port_protocol:
              eq: telnet
          dscp: ef
          ttl:
            eq: 10
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#         "ip access-list extended 110",
#         "10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www syn dscp ef ttl eq 10",
#         "ip access-list extended 150",
#         "deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10"
#     ]

# Using Parsed

# File: parsed.cfg
# ----------------
#
# ipv6 access-list R1_TRAFFIC
# deny tcp any eq www any eq telnet ack dscp af11

- name: Parse the commands for provided configuration
  cisco.ios.ios_acls:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#         {
#             "acls": [
#                 {
#                     "aces": [
#                         {
#                             "destination": {
#                                 "any": true,
#                                 "port_protocol": {
#                                     "eq": "telnet"
#                                 }
#                             },
#                             "dscp": "af11",
#                             "grant": "deny",
#                             "protocol_options": {
#                                 "tcp": {
#                                     "ack": true
#                                 }
#                             },
#                             "source": {
#                                 "any": true,
#                                 "port_protocol": {
#                                     "eq": "www"
#                                 }
#                             }
#                         }
#                     ],
#                     "name": "R1_TRAFFIC"
#                 }
#             ],
#             "afi": "ipv6"
#         }
#     ]
"""
RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: The configuration returned will always be in the same format of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: The configuration returned will always be in the same format of the parameters above.
commands:
  description: The set of commands pushed to the remote device
  returned: always
  type: list
  sample: ['ip access-list extended 110', 'deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10']
"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.acls.acls import (
    AclsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.acls.acls import (
    Acls,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "overridden", ("config",)),
        ("state", "rendered", ("config",)),
        ("state", "parsed", ("running_config",)),
    ]
    mutually_exclusive = [("config", "running_config")]
    module = AnsibleModule(
        argument_spec=AclsArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    result = Acls(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
