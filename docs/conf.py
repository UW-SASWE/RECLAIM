import os
import sys

# Point to src directory (adjust if different)
sys.path.insert(0, os.path.abspath("../src"))

project = "RECLAIM"
author = "Sanchit Minocha"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",   # supports Google/NumPy style docstrings
    "sphinx.ext.viewcode",   # adds [source] links
]
templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"