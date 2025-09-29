import os
import sys

# Point to src directory (adjust if different)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

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
html_logo = "_static/Reclaim_logo_clearBG.png"