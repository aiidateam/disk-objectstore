#
# Configuration file for the Sphinx documentation builder.
#
import disk_objectstore

# -- Project information -----------------------------------------------------

project = "disk-objectstore"
copyright = "2020-2022, The AiiDA team"
author = "The AiiDA team."

# The short X.Y version.
version = ".".join(disk_objectstore.__version__.split(".")[:2])
# The full version, including alpha/beta/rc tags.
release = disk_objectstore.__version__

# -- General configuration ---------------------------------------------------

needs_sphinx = "2.0"
extensions = [
    "myst_parser",
    "sphinx_panels",
    "sphinx.ext.intersphinx",
    "sphinxext.rediraffe",
]

myst_enable_extensions = ["colon_fence", "deflist", "html_image"]

# blog_path = "releases/index"
# blog_title = "Releases"
# blog_post_pattern = "releases/versions/*.md"
post_redirect_refresh = 1
post_auto_excerpt = 2
fontawesome_included = True
# html_sidebars = {"releases/index": ['tagcloud.html', 'archives.html', 'sbt-sidebar-nav.html']}

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_book_theme"
html_title = html_short_title = "disk-objectstore"
html_favicon = "_static/disk-objectstore-favicon.png"
html_logo = "_static/disk-objectstore.png"
html_theme_options = {
    "home_page_in_toc": True,
    "repository_url": "https://github.com/aiidateam/disk-objectstore",
    "repository_branch": "develop",
    "use_repository_button": True,
    "use_issues_button": True,
    "path_to_docs": "docs",
    "use_edit_page_button": True,
}

rediraffe_redirects = "redirects.txt"

html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
]
