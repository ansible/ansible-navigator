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


def _tmplt_ospf_int_authentication(config_data):
    if "authentication_v2" in config_data:
        command = "ip ospf authentication"
        if "message_digest" in config_data["authentication_v2"]:
            command += " message-digest"
        return command
    if "authentication_v3" in config_data:
        command = "ospfv3 authentication ipsec spi "
        command += "{spi} {algorithm}".format(
            **config_data["authentication_v3"]
        )
        if "passphrase" in config_data["authentication_v3"]:
            command += " passphrase"
        if "keytype" in config_data["authentication_v3"]:
            command += " {keytype}".format(**config_data["authentication_v3"])
        if "passphrase" not in config_data["authentication_v3"]:
            command += " {key}".format(**config_data["authentication_v3"])
        else:
            command += " {passphrase}".format(
                **config_data["authentication_v3"]
            )
        return command


def _tmplt_ospf_int_encryption_v3(config_data):
    if "encryption" in config_data:
        command = "ospfv3 encryption ipsec spi ".format(**config_data)
        command += "{spi} esp {encryption} {algorithm}".format(
            **config_data["encryption"]
        )
        if "passphrase" in config_data["encryption"]:
            command += " passphrase"
        if "keytype" in config_data["encryption"]:
            command += " {keytype}".format(**config_data["encryption"])
        if "passphrase" not in config_data["encryption"]:
            command += " {key}".format(**config_data["encryption"])
        else:
            command += " {passphrase}".format(**config_data["encryption"])
        return command


def _tmplt_ospf_int_authentication_key(config_data):
    if "authentication_key" in config_data:
        command = "ip ospf authentication-key"
        if "encryption" in config_data["authentication_key"]:
            command += " {encryption} {key}".format(
                **config_data["authentication_key"]
            )
        else:
            command += " {key}".format(**config_data["authentication_key"])
        return command


def _tmplt_ospf_int_cost(config_data):
    if config_data["afi"] == "ipv4":
        command = "ip ospf cost {cost}".format(**config_data)
    else:
        command = "ospfv3 cost {cost}".format(**config_data)
    return command


def _tmplt_ospf_int_bfd(config_data):
    if config_data["afi"] == "ipv4":
        command = "ip ospf bfd"
    else:
        command = "ospfv3 bfd"
    return command


def _tmplt_ospf_int_hello_interval(config_data):
    if "ip_params" in config_data:
        command = "ospfv3 {afi} hello-interval {hello_interval}".format(
            **config_data["ip_params"]
        )
    else:
        if config_data["afi"] == "ipv4":
            command = "ip ospf hello-interval {hello_interval}".format(
                **config_data
            )
        else:
            command = "ospfv3 hello-interval {hello_interval}".format(
                **config_data
            )
    return command


def _tmplt_ospf_int_mtu_ignore(config_data):
    if "ip_params" in config_data:
        command = "ospfv3 {afi} mtu-ignore".format(**config_data["ip_params"])
    else:
        if config_data["afi"] == "ipv4":
            command = "ip ospf mtu-ignore"
        else:
            command = "ospfv3 mtu-ignore"
    return command


def _tmplt_ospf_int_network(config_data):
    if "ip_params" in config_data:
        command = "ospfv3 {afi} network {network}".format(
            **config_data["ip_params"]
        )
    else:
        if config_data["afi"] == "ipv4":
            command = "ip ospf network {network}".format(**config_data)
        else:
            command = "ospfv3 network {network}".format(**config_data)
    return command


def _tmplt_ospf_int_priority(config_data):
    if "ip_params" in config_data:
        command = "ospfv3 {afi} priority {priority}".format(
            **config_data["ip_params"]
        )
    else:
        if config_data["afi"] == "ipv4":
            command = "ip ospf priority {priority}".format(**config_data)
        else:
            command = "ospfv3 priority {priority}".format(**config_data)
    return command


def _tmplt_ospf_int_retransmit_interval(config_data):
    if "ip_params" in config_data:
        command = "ospfv3 {afi} retransmit-interval {retransmit_interval}".format(
            **config_data["ip_params"]
        )
    else:
        if config_data["afi"] == "ipv4":
            command = "ip ospf retransmit-interval {retransmit_interval}".format(
                **config_data
            )
        else:
            command = "ospfv3 retransmit-interval {retransmit_interval}".format(
                **config_data
            )
    return command


def _tmplt_ospf_int_transmit_delay(config_data):
    if "ip_params" in config_data:
        command = "ospfv3 {afi} transmit-delay {transmit_delay}".format(
            **config_data["ip_params"]
        )
    else:
        if config_data["afi"] == "ipv4":
            command = "ip ospf transmit-delay {transmit_delay}".format(
                **config_data
            )
        else:
            command = "ospfv3 transmit-delay {transmit_delay}".format(
                **config_data
            )
    return command


