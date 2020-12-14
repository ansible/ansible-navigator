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
from ansible_collections.cisco.nxos.plugins.modules import nxos_bgp_neighbor
from .nxos_module import TestNxosModule, load_fixture, set_module_args


class TestNxosBgpNeighborModule(TestNxosModule):

    module = nxos_bgp_neighbor

    def setUp(self):
        super(TestNxosBgpNeighborModule, self).setUp()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_bgp_neighbor.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_bgp_neighbor.get_config"
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosBgpNeighborModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_get_config.stop()

    def load_fixtures(self, commands=None, device=""):
        self.get_config.return_value = load_fixture("nxos_bgp", "config.cfg")
        self.load_config.return_value = []

    def test_nxos_bgp_neighbor_bfd_1(self):
        # None (disable) -> enable
        set_module_args(dict(asn=65535, neighbor="1.1.1.1", bfd="enable"))
        self.execute_module(
            changed=True,
            commands=["router bgp 65535", "neighbor 1.1.1.1", "bfd"],
        )

        # enable -> enable (idempotence)
        set_module_args(dict(asn=65535, neighbor="1.1.1.2", bfd="enable"))
        self.execute_module(changed=False)

    def test_nxos_bgp_neighbor_bfd_2(self):
        # enable -> None (disable)
        set_module_args(dict(asn=65535, neighbor="1.1.1.2", bfd="disable"))
        self.execute_module(
            changed=True,
            commands=["router bgp 65535", "neighbor 1.1.1.2", "no bfd"],
        )

        # None (disable) -> disable (idempotence)
        set_module_args(dict(asn=65535, neighbor="1.1.1.1", bfd="disable"))
        self.execute_module(changed=False)

    def test_nxos_bgp_neighbor(self):
        set_module_args(
            dict(asn=65535, neighbor="192.0.2.3", description="some words")
        )
        self.execute_module(
            changed=True,
            commands=[
                "router bgp 65535",
                "neighbor 192.0.2.3",
                "description some words",
            ],
        )

    def test_nxos_bgp_neighbor_absent(self):
        set_module_args(dict(asn=65535, neighbor="1.1.1.1", state="absent"))
        self.execute_module(
            changed=True, commands=["router bgp 65535", "no neighbor 1.1.1.1"]
        )

    def test_nxos_bgp_neighbor_remove_private_as(self):
        set_module_args(
            dict(asn=65535, neighbor="3.3.3.4", remove_private_as="all")
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_bgp_neighbor_remove_private_as_changed(self):
        set_module_args(
            dict(asn=65535, neighbor="3.3.3.4", remove_private_as="replace-as")
        )
        self.execute_module(
            changed=True,
            commands=[
                "router bgp 65535",
                "neighbor 3.3.3.4",
                "remove-private-as replace-as",
            ],
        )

    def test_nxos_bgp_neighbor_peertype_border_leaf(self):
        set_module_args(
            dict(
                asn=65535, neighbor="192.0.2.3", peer_type="fabric_border_leaf"
            )
        )
        self.execute_module(
            changed=True,
            commands=[
                "router bgp 65535",
                "neighbor 192.0.2.3",
                "peer-type fabric-border-leaf",
            ],
        )

    def test_nxos_bgp_neighbor_peertype_external(self):
        set_module_args(
            dict(asn=65535, neighbor="192.0.2.3", peer_type="fabric_external")
        )
        self.execute_module(
            changed=True,
            commands=[
                "router bgp 65535",
                "neighbor 192.0.2.3",
                "peer-type fabric-external",
            ],
        )

    def test_nxos_bgp_neighbor_peertype_border_leaf_exists(self):
        set_module_args(
            dict(asn=65535, neighbor="5.5.5.5", peer_type="fabric_border_leaf")
        )
        self.execute_module(changed=False)

    def test_nxos_bgp_neighbor_peertype_external_exists(self):
        set_module_args(
            dict(asn=65535, neighbor="6.6.6.6", peer_type="fabric_external")
        )
        self.execute_module(changed=False)
