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

# HTML copyright with links
copyright = (
    'Written and maintained by <a href="https://www.linkedin.com/in/sanchitminochaiitr/">Sanchit Minocha</a>. '
    '&copy; 2023, <a href="https://saswe.net/">University of Washington SASWE Research Group</a>'
)

# If you want more control, you can use html_context (used by some themes)
html_context = {
    'display_github': False,
    'last_updated': True,
}

# -- Optional: LaTeX output (for PDF) --------------------------------------
latex_elements = {
    'maketitle': r'\author{Sanchit Minocha \\ University of Washington SASWE Research Group}'
}