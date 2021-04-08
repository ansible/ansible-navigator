.. _configuring_ansible_navigator:

*****************************
Configuring ansible-navigator
*****************************

.. contents::
   :local:

The ansible-navigator configuration file
========================================

Several options in ``ansible-navigator`` can be configured by making use of a
configuration file. The configuration file can live in one of several places.
Currently the following paths are checked and the first match is used:

- ``./.ansible-navigator/ansible-navigator.yml`` (project-specific directory)
- ``[ansible-navigator source code root]/etc/ansible-navigator/ansible-navigator.yml``
- ``~/.config/ansible-navigator/ansible-navigator.yml``
- ``/etc/ansible-navigator/ansible-navigator.yml``
- ``[prefix]/etc/ansible-navigator/ansible-navigator.yml`` (e.g., ``/usr/local/etc/...``)

Here is an example conifguration file which can be copied into one of those paths.

.. literalinclude:: sample-config.yml
   :language: yaml


The following table describes all available configuration options.
Note that all options here must be specified under the ``ansible-navigator``
outer key and that options with ``.`` in them specify suboptions. Thus,
``log.level`` below could be configured like this:

.. code-block:: yaml

    ansible-navigator:
      log:
        level: debug


+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| Option                          | Default                                          | Description                                | CLI argument                |
+=================================+==================================================+============================================+=============================+
| ``container-engine``            | ``podman``                                       | How containers get run when execution      | ``--container-engine``      |
|                                 |                                                  | environments are used. Valid options are:  |                             |
|                                 |                                                  | ``podman``, ``docker``.                    |                             |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| ``doc-plugin-type``             | ``modoule``                                      | Specifies which kind of Ansible plugin is  | ``--type`` (or ``-t``)      |
|                                 |                                                  | referenced by default when running         |                             |
|                                 |                                                  | ``ansible-navigator doc [some plugin]``.   |                             |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| ``editor.command``              | ``vi +{line_number} {filename}``                 | Which editor to use when opening           | N/A                         |
|                                 |                                                  | files with the ``:open`` command.          |                             |
|                                 |                                                  |                                            |                             |
|                                 |                                                  | ``{line_number}`` and ``{filename}`` both  |                             |
|                                 |                                                  | get interpolated accordingly.              |                             |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| ``editor.console``              | ``True``                                         | Specifies if the editor is a console       | N/A                         |
|                                 |                                                  | based editor or not. If it is, curses      |                             |
|                                 |                                                  | is suspended until the editor exits.       |                             |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| ``execution-environment``       | ``False``                                        | Specifies whether or not to run            | ``--execution-environment`` |
|                                 |                                                  | playbooks in an execution environment      |                             |
|                                 |                                                  | when using ``:run``.                       |                             |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| ``execution-environment-image`` | ``quay.io/ansible/ansible-runner:devel``         | If using execution environments, specifies | ``--ee-image``              |
|                                 |                                                  | the default image to use.                  |                             |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| ``inventory``                   | ``[]``                                           | The inventory, or inventories, to use      | ``--inventory``             |
|                                 |                                                  | when running playbooks.                    |                             |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| ``inventory-columns``           |                                                  | Additional (comma-separated) columns to    | ``--inventory-columns``     |
|                                 |                                                  | show in inventory views.                   |                             |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| ``log.file``                    | ``./ansible-navigator.log``                      | Where to write ansible-navigator logs.     | ``--logfile``               |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| ``log.level``                   | ``info``                                         | The log level to use.                      | ``--loglevel``              |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| ``mode``                        | ``interactive``                                  | Whether to run in interactive or stdout    | ``--mode``                  |
|                                 |                                                  | mode.                                      |                             |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| ``no-osc4``                     | ``False``                                        | Disable terminal color changing            | ``--no_osc4``               |
|                                 |                                                  |                                            |                             |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
| ``playbook-artifact``           | ``{playbook_dir}/{playbook_name}_artifact.json`` | The artifact path and filename for         |                             |
|                                 |                                                  | playbook results.                          |                             |
|                                 |                                                  |                                            |                             |
|                                 |                                                  | ``{playbook_dir}`` and ``{playbook_name}`` |                             |
|                                 |                                                  | both get interpolated accordingly. The     |                             |
|                                 |                                                  | playbook name is determined from the       |                             |
|                                 |                                                  | basename of the path to the playbook, sans |                             |
|                                 |                                                  | its extension.                             |                             |
+---------------------------------+--------------------------------------------------+--------------------------------------------+-----------------------------+
