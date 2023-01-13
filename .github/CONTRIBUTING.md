# Contributing to Ansible Navigator

Some background:

The ansible-navigator code base is not just for it's users but current and
future developers. Over time we have adopted a few tools that help us
maintain it and you contribute.

1. mypy (Helps with type checking)

2. pylint (lints all the things)

3. code-spell (prevents typos in code)

4. isort (sorts import statements)

```{note}
In early development cycles, a decision was made to use black as a formatter
which is why current pull-requests are required to pass a
`black --diff` check of the source tree. The decision to use `black` is
left to individual developers as the formatting changes it makes can be
achieved without it.
```

Details can be found below on how to run these manually, our CI will also
check them for you.

In order to contribute, you'll need to:

1. Fork the repository.

2. Create a branch, push your changes there.

3. Send it to us as a PR.

4. Iterate on your PR, incorporating the requested improvements
   and participating in the discussions.

Prerequisites:

1. Have {doc}`tox <tox:index>`.

2. Use {doc}`tox <tox:index>` to run the tests.

3. Before sending a PR, make sure that `lint` passes:

   ```shell-session
   $ tox -e lint
   lint create: .tox/lint
   lint installdeps: .[test]
   lint installed: ...
   lint run-test-pre: PYTHONHASHSEED='4242713142'
   lint run-test: commands[0] | pylint ansible_navigator tests ...
   ...
   _________________________________ summary __________________________________
   lint: commands succeeded
   congratulations :)
   ```

   ```{tip}
   Because the version of python is pinned to a specific version to ensure the
   outcome of running `tox -e lint` locally is the same as `tox -e lint` being run
   by github actions, you may see the following error: `RuntimeError: failed to
   find interpreter for Builtin discover of python_spec='python3.XX'`. This
   indicates the version of python that needs to be installed for tox to run
   locally.
   ```

## Debugging Ansible Navigator with VS Code

Getting started:

After cloning the repository, all we need is to install ansible-navigator from
the source. Use the following command in workspace (root folder of navigator).
This will install all the required dependencies for testing the local changes.

```shell-session
pip install -e .
```

### Configure VSCode settings

Once we are inside vscode with project installed, we need to configure the
`.vscode` folder.
Note: Use any of these two methods mentioned below to create a `.vscode` folder
(only if not present already). Otherwise skip this step and jump to the
configuration of _launch.json_ and _settings.json_ file inside this folder.

**Method 1:** Use Run and Debug View

Select the `Run and Debug` icon in the Activity Bar of VS Code to create
`launch.json` file. Choose 'Python' as debugger and 'Module' as debug
configuration. This step will create launch.json with default configuration
which can be changed later on.

**Method 2:** Use Command Line

VS Code keeps debugging configuration information in a launch.json file located
in a `.vscode` folder in your workspace (project root folder). Hence follow
the given steps to generate 'launch.json' and 'settings.json' using command
line.

```shell-session
machine@machine ~/a/c/ansible-navigator
❯ mkdir .vscode
machine@machine ~/a/c/ansible-navigator
❯ cd .vscode
machine@machine ~/a/c/ansible-navigator/.vscode
❯ touch launch.json settings.json
```

Drop the below configuration in launch.json

```shell-session
{
   "version": "0.2.0",
   "configurations": [
      {
         "name": "Python: Module",
         "type": "python",
         "request": "launch",
         "module": "ansible_navigator",
         "cwd": "${workspaceFolder}/src",
         "justMyCode": false
      }
   ]
}
```

And drop the below configuration in settings.json

```shell-session
{
   "python.testing.unittestEnabled": false,
   "python.testing.pytestEnabled": true
}
```

Now, the final steps!

- Put breakpoint(s) in the code where needed.
- Hover to the Menu Bar and click **Run -> Start Debugging** to start the
  debugger.

At this point, the debugger should hit your breakpoint and start the debugging
session.

### Debug Ansible-Navigator Subcommands

Ansible-Navigator comes in with bunch of [sub-commands]. To debug around any
specific subcommand, we will need to add `args` attribute (arguments passed to
the program to debug) in our launch.json configuration file.

[sub-commands]: https://ansible-navigator.readthedocs.io/en/latest/subcommands/

**Example:**

- Debug `ansible-navigator run` subcommand, use _args_ attribute, provide
  absolute path to the playbook as mentioned. Following configuration will allow
  to debug `ansible-navigator site.yml --mode stdout`.

```shell-session
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Module",
      "type": "python",
      "request": "launch",
      "module": "ansible_navigator",
      "args": ["run", "../Path/to/Playbook/site.yml", "--mode", "stdout"],
      "cwd": "${workspaceFolder}/src",
      "justMyCode": false
    }
  ]
}
```

- Debug `ansible-navigator exec` subcommand using _args_ with some parameter.
  Following configuration will allow to debug `ansible-navigator exec -- pwd`.

```shell-session
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Module",
      "type": "python",
      "request": "launch",
      "module": "ansible_navigator",
      "args": ["exec", "--", "pwd"],
      "cwd": "${workspaceFolder}/src",
      "justMyCode": false
    }
  ]
}
```

- To debug subcommand `ansible-navigator images`, add one more attribute as
  `"args": ["images"]` in our previously configured launch.json.
- To debug subcommand `ansible-navigator collections`, add one more attribute
  as `"args": ["collections"]` in launch.json, and so on.
- Moreover, to debug subcommands with some parameter use
  `"args": ["subcommand-name", "--", "parameter"]`
- While debugging any subcommand with arguments, make sure to use one _args_
  entry at a time in our configuration (comment/remove the ones not in use).

### Useful Links

- VS code debugging [guide].
- Facilitate [Python Debugger] (pdb) in navigator for pure command line
  debugging.

[guide]: https://code.visualstudio.com/docs/editor/debugging
[python debugger]: https://www.geeksforgeeks.org/python-debugger-python-pdb/
