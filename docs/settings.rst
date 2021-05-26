.. _configuring_ansible_navigator:

*****************************
ansible-navigator settings
*****************************

.. contents::
   :local:

The ansible-navigator settings file
========================================

Several options in ``ansible-navigator`` can be configured by making use of a
settings file. The settings file can live in one of two places.
Currently the following are checked and the first match is used:

- ``ANSIBLE_NAVIGATOR_CONFIG`` (settings file path environment variable if set)
- ``./ansible-navigator.<ext>`` (project directory)
- ``~/.ansible-navigator.<ext>`` (home directory)

.. note::
    - The settings file can be in ``JSON`` or ``YAML`` format.
    - For settings in ``JSON`` format the extention must be ``.json``.
    - For settings in ``YAML`` format the extention must be ``.yml`` or ``.yaml``.
    - The project and home directories can only contain one settings file each.
      If more than one settings file is found in either directory, it will result in an error.

You can copy the example settings file below into one of those paths to start your ``ansible-navigator`` settings file.

..
  start-settings-sample
.. code-block:: yaml

    ---
    ansible-navigator:
    #   ansible:
    #     config: /tmp/ansible.cfg
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
    #     image: test_image:latest
    #     pull-policy: never
    #   help-config: True
    #   help-doc: True
    #   help-inventory: True
    #   help-playbook: False
    #   inventories:
    #     - /tmp/test_inventory.yml
    #   inventory-columns:
    #     - ansible_network_os
    #     - ansible_network_cli_ssh_type
    #     - ansible_connection
      logging:
    #     append: False
        level: critical
    #     file: /tmp/log.txt
    #   mode: stdout
    #   osc4: False
    #   playbook: /tmp/test_playbook.yml
    #   playbook-artifact: 
    #     enable: True
    #     replay: /tmp/test_artifact.json
    #     save-as: /tmp/test_artifact.json
..
  end-settings-sample


The following table describes all available settings.

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
    - | **Choices:** 'collections', 'config', 'doc', 'inventory', 'replay', 'run' or 'welcome'
      | **Default:** welcome
      | **CLI:** positional
      | **ENV:** ANSIBLE_NAVIGATOR_APP
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              app:

  * - cmdline
    - Extra parameters passed to the corresponding command
    - | **Default:** No default value set
      | **CLI:** positional
      | **ENV:** ANSIBLE_NAVIGATOR_CMDLINE
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              cmdline:

  * - collection-doc-cache-path
    - The path to collection doc cache
    - | **Default:** $HOME/.cache/ansible-navigator/collection_doc_cache.db
      | **CLI:** `--cdcp` or `--collection-doc-cache-path`
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
    - Specify the editor command
    - | **Default:** vi +{line_number} {filename}
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
      | **Default:** True
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
      | **Default:** True
      | **CLI:** `--ee` or `--execution-environment`
      | **ENV:** ANSIBLE_NAVIGATOR_EXECUTION_ENVIRONMENT
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                enabled:

  * - execution-environment-image
    - Specify the name of the execution environment image
    - | **Default:** quay.io/ansible/ansible-runner:devel
      | **CLI:** `--eei` or `--execution-environment-image`
      | **ENV:** ANSIBLE_NAVIGATOR_EXECUTION_ENVIRONMENT_IMAGE
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                image:

  * - log-append
    - Specify if log messages should be appended to an existing log file, otherwise a new log file will be created per session
    - | **Choices:** 'True' or 'False'
      | **Default:** True
      | **CLI:** `--la` or `--log-append`
      | **ENV:** ANSIBLE_NAVIGATOR_LOG_APPEND
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              logging:
                append:

  * - log-file
    - Specify the full path for the ansible-navigator log file
    - | **Default:** $PWD/ansible-navigator.log
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
    - Specify an exiting environment variable to be passed through to and set within the execution environment (--penv MY_VAR)
    - | **Default:** No default value set
      | **CLI:** `--penv` or `--pass-environment-variable`
      | **ENV:** ANSIBLE_NAVIGATOR_PASS_ENVIRONMENT_VARIABLES
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                environment-variables:
                  pass:

  * - pull-policy
    - Specify the image pull policy. always:Always pull the image, missing:Pull if not locally available, never:Never pull the image, tag:if the image tag is 'latest', always pull the image, otherwise pull if not locally available
    - | **Choices:** 'always', 'missing', 'never' or 'tag'
      | **Default:** tag
      | **CLI:** `--pp` or `--pull-policy`
      | **ENV:** ANSIBLE_NAVIGATOR_PULL_POLICY
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              execution-environment:
                pull-policy:

  * - set-environment-variable
    - Specify an environment variable and a value to be set within the execution environment (--senv MY_VAR=42)
    - | **Default:** No default value set
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

