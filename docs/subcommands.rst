.. _available_subcommands:

*****************************
ansible-navigator subcommands
*****************************

.. contents::
   :local:

ansible-navigator subcommand overview
========================================

.. ansible-navigator-subcommands-table::


Mapping ansible-navigator commands to ansible commands
======================================================

Some ansible-navigator commands map to ansible commands. The table below provides some examples.

.. list-table:: Mapping to ansible commands
  :header-rows: 1

  * - ansible command
    - ansible-navigator command
    - ansible-navigator colon command
  * - ``ansible``
    - ``ansible-navigator exec -- ansible``
    - N/A
  * - ``ansible-builder``
    - ``ansible-navigator builder``
    - N/A
  * - ``ansible-config``
    - ``ansible-navigator config``
    - ``:config``
  * - ``ansible-doc``
    - ``ansible-navigator doc``
    - ``:doc``
  * - ``ansible-inventory``
    - ``ansible-navigator inventory``
    - ``:inventory``
  * - ``ansible-galaxy``
    - ``ansible-navigator exec -- ansible-galaxy ...``
    - N/A
  * - ``ansible-lint``
    - ``ansible-navigator lint``
    - ``:lint``
  * - ``ansible-playbook``
    - ``ansible-navigator run``
    - ``:run``
  * - ``ansible-test``
    - ``ansible-navigator exec -- ansible-test ...``
    - N/A
  * - ``ansible-vault``
    - ``ansible-navigator exec -- ansible-vault ...``
    - N/A
