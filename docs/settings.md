# ansible-navigator settings

## The ansible-navigator settings file

Settings for `ansible-navigator` can be provided on the command line, set using
an environment variable or specified in a settings file.

The settings file name and path can be specified with an environment variable or
it can be placed in one of two default directories.

Currently the following are checked and the first match is used:

- `ANSIBLE_NAVIGATOR_CONFIG` (settings file path environment variable if set)
- `./ansible-navigator.<ext>` (project directory) (**NOTE:** no dot in the file
  name)
- `~/.ansible-navigator.<ext>` (home directory) (**NOTE:** note the dot in the
  file name)

!!! note

    - The settings file can be in `JSON` or `YAML` format.
    - For settings in `JSON` format, the extension must be `.json`.
    - For settings in `YAML` format, the extension must be `.yml` or `.yaml`.
    - The project and home directories can only contain one settings file each.
    - If more than one settings file is found in either directory, it will
      result in an error.

You can copy the example settings file below into one of those paths to start
your `ansible-navigator` settings file.

{!.generated/ansible-navigator.yml!}

The following table describes all available settings.

{!.generated/settings-dump.md!}
