# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Ospfv3 parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_ospf_vrf_cmd(process):
    command = "router ospfv3"
    vrf = "{vrf}".format(**process)
    if "vrf" in process and vrf != "default":
        command += " vrf " + vrf
    return command


def _tmplt_ospf_address_family_cmd(config_data):
    afi = "{afi}".format(**config_data)
    if afi == "router":
        command = ""
    else:
        command = "address-family " + afi
    return command


def _tmplt_ospf_adjacency_cmd(config_data):
    command = "adjacency exchange-start threshold"
    if "adjacency" in config_data:
        command += " {threshold}".format(
            **config_data["adjacency"]["exchange_start"]
        )
    return command


def _tmplt_ospf_auto_cost(config_data):
    if "auto_cost" in config_data:
        command = "auto-cost"
        if "reference_bandwidth" in config_data["auto_cost"]:
            command += " reference-bandwidth {reference_bandwidth}".format(
                **config_data["auto_cost"]
            )
        return command


def _tmplt_ospf_area_authentication(config_data):
    if "area_id" in config_data:
        command = "area {area_id} authentication ipsec spi ".format(
            **config_data
        )
        command += "{spi} {algorithm}".format(**config_data["authentication"])
        if "passphrase" in config_data["authentication"]:
            command += " passphrase"
        if (
            "encrypt_key" in config_data["authentication"]
            and config_data["authentication"]["encrypt_key"] is False
        ):
            command += " 0"
        if (
            "hidden_key" in config_data["authentication"]
            and config_data["authentication"]["hidden_key"] is True
        ):
            command += " 7"
        if "passphrase" not in config_data["authentication"]:
            command += " {key}".format(**config_data["authentication"])
        else:
            command += " {passphrase}".format(**config_data["authentication"])
        return command


def _tmplt_ospf_area_encryption(config_data):
    if "area_id" in config_data:
        command = "area {area_id} encryption ipsec spi ".format(**config_data)
        command += "{spi} esp {encryption} {algorithm}".format(
            **config_data["encryption"]
        )
        if "passphrase" in config_data["encryption"]:
            command += " passphrase"
        if (
            "encrypt_key" in config_data["encryption"]
            and config_data["encryption"]["encrypt_key"] is False
        ):
            command += " 0"
        if (
            "hidden_key" in config_data["encryption"]
            and config_data["encryption"]["hidden_key"] is True
        ):
            command += " 7"
        if "passphrase" not in config_data["encryption"]:
            command += " {key}".format(**config_data["encryption"])
        else:
            command += " {passphrase}".format(**config_data["encryption"])
        return command


def _tmplt_ospf_area_nssa(config_data):
    if "nssa" in config_data:
        command = "area {area_id} nssa".format(**config_data)
        if "default_information_originate" in config_data["nssa"]:
            command += " default-information-originate"
            if (
                "metric"
                in config_data["nssa"]["default_information_originate"]
            ):
                command += " metric {metric}".format(
                    **config_data["nssa"]["default_information_originate"]
                )
            if (
                "metric_type"
                in config_data["nssa"]["default_information_originate"]
            ):
                command += " metric-type {metric_type}".format(
                    **config_data["nssa"]["default_information_originate"]
                )
            if (
                "nssa_only"
                in config_data["nssa"]["default_information_originate"]
            ):
                command += " nssa-only"
        if config_data["nssa"].get("nssa_only"):
            command += " nssa-only"
        if config_data["nssa"].get("translate"):
            command += " translate type7 always"
        if config_data["nssa"].get("no_summary"):
            command += " no-summary"
        return command


def _tmplt_ospf_area_range(config_data):
    if "area_id" in config_data:
        command = "area {area_id} range".format(**config_data)
        if "address" in config_data:
            command += " {address}".format(**config_data)
        if "subnet_address" in config_data:
            command += " {subnet_address}".format(**config_data)
        if "subnet_mask" in config_data:
            command += " {subnet_mask}".format(**config_data)
        if "advertise" in config_data:
            if config_data.get("advertise"):
                command += " advertise"
            else:
                command += " not-advertise"
        if "cost" in config_data:
            command += " cost {cost}".format(**config_data)
        return command


def _tmplt_ospf_area_stub(config_data):
    if "stub" in config_data:
        command = "area {area_id} stub".format(**config_data)
        if "summary_lsa" in config_data["stub"]:
            if not config_data["stub"]["summary_lsa"]:
                command += " no-summary"
        return command


