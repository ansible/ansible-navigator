#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
"""
The arg spec for the nxos facts module.
"""


class FactsArgs(object):
    """ The arg spec for the nxos facts module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "gather_subset": dict(
            default=["!config"], type="list", elements="str"
        ),
        "gather_network_resources": dict(type="list", elements="str"),
    }
