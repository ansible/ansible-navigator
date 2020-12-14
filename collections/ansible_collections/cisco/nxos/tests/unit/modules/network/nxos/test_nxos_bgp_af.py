# (c) 2016 Red Hat Inc.
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

# Make coding more python3-ish

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.plugins.modules import nxos_bgp_af
from .nxos_module import TestNxosModule, load_fixture, set_module_args


class TestNxosBgpAfModule(TestNxosModule):

    module = nxos_bgp_af

    def setUp(self):
        super(TestNxosBgpAfModule, self).setUp()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_bgp_af.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_bgp_af.get_config"
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosBgpAfModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_get_config.stop()

    def load_fixtures(self, commands=None, device=""):
        self.get_config.return_value = load_fixture("nxos_bgp", "config.cfg")
        self.load_config.return_value = None

    def test_nxos_bgp_af(self):
        set_module_args(dict(asn=65535, afi="ipv4", safi="unicast"))
        self.execute_module(
            changed=True,
            sort=False,
            commands=["router bgp 65535", "address-family ipv4 unicast"],
        )

    def test_nxos_bgp_af_vrf(self):
        set_module_args(
            dict(asn=65535, vrf="test", afi="ipv4", safi="unicast")
        )
        self.execute_module(
            changed=True,
            sort=False,
            commands=[
                "router bgp 65535",
                "vrf test",
                "address-family ipv4 unicast",
            ],
        )

    def test_nxos_bgp_af_vrf_exists(self):
        set_module_args(
            dict(asn=65535, vrf="test2", afi="ipv4", safi="unicast")
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_bgp_af_dampening_routemap(self):
        set_module_args(
            dict(
                asn=65535,
                afi="ipv4",
                safi="unicast",
                dampening_routemap="route-map-a",
            )
        )
        self.execute_module(
            changed=True,
            commands=[
                "router bgp 65535",
                "address-family ipv4 unicast",
                "dampening route-map route-map-a",
            ],
        )

    def test_nxos_bgp_af_dampening_manual(self):
        set_module_args(
            dict(
                asn=65535,
                afi="ipv4",
                safi="unicast",
                dampening_half_time=5,
                dampening_suppress_time=2000,
                dampening_reuse_time=1900,
                dampening_max_suppress_time=10,
            )
        )
        self.execute_module(
            changed=True,
            commands=[
                "router bgp 65535",
                "address-family ipv4 unicast",
                "dampening 5 1900 2000 10",
            ],
        )

    def test_nxos_bgp_af_dampening_mix(self):
        set_module_args(
            dict(
                asn=65535,
                afi="ipv4",
                safi="unicast",
                dampening_routemap="route-map-a",
                dampening_half_time=5,
                dampening_suppress_time=2000,
                dampening_reuse_time=1900,
                dampening_max_suppress_time=10,
            )
        )
        result = self.execute_module(failed=True)
        self.assertEqual(
            result["msg"],
            "parameters are mutually exclusive: dampening_routemap|dampening_half_time, "
            "dampening_routemap|dampening_suppress_time, dampening_routemap|dampening_reuse_time, "
            "dampening_routemap|dampening_max_suppress_time",
        )

    def test_nxos_bgp_af_client(self):
        set_module_args(
            dict(asn=65535, afi="ipv4", safi="unicast", client_to_client=False)
        )
        self.execute_module(
            changed=True,
            commands=[
                "router bgp 65535",
                "address-family ipv4 unicast",
                "no client-to-client reflection",
            ],
        )

    def test_nxos_bgp_af_retain_route_target(self):
        set_module_args(
            dict(
                asn=65535, afi="l2vpn", safi="evpn", retain_route_target="abc"
            )
        )
        self.execute_module(
            changed=True,
            commands=[
                "router bgp 65535",
                "address-family l2vpn evpn",
                "retain route-target route-map abc",
            ],
        )

    def test_nxos_bgp_af_retain_route_target_all(self):
        set_module_args(
            dict(
                asn=65535, afi="l2vpn", safi="evpn", retain_route_target="all"
            )
        )
        self.execute_module(
            changed=True,
            commands=[
                "router bgp 65535",
                "address-family l2vpn evpn",
                "retain route-target all",
            ],
        )

    def test_nxos_bgp_af_retain_route_target_exists(self):
        set_module_args(
            dict(
                asn=65535, afi="l2vpn", safi="evpn", retain_route_target="xyz"
            )
        )
        self.execute_module(changed=False, commands=[])
