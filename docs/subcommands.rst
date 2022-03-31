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
    - Notes
  * - ``ansible``
    - ``ansible-navigator exec -- ansible``
    - N/A
    - The ``exec`` subcommand requires execution environment support.
  * - ``ansible-builder``
    - ``ansible-navigator builder``
    - N/A
    - ``ansible-builder`` is installed with ``ansible-navigator``
  * - ``ansible-config``
    - ``ansible-navigator config``
    - ``:config``
    -
  * - ``ansible-doc``
    - ``ansible-navigator doc``
    - ``:doc``
    -
  * - ``ansible-inventory``
    - ``ansible-navigator inventory``
    - ``:inventory``
    -
  * - ``ansible-galaxy``
    - ``ansible-navigator exec -- ansible-galaxy ...``
    - N/A
    -  The ``exec`` subcommand requires execution environment support.
  * - ``ansible-lint``
    - ``ansible-navigator lint``
    - ``:lint``
    - ``ansible-lint`` needs to be installed locally or in the selected execution-environment.
  * - ``ansible-playbook``
    - ``ansible-navigator run``
    - ``:run``
    -
  * - ``ansible-test``
    - ``ansible-navigator exec -- ansible-test ...``
    - N/A
    -  The ``exec`` subcommand requires execution environment support.
  * - ``ansible-vault``
    - ``ansible-navigator exec -- ansible-vault ...``
    - N/A
    -  The ``exec`` subcommand requires execution environment support.
