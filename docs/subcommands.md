# ansible-navigator subcommands

{!.generated/subcommands-overview.md!}

## Mapping ansible-navigator commands to ansible commands

Some ansible-navigator commands map to ansible commands. The list below provides
some examples.

### `ansible`

Use `ansible-navigator exec -- ansible` from shell. The exec subcommand requires
execution environment support.

### `ansible-builder`

Use `ansible-navigator builder` from shell.`ansible-builder` is installed with
`ansible-navigator`

### `ansible-config`

Use `ansible-navigator config` from shell, or `:config` from the
`ansible-navigator` prompt.

### `ansible-doc`

Use `ansible-navigator doc` from shell, or `:doc` from the `ansible-navigator`
prompt.

### `ansible-inventory`

Use `ansible-navigator inventory` from shell, or `:inventory` from the
`ansible-navigator` prompt.

### `ansible-galaxy`

Use `ansible-navigator exec -- ansible-galaxy ...` from shell. The exec
subcommand requires execution environment support.

### `ansible-lint`

Use `ansible-navigator lint` from shell, or `:lint` from the `ansible-navigator`
prompt. `ansible-lint` needs to be installed locally or in the selected
execution-environment.

### `ansible-playbook`

Use `ansible-navigator run` from shell or `:run` from the `ansible-navigator`
prompt.

### `ansible-test`

Use `ansible-navigator exec -- ansible-test ...` from shell. The `exec`
subcommand requires execution environment support.

### `ansible-vault`

Use `ansible-navigator exec -- ansible-vault ...` from shell. The `exec`
subcommand requires execution environment support.
