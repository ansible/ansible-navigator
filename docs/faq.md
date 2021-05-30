## Some frequently asked questions:

**Q: Where should the `ansible.cfg` file go when using an execution environment?**

A: The easiest place to have the `ansible.cfg` is in the project directory adjacent to the playbook. The playbook directory is automatically mounted in the execution enviroment and the `ansible.cfg` file will be found.  If the `ansible.cfg` file is in another directory, the `ANSIBLE_CONFIG` variable needs to be set and the directory specified as a custom volume mount. (See the settings for `execution-environment-volume-mounts`)

**Q: Where should the `ansible.cfg` file go when not using an execution environment?**

A: ansible will look for the `ansible.cfg` in the typical location when not using an exectuion-environment.  (See the ansible docs for the possibilities)

**Q: Why does the playbook hang when `vars_prompt` or `pause/prompt` is used?**

A: By default `ansible-navigator` runs the playbook in the same manner that ansible controller and AWX would run the playbook. This was done to help playbook developers author playbooks that would be ready for production. If the use of `vars_prompt` or `pause\prompt` can not be avoided, disabling `playbook-artifact` creation causes `ansible-navigator` to run the playbook in a manner that is compatible with `ansible-playbook` and allows for user interaction.


**Q: Why does `ansible-navigator` change the terminal colors or look terrible?**

A: `ansible-navigator` queries the terminal for its OSC4 compatibility. OSC4, 10, 11, 104, 110, 111 indicate the terminal supports color changing and reverting. It is possible that the terminal is misrepresenting its ability.  OSC4 detection can be disabled by setting `--osc4 false`. (See the settings for how to handle this with an enviroment variable or in the settings file)

**Q: How can I change the colors used by `ansible-navigator`?**

A: Full theme support should come in a later release, for now try `--osc4 false`. This will cause `ansible-navigaor` to use the terminal's defined colors. (See the settings for how to handle this with an enviroment variable or in the settings file)

**Q: Something didn't work, how can I troubleshoot it?**

A: `ansible-navigator` has reasonable logging messages, debug logging can be enabled with `--log-level debug`. If you think you might have found a bug, please log an issue and include the details from the log file.