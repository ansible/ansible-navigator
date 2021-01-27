## winston

### A protoype CLI for the Red Hat Ansible Automation Platform

Although winston is in his infancy, he wants nothing more than to bring all the people, teams, tools and automation together to ensure experience doesn't come at the cost of outcomes.

## Quick start

```
git clone https://github.com/ansible/winston.git
mkdir winston_demo
cd winston_demo
python3 -m venv venv
source venv/bin/activate
pip install -U setuptools
pip install ../winston
```

RHEL8/Centos8 prerequisites:

```
sudo dnf install python3
sudo dnf install gcc python3-devel
```




### Welcome
Start at the welcome page, from the welcome page you can run playbooks, explore inventories, review docs, and check out blogs
```
winston
```

### Other things to try direct from the command line

Review the help
```
winston --help
```

Checkout some blogs
```
winston blog
winston bullhorn
winston redhat
```

Review current configuration
```
winston config
```

Explore available collections
```
winston collections
```

Review documentation
```
winston doc ansible.netcommon.cli_command
```

Run and explore a playbook
```
winston explore site.yaml -i inventory.yaml
```

Review and explore and inventory
```
winston inventory -i inventory.yaml
```

Run a playbook with classic output
```
winston playbook site.yaml -i inventory.yaml
```

## help

```
(venv) ➜  winston git:(inventory) ✗ winston --help
usage: winston [-h] [-ce {podman,docker}] [-ee] [-eei EE_IMAGE] [--inventory_columns INVENTORY_COLUMNS] [--ide {pycharm,vim,vscode}] [-lf LOGFILE] [-ll {debug,info,warning,error,critical}] [-no-osc4] [--web]
               {command} --help ...

optional arguments:
  -h, --help            show this help message and exit
  -ce {podman,docker}, --container-engine {podman,docker}
                        Specify the container engine to run the Execution Environment (default: podman)
  -ee, --execution-environment
                        Run the playbook in an Execution Environment (default: False)
  -eei EE_IMAGE, --ee-image EE_IMAGE
                        Specify the name of the container image containing an Execution Environment (default: quay.io/ansible/ansible-runner:devel)
  --inventory_columns INVENTORY_COLUMNS
                        Additional columns to be shown in the inventory views, comma delimited, eg 'xxx,yyy,zzz' (default: )
  --ide {pycharm,vim,vscode}
                        Specify the current ide (default: vim)
  -lf LOGFILE, --logfile LOGFILE
                        Specify the application log file location (default: ./winston.log)
  -ll {debug,info,warning,error,critical}, --loglevel {debug,info,warning,error,critical}
                        Specify the application log level (default: info)
  -no-osc4              Disable OSC-4 support (xterm.js color fix) (default: False)
  --web                 Run the application in a browser rather than the current terminal (default: False)

subcommands:
  valid subcommands

  {command} --help      additional help
    blog                Check out the recent Ansible blog entries
    bullhorn            Catch up on the latest bullhorn issues
    doc                 Show a plugin doc
    explore             Run playbook(s) interactive
    inventory           Explore inventories
    load                Load an artifact
    playbook            Run playbook(s)
    playquietly         Run playbook(s) quietly
    redhat              See the latest from Red Hat

```


## winston.cfg example

```
[default]
container_engine              = podman
ee_image                      = ee_libssh
execution_environment         = False
ide                           = vscode
inventory_columns             = ansible_network_os,ansible_network_cli_ssh_type,ansible_connection
loglevel                      = debug
no_osc4                       = True

[explore]
playbook                      = site.yaml
inventory                     = inventory.yaml
forks                         = 15

[inventory]
inventory                     = inventory.yaml

[playbook]
playbook                      = site.yaml
inventory                     = inventory.yaml

```

## in app key bindings

```
## GENERAL
--------------------------------------------------------------------------------------
esc                                     Go back
^f/PgUp                                 Page up
^b/PgDn                                 Page down
arrow up, arrow down                    Scroll up/down
:blog                                   Check out the recent Ansible blog entries
:bullhorn                               Catch up on the latest bullhorn issues
:d, :doc <plugin>                       Show a plugin doc
:e, :explore <playbook> -i <inventory>  Run a playbook using explore
:f, :filter <re>                        Filter page lines using a regex
:h, :help                               This page
:i, :inventory <inventory>              Explore the current or alternate inventory
:l, :log                                Review current log file
:o, :open                               Open current page in the editor
:o, :open {{ some_key }}                Open file path in a key's value
:q, :quit                               Quit the application
:q!, :quit!, ^c                         Force quit while a playbook is running
:redhat                                 See the latest from Red Hat
:rr, :rerun                             Rerun the playbook
:s, :save <file>                        Save current plays as an artifact
:st, :stream                            Watch playbook results realtime
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
[0-9]                                   Goto task number
:<number>                               Goto task number
+, -                                    Next/Previous task
_, :_                                   Toggle hidden keys
:{{ key|filter }}                       Template the key's value
:d, :doc                                Show the doc for the current task's module
:j, :json                               Switch to json serializtion
:y, :yaml                               Switch to yaml serialization

## LINE INPUT
--------------------------------------------------------------------------------------
esc                                     Exit line input
^A                                      Beginning of line
^E                                      End of line
insert                                  Enable/disable insert mode
arrow up, arrow down                    Previous/next command in history
```
