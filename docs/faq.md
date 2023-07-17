# Frequently asked questions

[TOC]

## Execution environments

### What is an execution environment?

An execution environment is a container image serving as an Ansible control
node.

See the
[Getting started with Execution Environments guide](https://docs.ansible.com/ansible/devel/getting_started_ee/index.html)
for details.

## The `ansible.cfg` file

### Where should the `ansible.cfg` file go when using an execution environment?

The easiest place to have the `ansible.cfg` is in the project directory adjacent
to the playbook. The playbook directory is automatically mounted in the
execution environment and the `ansible.cfg` file will be found. If the
`ansible.cfg` file is in another directory, the `ANSIBLE_CONFIG` variable needs
to be set and the directory specified as a custom volume mount. (See the
[settings guide](settings.md) for `execution-environment-volume-mounts`)

### Where should the `ansible.cfg` file go when not using an execution environment?

Ansible will look for the `ansible.cfg` in the typical locations when not using
an execution-environment. (See the ansible docs for the possibilities)

## Placement of ansible collections

### Where should ansible collections be placed when using an execution environment?

The easiest place to have ansible collections is in the project directory, in a
playbook adjacent collections directory. (eg
`ansible-galaxy collections install ansible.utils -p ./collections`). The
playbook directory is automatically mounted in the execution environment and the
collections should be found. Another option is to build the collections into an
execution environment using
[ansible builder](https://ansible-builder.readthedocs.io/en/latest/). This was
done to help playbook developers author playbooks that are production ready, as
both ansible controller and awx support playbook adjacent collection
directories. If the collections are in another directory, the
`ANSIBLE_COLLECTIONS_PATHS` variable needs to be set and the directory specified
as a custom volume mount. (See the [settings guide](settings.md) for
`execution-environment-volume-mounts`)

### Where should ansible collections be placed when not using an execution environment?

When not using an execution environment, ansible will look in the default
locations for collections. For more information about these, check out the
[collections guide](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).

## `ansible-navigator` settings

### What is the order in which configuration settings are applied?

The configuration system of ansible-navigator pulls in settings from various
sources and applies them hierarchically in the following order (where the last
applied changes are the most prevalent):

1. Default internal values
2. Values from a [settings file](settings.md)
3. Values from environment variables
4. Flags and arguments specified on the command line
5. While issuing `:` commands within the text-based user interface (TUI)

### Why does `ansible-navigator` change the terminal colors or look terrible?

`ansible-navigator` queries the terminal for its OSC4 compatibility. OSC4, 10,
11, 104, 110, 111 indicate the terminal supports color changing and reverting.
It is possible that the terminal is misrepresenting its ability. OSC4 detection
can be disabled by setting `--osc4 false`. (See the
[settings guide](settings.md) for how to handle this with an environment
variable or in the settings file)

### How can I change the colors used by `ansible-navigator`

Full theme support should come in a later release, for now, try `--osc4 false`.
This will cause `ansible-navigator` to use the terminal's defined colors. (See
the [settings guide](settings.md) for how to handle this with an environment
variable or in the settings file)

### What's with all these `site-artifact-2021-06-02T16:02:33.911259+00:00.json` files in the playbook directory?

`ansible-navigator` creates a playbook artifact for every playbook run. These
can be helpful for reviewing the outcome of automation after it is complete,
sharing and troubleshooting with a colleague, or keeping for compliance or
change-control purposes. The playbook artifact file contains the detailed
information about every play and task, as well as the stdout from the playbook
run. Playbook artifacts can be review with `ansible-navigator replay <filename>`
or `:replay <filename>` while in an ansible-navigator session. All playbook
artifacts can be reviewed with both `--mode stdout` and `--mode interactive`,
depending on the desired view. Playbook artifacts writing can be disabled and
the default file naming convention changed as well.(See the
[settings guide](settings.md) for additional information)

### Why does `vi` open when I use `:open`?

`ansible-navigator` will open anything showing in the terminal in the default
editor. The default is set to either `vi +{line_number} {filename}` or the
current value of the `EDITOR` environment variable. Related to this is the
`editor-console` setting which indicates if the editor is console/terminal
based. Here are examples of alternate settings that may be useful:

```yaml
# emacs
ansible-navigator:
  editor:
    command: emacs -nw +{line_number} {filename}
    console: true
```

```yaml
# vscode
ansible-navigator:
  editor:
    command: code -g {filename}:{line_number}
    console: false
```

```yaml
#pycharm
ansible-navigator:
  editor:
    command: charm --line {line_number} {filename}
    console: false
```

### How do I define volume mounts using an environment variable?

Because the definition of a volume mount may contain the `:` these need to be
delimited with a `;`.

```bash
$ export ANSIBLE_NAVIGATOR_EXECUTION_ENVIRONMENT_VOLUME_MOUNTS /tmp/1:/tmp/1\;/tmp/2:/tmp/2:Z
$ ansible-navigator exec
bash-4.4# ls /tmp/1
file.txt
```

### How can `tls-verify` be disabled when an execution environment image is being pulled?

Although disabling TLS verification is not recommended, it may be necessary in
lab and non-production environments. The pull policy parameters can be provided
on the command line or in the settings file.

```bash
$ ansible-navigator --pull-arguments=--tls-verify=false
```

```yaml
ansible-navigator:
  execution-environment:
    pull:
      arguments:
        - "--tls-verify=false"
```

## SSH keys

### How do I use my SSH keys with an execution environment?

The simplest way to use SSH keys with an execution environment is to use
`ssh-agent` and use default key names. Register keys as needed if they do not
use one of the default key names. (`~/.ssh/id_rsa`, `~/.ssh/id_dsa`,
`~/.ssh/id_ecdsa`, `~/.ssh/id_ed25519`, and `~/.ssh/identity`. (eg
`ssh-add ~/.ssh/my_key`). `ansible-navigator` will automatically setup and
enable the use of `ssh-agent` within the execution environment by volume
mounting the SSH authentication socket path and setting the SSH_AUTH_SOCK
environment variable. (eg

`-v /run/user/1000/keyring/:/run/user/1000/keyring/ -e SSH_AUTH_SOCK=/run/user/1000/keyring/ssh`
(as seen in the `ansible-navigator` log file when using an execution environment
and `--log-level debug`)

The use of `ssh-agent` results in the simplest configuration and eliminates
issues with SSH key passphrases when using `ansible-navigator` with execution
environments.

Additionally, `ansible-navigator` will automatically volume mount the user's SSH
keys into the execution environment in 2 different locations to assist users not
running `ssh-agent`.

1. For compatibility with SSH connections using OpenSSH, the keys are mounted
   into the home directory of the default user within the execution environment
   as specified by the user's entry in the execution environment's `/etc/passwd`
   file. When using OpenSSH without `ssh-agent`, only keys using the default
   names (`id_rsa`, `id_dsa`, `id_ecdsa`, `id_ed25519`, and `id_xmss`) will be
   used. The use of `ansible_ssh_private_key_file` will enable the use of
   non-default named keys.

`-v /home/current_user/.ssh/:/root/.ssh/` (as seen in the `ansible-navigator`
log file when using an execution environment and `--log-level debug`)

2. For compatibility with SSH connections using `paramiko`, the keys are mounted
   into the home directory of the default user within the execution environment
   as specified by the `HOME` environment variable within the execution
   environment. When using `paramiko` without `ssh-agent`, only key using
   default names (`id_rsa`, `id_dsa` or `id_ecdsa`, and `id_ed25519`) will by
   used. The use of `ansible_ssh_private_key_file` will enable the use of
   non-default named keys.

`-v /home/current_user/.ssh/:/home/runner/.ssh/` (as seen in the
`ansible-navigator` log file when using an execution environment and
`--log-level debug`)

Note: When using `ansible_ssh_private_key_file` with execution environments, the
path to the key needs to reference it's location after being volume mounted to
the execution environment. (eg `/home/runner/.ssh/key_name` or
`/root/.ssh/key_name`). It may be convenient to specify the path to the key as
`~/.ssh/key_name` which will resolve to the user's home directory with or
without the use of an execution environment.

## Compatibility with `ansible-*` utilities

### Why does the playbook hang when `vars_prompt`, `pause/prompt` or `--ask-pass` is used?

By default `ansible-navigator` runs the playbook in the same manner that ansible
controller and AWX would run the playbook. This was done to help playbook
developers author playbooks that would be ready for production. If the use of
`vars_prompt`, `pause\prompt` or `--ask-pass` can not be avoided, use the
`enable-prompts` parameter that disables `playbook-artifact` creation and sets
the mode to `stdout` causing `ansible-navigator` to run the playbook in a manner
that is compatible with `ansible-playbook` and allows for user interaction.

```bash
$ ansible-navigator run site.yml --enable-prompts --ask-pass
```

### How can I use `ansible-test` without having it locally installed?

The `ansible-test` utility can be used from within an execution environment
using the `exec` subcommand.

```bash
$ cd  ./collections/ansible_collections/ansible/utils/
$ ansible-navigator exec -- ansible-test sanity --python 3.9
```

### How do I use `ansible-playbook` parameters like `--forks 15`?

All parameters not directly used by `ansible-navigator` will be passed to the
`ansible-playbook` command. These can be provided inline after the
`ansible-navigator` parameters or delimited by a `--`

```bash
$ ansible-navigator run site.yml --forks 15
$ ansible-navigator run site.yml -- --forks 15
```

### How can I use a vault password with `ansible-navigator`?

The following options provide a vault password to `ansible-navigator` when using
the text-based user interface (TUI). **Please ensure these do not conflict with
your enterprise security standards. Do not add password files to source
control.**

1. Store the vault password securely on the local file system

```bash
$ touch ~/.vault_password
$ chmod 600 ~/.vault_password
# The leading space here is necessary to keep the command out of the command history
$  echo my_password >> ~/.vault_password
# Link the password file into the current working directory
$ ln ~/.vault_password .
# Set the environment variable to the location of the file
$ export ANSIBLE_VAULT_PASSWORD_FILE=.vault_password
# Pass the variable into the execution-environment
$ ansible-navigator run --pass-environment-variable ANSIBLE_VAULT_PASSWORD_FILE site.yml
```

2. Store the vault password in an environment variable

Chances are that your environment prohibits saving passwords in clear text on
disk. If you are subject to such a rule, then this will obviously include any
command history file your shell saves to disk.

In case you use bash, you can leverage
[HISTCONTROL](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html#index-HISTCONTROL)
and an
[environment](https://www.gnu.org/software/bash/manual/html_node/Environment.html)
variable as shown in the following example.

```bash
$ touch ~/.vault_password.sh
$ chmod 700 ~/.vault_password.sh
$ echo -e '#!/bin/sh\necho ${ANSIBLE_VAULT_PASSWORD}' >> ~/.vault_password.sh
# Link the password file into the current working directory
$ ln ~/.vault_password.sh .
# The leading space here is necessary to keep the command out of the command history
# by using an environment variable prefixed with ANSIBLE it will automatically get passed
# into the execution environment
$ HISTCONTROL=ignorespace
$  export ANSIBLE_VAULT_PASSWORD=my_password
# Set the environment variable to the location of the file when executing ansible-navigator
$ ANSIBLE_VAULT_PASSWORD_FILE=.vault_password.sh ansible-navigator run site.yml
```

Additional information about `ansible-vault` can be found
[here](https://docs.ansible.com/ansible/latest/user_guide/vault.html)

## Other

### How can complex commands be run inside an execution-environment?

The easiest way to pass complex commands to an execution environment is by using
the `--` delimiter. Everything after the `--` will be passed into the
execution-environment.

```bash
$ ansible-navigator exec -- ansible --version | head -n 1 | awk -F '\\[|\\]|\\s' '{print $4}'
2.12.4rc1.post0
```

### Why did I get an error about `/dev/mqueue` missing?

Although the `/dev/mqueue` directory is not used by `ansible-navigator`, it is
currently required when using `podman`. Not all operating systems have a
`/dev/mqueue` directory by default.

Please reference the documentation for your operating system related to POSIX
message queues, or simply create the directory.

### Something didn't work, how can I troubleshoot it?

`ansible-navigator` has reasonable logging messages, debug logging can be
enabled with `--log-level debug`. If you think you might have found a bug,
please
[log an issue](https://github.com/ansible/ansible-navigator/issues/new/choose)
and include the details from the log file.
