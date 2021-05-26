.. _available_subcommands:

*****************************
ansible-navigator subcommands
*****************************

.. contents::
   :local:

ansible-navigator subcommand overview
========================================

..
  start-subcommands-table
.. list-table:: Available subcommands
  :widths: 1 3 3 1
  :header-rows: 1

  * - Name
    - Description
    - CLI Example
    - Colon command
  * - collections
    - Explore available collections
    - ansible-navigator collections --help
    - :collections
  * - config
    - Explore the current ansible configuration
    - ansible-navigator config --help
    - :config
  * - doc
    - Review documentation for a module or plugin
    - ansible-navigator doc --help
    - :doc
  * - images
    - Explore execution environment images
    - ansible-navigator images --help
    - :images
  * - inventory
    - Explore an inventory
    - ansible-navigator inventory --help
    - :inventory
  * - replay
    - Explore a previous run using a playbook artifact
    - ansible-navigator replay --help
    - :replay
  * - run
    - Run a playbook
    - ansible-navigator run --help
    - :run
  * - welcome
    - Start at the welcome page
    - ansible-navigator welcome --help
    - :welcome
..
  end-subcommands-table


Mapping ansible-navigator commands to ansible commands
======================================================

Some ansible-navigator commands map to ansible commands. The table below provides some examples.

.. list-table:: Mapping to ansible commands
  :header-rows: 1

  * - ansible command
    - ansible-navigator command
    - ansible-navigator colon command
  * - `ansible-config`
    - `ansible-navigator config`
    - `:config`
  * - `ansible-doc`
    - `ansible-navigator doc`
    - `:doc`
  * - `ansible-inventory`
    - `ansible-navigator inventory`
    - `:inventory`
  * - `ansible-playbook`
    - `ansible-navigator run`
    - `:run`
