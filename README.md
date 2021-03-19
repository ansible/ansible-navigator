## ansible-navigator

A TUI for the Red Hat Ansible Automation Platform

## Quick start

```
git clone https://github.com/ansible/ansible-navigator.git
mkdir ansible-navigator_demo
cd ansible-navigator_demo
python3 -m venv venv
source venv/bin/activate
pip install -U setuptools
pip install ../ansible-navigator
```

RHEL8/Centos8 prerequisites:

```
sudo dnf install python3
sudo dnf install gcc python3-devel
```


### Welcome
Start at the welcome page, from the welcome page you can run playbooks, explore inventories, and review docs
```
ansible-navigator
```

### Other things to try direct from the command line

Review the help
```
ansible-navigator --help
```

Review current configuration
```
ansible-navigator config
```

Explore available collections
```
ansible-navigator collections
```

Review documentation
```
ansible-navigator doc ansible.netcommon.cli_command
```

Run and explore a playbook
```
ansible-navigator run -m interactive site.yaml -i inventory.yaml
```

Review and explore and inventory
```
ansible-navigator inventory -i inventory.yaml
```

Run a playbook with classic output (default mode)
```
ansible-navigator run -m stdout site.yaml -i inventory.yaml
```


## ansible_navigator.cfg example

Note: the config file currently uses an underscore not dash

Environment variables will be expanded automatically.

```
[default]
container_engine              = podman
ee_image                      = quay.io/ansible/network-ee
execution_environment         = true
ide                           = vscode
inventory                     = ~/github/demo_content/inventory
inventory_columns             = ansible_network_os,ansible_network_cli_ssh_type,ansible_connection
loglevel                      = debug
no_osc4                       = true
playbook                      = ~/github/demo_content/gather.yaml

```

## in app key bindings

```
## GENERAL
--------------------------------------------------------------------------------------
esc                                     Go back
^f/PgUp                                 Page up
^b/PgDn                                 Page down
arrow up, arrow down                    Scroll up/down
:collections                            Explore installed collections
:config                                 Explore the current Ansible configuration
:d, :doc <plugin>                       Show a plugin doc
:r, :run <playbook> -i <inventory>      Run a playbook using in interactive mode
:f, :filter <re>                        Filter page lines using a regex
:h, :help                               This page
:i, :inventory <inventory>              Explore the current or alternate inventory
:l, :log                                Review current log file
:o, :open                               Open current page in the editor
:o, :open {{ some_key }}                Open file path in a key's value
:q, :quit                               Quit the application
:q!, :quit!, ^c                         Force quit while a playbook is running
:rr, :rerun                             Rerun the playbook
:s, :save <file>                        Save current plays as an artifact
:st, :stream                            Watch playbook results real time
:w, :write <file>                       Write current page to a new file
:w!, :write! <file>                     Write current page to an existing or new file
:w>>, :write>> <file>                   Append current page to an existing file
:w!>>, :write!>> <file>                 Append current page to an existing or new file

## MENUS
--------------------------------------------------------------------------------------
[0-9]                                   Go to menu item
:<number>                               Go to menu item
:{{ n|filter }}                         Template the menu item

## TASKS
--------------------------------------------------------------------------------------
[0-9]                                   Go to task number
:<number>                               Go to task number
+, -                                    Next/Previous task
_, :_                                   Toggle hidden keys
:{{ key|filter }}                       Template the key's value
:d, :doc                                Show the doc for the current task's module
:j, :json                               Switch to JSON serialization
:y, :yaml                               Switch to YAML serialization

## LINE INPUT
--------------------------------------------------------------------------------------
esc                                     Exit line input
^A                                      Beginning of line
^E                                      End of line
insert                                  Enable/disable insert mode
arrow up, arrow down                    Previous/next command in history
```
