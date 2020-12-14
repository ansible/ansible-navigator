# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Ospf_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_authentication(data):
    auth = data.get("authentication")
    cmd = "ip ospf authentication"

    if auth.get("enable") is False:
        cmd = "no " + cmd
    else:
        if auth.get("message_digest"):
            cmd += " message-digest"
        elif auth.get("null_auth"):
            cmd += " null"
    return cmd


class Ospf_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Ospf_interfacesTemplate, self).__init__(lines=lines, tmplt=self)

    # fmt: off
    PARSERS = [
        {
            "name": "interface",
            "getval": re.compile(r'''
              ^interface
              \s(?P<name>\S+)$''', re.VERBOSE),
            "setval": "interface {{ name }}",
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                    "address_family": {},
                },
            },
            "shared": True,
        },
        {
            "name": "area",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)
                \srouter\s(ospf|ospfv3)
                \s(?P<process_id>\S+)
                \sarea\s(?P<area_id>\S+)
                (\s(?P<secondaries>secondaries\snone))?$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip' if afi == 'ipv4' else 'ipv6' }} "
                      "router {{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "{{ process_id }} area {{ area.area_id }}{{ ' secondaries none' if area.secondaries|default('True') == False}}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "processes": {
                                "{{ process_id }}": {
                                    "process_id": "{{ process_id }}",
                                    "area": {
                                        "area_id": "{{ area_id }}",
                                        "secondaries": "{{ False if secondaries is defined else None }}",
                                    },
                                }
                            }
                        },
                    }
                }
            }
        },
        {
            "name": "processes_multi_areas",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)
                \srouter\s(ospf|ospfv3)
                \s(?P<process_id>\S+)
                \smulti-area\s(?P<area>\S+)$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip' if afi == 'ipv4' else 'ipv6' }} "
                      "router {{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "{{ process_id }} multi-area {{ area }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "processes": {
                                "{{ process_id }}": {
                                    "process_id": "{{ process_id }}",
                                    "multi_areas": [
                                        "{{ area }}",
                                    ],
                                }
                            }
                        },
                    }
                }
            }
        },
        {
            "name": "multi_areas",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)
                \srouter\s(ospf|ospfv3)
                \smulti-area\s(?P<area>\S+)$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip' if afi == 'ipv4' else 'ipv6' }} "
                      "router {{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "multi-area {{ area }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "multi_areas": [
                                "{{ area }}",
                            ]
                        },
                    }
                }
            }
        },
        {
            "name": "authentication",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)
                \s(ospf|ospfv3)
                \s(?P<authentication>authentication)
                (\s(?P<opt>(message-digest|null)))?$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_authentication,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "authentication": {
                                "enable": "{{ True if authentication is defined and opt is undefined }}",
                                "message_digest": "{{ True if opt == 'message-digest' else None }}",
                                "null_auth": "{{ True if opt == 'null' else None }}",
                            }
                        },
                    }
                }
            }
        },
        {
            "name": "authentication.key_chain",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)
                \sospf
                \s(?P<authentication>authentication)
                \skey-chain\s(?P<key_chain>\S+)$""",
                re.VERBOSE,
            ),
            "setval": "ip ospf authentication key-chain {{ authentication.key_chain }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ afi|replace('ip', 'ipv4') }}",
                            "authentication": {
                                "key_chain": "{{ key_chain }}",
                            }
                        },
                    }
                }
            }
        },
        {
            "name": "authentication_key",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)
                \sospf
                \sauthentication-key
                \s(?P<encryption>\d)
                \s(?P<key>\S+)$""",
                re.VERBOSE,
            ),
            "setval": "ip ospf authentication-key "
                      "{{ authentication_key.encryption }} {{ authentication_key.key }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ afi|replace('ip', 'ipv4') }}",
                            "authentication_key": {
                                "encryption": "{{ encryption }}",
                                "key": "{{ key }}",
                            }
                        },
                    }
                }
            }
        },
        {
            "name": "message_digest_key",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)
                \sospf
                \smessage-digest-key
                \s(?P<key_id>\d+)
                \smd5
                \s(?P<encryption>\d)
                \s(?P<key>\S+)$""",
                re.VERBOSE,
            ),
            "setval": "ip ospf "
                      "message-digest-key {{ message_digest_key.key_id }} "
                      "md5 {{ message_digest_key.encryption|default('') }} {{ message_digest_key.key }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ afi|replace('ip', 'ipv4') }}",
                            "message_digest_key": {
                                "key_id": "{{ key_id }}",
                                "encryption": "{{ encryption }}",
                                "key": "{{ key }}",
                            }
                        },
                    }
                }
            }
        },
        {
            "name": "cost",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)?
                \s(ospf|ospfv3)
                \scost\s(?P<cost>\d+)$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ' if afi == 'ipv4' else '' }}"
                      "{{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "cost {{ cost }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi|d('ipv6') }}": {
                            "afi": "{{ 'ipv4' if afi is defined else 'ipv6' }}",
                            "cost": "{{ cost }}",
                        },
                    }
                }
            }
        },
        {
            "name": "dead_interval",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)?
                \s(ospf|ospfv3)
                \sdead-interval\s(?P<dead_interval>\d+)$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ' if afi == 'ipv4' else '' }}"
                      "{{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "dead-interval {{ dead_interval }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi|d('ipv6') }}": {
                            "afi": "{{ 'ipv4' if afi is defined else 'ipv6' }}",
                            "dead_interval": "{{ dead_interval }}",
                        },
                    }
                }
            }
        },
        {
            "name": "hello_interval",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)?
                \s(ospf|ospfv3)
                \shello-interval\s(?P<hello_interval>\d+)$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ' if afi == 'ipv4' else '' }}"
                      "{{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "hello-interval {{ hello_interval }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi|d('ipv6') }}": {
                            "afi": "{{ 'ipv4' if afi is defined else 'ipv6' }}",
                            "hello_interval": "{{ hello_interval }}",
                        },
                    }
                }
            }
        },
        {
            "name": "instance",
            "getval": re.compile(
                r"""
                \s+(ospf|ospfv3)
                \sinstance\s(?P<instance>\d+)$""",
                re.VERBOSE,
            ),
            "setval": "ospfv3 instance {{ instance }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi|d('ipv6') }}": {
                            "afi": "ipv6",
                            "instance": "{{ instance }}",
                        },
                    }
                }
            }
        },
        {
            "name": "mtu_ignore",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)?
                \s(ospf|ospfv3)
                \s(?P<mtu_ignore>mtu-ignore)$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ' if afi == 'ipv4' else '' }}"
                      "{{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "mtu-ignore",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi|d('ipv6') }}": {
                            "afi": "{{ 'ipv4' if afi is defined else 'ipv6' }}",
                            "mtu_ignore": "{{ not not mtu_ignore }}",
                        },
                    }
                }
            }
        },
        {
            "name": "network",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)?
                \s(ospf|ospfv3)
                \snetwork\s(?P<network>(broadcast|point-to-point))$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ' if afi == 'ipv4' else '' }}"
                      "{{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "network {{ network }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi|d('ipv6') }}": {
                            "afi": "{{ 'ipv4' if afi is defined else 'ipv6' }}",
                            "network": "{{ network }}",
                        },
                    }
                }
            }
        },
        {
            "name": "passive_interface",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)?
                \s(ospf|ospfv3)
                \s(?P<passive_interface>passive-interface)$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ' if afi == 'ipv4' else '' }}"
                      "{{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "passive-interface",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi|d('ipv6') }}": {
                            "afi": "{{ 'ipv4' if afi is defined else 'ipv6' }}",
                            "passive_interface": "{{ not not passive_interface }}",
                        },
                    }
                }
            }
        },
        {
            "name": "priority",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)?
                \s(ospf|ospfv3)
                \spriority\s(?P<priority>\d+)$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ' if afi == 'ipv4' else '' }}"
                      "{{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "priority {{ priority }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi|d('ipv6') }}": {
                            "afi": "{{ 'ipv4' if afi is defined else 'ipv6' }}",
                            "priority": "{{ priority }}",
                        },
                    }
                }
            }
        },
        {
            "name": "retransmit_interval",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)?
                \s(ospf|ospfv3)
                \sretransmit-interval\s(?P<retransmit_interval>\d+)$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ' if afi == 'ipv4' else '' }}"
                      "{{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "retransmit-interval {{ retransmit_interval }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi|d('ipv6') }}": {
                            "afi": "{{ 'ipv4' if afi is defined else 'ipv6' }}",
                            "retransmit_interval": "{{ retransmit_interval }}",
                        },
                    }
                }
            }
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)?
                \s(ospf|ospfv3)
                \s(?P<shutdown>shutdown)$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ' if afi == 'ipv4' else '' }}"
                      "{{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "shutdown",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi|d('ipv6') }}": {
                            "afi": "{{ 'ipv4' if afi is defined else 'ipv6' }}",
                            "shutdown": "{{ not not shutdown }}",
                        },
                    }
                }
            }
        },
        {
            "name": "transmit_delay",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip)?
                \s(ospf|ospfv3)
                \stransmit-delay\s(?P<transmit_delay>\d+)$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ' if afi == 'ipv4' else '' }}"
                      "{{ 'ospf' if afi == 'ipv4' else 'ospfv3' }} "
                      "transmit-delay {{ transmit_delay }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi|d('ipv6') }}": {
                            "afi": "{{ 'ipv4' if afi is defined else 'ipv6' }}",
                            "transmit_delay": "{{ transmit_delay }}",
                        },
                    }
                }
            }
        },
    ]
    # fmt: on
