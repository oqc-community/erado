"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import sphinx.util.logging


_logger = sphinx.util.logging.getLogger(__name__)


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

html_theme = "furo"
html_static_path = [
    "_static",
]

html_title = "erado | docs"

html_theme_options = {
    "light_logo": "OQC-Logo-Black.svg",
    "dark_logo": "OQC-Logo-White.svg",
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
