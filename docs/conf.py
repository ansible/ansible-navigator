# cspell:ignore ansiblefest, cyaml, DONT, fchainmap, linkify, toctree
# pylint: disable=invalid-name
# Ref: https://www.sphinx-doc.org/en/master/usage/configuration.html
"""Configuration file for the Sphinx docs."""

from functools import partial
from pathlib import Path
from sys import path

from setuptools_scm import get_version
from setuptools_scm.git import fetch_on_shallow
from setuptools_scm.git import parse


# -- Special accommodations for RTD ------------------------------------------


def parse_with_fetch(*args, **kwargs) -> str:
    """If the repo is found to be shallow, fetch a full.

    By default, RTD does a fetch --limit 50, if a tag is not
    present in the last 50 commits, the version reported by setuptools_scm
    will be incorrect and appears as ``v0.1.dev...`` in the towncrier changelog.
    Another approach is to enable ``DONT_SHALLOW_CLONE`` for the repo
    https://docs.readthedocs.io/en/stable/feature-flags.html#feature-flags
    This was done for ansible-navigator on the day of this commit.

    :param args: The arguments
    :param kwargs: The keyword arguments
    :returns: The parsed version
    """
    assert "pre_parse" not in kwargs
    return parse(*args, pre_parse=fetch_on_shallow, **kwargs)


get_scm_version = partial(get_version, parse=parse_with_fetch)

# -- Path setup --------------------------------------------------------------

PROJECT_ROOT_DIR = Path(__file__).parents[1].resolve()
get_scm_version = partial(get_scm_version, root=PROJECT_ROOT_DIR)

# Make in-tree extension importable in non-tox setups/envs, like RTD.
# Refs:
# https://github.com/readthedocs/readthedocs.org/issues/6311
# https://github.com/readthedocs/readthedocs.org/issues/7182
path.insert(0, str((Path(__file__).parent / "_ext").resolve()))


# -- Project information -----------------------------------------------------

ansible_homepage_url = "https://www.ansible.com"
github_url = "https://github.com"
github_repo_org = "ansible"
github_repo_name = "ansible-navigator"
github_repo_slug = f"{github_repo_org}/{github_repo_name}"
github_repo_url = f"{github_url}/{github_repo_slug}"
github_sponsors_url = f"{github_url}/sponsors"

project = "Ansible Navigator"
author = f"{project} project contributors"
copyright = author  # pylint:disable=redefined-builtin

# The short X.Y version
version = ".".join(get_scm_version(local_scheme="no-local-version").split(".")[:3])

# The full version, including alpha/beta/rc tags
release = get_scm_version()

rst_epilog = f"""
.. |project| replace:: {project}
.. |release_l| replace:: ``v{release}``
"""


# -- General configuration ---------------------------------------------------


# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ""  # noqa: E800
# Else, today_fmt is used as the format for a strftime call.
today_fmt = "%B %d, %Y"

# The reST default role (used for this markup: `text`) to use for all
# documents.
# Ref: python-attrs/attrs#571
default_role = "any"

# If true, "()" will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "ansible"

nitpicky = True
nitpick_ignore = [
    ("py:class", "_Rule"),
    (
        "py:class",
        "ansible_navigator.configuration_subsystem.defs_presentable.PresentableSettingsEntries",
    ),
    ("py:class", "ansible_navigator.configuration_subsystem.defs_presentable.TCli"),
    ("py:class", "ansible_navigator.configuration_subsystem.defs_presentable.TEnt"),
    ("py:class", "ansible_navigator.tm_tokenize.fchainmap.TKey"),
    ("py:class", "ansible_navigator.tm_tokenize.fchainmap.TValue"),
    ("py:class", "ansible_runner.runner.Runner"),
    ("py:class", "argparse._SubParsersAction"),
    ("py:class", "Captures"),
    ("py:class", "CompiledRegsetRule"),
    ("py:class", "CompiledRule"),
    ("py:class", "Compiler"),
    ("py:class", "ContentBase"),
    ("py:class", "ContentView"),
    ("py:class", "CursesLine"),
    ("py:class", "CursesLines"),
    ("py:class", "dataclasses.InitVar"),
    ("py:class", "Entry"),
    ("py:class", "FieldButton"),
    ("py:class", "FieldChecks"),
    ("py:class", "FieldInformation"),
    ("py:class", "FieldRadio"),
    ("py:class", "FieldWorking"),
    ("py:class", "Form"),
    ("py:class", "Grammar"),
    ("py:class", "Grammars"),
    ("py:class", "Internals"),
    ("py:class", "IO"),
    ("py:class", "Match"),
    ("py:class", "multiprocessing.context.BaseContext.Queue"),
    ("py:class", "NavigatorPostProcessor"),
    ("py:class", "Pattern"),
    ("py:class", "PatternRule"),
    ("py:class", "Region"),
    ("py:class", "Regions"),
    ("py:class", "Scope"),
    ("py:class", "State"),
    ("py:class", "WhileRule"),
    ("py:class", "Window"),
    ("py:class", "yaml.cyaml.CSafeDumper"),
    ("py:class", "yaml.nodes.ScalarNode"),
    ("py:obj", "ansible_navigator.tm_tokenize.fchainmap.TKey"),
    ("py:obj", "ansible_navigator.tm_tokenize.fchainmap.TValue"),
]

