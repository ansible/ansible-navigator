<!-- markdownlint-disable first-line-heading -->

```{spelling}
de
facto
linters
Pre
reStructuredText
Towncrier
```

```{include} ../../.github/CONTRIBUTING.md

```

# Contributing docs

We use [Sphinx] to generate our docs website. You can trigger
the process locally by executing:

<!-- cspell:disable -->

```shell-session
$ tox -e docs
docs create: .tox/docs
docs installdeps: --editable .[docs]
...

========================================================================================================================

Documentation available under:

    file://.tox/docs/docs_out/index.html

To serve docs, use

    $ python3 -m http.server --directory  ".tox/docs/docs_out" 0

========================================================================================================================
_______________________________________________________ summary ________________________________________________________
  docs: commands succeeded
  congratulations :)
```

<!-- cspell:enable -->

It is also integrated with [Read The Docs] that builds and
publishes each commit to the main branch and generates live
docs previews for each pull request.

The sources of the [Sphinx] documents use reStructuredText as a
de-facto standard. But in order to make contributing docs more
beginner-friendly, we have integrated [MyST parser] allowing us
to also accept new documents written in an extended version of
Markdown that supports using Sphinx directives and roles.
{ref}`Read the docs <myst:intro/writing>` to learn more on how
to use it.

[myst parser]: https://pypi.org/project/myst-parser/
[read the docs]: https://readthedocs.org
[sphinx]: https://www.sphinx-doc.org

```{include} ../changelog-fragments.d/README.md

```
