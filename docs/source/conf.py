# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
import datetime
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

year = datetime.datetime.now().year
project = 'python201'
copyright = f'2019-{year} Geoffrey Lentner, 2018 Ashwin Srinath'
author = 'Geoffrey Lentner, Ashwin Srinath'

version = '0.0.1'
release = '0.0.1'


# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',
    'sphinx.ext.autodoc',
    'IPython.sphinxext.ipython_directive',
    'IPython.sphinxext.ipython_console_highlighting',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

html_theme = 'pydata_sphinx_theme'
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'
html_static_path = ['_static']
html_theme_options = {
    'external_links': [],
    'github_url': 'https://github.com/glentner/python201',
}


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {}
latex_documents = [
    (master_doc, 'python-201.tex', 'python-201 Documentation',
     'Geoffrey Lentner, Ashwin Srinath', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# manual pages options
man_pages = [(
    'manpage',
    'cumprod',
    'Compute cumulative product of a sequence of numbers.',
    'Geoffrey Lentner <glentner@purdue.edu>.',
    '1'
),
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'python-201', 'python-201 Documentation',
     author, 'python-201', 'One line description of project.',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------
intersphinx_mapping = {'https://docs.python.org/3/': None}

# export variables with epilogue
rst_epilog = f"""
.. |release| replace:: {release}
.. |copyright| replace:: {copyright}
"""
