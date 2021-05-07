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

- ``ANSIBLE_NAVIGATOR_CONFIG`` (configuration file path environment variable if set)
- ``./.ansible-navigator/<ansible-navigator-filename>`` (project-specific directory)
- ``[ansible-navigator source code root]/etc/ansible-navigator/<ansible-navigator-filename>``
- ``~/.config/ansible-navigator/<ansible-navigator-filename>``
- ``/etc/ansible-navigator/<ansible-navigator-filename>``
- ``[prefix]/etc/ansible-navigator/<ansible-navigator-filename>`` (e.g., ``/usr/local/etc/...``)

.. note::
    - The configuration file can either be in ``JSON`` or ``YAML`` format.
    - For configuration in ``JSON`` format the file name should be ``ansible-navigator.json``
    - For configuration in ``YAML`` format the file name can be either ``ansible-navigator.yml``
      or ``ansible-navigator.yaml``.
    - The first found matched directory path (based on order mentioned above) can have only one
      valid configuration file. If in case more than one configuration files (with different
      supported extensions) are found it will result in an error to avoid conflict.

You can copy the example configuration file below into one of those paths to start your ``ansible-navigator`` config file.

..
  start-settings-sample
.. code-block:: yaml

    # ---
    ansible-navigator:
    #   app: run
    #   collection-doc-cache-path: /tmp/cache.db
    #   cmdline: "--forks 15"
    #   editor:
    #     command: vim_from_setting
    #     console: False
    #   documentation:
    #     plugin:
    #       name: shell
    #       type: become
    #   execution-environment:
    #     container-engine: podman
    #     enabled: False
    #     environment-variables:
    #       pass:
    #         - ONE
    #         - TWO
    #         - THREE
    #       set:
    #         KEY1: VALUE1
    #         KEY2: VALUE2
    #         KEY3: VALUE3
    #     image: test_image
    #   inventories:
    #     - /tmp/test_inventory.yml
    #   inventory-columns:
    #     - ansible_network_os
    #     - ansible_network_cli_ssh_type
    #     - ansible_connection
      logging:
        level: critical
    #     file: /tmp/log.txt
    #   mode: stdout
    #   osc4: False
    #   playbook: /tmp/test_playbook.yml
    #   playbook-artifact: 
    #     enable: True
    #     load: /tmp/test_artifact.json
    #     save-as: /tmp/test_artifact.json
..
  end-settings-sample


The following table describes all available configuration options.
Note that all options here must be specified under the ``ansible-navigator``
outer key and that options with ``.`` in them specify suboptions. Thus,
``logging.level`` below could be configured like this:

.. code-block:: yaml

    ansible-navigator:
      logging:
        level: debug

..
  start-parameters-tables
.. list-table:: General parameters
  :widths: 10 10 35 10 35
  :header-rows: 1

  * - Name
    - Description
    - Settings
    - Choices
    - Default
  * - app
    - Subcommands
    - | CLI: positional
      | ENV: ANSIBLE_NAVIGATOR_APP
      | Setting file:

      .. code-block:: yaml
      
            ansible-navigator:
              app:

    - 
    - welcome
  * - cmdline
    - Extra parameters passed to the cooresponding command
    - | CLI: positional
      | ENV: ANSIBLE_NAVIGATOR_CMDLINE
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              cmdline:

    - 
    - No default value set
  * - collection-doc-cache-path
    - The path to collection doc cache
    - | CLI: positional
      | ENV: ANSIBLE_NAVIGATOR_COLLECTION_DOC_CACHE_PATH
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              collection-doc-cache-path:

    - 
    - $HOME/.cache/ansible-navigator/collection_doc_cache.db
  * - container-engine
    - Specify the container engine
    - | CLI: `--ce` or `--container-engine`
      | ENV: ANSIBLE_NAVIGATOR_CONTAINER_ENGINE
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                container-engine:

    - 'podman' or 'docker'
    - podman
  * - editor-command
    - Specify the editor comamnd
    - | CLI: `--ecmd` or `--editor-command`
      | ENV: ANSIBLE_NAVIGATOR_EDITOR_COMMAND
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              editor:
                command:

    - 
    - vi +{line_number} {filename}
  * - editor-console
    - Specify if the editor is console based
    - | CLI: `--econ` or `--editor-console`
      | ENV: ANSIBLE_NAVIGATOR_EDITOR_CONSOLE
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              editor:
                console:

    - 'True' or 'False'
    - No default value set
  * - execution-environment
    - Enable or disable the use of an execution environment
    - | CLI: `--ee` or `--execution-environment`
      | ENV: ANSIBLE_NAVIGATOR_EXECUTION_ENVIRONMENT
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                enabled:

    - 'True' or 'False'
    - No default value set
  * - execution-environment-image
    - Specify the name of the execution environment image
    - | CLI: `--eei` or `--execution-environment-image`
      | ENV: ANSIBLE_NAVIGATOR_EXECUTION_ENVIRONMENT_IMAGE
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                image:

    - 
    - quay.io/ansible/ansible-runner:devel
  * - log-file
    - Specify the full path for the ansible-navigator log file
    - | CLI: `--lf` or `--log-file`
      | ENV: ANSIBLE_NAVIGATOR_LOG_FILE
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              logging:
                file:

    - 
    - $PWD/ansible-navigator.log
  * - log-level
    - Specify the ansible-navigator log level
    - | CLI: `--ll` or `--log-level`
      | ENV: ANSIBLE_NAVIGATOR_LOG_LEVEL
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              logging:
                level:

    - 'debug', 'info', 'warning', 'error' or 'critical'
    - warning
  * - mode
    - Specify the user-interface mode
    - | CLI: `-m` or `--mode`
      | ENV: ANSIBLE_NAVIGATOR_MODE
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              mode:

    - 'stdout' or 'interactive'
    - interactive
  * - osc4
    - Enable or disable terminal color changing support with OSC 4
    - | CLI: `--osc4` or `--osc4`
      | ENV: ANSIBLE_NAVIGATOR_OSC4
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              osc4:

    - 'True' or 'False'
    - Current terminal capabilities
  * - pass-environment-variable
    - Specify an exiting environment variable to be passed through to and set within the execution enviroment (--penv MY_VAR)
    - | CLI: `--penv` or `--pass-environment-variable`
      | ENV: ANSIBLE_NAVIGATOR_PASS_ENVIRONMENT_VARIABLES
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                environment-variables:
                  pass:

    - 
    - No default value set
  * - set-environment-variable
    - Specify an environment variable and a value to be set within the execution enviroment (--senv MY_VAR=42)
    - | CLI: `--senv` or `--set-environment-variable`
      | ENV: ANSIBLE_NAVIGATOR_SET_ENVIRONMENT_VARIABLES
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                environment-variables:
                  set:

    - 
    - No default value set

