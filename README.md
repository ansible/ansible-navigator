## ansible-navigator

A TUI for the Red Hat Ansible Automation Platform

[![asciicast](https://asciinema.org/a/gl7uVblC23dxGGTkVOEigDHCl.svg)](https://asciinema.org/a/gl7uVblC23dxGGTkVOEigDHCl)

## Quick start

```
mkdir project_directory
git clone https://github.com/ansible/ansible-navigator.git
python3 -m venv venv
source venv/bin/activate
pip install -U setuptools
pip install -U ansible
pip install ./ansible-navigator
ansible-navigator --help
```

RHEL8/Centos8 prerequisites:

```
sudo dnf install python3
sudo dnf install gcc python3-devel
```


### Welcome
Start at the welcome page, from the welcome page you can run playbooks, browse collections, explore inventories, review docs and more.
```
ansible-navigator
```

### Other things to try direct from the command line

Review the help
```
ansible-navigator --help
```

Review current ansible configuration (default mode)
```
ansible-navigator config
```

Review current configuration in classic mode
```
ansible-navigator config -m stdout dump
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
ansible-navigator run site.yaml -i inventory.yaml
```

Review and explore and inventory
```
ansible-navigator inventory -i inventory.yaml
```

Run a playbook with classic output (default mode)
```
ansible-navigator run -m stdout site.yaml -i inventory.yaml
```

### Available subcommands

For the full list of available subcomamnds, see the [subcommand guide](docs/subcommands.rst)

### Configuring ansible-navigator:

ansible-navigator can be configured:

1) using default values
2) with a settings file
3) with environment variables
4) at the command line
5) while issueing `:` comamnd with the application

Setting are applied in that order. For an overview of these methods, see the [configuration guide](docs/configuration.rst)


### Key bindings and colon commands

While using the terminal user interface keys and commands are avilable, the following 
is also available within the application by typing `:help`:


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
