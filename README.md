## winston

### A protoype CLI for the Red Hat Ansible Automation Platform

Although winston is in his infancy, he wants nothing more than to bring all the people, teams, tools and automation together to ensure experience doesn't come at the cost of outcomes.

## Quick start

```
git clone git@github.com:ansible-network/winston.git
cd winston
pip install .

winston --help
winston blog
winston bullhorn
winston redhat
winston doc ansible.netcommon.cli_command
winston explore site.yaml -i inventory.yaml
winston playbook site.yaml -i inventory.yaml
```

## help

```
usage: winston [-h] [-ce {podman,docker}] [-ee] [-eei EE_IMAGE] [-ide {pycharm,vim,vscode}] [-lf LOGFILE] [-ll {debug,info,warning,error,critical}] [-no-osc4] [--web]
               {command} --help ...

optional arguments:
  -h, --help            show this help message and exit
  -ce {podman,docker}, --container-engine {podman,docker}
                        Specify the container engine to run the Execution Environment (default: podman)
  -ee, --execution-environment
                        Run the playbook in an Execution Environment (default: False)
  -eei EE_IMAGE, --ee-image EE_IMAGE
                        Specify the name of the container image containing an Execution Environment (default: quay.io/ansible/ansible-runner:devel)
  -ide {pycharm,vim,vscode}
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
    load                Load an artifact
    playbook            Run playbook(s)
    playquietly         Run playbook(s) quietly
    redhat              See the latest from Red Hat

```


## winston.cfg example

```
[default]
artifact                      = playbook.json
container_engine              = podman
execution_environment         = False
ee_image                      = quay.io/ansible/ansible-runner:devel
ide                           = vscode
inventory                     = /home/user/inventory.yaml
loglevel                      = debug

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
:d <plugin> :doc <plugin>               Show a plugin doc
:f, :filter <re>                        Filter page lines using a regex
:h, :help                               This page
:l, :log                                Review current log file
:o, :open                               Open current page in the editor
:o, :open {{ some_key }}                Open file path in a key's value
:q, :quit                               Quit after playbook complete
:q!, :quit!, ^c                         Force quit
:redhat                                 See the latest from Red Hat
:rr, :rerun                             Rerun the playbook
:s <file>, :save <file>                 Save current plays as an artifact
:st, :stream                            Watch playbook results realtime
:w <file>, :write <file>                Write current page to a new file
:w! <file>, :write! <file>              Write current page to an existing or new file
:w>> <file> :write>> <file>             Append current page to an existing file
:w!>> <file> :write!>> <file>           Append current page to an existing or new file

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