|
|

.. list-table:: Subcommand: doc
  :widths: 10 10 35 10 35
  :header-rows: 1

  * - Name
    - Description
    - Settings
    - Choices
    - Default
  * - plugin-name
    - Specify the plugin name
    - | CLI: positional
      | ENV: ANSIBLE_NAVIGATOR_PLUGIN_NAME
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              documentation:
                plugin:
                  name:

    - 
    - No default value set
  * - plugin-type
    - Specify the plugin type, 'become', 'cache', 'callback', 'cliconf', 'connection', 'httpapi', 'inventory', 'lookup', 'module', 'netconf', 'shell', 'strategy' or 'vars'
    - | CLI: `-t` or `----type`
      | ENV: ANSIBLE_NAVIGATOR_PLUGIN_TYPE
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              documentation:
                plugin:
                  type:

    - 'become', 'cache', 'callback', 'cliconf', 'connection', 'httpapi', 'inventory', 'lookup', 'module', 'netconf', 'shell', 'strategy' or 'vars'
    - module

|

.. list-table:: Subcommand: inventory
  :widths: 10 10 35 10 35
  :header-rows: 1

  * - Name
    - Description
    - Settings
    - Choices
    - Default
  * - inventory
    - Specify an inventory file path or comma separated host list
    - | CLI: `-i` or `--inventory`
      | ENV: ANSIBLE_NAVIGATOR_INVENTORIES
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              inventories:

    - 
    - No default value set
  * - inventory-column
    - Specify a host attribute to show in the inventory view
    - | CLI: `--ic` or `--inventory-column`
      | ENV: ANSIBLE_NAVIGATOR_INVENTORY_COLUMNS
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              inventory-columns:

    - 
    - No default value set

|

.. list-table:: Subcommand: load
  :widths: 10 10 35 10 35
  :header-rows: 1

  * - Name
    - Description
    - Settings
    - Choices
    - Default
  * - playbook-artifact-load
    - Specify the path for the playbook artifact to load
    - | CLI: positional
      | ENV: ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_LOAD
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              playbook-artifact:
                load:

    - 
    - No default value set

|

.. list-table:: Subcommand: run
  :widths: 10 10 35 10 35
  :header-rows: 1

  * - Name
    - Description
    - Settings
    - Choices
    - Default
  * - inventory
    - Specify an inventory file path or comma separated host list
    - | CLI: `-i` or `--inventory`
      | ENV: ANSIBLE_NAVIGATOR_INVENTORIES
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              inventories:

    - 
    - No default value set
  * - inventory-column
    - Specify a host attribute to show in the inventory view
    - | CLI: `--ic` or `--inventory-column`
      | ENV: ANSIBLE_NAVIGATOR_INVENTORY_COLUMNS
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              inventory-columns:

    - 
    - No default value set
  * - playbook
    - Specify the playbook name
    - | CLI: positional
      | ENV: ANSIBLE_NAVIGATOR_PLAYBOOK
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              playbook:

    - 
    - No default value set
  * - playbook-artifact-enable
    - Enable or disable the creation of artifacts for completed playbooks
    - | CLI: `--pae` or `--playbook-artifact-enable`
      | ENV: ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_ENABLE
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              playbook-artifact:
                enable:

    - 'True' or 'False'
    - No default value set
  * - playbook-artifact-save-as
    - Specify the name for artifacts created from completed playbooks
    - | CLI: `--pas` or `--playbook-artifact-save-as`
      | ENV: ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_SAVE_AS
      | Setting file:

      .. code-block:: yaml

            ansible-navigator:
              playbook-artifact:
                save-as:

    - 
    - {playbook_dir}/{playbook_name}-artifact-{ts_utc}.json

|

..
  end-parameters-tables