def _tmplt_ospf_default_information(config_data):
    if "default_information" in config_data:
        command = "default-information"
        if "originate" in config_data["default_information"]:
            command += " originate"
        if "always" in config_data["default_information"]:
            command += " always"
        if "metric" in config_data["default_information"]:
            command += " metric {metric}".format(
                **config_data["default_information"]
            )
        if "metric_type" in config_data["default_information"]:
            command += " metric-type {metric_type}".format(
                **config_data["default_information"]
            )
        if "route_map" in config_data["default_information"]:
            command += " route-map {route_map}".format(
                **config_data["default_information"]
            )
        return command


def _tmplt_ospf_log_adjacency_changes(config_data):
    if "log_adjacency_changes" in config_data:
        command = "log-adjacency-changes"
        if "detail" in config_data["log_adjacency_changes"]:
            if config_data["log_adjacency_changes"].get("detail"):
                command += " detail"
        return command


def _tmplt_ospf_max_metric(config_data):
    if "max_metric" in config_data:
        command = "max-metric"
        if "router_lsa" in config_data["max_metric"]:
            command += " router-lsa"
        if "external_lsa" in config_data["max_metric"]["router_lsa"]:
            command += " external-lsa"
            if (
                "max_metric_value"
                in config_data["max_metric"]["router_lsa"]["external_lsa"]
            ):
                command += " {max_metric_value}".format(
                    **config_data["max_metric"]["router_lsa"]["external_lsa"]
                )
        if "include_stub" in config_data["max_metric"]["router_lsa"]:
            if config_data["max_metric"]["router_lsa"].get("include_stub"):
                command += " include-stub"
        if "on_startup" in config_data["max_metric"]["router_lsa"]:
            command += " on-startup {wait_period}".format(
                **config_data["max_metric"]["router_lsa"]["on_startup"]
            )
        if "summary_lsa" in config_data["max_metric"]["router_lsa"]:
            command += " summary-lsa"
            if (
                "max_metric_value"
                in config_data["max_metric"]["router_lsa"]["summary_lsa"]
            ):
                command += " {max_metric_value}".format(
                    **config_data["max_metric"]["router_lsa"]["summary_lsa"]
                )
        return command


def _tmplt_ospf_redistribute(config_data):
    command = "redistribute {routes}".format(**config_data)
    if "route_map" in config_data:
        command += " route-map {route_map}".format(**config_data)
    return command


def _tmplt_ospf_timers_throttle(config_data):
    if "throttle" in config_data["timers"]:
        command = "timers throttle"
        if "lsa" in config_data["timers"]["throtle"]:
            if config_data["timers"]["throtle"].get("lsa"):
                command += " lsa all"
        if "spf" in config_data["timers"]["throtle"]:
            if config_data["timers"]["throtle"].get("spf"):
                command += " spf"
        if "initial" in config_data["timers"]["throttle"]:
            command += " {initial}".format(**config_data["timers"]["throttle"])
        if "min" in config_data["timers"]["throttle"]:
            command += " {min}".format(**config_data["timers"]["throttle"])
        if "max" in config_data["timers"]["throttle"]:
            command += " {max}".format(**config_data["timers"]["max"])

        return command


