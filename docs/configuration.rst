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

..
  start-parameters-tables
.. list-table:: **General parameters**
  :widths: 2 3 5
  :header-rows: 1

  * - Name
    - Description
    - Settings
  * - app
    - Subcommands
    - | **Choices:** 
      | **Default:** welcome
      | **CLI:** positional
      | **ENV:** ANSIBLE_NAVIGATOR_APP
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              app:

  * - cmdline
    - Extra parameters passed to the cooresponding command
    - | **Choices:** 
      | **Default:** No default value set
      | **CLI:** positional
      | **ENV:** ANSIBLE_NAVIGATOR_CMDLINE
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              cmdline:

  * - collection-doc-cache-path
    - The path to collection doc cache
    - | **Choices:** 
      | **Default:** $HOME/.cache/ansible-navigator/collection_doc_cache.db
      | **CLI:** positional
      | **ENV:** ANSIBLE_NAVIGATOR_COLLECTION_DOC_CACHE_PATH
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              collection-doc-cache-path:

  * - container-engine
    - Specify the container engine
    - | **Choices:** 'podman' or 'docker'
      | **Default:** podman
      | **CLI:** `--ce` or `--container-engine`
      | **ENV:** ANSIBLE_NAVIGATOR_CONTAINER_ENGINE
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                container-engine:

  * - editor-command
    - Specify the editor comamnd
    - | **Choices:** 
      | **Default:** vi +{line_number} {filename}
      | **CLI:** `--ecmd` or `--editor-command`
      | **ENV:** ANSIBLE_NAVIGATOR_EDITOR_COMMAND
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              editor:
                command:

  * - editor-console
    - Specify if the editor is console based
    - | **Choices:** 'True' or 'False'
      | **Default:** No default value set
      | **CLI:** `--econ` or `--editor-console`
      | **ENV:** ANSIBLE_NAVIGATOR_EDITOR_CONSOLE
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              editor:
                console:

  * - execution-environment
    - Enable or disable the use of an execution environment
    - | **Choices:** 'True' or 'False'
      | **Default:** No default value set
      | **CLI:** `--ee` or `--execution-environment`
      | **ENV:** ANSIBLE_NAVIGATOR_EXECUTION_ENVIRONMENT
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                enabled:

  * - execution-environment-image
    - Specify the name of the execution environment image
    - | **Choices:** 
      | **Default:** quay.io/ansible/ansible-runner:devel
      | **CLI:** `--eei` or `--execution-environment-image`
      | **ENV:** ANSIBLE_NAVIGATOR_EXECUTION_ENVIRONMENT_IMAGE
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                image:

  * - log-file
    - Specify the full path for the ansible-navigator log file
    - | **Choices:** 
      | **Default:** $PWD/ansible-navigator.log
      | **CLI:** `--lf` or `--log-file`
      | **ENV:** ANSIBLE_NAVIGATOR_LOG_FILE
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              logging:
                file:

  * - log-level
    - Specify the ansible-navigator log level
    - | **Choices:** 'debug', 'info', 'warning', 'error' or 'critical'
      | **Default:** warning
      | **CLI:** `--ll` or `--log-level`
      | **ENV:** ANSIBLE_NAVIGATOR_LOG_LEVEL
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              logging:
                level:

  * - mode
    - Specify the user-interface mode
    - | **Choices:** 'stdout' or 'interactive'
      | **Default:** interactive
      | **CLI:** `-m` or `--mode`
      | **ENV:** ANSIBLE_NAVIGATOR_MODE
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              mode:

  * - osc4
    - Enable or disable terminal color changing support with OSC 4
    - | **Choices:** 'True' or 'False'
      | **Default:** Current terminal capabilities
      | **CLI:** `--osc4` or `--osc4`
      | **ENV:** ANSIBLE_NAVIGATOR_OSC4
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              osc4:

  * - pass-environment-variable
    - Specify an exiting environment variable to be passed through to and set within the execution enviroment (--penv MY_VAR)
    - | **Choices:** 
      | **Default:** No default value set
      | **CLI:** `--penv` or `--pass-environment-variable`
      | **ENV:** ANSIBLE_NAVIGATOR_PASS_ENVIRONMENT_VARIABLES
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                environment-variables:
                  pass:

  * - set-environment-variable
    - Specify an environment variable and a value to be set within the execution enviroment (--senv MY_VAR=42)
    - | **Choices:** 
      | **Default:** No default value set
      | **CLI:** `--senv` or `--set-environment-variable`
      | **ENV:** ANSIBLE_NAVIGATOR_SET_ENVIRONMENT_VARIABLES
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                environment-variables:
                  set:


