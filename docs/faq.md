## Some frequently asked questions:

**Q: Where should the `ansible.cfg` file go when using an execution environment?**

A: The easiest place to have the `ansible.cfg` is in the project directory adjacent to the playbook. The playbook directory is automatically mounted in the execution enviroment and the `ansible.cfg` file will be found.  If the `ansible.cfg` file is in another directory, the `ANSIBLE_CONFIG` variable needs to be set and the directory specified as a custom volume mount. (See the [settings guide](settings.rst) for `execution-environment-volume-mounts`)

**Q: Where should the `ansible.cfg` file go when not using an execution environment?**

A: ansible will look for the `ansible.cfg` in the typical locations when not using an execution-environment.  (See the ansible docs for the possibilities)

**Q: Where should ansible collections be placed when using an execution environment?**

A: The easiest place to have ansible collections is in the project directory, in a playbook adjacent collections directory. (eg `ansible-galaxy collections install ansible.utils -p ./collections`).  The playbook directory is automatically mounted in the execution environment and the collections should be found. Another option is to build the collections into an execution environment using [ansible builder](https://ansible-builder.readthedocs.io/en/latest/). This was done to help playbook developers author playbooks that are production ready, as both ansible controller and awx support playbook adjacent collection directories. If the collections are in another directory, the `ANSIBLE_COLLECTIONS_PATHS` variable needs to be set and the directory specified as a custom volume mount. (See the [settings guide](settings.rst) for `execution-environment-volume-mounts`)

**Q: Where should ansible collections be placed when not using an execution environment?**

A: When not using an execution enviroment, ansible will look in the default locations for collections.  For more information about these, check out the [collections guide](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).

**Q: Why does the playbook hang when `vars_prompt` or `pause/prompt` is used?**

A: By default `ansible-navigator` runs the playbook in the same manner that ansible controller and AWX would run the playbook. This was done to help playbook developers author playbooks that would be ready for production. If the use of `vars_prompt` or `pause\prompt` can not be avoided, disabling `playbook-artifact` creation causes `ansible-navigator` to run the playbook in a manner that is compatible with `ansible-playbook` and allows for user interaction.

**Q: Why does `ansible-navigator` change the terminal colors or look terrible?**

A: `ansible-navigator` queries the terminal for its OSC4 compatibility. OSC4, 10, 11, 104, 110, 111 indicate the terminal supports color changing and reverting. It is possible that the terminal is misrepresenting its ability.  OSC4 detection can be disabled by setting `--osc4 false`. (See the [settings guide](settings.rst) for how to handle this with an enviroment variable or in the settings file)

**Q: How can I change the colors used by `ansible-navigator`?**

A: Full theme support should come in a later release, for now, try `--osc4 false`. This will cause `ansible-navigator` to use the terminal's defined colors. (See the [settings guide](settings.rst) for how to handle this with an enviroment variable or in the settings file)

**Q: What's with all these `site-artifact-2021-06-02T16:02:33.911259+00:00.json` files in the playbook directory?**

A: `ansible-navigator` creates a playbook artifact for every playbook run.  These can be helpful for reviewing the outcome of automation after it is complete, sharing and troubleshooting with a colleague, or keeping for compliance or change-control purposes.  The playbook artifact file contains the detailed information about every play and task, as well as the stdout from the playbook run. Playbook artifacts can be review with `ansible-navigator replay <filename>` or `:replay <filename>` while in an ansible-navigator session. All playbook artifacts can be reviewed with both `--mode stdout` and `--mode interactive`, depending on the desired view. Playbook artifacts writing can be disabled and the default file naming convention changed as well.(See the [settings guide](settings.rst) for additional information)

**Q: Why does `vi` open when I use `:open`?**

A: `ansible-navigator` will open anything showing in the terminal in the default editor.  The default is set to either `vi +{line_number} {filename}` or the current value of the `EDITOR` environment variable. Related to this is the `editor-console` setting which indicates if the editor is console/terminal based. Here are examples of alternate settings that may be useful:

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

**Q: What is the order in which configuration settings are aplied?**

The configuration system of ansible-navigator pulls in settings from various sources and applies them hierarchically in the following order (where the last applied changes are the most prevalent):

1. Default internal values
2. Values from a [settings file](settings.rst)
3. Values from environment variables
4. Flags and arguments specified on the command line
5. While issuing `:` commands within the text-based user interface (TUI)

**Q: Something didn't work, how can I troubleshoot it?**

A: `ansible-navigator` has reasonable logging messages, debug logging can be enabled with `--log-level debug`. If you think you might have found a bug, please log an issue and include the details from the log file.