nitpick_ignore_regex = [
    # Any single letter TypeVar, class or object
    ("py:(class|obj)", r"^.*\.[A-Z]$"),
]

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    # stdlib-party extensions:
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    # Third-party extensions:
    "myst_parser",
    "notfound.extension",
    "sphinxcontrib.apidoc",
    "sphinxcontrib.towncrier",  # provides `towncrier-draft-entries` directive
    "sphinx_copybutton",
    # Tree-local extensions:
    "single_sourced_data",  # in-tree extension
]

# Conditional third-party extensions:
try:
    import sphinxcontrib.spelling as _sphinxcontrib_spelling
except ImportError:
    extensions.append("spelling_stub_ext")
else:
    del _sphinxcontrib_spelling
    extensions.append("sphinxcontrib.spelling")

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "changelog-fragments.d/**",  # Towncrier-managed change notes
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_ansible_theme"

html_show_sphinx = True

html_theme_options = {
    "collapse_navigation": False,
    "analytics_id": "",
    "style_nav_header_background": "#5bbdbf",
    "style_external_links": True,
    "canonical_url": f"https://{github_repo_name}.readthedocs.io/en/latest/",
    "vcs_pageview_mode": "edit",
    "topbar_links": {
        "AnsibleFest": f"{ansible_homepage_url}/ansiblefest",
        "Products": f"{ansible_homepage_url}/tower",
        "Community": f"{ansible_homepage_url}/community",
        "Webinars & Training": f"{ansible_homepage_url}/webinars-training",
        "Blog": f"{ansible_homepage_url}/blog",
    },
    "navigation_depth": 3,
}

html_context = {
    "display_github": True,
    "github_user": github_repo_org,
    "github_repo": github_repo_name,
    "github_version": "main/docs/",
    "current_version": version,
    "latest_version": "latest",
    "available_versions": ("latest",),
}


# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = f"{project} Documentation"

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "Documentation"

# If not "", a "Last updated on:" timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%b %d, %Y"

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
html_use_opensearch = f"https://{github_repo_name}.readthedocs.io/en/latest/"

# The master toctree document.
root_doc = master_doc = "index"  # Sphinx 4+ / 3-


# -- Extension configuration -------------------------------------------------

# -- Options for extlinks extension ---------------------------------------
extlinks = {
    "issue": (f"{github_repo_url}/issues/%s", "#"),  # noqa: WPS323
    "pr": (f"{github_repo_url}/pull/%s", "PR #"),  # noqa: WPS323
    "commit": (f"{github_repo_url}/commit/%s", ""),  # noqa: WPS323
    "gh": (f"{github_url}/%s", "GitHub: "),  # noqa: WPS323
    "user": (f"{github_sponsors_url}/%s", "@"),  # noqa: WPS323
}

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "ansible-runner": ("https://ansible-runner.readthedocs.io/en/latest", None),
    "myst": ("https://myst-parser.readthedocs.io/en/latest", None),
    "python": ("https://docs.python.org/3", None),
    "python2": ("https://docs.python.org/2", None),
    "tox": ("https://tox.wiki/en/latest", None),
}

# -- Options for sphinxcontrib.apidoc extension ------------------------------

apidoc_extra_args = [
    "--implicit-namespaces",
    "--private",  # include “_private” modules
]
apidoc_module_dir = "../src/ansible_navigator"
apidoc_module_first = False
apidoc_output_dir = "pkg"
apidoc_separate_modules = True
apidoc_toc_file = None

# -- Options for linkcheck builder -------------------------------------------

linkcheck_workers = 25

# -- Options for towncrier_draft extension -----------------------------------

towncrier_draft_autoversion_mode = "draft"  # or: "sphinx-version", "sphinx-release"
towncrier_draft_include_empty = True
towncrier_draft_working_directory = PROJECT_ROOT_DIR
# Not yet supported: towncrier_draft_config_path = "pyproject.toml"  # relative to cwd

# -- Options for myst_parser extension ---------------------------------------

myst_enable_extensions = [
    "colon_fence",  # allow to optionally use ::: instead of ```
    "deflist",
    "html_admonition",  # allow having HTML admonitions
    "html_image",  # allow HTML <img> in Markdown
    "linkify",  # auto-detect URLs @ plain text, needs myst-parser[linkify]
    "replacements",  # allows Jinja2-style replacements
    "smartquotes",  # use "cursive" quotes
    "substitution",  # replace common ASCII shortcuts into their symbols
]
myst_substitutions = {
    "project": project,
    "release": release,
    "release_l": f"`v{release}`",
    "version": version,
}