|
|

.. list-table:: **Subcommand: doc**
  :widths: 2 3 5
  :header-rows: 1

  * - Name
    - Description
    - Settings
  * - plugin-name
    - Specify the plugin name
    - | **Choices:** 
      | **Default:** No default value set
      | **CLI:** positional
      | **ENV:** ANSIBLE_NAVIGATOR_PLUGIN_NAME
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              documentation:
                plugin:
                  name:

  * - plugin-type
    - Specify the plugin type, 'become', 'cache', 'callback', 'cliconf', 'connection', 'httpapi', 'inventory', 'lookup', 'module', 'netconf', 'shell', 'strategy' or 'vars'
    - | **Choices:** 'become', 'cache', 'callback', 'cliconf', 'connection', 'httpapi', 'inventory', 'lookup', 'module', 'netconf', 'shell', 'strategy' or 'vars'
      | **Default:** module
      | **CLI:** `-t` or `----type`
      | **ENV:** ANSIBLE_NAVIGATOR_PLUGIN_TYPE
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              documentation:
                plugin:
                  type:


|

.. list-table:: **Subcommand: inventory**
  :widths: 2 3 5
  :header-rows: 1

  * - Name
    - Description
    - Settings
  * - inventory
    - Specify an inventory file path or comma separated host list
    - | **Choices:** 
      | **Default:** No default value set
      | **CLI:** `-i` or `--inventory`
      | **ENV:** ANSIBLE_NAVIGATOR_INVENTORIES
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              inventories:

  * - inventory-column
    - Specify a host attribute to show in the inventory view
    - | **Choices:** 
      | **Default:** No default value set
      | **CLI:** `--ic` or `--inventory-column`
      | **ENV:** ANSIBLE_NAVIGATOR_INVENTORY_COLUMNS
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              inventory-columns:


|

.. list-table:: **Subcommand: load**
  :widths: 2 3 5
  :header-rows: 1

  * - Name
    - Description
    - Settings
  * - playbook-artifact-load
    - Specify the path for the playbook artifact to load
    - | **Choices:** 
      | **Default:** No default value set
      | **CLI:** positional
      | **ENV:** ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_LOAD
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              playbook-artifact:
                load:


|

.. list-table:: **Subcommand: run**
  :widths: 2 3 5
  :header-rows: 1

  * - Name
    - Description
    - Settings
  * - inventory
    - Specify an inventory file path or comma separated host list
    - | **Choices:** 
      | **Default:** No default value set
      | **CLI:** `-i` or `--inventory`
      | **ENV:** ANSIBLE_NAVIGATOR_INVENTORIES
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              inventories:

  * - inventory-column
    - Specify a host attribute to show in the inventory view
    - | **Choices:** 
      | **Default:** No default value set
      | **CLI:** `--ic` or `--inventory-column`
      | **ENV:** ANSIBLE_NAVIGATOR_INVENTORY_COLUMNS
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              inventory-columns:

  * - playbook
    - Specify the playbook name
    - | **Choices:** 
      | **Default:** No default value set
      | **CLI:** positional
      | **ENV:** ANSIBLE_NAVIGATOR_PLAYBOOK
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              playbook:

  * - playbook-artifact-enable
    - Enable or disable the creation of artifacts for completed playbooks
    - | **Choices:** 'True' or 'False'
      | **Default:** No default value set
      | **CLI:** `--pae` or `--playbook-artifact-enable`
      | **ENV:** ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_ENABLE
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              playbook-artifact:
                enable:

  * - playbook-artifact-save-as
    - Specify the name for artifacts created from completed playbooks
    - | **Choices:** 
      | **Default:** {playbook_dir}/{playbook_name}-artifact-{ts_utc}.json
      | **CLI:** `--pas` or `--playbook-artifact-save-as`
      | **ENV:** ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_SAVE_AS
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              playbook-artifact:
                save-as:


|

..
  end-parameters-tables
