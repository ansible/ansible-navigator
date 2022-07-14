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

2. Create a branch, push your changes there. Don't forget to
   {ref}`include news files for the changelog <_ansible_navigator_adding_changelog_fragments>`.

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
