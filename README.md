# ansible-navigator

[//]: # (DO-NOT-REMOVE-docs-intro-START)

A text-based user interface (TUI) for Ansible.

A demo of the interface can be found [on YouTube][YT demo].

[YT demo]: https://www.youtube.com/watch?v=J9PBKi8ydi4

[//]: # (DO-NOT-REMOVE-docs-intro-END)

## Quick start

### Installing

Getting started with ansible-navigator is as simple as:

```
pip3 install 'ansible-navigator[ansible-core]'
ansible-navigator --help
```

(Users wishing to install within a virtual environment might find the relevant
[Python documentation][Python venv doc] useful.)

By default, ansible-navigator uses a container runtime (`podman` or `docker`,
whichever it finds first) and runs Ansible within an execution environment
(a pre-built container image which includes [ansible-core] along with a set
of Ansible collections.)

This default behavior can be disabled by starting ansible-navigator with
`--execution-environment false`. In this case, Ansible and any collections
needed must be installed manually on the system.

[ansible-core]: https://docs.ansible.com/ansible-core/devel
[Python venv doc]: https://docs.python.org/3/library/venv.html

Additional `Linux`, `macOS` and `Windows with WSL2` installation
instructions are available in the [Installation guide].

[Installation guide]:
https://ansible-navigator.readthedocs.io/installation/

## Welcome

When running `ansible-navigator` with no arguments, you will be presented with
the *welcome page*. From this page, you can run playbooks, browse collections,
explore inventories, read Ansible documentation, and more.

A full list of key bindings can be viewed by typing `:help`.

## Output modes

There are two modes in which ansible-navigator can be run:

* The **interactive** mode, which provides a curses-based user interface and
  allows you to "zoom in" on data in real time, filter it, and navigate between
  various Ansible components; and
* The **stdout** mode, which does *not* use curses, and simply returns the
  output to the terminal's standard output stream, as Ansible's commands
  would.

The **interactive** mode is the default and this default can be overwritten by
passing `--mode stdout` (`-m stdout`) or setting `mode` in
[configuration][settings documentation].

[settings documentation]: https://ansible-navigator.readthedocs.io/settings/

## Example commands

All of ansible-navigator's features can be accessed from the *welcome page*
described above, but as a shortcut, commands can also be provided directly as
command-line arguments.

Some examples:

* Review and explore available collections: `ansible-navigator collections`
* Review and explore current Ansible configuration: `ansible-navigator config`
* Review and explore Ansible documentation:
  `ansible-navigator doc ansible.netcommon.cli_command`
* Review execution environment images available locally:
  `ansible-navigator images`
* Review and explore an inventory:
  `ansible-navigator inventory -i inventory.yaml`
* Run and explore a playbook:
  `ansible-navigator run site.yaml -i inventory.yaml`

Or using the **stdout** mode described above:

* Show the current Ansible configuration:
  `ansible-navigator config dump -m stdout`
* Show documentation: `ansible-navigator doc sudo -t become  -m stdout`

... and so on. A full list of subcommands and their relation to Ansible
commands can be found in the [subcommand documentation].

[subcommand documentation]:
https://ansible-navigator.readthedocs.io/subcommands/

## Configuring ansible-navigator

There are several ways to configure ansible-navigator and users and projects
are free to choose the most convenient method for them. The full hierarchy of
how various configuration sources are applied can be found in the FAQ mentioned
below.

Of note, projects making use of ansible-navigator can include a project-wide
configuration file with the project. If one is not found, ansible-navigator
will look for a user-specific configuration file in the user's home directory.
Details about this can be found in the [settings documentation].

## Frequently Asked Questions (FAQ)

We maintain a [list of common questions][FAQ] which provides a good
resource to check if something is tripping you up. We also encourage additions
to this document for the greater community!

[FAQ]: https://ansible-navigator.readthedocs.io/faq/

## License

ansible-navigator is released under the Apache License version 2. See the
[LICENSE] file for more details.

[LICENSE]: https://github.com/ansible/ansible-navigator/blob/main/LICENSE
