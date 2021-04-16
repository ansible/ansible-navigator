.. _explore_content:

******************************
Exploring content
******************************

``ansible-navigator`` provides a rich set of tools to explore your Ansible content.

.. note::

	This section uses examples from interactive mode.

.. contents::
   :local:

.. _view_collections:

Viewing collections
====================

You can use ``:collections`` in interactive mode to view all your collections within ``ansible-navigator`` and step into each to get more details:

.. code-block:: text

  NAME                  VERSION SHADOWED PATH
  0│ansible.netcommon     2.0.0      False /home/samccann/dev/ansible_collections/ansible/netcommon/
  1│vyos.vyos                     1.1.1      False /home/samccann/ansible-navigator_demo/venv/lib/python3.9/site-packages/ansible_c

You can then step into an individual collection for more details:

.. code-block:: text
  :emphasize-lines: 10, 12

  VYOS.VYOS                TYPE    ADDED DEPRECATED DESCRIPTION
  0│vyos                     cliconf 1.0.0      False Use vyos cliconf to run command on VyOS platform
  1│vyos_banner              module  1.0.0      False Manage multiline banners on VyOS devices
  2│vyos_command             module  1.0.0      False Run one or more commands on VyOS devices
  3│vyos_config              module  1.0.0      False Manage VyOS configuration on remote device
  4│vyos_facts               module  1.0.0      False Get facts about vyos devices.
  5│vyos_firewall_global     module  1.0.0      False FIREWALL global resource module
  6│vyos_firewall_interfaces module  1.0.0      False FIREWALL interfaces resource module
  7│vyos_firewall_rules      module  1.0.0      False FIREWALL rules resource module
  8│vyos_interface           module  1.0.0       True (deprecated, removed after 2022-06-01) Manage Interface on VyOS network devices
  9│vyos_interfaces          module  1.0.0      False Interfaces resource module
  10│vyos_l3_interface        module  1.0.0       True (deprecated, removed after 2022-06-01) Manage L3 interfaces on VyOS network devices
  11│vyos_l3_interfaces       module  1.0.0      False L3 interfaces resource module

By default, the output highlights deprecated modules in red that you should consider changing in any playbooks that use them. You can also type the line number to get the complete documentation for that module. See :ref:`explore_docs` for details.

.. _explore_config:

Exploring Ansible configuration settings
========================================

You can also see your Ansible configuration with the ``:config`` option:

.. code-block:: text

  OPTION                        DEFAULT SOURCE  VIA     CURRENT VALUE
  0│ACTION_WARNINGS                  True default default True
  1│AGNOSTIC_BECOME_PROMPT           True default default True
  2│ALLOW_WORLD_READABLE_TMPFILES    True default default False
  3│ANSIBLE_CONNECTION_PATH          True default default None
  4│ANSIBLE_COW_PATH                 True default default None
  5│ANSIBLE_COW_SELECTION            True default default default

And similarly, you can type the line number to deep dive into an individual configuration setting:

.. code-block:: text

  ACTION WARNINGS (current/default: True)
  0│---
  1│current: true
  2│default: true
  3│description:
  4│- By default Ansible will issue a warning when received from a task action (module
  5│  or action plugin)
  6│- These warnings can be silenced by adjusting this setting to False.
  7│env:
  8│- name: ANSIBLE_ACTION_WARNINGS
  9│ini:
  10│- key: action_warnings
  11│  section: defaults
  12│name: Toggle action warnings
  13│option: ACTION_WARNINGS
  14│source: default
  15│type: boolean
  16│version_added: '2.5'
  17│via: default


.. _explore_docs:

Exploring module documentation and copying examples
====================================================

You can use the ``:doc`` option to see the full documentation for a module.

.. code-block:: text

  :doc vyos.vyos.vyos_interfaces

The output displays as follows:

.. code-block:: yaml

  VYOS.VYOS.VYOS_INTERFACES: Interfaces resource module
  0│---
  1│additional_information: {}
  2│collection_info:
  3│  authors:
  4│  - Ansible Network Community (ansible-network)
  5│  dependencies:
  6│    ansible.netcommon: '\*'
  7│  description: Ansible Network Collection for VYOS devices.
  8│  documentation: null
  9│  homepage: null
 10│  issues: null
 11│  license: []
 12│  license_file: LICENSE
 13│  name: vyos.vyos
 14│  namespace: vyos
 15│  path: /home/samccann/ansible-navigator_demo/venv/lib/python3.9/site-packages/ansible_collections/vyos/vyos/
 16│  readme: README.md
 17│  repository: https://github.com/ansible-collections/vyos.vyos
 18│  shadowed_by: []
 19│  tags:
 20│  - vyos
 21│  - networking
 22│  version: 1.1.1
 23│doc:
 24│  author:
 25│  - Nilashish Chakraborty (@nilashishc)
 26│  - Rohit Thakur (@rohitthakur2590)
 27│  description:
 28│  - This module manages the interface attributes on VyOS network devices.
 29│  - This module supports managing base attributes of Ethernet, Bonding, VXLAN, Loopback
 30│    and Virtual Tunnel Interfaces.
 31│  module: vyos_interfaces
 <...>

And from here, you can type ``:{{ examples | from_yaml }}`` which shows the examples from the module documentation in YAML format. You can then type ``open`` to open the  examples into a file to start or copy into a playbook.

.. _explore_logs:

Exploring logs
==============

You can use the ``:log`` option to display the logs of recent playbook runs:

.. code-block:: text

  0│210326194732.807 INFO 'ansible_navigator.actions.explore.407d._init_explore' Explore initialized and playbook started.
  1│210326194734.130 INFO 'ansible_navigator.actions.explore.407d.update' Playbook complete
