# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "sutton-signwriting-font"
copyright = "2025, Steve Slevinski <slevinski@signwriting.org>"
author = "Steve Slevinski <slevinski@signwriting.org>"
version = "1.0"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",  # Parse Google-style docstrings
    "sphinx.ext.autodoc",  # Pull docstrings from code
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = []

autodoc_member_order = "bysource"
autodoc_typehints = "description"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]

html_css_files = ["custom.css"]

sys.path.insert(0, os.path.abspath("../.."))
