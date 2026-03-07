"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

from sphinx.util import logging

import os
import re
import pathlib


_logger = logging.getLogger(__name__)


BUILD_PATH = pathlib.Path("docs/_build")


# Project information
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "erado"
copyright = "2026, Oxford Quantum Circuits"
author = "Sam J. Griffiths"


# General configuration
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx_multiversion",
    "autoapi.extension",
    "myst_parser",
]

templates_path = [
    "_templates",
]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

autodoc_typehints = "both"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pydantic": ("https://docs.pydantic.dev/latest", None),
    "qiskit": ("https://quantum.cloud.ibm.com/docs/api/qiskit", None),
    "qiskit-aer": ("https://qiskit.github.io/qiskit-aer", None),
}


# Options for HTML output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

ACCENT_COLOUR = "#ff8001"
API_COLOUR = "#4682b4"

html_theme = "furo"
html_static_path = [
    "_static",
]

html_title = "erado | docs"

html_theme_options = {
    "light_logo": "OQC-Logo-Black.svg",
    "dark_logo": "OQC-Logo-White.svg",
    "light_css_variables": {
        "color-brand-primary": ACCENT_COLOUR,
        "color-brand-content": ACCENT_COLOUR,
        "color-api-name": API_COLOUR,
        "color-api-pre-name": API_COLOUR,
    },
    "dark_css_variables": {
        "color-brand-primary": ACCENT_COLOUR,
        "color-brand-content": ACCENT_COLOUR,
        "color-api-name": API_COLOUR,
        "color-api-pre-name": API_COLOUR,
    },
}


# Furo theme default reference:
# https://daobook.github.io/furo/customisation/sidebar/#default-design
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "versioning.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/scroll-start.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ],
}


# Options for AutoAPI
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html

autoapi_dirs = [
    "../src/erado",
]

autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]

autoapi_python_class_content = "both"


# Options for sphinx-multiversion
# https://sphinx-contrib.github.io/multiversion/main/configuration.html

# Releases are tags in the form: vX.X.X(.postX)
RELEASE_PATTERN = r"v\d+\.\d+\.\d+(?:\.post\d+)*"
RELEASE_PATTERN_TAG = r"^" + RELEASE_PATTERN + r"$"
RELEASE_PATTERN_REF = r"^refs\/tags\/" + RELEASE_PATTERN + r"$"

RELEASE_REGEX_TAG = re.compile(RELEASE_PATTERN_TAG)
RELEASE_REGEX_REF = re.compile(RELEASE_PATTERN_REF)

# Store the latest release as a loadable environment variable
ENV_FILE = "version.env"
ENV_LATEST_RELEASE = "ERADO_LATEST_RELEASE"

latest_release_tag = os.environ.get("ERADO_LATEST_RELEASE", "NOT_SET")
_logger.info(f"latest_release_tag: {latest_release_tag}")

smv_released_pattern = RELEASE_PATTERN_REF
smv_latest_version = latest_release_tag

smv_tag_whitelist = RELEASE_PATTERN_TAG
smv_branch_whitelist = r"^main$"


# Event callbacks
# https://www.sphinx-doc.org/en/master/extdev/event_callbacks.html

def skip_submodules(app, what, name, obj, skip, options):
    """Hide private/implementation modules from documentation."""
    SKIPPED_MODULES = [
        "erado.models.circuit_sampler",
        "erado.models.core",
        "erado.models.transpiler_pass",
    ]

    if what == "module" and name in SKIPPED_MODULES:
        _logger.info(f"Skipping module {name}.")
        skip = True

    return skip


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_submodules)
