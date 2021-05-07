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

.. literalinclude:: sample-config.yml
   :language: yaml


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
  :header-rows: 1

  * - Name
    - Description
    - Default
    - Choices
    - CLI paramters
    - Environment variable
    - Settings file (ansible-navigator.)
  * - app
    - Subcommands
    - welcome
    - 
    - positional
    - ANSIBLE_NAVIGATOR_APP
    - app
  * - cmdline
    - Extra parameters passed to the cooresponding command
    - No default value set
    - 
    - positional
    - ANSIBLE_NAVIGATOR_CMDLINE
    - cmdline
  * - collection-doc-cache-path
    - The path to collection doc cache
    - $HOME/.cache/ansible-navigator/collection_doc_cache.db
    - 
    - positional
    - ANSIBLE_NAVIGATOR_COLLECTION_DOC_CACHE_PATH
    - collection-doc-cache-path
  * - container-engine
    - Specify the container engine
    - podman
    - 'podman' or 'docker'
    - --ce or --container-engine
    - ANSIBLE_NAVIGATOR_CONTAINER_ENGINE
    - execution-environment.container-engine
  * - editor-command
    - Specify the editor comamnd
    - vi +{line_number} {filename}
    - 
    - --ecmd or --editor-command
    - ANSIBLE_NAVIGATOR_EDITOR_COMMAND
    - editor.command
  * - editor-console
    - Specify if the editor is console based
    - No default value set
    - 'True' or 'False'
    - --econ or --editor-console
    - ANSIBLE_NAVIGATOR_EDITOR_CONSOLE
    - editor.console
  * - execution-environment
    - Enable or disable the use of an execution environment
    - No default value set
    - 'True' or 'False'
    - --ee or --execution-environment
    - ANSIBLE_NAVIGATOR_EXECUTION_ENVIRONMENT
    - execution-environment.enabled
  * - execution-environment-image
    - Specify the name of the execution environment image
    - quay.io/ansible/ansible-runner:devel
    - 
    - --eei or --execution-environment-image
    - ANSIBLE_NAVIGATOR_EXECUTION_ENVIRONMENT_IMAGE
    - execution-environment.image
  * - log-file
    - Specify the full path for the ansible-navigator log file
    - $PWD/ansible-navigator.log
    - 
    - --lf or --log-file
    - ANSIBLE_NAVIGATOR_LOG_FILE
    - logging.file
  * - log-level
    - Specify the ansible-navigator log level
    - warning
    - 'debug', 'info', 'warning', 'error' or 'critical'
    - --ll or --log-level
    - ANSIBLE_NAVIGATOR_LOG_LEVEL
    - logging.level
  * - mode
    - Specify the user-interface mode
    - interactive
    - 'stdout' or 'interactive'
    - -m or --mode
    - ANSIBLE_NAVIGATOR_MODE
    - mode
  * - osc4
    - Enable or disable terminal color changing support with OSC 4
    - Current terminal capabilities
    - 'True' or 'False'
    - --osc4 or --osc4
    - ANSIBLE_NAVIGATOR_OSC4
    - osc4
  * - pass-environment-variable
    - Specify an exiting environment variable to be passed through to and set within the execution enviroment (--penv MY_VAR)
    - No default value set
    - 
    - --penv or --pass-environment-variable
    - ANSIBLE_NAVIGATOR_PASS_ENVIRONMENT_VARIABLES
    - execution-environment.environment-variables.pass
  * - set-environment-variable
    - Specify an environment variable and a value to be set within the execution enviroment (--senv MY_VAR=42)
    - No default value set
    - 
    - --senv or --set-environment-variable
    - ANSIBLE_NAVIGATOR_SET_ENVIRONMENT_VARIABLES
    - execution-environment.environment-variables.set

|
|

.. list-table:: Subcommand: doc
  :header-rows: 1

  * - Name
    - Description
    - Default
    - Choices
    - CLI paramters
    - Environment variable
    - Settings file (ansible-navigator.)
  * - plugin-name
    - Specify the plugin name
    - No default value set
    - 
    - positional
    - ANSIBLE_NAVIGATOR_PLUGIN_NAME
    - documentation.plugin.name
  * - plugin-type
    - Specify the plugin type, 'become', 'cache', 'callback', 'cliconf', 'connection', 'httpapi', 'inventory', 'lookup', 'module', 'netconf', 'shell', 'strategy' or 'vars'
    - module
    - 'become', 'cache', 'callback', 'cliconf', 'connection', 'httpapi', 'inventory', 'lookup', 'module', 'netconf', 'shell', 'strategy' or 'vars'
    - -t or ----type
    - ANSIBLE_NAVIGATOR_PLUGIN_TYPE
    - documentation.plugin.type

|

.. list-table:: Subcommand: inventory
  :header-rows: 1

  * - Name
    - Description
    - Default
    - Choices
    - CLI paramters
    - Environment variable
    - Settings file (ansible-navigator.)
  * - inventory
    - Specify an inventory file path or comma separated host list
    - No default value set
    - 
    - -i or --inventory
    - ANSIBLE_NAVIGATOR_INVENTORIES
    - inventories
  * - inventory-column
    - Specify a host attribute to show in the inventory view
    - No default value set
    - 
    - --ic or --inventory-column
    - ANSIBLE_NAVIGATOR_INVENTORY_COLUMNS
    - inventory-columns

|

.. list-table:: Subcommand: load
  :header-rows: 1

  * - Name
    - Description
    - Default
    - Choices
    - CLI paramters
    - Environment variable
    - Settings file (ansible-navigator.)
  * - playbook-artifact-load
    - Specify the path for the playbook artifact to load
    - No default value set
    - 
    - positional
    - ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_LOAD
    - playbook-artifact.load

|

.. list-table:: Subcommand: run
  :header-rows: 1

  * - Name
    - Description
    - Default
    - Choices
    - CLI paramters
    - Environment variable
    - Settings file (ansible-navigator.)
  * - inventory
    - Specify an inventory file path or comma separated host list
    - No default value set
    - 
    - -i or --inventory
    - ANSIBLE_NAVIGATOR_INVENTORIES
    - inventories
  * - inventory-column
    - Specify a host attribute to show in the inventory view
    - No default value set
    - 
    - --ic or --inventory-column
    - ANSIBLE_NAVIGATOR_INVENTORY_COLUMNS
    - inventory-columns
  * - playbook
    - Specify the playbook name
    - No default value set
    - 
    - positional
    - ANSIBLE_NAVIGATOR_PLAYBOOK
    - playbook
  * - playbook-artifact-enable
    - Enable or disable the creation of artifacts for completed playbooks
    - No default value set
    - 'True' or 'False'
    - --pae or --playbook-artifact-enable
    - ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_ENABLE
    - playbook-artifact.enable
  * - playbook-artifact-save-as
    - Specify the name for artifacts created from completed playbooks
    - {playbook_dir}/{playbook_name}-artifact-{ts_utc}.json
    - 
    - --pas or --playbook-artifact-save-as
    - ANSIBLE_NAVIGATOR_PLAYBOOK_ARTIFACT_SAVE_AS
    - playbook-artifact.save-as

|

..
  end-parameters-tables