.. list-table:: **Subcommand: config**
  :widths: 2 3 5
  :header-rows: 1

  * - Name
    - Description
    - Settings
  * - config
    - Specify the path to the ansible configuration file
    - | **Default:** No default value set
      | **CLI:** `-c` or `--config`
      | **ENV:** ANSIBLE_CONFIG
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              ansible:
                config:

  * - help-config
    - Help options for ansible-config command in stdout mode
    - | **Choices:** 'True' or 'False'
      | **Default:** False
      | **CLI:** `--hc` or `--help-config`
      | **ENV:** ANSIBLE_NAVIGATOR_HELP_CONFIG
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              help-config:


|

.. list-table:: **Subcommand: doc**
  :widths: 2 3 5
  :header-rows: 1

  * - Name
    - Description
    - Settings
  * - help-doc
    - Help options for ansible-doc command in stdout mode
    - | **Choices:** 'True' or 'False'
      | **Default:** False
      | **CLI:** `--hd` or `--help-doc`
      | **ENV:** ANSIBLE_NAVIGATOR_HELP_DOC
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              help-doc:

  * - plugin-name
    - Specify the plugin name
    - | **Default:** No default value set
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
  * - help-inventory
    - Help options for ansible-inventory command in stdout mode
    - | **Choices:** 'True' or 'False'
      | **Default:** False
      | **CLI:** `--hi` or `--help-inventory`
      | **ENV:** ANSIBLE_NAVIGATOR_HELP_INVENTORY
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              help-inventory:

  * - inventory
    - Specify an inventory file path or comma separated host list
    - | **Default:** No default value set
      | **CLI:** `-i` or `--inventory`
      | **ENV:** ANSIBLE_NAVIGATOR_INVENTORIES
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              inventories:

  * - inventory-column
    - Specify a host attribute to show in the inventory view
    - | **Default:** No default value set
      | **CLI:** `--ic` or `--inventory-column`
      | **ENV:** ANSIBLE_NAVIGATOR_INVENTORY_COLUMNS
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              inventory-columns:


|

.. list-table:: **Subcommand: replay**
  :widths: 2 3 5
  :header-rows: 1

  * - Name
    - Description
    - Settings
  * - playbook-artifact-replay
    - Specify the path for the playbook artifact to replay
    - | **Default:** No default value set
      | **CLI:** positional
      | **ENV:** ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_REPLAY
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              playbook-artifact:
                replay:


|

.. list-table:: **Subcommand: run**
  :widths: 2 3 5
  :header-rows: 1

  * - Name
    - Description
    - Settings
  * - help-playbook
    - Help options for ansible-playbook command in stdout mode
    - | **Choices:** 'True' or 'False'
      | **Default:** False
      | **CLI:** `--hp` or `--help-playbook`
      | **ENV:** ANSIBLE_NAVIGATOR_HELP_PLAYBOOK
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              help-playbook:

  * - inventory
    - Specify an inventory file path or comma separated host list
    - | **Default:** No default value set
      | **CLI:** `-i` or `--inventory`
      | **ENV:** ANSIBLE_NAVIGATOR_INVENTORIES
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              inventories:

  * - inventory-column
    - Specify a host attribute to show in the inventory view
    - | **Default:** No default value set
      | **CLI:** `--ic` or `--inventory-column`
      | **ENV:** ANSIBLE_NAVIGATOR_INVENTORY_COLUMNS
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              inventory-columns:

  * - playbook
    - Specify the playbook name
    - | **Default:** No default value set
      | **CLI:** positional
      | **ENV:** ANSIBLE_NAVIGATOR_PLAYBOOK
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              playbook:

  * - playbook-artifact-enable
    - Enable or disable the creation of artifacts for completed playbooks
    - | **Choices:** 'True' or 'False'
      | **Default:** True
      | **CLI:** `--pae` or `--playbook-artifact-enable`
      | **ENV:** ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_ENABLE
      | **Settings file:**

      .. code-block:: yaml

            ansible-navigator:
              playbook-artifact:
                enable:

  * - playbook-artifact-save-as
    - Specify the name for artifacts created from completed playbooks
    - | **Default:** {playbook_dir}/{playbook_name}-artifact-{ts_utc}.json
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