def _tmplt_ospf_int_dead_interval(config_data):
    if "ip_params" in config_data:
        command = "ospfv3 {afi} dead-interval {dead_interval}".format(
            **config_data["ip_params"]
        )
    else:
        if config_data["afi"] == "ipv4":
            command = "ip ospf dead-interval {dead_interval}".format(
                **config_data
            )
        else:
            command = "ospfv3 dead-interval {dead_interval}".format(
                **config_data
            )
    return command


class Ospf_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Ospf_interfacesTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "interfaces",
            "getval": re.compile(
                r"""
                ^interface
                \s+(?P<name>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "interface {{ name }}",
            "result": {"name": "{{ name }}"},
            "shared": True,
        },
        {
            "name": "area",
            "getval": re.compile(
                r"""
                \s*ip
                \s+ospf
                \s+area
                \s+(?P<area_id>\S+)*
                $""",
                re.VERBOSE,
            ),
            "setval": "ip ospf area {{ area.area_id }}",
            "compval": "area",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "area": {"area_id": "{{ area_id }}"},
                    }
                }
            },
        },
        {
            "name": "authentication_v2",
            "getval": re.compile(
                r"""
                \s*ip
                \s+ospf
                \s+authentication
                \s*(?P<message_digest>\S+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_authentication,
            "compval": "authentication_v2",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "authentication_v2": {
                            "set": "{{ True if message_digest is undefined }}",
                            "message_digest": "{{ True if message_digest is defined }}",
                        },
                    }
                }
            },
        },
        {
            "name": "authentication_v3",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+authentication
                \s+ipsec
                \s+spi
                \s+(?P<val>\d+)
                \s+(?P<algorithm>md5|sha1)
                \s*(?P<passphrase>passphrase)*
                \s*(?P<type>0|7)*
                \s*(?P<line>\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_authentication,
            "compval": "authentication_v3",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "authentication_v3": {
                            "spi": "{{ val }}",
                            "algorithm": "{{ algorithm }}",
                            "keytype": "{{ type }}",
                            "passphrase": "{{ line if passphrase is defined }}",
                            "key": "{{ str(line) if passphrase is undefined }}",
                        },
                    }
                }
            },
        },
        {
            "name": "authentication_key",
            "getval": re.compile(
                r"""
                \s*ip
                \s+ospf
                \s+authentication-key
                \s*(?P<encryption>\d+)*
                \s*(?P<line>\S+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_authentication_key,
            "compval": "authentication_key",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "authentication_key": {
                            "encryption": "{{ encryption }}",
                            "key": "{{ line }}",
                        },
                    }
                }
            },
        },
        {
            "name": "bfd",
            "getval": re.compile(
                r"""
                \s*ip
                \s+ospf
                \s+bfd
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_bfd,
            "compval": "bfd",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "bfd": "{{ True }}",
                    }
                }
            },
        },
        {
            "name": "deadinterval",
            "getval": re.compile(
                r"""
                \s*ip
                \s+ospf
                \s+dead-interval
                \s+(?P<interval>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_dead_interval,
            "compval": "dead_interval",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "dead_interval": "{{ interval }}",
                    }
                }
            },
        },
        {
            "name": "encryption",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+encryption
                \s+ipsec
                \s+spi
                \s+(?P<val>\d+)
                \s+esp
                \s+(?P<encryption>\S+)
                \s*(?P<algorithm>md5|sha1)
                \s*(?P<passphrase>passphrase)
                \s*(?P<type>0|7)
                \s*(?P<line>\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_encryption_v3,
            "compval": "encryption_v3",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "encryption_v3": {
                            "spi": "{{ val }}",
                            "encryption": "{{ encryption }}",
                            "algorithm": "{{ algorithm }}",
                            "keytype": "{{ type }}",
                            "passphrase": "{{ line if passphrase is defined }}",
                            "key": "{{ str(line) if passphrase is undefined }}",
                        },
                    }
                }
            },
        },
        {
            "name": "hellointerval",
            "getval": re.compile(
                r"""
                \s*ip
                \s+ospf
                \s+hello-interval
                \s+(?P<interval>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_hello_interval,
            "compval": "hello_interval",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "hello_interval": "{{ interval }}",
                    }
                }
            },
        },
        {
            "name": "bfd",
            "getval": re.compile(
                r"""
                \s+ospfv3
                \s+bfd
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_bfd,
            "compval": "bfd",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "bfd": "{{ True }}",
                    }
                }
            },
        },
        {
            "name": "cost",
            "getval": re.compile(
                r"""
                \s+ip
                \s+ospf
                \s+cost
                \s+(?P<val>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_cost,
            "compval": "cost",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "cost": "{{ val }}",
                    }
                }
            },
        },
        {
            "name": "cost",
            "getval": re.compile(
                r"""
                \s+ospfv3
                \s+cost
                \s+(?P<cost>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_cost,
            "compval": "cost",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "cost": "{{ cost }}",
                    }
                }
            },
        },
        {
            "name": "deadinterval",
            "getval": re.compile(
                r"""
                \s+ospfv3
                \s+dead-interval
                \s+(?P<interval>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_dead_interval,
            "compval": "dead_interval",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "dead_interval": "{{ interval }}",
                    }
                }
            },
        },
        {
            "name": "hellointerval",
            "getval": re.compile(
                r"""
                \s+ospfv3
                \s+hello-interval
                \s+(?P<interval>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_hello_interval,
            "compval": "hello_interval",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "hello_interval": "{{ interval }}",
                    }
                }
            },
        },
        {
            "name": "ip_params_area",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+(?P<afi>ipv4|ipv6)
                \s+area
                \s+(?P<area_id>\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": "ospfv3 {{ ip_params.afi }} area {{ ip_params.area.area_id }}",
            "compval": "ip_params.area",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "ip_params": {
                            "{{ afi }}": {
                                "afi": "{{ afi }}",
                                "area": {"area_id": "{{ area_id }}"},
                            }
                        },
                    }
                }
            },
        },
        {
            "name": "ip_params_bfd",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+(?P<afi>ipv4|ipv6)
                \s+bfd
                *$""",
                re.VERBOSE,
            ),
            "setval": "ospfv3 {{ afi }} bfd",
            "compval": "ip_params.bfd",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "ip_params": {
                            "{{ afi }}": {
                                "afi": "{{ afi }}",
                                "bfd": "{{ True }}",
                            }
                        },
                    }
                }
            },
        },
        {
            "name": "ip_params_cost",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+(?P<afi>ipv4|ipv6)
                \s+cost
                \s+(?P<cost>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": "ospfv3 {{ afi }} cost {{ cost }}",
            "compval": "ip_params.cost",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "ip_params": {
                            "{{ afi }}": {
                                "afi": "{{ afi }}",
                                "cost": "{{ cost }}",
                            }
                        },
                    }
                }
            },
        },
        {
            "name": "ip_params_dead_interval",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+(?P<afi>ipv4|ipv6)
                \s+dead-interval
                \s+(?P<interval>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_dead_interval,
            "compval": "ip_params.dead_interval",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "ip_params": {
                            "{{ afi }}": {
                                "afi": "{{ afi }}",
                                "dead_interval": "{{ interval }}",
                            }
                        },
                    }
                }
            },
        },
        {
            "name": "ip_params_hello_interval",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+(?P<afi>ipv4|ipv6)
                \s+hello-interval
                \s+(?P<interval>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": "ospfv3 {{ ip_params.afi }} hello-interval {{ ip_params.hello_interval }}",
            "compval": "ip_params.hello_interval",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "ip_params": {
                            "{{ afi }}": {
                                "afi": "{{ afi }}",
                                "hello_interval": "{{ interval }}",
                            }
                        },
                    }
                }
            },
        },
        {
            "name": "ip_params_mtu_ignore",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+(?P<afi>ipv4|ipv6)
                \s+(?P<mtu>mtu-ignore)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_mtu_ignore,
            "compval": "ip_params.mtu_ignore",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "ip_params": {
                            "{{ afi }}": {
                                "afi": "{{ afi }}",
                                "mtu_ignore": "{{ True if mtu is defined}}",
                            }
                        },
                    }
                }
            },
        },
        {
            "name": "ip_params_network",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+(?P<afi>ipv4|ipv6)
                \s+network
                \s+(?P<val>\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_network,
            "compval": "ip_params.network",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "ip_params": {
                            "{{ afi }}": {
                                "afi": "{{ afi }}",
                                "network": "{{ val }}",
                            }
                        },
                    }
                }
            },
        },
        {
            "name": "ip_params_priority",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+(?P<afi>ipv4|ipv6)
                \s+priority
                \s+(?P<val>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_priority,
            "compval": "ip_params.priority",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "ip_params": {
                            "{{ afi }}": {
                                "afi": "{{ afi }}",
                                "priority": "{{ val }}",
                            }
                        },
                    }
                }
            },
        },
        {
            "name": "ip_params_passive_interface",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+(?P<afi>ipv4|ipv6)
                \s+passive-interface
                *$""",
                re.VERBOSE,
            ),
            "setval": "ospfv3 {{ ip_params.afi }} passive-interface",
            "compval": "ip_params.passive_interface",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "ip_params": {
                            "{{ afi }}": {
                                "afi": "{{ afi }}",
                                "passive_interface": "{{ True }}",
                            }
                        },
                    }
                }
            },
        },
        {
            "name": "ip_params_retransmit_interval",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+(?P<afi>ipv4|ipv6)
                \s+retransmit-interval
                \s+(?P<val>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_retransmit_interval,
            "compval": "ip_params.retransmit_interval",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "ip_params": {
                            "{{ afi }}": {
                                "afi": "{{ afi }}",
                                "retransmit_interval": "{{ val }}",
                            }
                        },
                    }
                }
            },
        },
        {
            "name": "ip_params_transmit_delay",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+(?P<afi>ipv4|ipv6)
                \s+transmit-delay
                \s+(?P<val>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_transmit_delay,
            "compval": "ip_params.transmit_delay",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "ip_params": {
                            "{{ afi }}": {
                                "afi": "{{ afi }}",
                                "transmit_delay": "{{ val }}",
                            }
                        },
                    }
                }
            },
        },
        {
            "name": "mtu_ignore",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+mtu-ignore
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_mtu_ignore,
            "compval": "mtu_ignore",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "mtu_ignore": "{{ True }}",
                    }
                }
            },
        },
        {
            "name": "network",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+network
                \s+(?P<interface>\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_network,
            "compval": "network",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "network": "{{ interface }}",
                    }
                }
            },
        },
        {
            "name": "priority",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+priority
                \s+(?P<val>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_priority,
            "compval": "priority",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "priority": "{{ val }}",
                    }
                }
            },
        },
        {
            "name": "passive_interface",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+passive-interface
                *$""",
                re.VERBOSE,
            ),
            "setval": "ospfv3 passive-interface",
            "compval": "passive_interface",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "passive_interface": "{{ True }}",
                    }
                }
            },
        },
        {
            "name": "retransmit_interval",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+retransmit-interval
                \s+(?P<val>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_retransmit_interval,
            "compval": "retransmit_interval",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "retransmit_interval": "{{ val }}",
                    }
                }
            },
        },
        {
            "name": "transmit_delay",
            "getval": re.compile(
                r"""
                \s*ospfv3
                \s+transmit-delay
                \s+(?P<val>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_transmit_delay,
            "compval": "transmit_delay",
            "result": {
                "address_family": {
                    "{{ 'ipv6' }}": {
                        "afi": '{{ "ipv6" }}',
                        "transmit_delay": "{{ val }}",
                    }
                }
            },
        },
        {
            "name": "mtu_ignore",
            "getval": re.compile(
                r"""
                \s*ip
                \s+ospf
                \s+mtu-ignore
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_mtu_ignore,
            "compval": "mtu_ignore",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "mtu_ignore": "{{ True }}",
                    }
                }
            },
        },
        {
            "name": "network",
            "getval": re.compile(
                r"""
                \s*ip
                \s+ospf
                \s+network
                \s+(?P<interface>\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_network,
            "compval": "network",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "network": "{{ interface }}",
                    }
                }
            },
        },
        {
            "name": "priority",
            "getval": re.compile(
                r"""
                \s*ip ospf
                \s+priority
                \s+(?P<val>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_priority,
            "compval": "priority",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "priority": "{{ val }}",
                    }
                }
            },
        },
        {
            "name": "retransmit_interval",
            "getval": re.compile(
                r"""
                \s*ip
                \s+ospf
                \s+retransmit-interval
                \s+(?P<val>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_retransmit_interval,
            "compval": "retransmit_interval",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "retransmit_interval": "{{ val }}",
                    }
                }
            },
        },
        {
            "name": "transmit_delay",
            "getval": re.compile(
                r"""
                \s*ip
                \s+ospf
                \s+transmit-delay
                \s+(?P<val>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_int_transmit_delay,
            "compval": "transmit_delay",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "transmit_delay": "{{ val }}",
                    }
                }
            },
        },
        {
            "name": "message_digest_key",
            "getval": re.compile(
                r"""
                \s*ip
                \s+ospf
                \s+message-digest-key
                \s+(?P<id>\d+)
                \s+md5
                \s*(?P<type>0|7)*
                \s+(?P<line>\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": "ip ospf message-digest-key {{ message_digest_key.key_id }} md5 {{ message_digest_key.encryption }} {{ message_digest_key.key }}",
            "compval": "message_digest_key",
            "result": {
                "address_family": {
                    "{{ 'ipv4' }}": {
                        "afi": '{{ "ipv4" }}',
                        "message_digest_key": {
                            "key_id": "{{ id }}",
                            "encryption": "{{ type }}",
                            "key": "{{ line }}",
                        },
                    }
                }
            },
        },
    ]