class Ospfv3Template(NetworkTemplate):
    def __init__(self, lines=None):
        super(Ospfv3Template, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "vrf",
            "getval": re.compile(
                r"""
                ^router\s
                ospfv3
                \svrf
                \s(?P<vrf>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_vrf_cmd,
            "result": {"processes": {"vrf": "{{ vrf }}"}},
            "shared": True,
        },
        {
            "name": "vrf",
            "getval": re.compile(
                r"""
                ^router\s
                ospfv3
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_vrf_cmd,
            "result": {"processes": {"vrf": '{{ "default" }}'}},
            "shared": True,
        },
        {
            "name": "address_family",
            "getval": re.compile(
                r"""
                \s*address-family
                \s(?P<afi>\S+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_address_family_cmd,
            "compval": "address_family",
            "result": {
                "processes": {
                    "address_family": {"{{ afi }}": {"afi": "{{ afi }}"}}
                }
            },
            "shared": True,
        },
        {
            "name": "adjacency",
            "getval": re.compile(
                r"""
                \s*adjacency
                \s+exchange-start
                \s+threshold
                \s+(?P<threshold>\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_adjacency_cmd,
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "adjacency": {
                                "exchange_start": {
                                    "threshold": "{{ threshold|int }}"
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "auto_cost",
            "getval": re.compile(
                r"""\s+(?P<auto_cost>auto-cost)*
                    \s*(?P<ref_band>reference-bandwidth\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_auto_cost,
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "auto_cost": {
                                "reference_bandwidth": '{{ ref_band.split(" ")[1] }}'
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.default_cost",
            "getval": re.compile(
                r"""\s+area
                    \s(?P<area_id>\S+)*
                    \sdefault-cost*
                    \s*(?P<default_cost>\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "area {{ area_id }} default-cost {{ default_cost }}",
            "compval": "default_cost",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "areas": {
                                "{{ area_id }}": {
                                    "area_id": "{{ area_id }}",
                                    "default_cost": "{{ default_cost|int }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.authentication",
            "getval": re.compile(
                r"""
                \s*area
                \s+(?P<area_id>\S+)
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
            "setval": _tmplt_ospf_area_authentication,
            "compval": "authentication",
            "remval": "area {{ area_id }} authentication",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "areas": {
                                "{{ area_id }}": {
                                    "area_id": "{{ area_id }}",
                                    "authentication": {
                                        "spi": "{{ val }}",
                                        "algorithm": "{{ algorithm }}",
                                        "encrypt_key": '{{ False if type is defined and type == "0" }}',
                                        "hidden_key": '{{ True if type is defined and type == "7" }}',
                                        "passphrase": "{{ line if passphrase is defined }}",
                                        "key": "{{ str(line) if passphrase is undefined }}",
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.encryption",
            "getval": re.compile(
                r"""
                \s*area
                \s+(?P<area_id>\S+)*
                \s+encryption
                \s+ipsec
                \s+spi
                \s+(?P<val>\d+)
                \s+esp
                \s*(?P<encryption>\S+)
                \s*(?P<algorithm>md5|sha1)*
                \s*(?P<passphrase>passphrase)*
                \s*(?P<type>0|7)*
                \s*(?P<line>\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_encryption,
            "compval": "encryption",
            "remval": "area {{ area_id }} encryption",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "areas": {
                                "{{ area_id }}": {
                                    "area_id": "{{ area_id }}",
                                    "encryption": {
                                        "spi": "{{ val }}",
                                        "encryption": "{{ encryption }}",
                                        "algorithm": "{{ algorithm }}",
                                        "encrypt_key": "{{ False if type is defined and type == '0'}}",
                                        "passphrase": "{{line if passphrase is defined }}",
                                        "hidden_key": "{{ True if type is defined and type == '7'}}",
                                        "key": "{{ line if passphrase is not defined }}",
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.nssa",
            "getval": re.compile(
                r"""
                \s+area\s(?P<area_id>\S+)
                \s(?P<nssa>nssa)
                \s*(?P<def_origin>default-information-originate)*
                \s*(metric)*
                \s*(?P<metric>\d+)*
                \s*(metric-type)*
                \s*(?P<metric_type>\d+)*
                \s*(?P<no_summary>no-summary)*
                \s*(?P<translate>translate.*)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_nssa,
            "compval": "nssa",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "areas": {
                                "{{ area_id }}": {
                                    "area_id": "{{ area_id }}",
                                    "nssa": {
                                        "set": "{{ True if nssa is defined and def_origin is undefined and "
                                        "no_summary is undefined and translate is undefined }}",
                                        "default_information_originate": {
                                            "set": "{{ True if def_origin is defined and metric is undefined and "
                                            "metric_type is undefined and nssa_only is undefined }}",
                                            "metric": "{{ metric.split("
                                            ")[1]|int }}",
                                            "metric_type": "{{ metric_type.split("
                                            ")[1]|int }}",
                                            "nssa_only": "{{ True if nssa_only is defined }}",
                                        },
                                        "translate": "{{ True if translate is defined }}",
                                        "no_summary": "{{ True if no_summary is defined }}",
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.ranges",
            "getval": re.compile(
                r"""
                \s*area
                \s+(?P<area_id>\S+)*
                \s+range
                \s+(?P<address>\S+)*
                \s*(?P<not_advertise>not-advertise)*
                \s*(?P<subnet_mask>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})*
                \s*(?P<subnet_address>\S+)*
                \s*(?P<cost>cost)*
                \s*(?P<cost_val>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_range,
            "compval": "ranges",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "areas": {
                                "{{ area_id }}": {
                                    "area_id": "{{ area_id }}",
                                    "ranges": [
                                        {
                                            "address": "{{ address }}",
                                            "subnet_mask": "{{ subnet_mask }}",
                                            "advertise": "{{ not not_advertise }}",
                                            "cost": "{{ cost_val }}",
                                        }
                                    ],
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "area.stub",
            "getval": re.compile(
                r"""\s+area\s(?P<area_id>\S+)
                    \s(?P<stub>stub)*
                    \s*(?P<no_sum>no-summary)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_area_stub,
            "compval": "stub",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "areas": {
                                "{{ area_id }}": {
                                    "area_id": "{{ area_id }}",
                                    "stub": {
                                        "set": "{{ True if stub is defined and no_sum is undefined }}",
                                        "summary_lsa": "{{ True if no_sum is defined }}",
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "bfd",
            "getval": re.compile(
                r"""\s+bfd*
                    \s*(?P<bfd>all-interfaces)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "bfd all-interfaces",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "bfd": {
                                "all_interfaces": "{{ True if bfd is defined }}"
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "default_information",
            "getval": re.compile(
                r"""\s+default-information*
                    \s*(?P<originate>originate)*
                    \s*(?P<always>always)*
                    \s*(?P<metric>metric\s\d+)*
                    \s*(?P<metric_type>metric-type\s\d+)*
                    \s*(?P<route_map>route-map\s\S+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_default_information,
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "default_information": {
                                "originate": "{{ True if originate is defined }}",
                                "always": "{{ True if always is defined }}",
                                "metric": "{{ metric.split(" ")[1]|int }}",
                                "metric_type": "{{ metric_type.split("
                                ")[1]|int }}",
                                "route_map": "{{ route_map.split(" ")[1] }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "default_metric",
            "getval": re.compile(
                r"""\s+default-metric(?P<default_metric>\s\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "default-metric {{ default_metric }}",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "default_metric": "{{ default_metric| int}}"
                        }
                    }
                }
            },
        },
        {
            "name": "distance",
            "getval": re.compile(
                r"""\s+distance
                    \s+ospf
                    \s+intra-area
                    \s+(?P<distance>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "distance ospf intra-area {{ distance }}",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "distance": "{{ distance| int}}"
                        }
                    }
                }
            },
        },
        {
            "name": "fips_restrictions",
            "getval": re.compile(
                r"""
                \s+(?P<fips>fips\s*\S+)
                *$""",
                re.VERBOSE,
            ),
            "setval": "fips restrictions",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "fips_restrictions": "{{ True if fips is defined }}"
                        }
                    }
                }
            },
        },
        {
            "name": "graceful_restart_period",
            "getval": re.compile(
                r"""
                \s+graceful-restart
                \s*grace-period*
                \s*(?P<period>\d+)*
                $""",
                re.VERBOSE,
            ),
            "setval": "graceful-restart grace-period {{ graceful_restart.grace_period }}",
            "remval": "graceful-restart",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "graceful_restart": {
                                "grace_period": "{{ period|int }}"
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "graceful_restart",
            "getval": re.compile(
                r"""
                \s+graceful-restart
                $""",
                re.VERBOSE,
            ),
            "setval": "graceful-restart",
            "remval": "graceful-restart",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "graceful_restart": {"set": "{{ True }}"}
                        }
                    }
                }
            },
        },
        {
            "name": "graceful_restart_helper",
            "getval": re.compile(
                r"""\s+(?P<grace>graceful-restart-helper)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "{{ grace }}",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "graceful_restart_helper": {
                                "set": "{{ True if grace is defined }}"
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "log_adjacency_changes",
            "getval": re.compile(
                r"""\s+(?P<log>log-adjacency-changes)*
                    \s*(?P<detail>detail)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_log_adjacency_changes,
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "log_adjacency_changes": {
                                "set": "{{ True if log is defined and detail is undefined }}",
                                "detail": "{{ True if detail is defined }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "max_metric",
            "getval": re.compile(
                r"""\s+max-metric
                    \s+(?P<router_lsa>router-lsa)
                    \s*(?P<external_lsa>external-lsa)*
                    \s*(?P<external_lsa_metric>\d+)*
                    \s*(?P<on_startup>on-startup)*
                    \s*(?P<wait_for_bgp>wait-for-bgp)*
                    \s*(?P<startup_time>\d+)*
                    \s*(?P<summary_lsa>summary-lsa)*
                    \s*(?P<summary_lsa_metric>\d+)*
                    \s*(?P<include_stub>include-stub)
                    *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_max_metric,
            "remval": "max-metric router-lsa",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "max_metric": {
                                "router_lsa": {
                                    "set": "{{ True if router_lsa is defined and external_lsa is undefined and "
                                    "include_stub is undefined and on_startup is undefined and "
                                    "summary_lsa is undefined }}",
                                    "external_lsa": {
                                        "set": "{{ True if external_lsa is defined and external_lsa_metric is undefined }}",
                                        "max_metric_value": "{{ external_lsa_metric }}",
                                    },
                                    "include_stub": "{{ True if include_stub is defined }}",
                                    "on_startup": {
                                        "wait_period": "{{ startup_time }}",
                                        "wait_for_bgp": "{{ True if wait_for_bgp is defined }}",
                                    },
                                    "summary_lsa": {
                                        "set": "{{ True if summary_lsa is defined and summary_lsa_metric is undefined }}",
                                        "max_metric_value": "{{ summary_lsa_metric }}",
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "maximum_paths",
            "getval": re.compile(
                r"""\s+maximum-paths*
                    \s+(?P<paths>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "maximum-paths {{ maximum_paths }}",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "maximum_paths": "{{ paths }}"
                        }
                    }
                }
            },
        },
        {
            "name": "passive_interface",
            "getval": re.compile(
                r"""
                \s*(?P<passive>passive-interface.*)
                 *$""",
                re.VERBOSE,
            ),
            "setval": "passive-interface default",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "passive_interface": "{{ True if passive is defined }}"
                        }
                    }
                }
            },
        },
        {
            "name": "redistribute",
            "getval": re.compile(
                r"""
                \s+redistribute
                \s(?P<route>\S+)
                \s*(?P<rmpa>route-map)*
                \s*(?P<map>\S+)*
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_redistribute,
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "redistribute": [
                                {
                                    "routes": "{{ route }}",
                                    "route_map": "{{ map }}",
                                }
                            ]
                        }
                    }
                }
            },
        },
        {
            "name": "router_id",
            "getval": re.compile(
                r"""
                \s+router-id
                \s(?P<id>\S+)$""",
                re.VERBOSE,
            ),
            "setval": ("router-id" " {{ router_id }}"),
            "remval": "router-id",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "router_id": "{{ id }}"
                        }
                    }
                }
            },
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""\s+(?P<shutdown>shutdown)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "shutdown",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "shutdown": "{{ True if shutdown is defined }}"
                        }
                    }
                }
            },
        },
        {
            "name": "timers.lsa",
            "getval": re.compile(
                r"""\s+timers
                    \slsa
                    \sarrival
                    \s(?P<lsa>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "timers lsa arrival {{ timers.lsa }}",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "timers": {"lsa": "{{ lsa }}"}
                        }
                    }
                }
            },
        },
        {
            "name": "timers.out_delay",
            "getval": re.compile(
                r"""\s+timers
                    \sout-delay
                    \s(?P<out_delay>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "timers out-delay {{ timers.out_delay }}",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "timers": {"out_delay": "{{ out_delay }}"}
                        }
                    }
                }
            },
        },
        {
            "name": "timers.pacing",
            "getval": re.compile(
                r"""\s+timers
                    \spacing
                    \sflood
                    \s(?P<pacing>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "timers pacing flood {{ timers.pacing }}",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "timers": {"pacing": "{{ pacing }}"}
                        }
                    }
                }
            },
        },
        {
            "name": "timers.throttle.lsa",
            "getval": re.compile(
                r"""\s+timers
                    \sthrottle
                    \s*(?P<lsa>lsa all)*
                    \s*(?P<initial>\d+)*
                    \s*(?P<min>\d+)*
                    \s*(?P<max>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "timers throttle lsa all {{ timers.throttle.initial }} {{ timers.throttle.min }} {{ timers.throttle.max }}",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "timers": {
                                "throttle": {
                                    "lsa": "{{ True if lsa is defined }}",
                                    "initial": "{{ initial }}",
                                    "min": "{{ min_delay }}",
                                    "max": "{{ max_delay }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "timers.throttle.spf",
            "getval": re.compile(
                r"""\s+timers
                    \sthrottle
                    \s*(?P<spf>spf)
                    \s*(?P<initial>\d+)
                    \s*(?P<min>\d+)
                    \s*(?P<max>\d+)
                    *$""",
                re.VERBOSE,
            ),
            "setval": "timers throttle spf {{ timers.throttle.initial }} {{ timers.throttle.min }} {{ timers.throttle.max }}",
            "result": {
                "processes": {
                    "address_family": {
                        '{{ afi|default("router", true) }}': {
                            "timers": {
                                "throttle": {
                                    "spf": "{{ True if spf is defined }}",
                                    "initial": "{{ initial }}",
                                    "min": "{{ min }}",
                                    "max": "{{ max }}",
                                }
                            }
                        }
                    }
                }
            },
        },
    ]
