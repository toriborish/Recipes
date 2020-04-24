# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sphinx_bootstrap_theme
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils import nodes
from docutils.parsers.rst.roles import set_classes

# sys.path.insert(0, os.path.abspath('.'))

# Hack for lacking git-lfs support on ReadTheDocs
# (mainly gotten from https://test-builds.readthedocs.io/en/git-lfs/conf.html)
if os.environ.get('READTHEDOCS', None) == 'True':
    if not os.path.exists('./git-lfs'):
        import requests
        from urllib.parse import urlparse
        # figure out what's the latest releast of git-lfs
        r = requests.get("https://api.github.com/repos/git-lfs/git-lfs/releases/latest")
        # find the download url for the latest release for Linux AMD
        assets = r.json()["assets"]
        url_to_download = list(
            filter(lambda x: x["label"] == "Linux AMD64", assets)
        )[0]['browser_download_url']
        # download
        os.system('wget ' + url_to_download)
        # uncompress
        path = os.path.basename(urlparse(url_to_download).path)
        os.system('tar xvfz ' + path)
        # install
        os.system('./git-lfs install')  # make lfs available in current repository
    os.system('./git-lfs fetch')  # download content from remote
    os.system('./git-lfs checkout')  # make local files to have the real content on them

# -- Project information -----------------------------------------------------

project = 'Recipes'
copyright = '2020, Carlo Giacometti'
author = 'Carlo Giacometti'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

master_doc = 'index'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme_options = {
    'source_link_position': "nav",
    'bootswatch_theme': "paper",
    'navbar_pagenav': False,
    'navbar_site_name': "Chapters",
    'navbar_sidebarrel': True,
    'bootstrap_version': "3",
    'globaltoc_depth': -1
    }

html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


class Ingredients(BaseAdmonition):

    required_arguments = 0
    node_class = nodes.admonition

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        text = '\n'.join(self.content)
        admonition_node = self.node_class(text, **self.options)
        self.add_name(admonition_node)
        if self.node_class is nodes.admonition:
            title_text = 'Ingredients'
            textnodes, messages = self.state.inline_text(title_text,
                                                         self.lineno)
            title = nodes.title(title_text, '', *textnodes)
            title.source, title.line = (
                    self.state_machine.get_source_and_line(self.lineno))
            admonition_node += title
            admonition_node += messages
            if 'classes' not in self.options:
                admonition_node['classes'] += ['admonition-' +
                                               nodes.make_id(title_text)]
        self.state.nested_parse(self.content, self.content_offset,
                                admonition_node)
        return [admonition_node]


def setup(app):
    print(os.getcwd())
    app.add_stylesheet("source/_static/styles.css")
    app.add_stylesheet("_static/styles.css")
    app.add_stylesheet("styles.css")
    app.add_directive('ingredients', Ingredients)


# -- Options for LaTeX output ---------------------------------------------

latex_engine = 'pdflatex'
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    'papersize': 'a4paper',
    'releasename':" ",
    # Sonny, Lenny, Glenn, Conny, Rejne, Bjarne and Bjornstrup
    # 'fncychap': '\\usepackage[Lenny]{fncychap}',
    # 'fncychap': '\\usepackage{fncychap}',
    'fontpkg': '\\usepackage{amsmath,amsfonts,amssymb,amsthm}',

    'figure_align':'htbp',
    # The font size ('10pt', '11pt' or '12pt').
    #
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    'preamble': r'''
        %%%%%%%%%%%%%%%%%%%% Meher %%%%%%%%%%%%%%%%%%
        %%%add number to subsubsection 2=subsection, 3=subsubsection
        %%% below subsubsection is not good idea.
        \setcounter{secnumdepth}{1}
        %
        %%%% Table of content upto 2=subsection, 3=subsubsection
        \setcounter{tocdepth}{1}

        \usepackage{amsmath,amsfonts,amssymb,amsthm}
        \usepackage{graphicx}

        %%% reduce spaces for Table of contents, figures and tables
        %%% it is used "\addtocontents{toc}{\vskip -1.2cm}" etc. in the document
        \usepackage[notlot,nottoc,notlof]{}

        \usepackage{color}
        \usepackage{transparent}
        \usepackage{eso-pic}
        \usepackage{lipsum}

        \usepackage{footnotebackref} %%link at the footnote to go to the place of footnote in the text

        %% spacing between line
        \usepackage{setspace}
        %%%%\onehalfspacing
        %%%%\doublespacing
        \singlespacing


        %%%%%%%%%%% datetime
        \usepackage{datetime}

        \newdateformat{MonthYearFormat}{%
            \monthname[\THEMONTH], \THEYEAR}


        %% RO, LE will not work for 'oneside' layout.
        %% Change oneside to twoside in document class
        \usepackage{fancyhdr}
        \pagestyle{fancy}
        \fancyhf{}

        %%% Alternating Header for oneside
        \fancyhead[L]{\ifthenelse{\isodd{\value{page}}}{ \small \nouppercase{\leftmark} }{}}
        \fancyhead[R]{\ifthenelse{\isodd{\value{page}}}{}{ \small \nouppercase{\rightmark} }}

        %%% Alternating Header for two side
        %\fancyhead[RO]{\small \nouppercase{\rightmark}}
        %\fancyhead[LE]{\small \nouppercase{\leftmark}}

        %%% page number
        \fancyfoot[CO, CE]{\thepage}

        \renewcommand{\headrulewidth}{0.5pt}
        \renewcommand{\footrulewidth}{0.5pt}

        \RequirePackage{tocbibind} %%% comment this to remove page number for following
        \addto\captionsenglish{\renewcommand{\contentsname}{Table of contents}}
        % \addto\captionsenglish{\renewcommand{\chaptername}{Chapter}}


        %%reduce spacing for itemize
        \usepackage{enumitem}
        \setlist{nosep}

        %%%%%%%%%%% Quote Styles at the top of chapter
        \usepackage{epigraph}
        \setlength{\epigraphwidth}{0.8\columnwidth}
        \newcommand{\chapterquote}[2]{\epigraphhead[60]{\epigraph{\textit{#1}}{\textbf {\textit{--#2}}}}}
        %%%%%%%%%%% Quote for all places except Chapter
        \newcommand{\sectionquote}[2]{{\quote{\textit{``#1''}}{\textbf {\textit{--#2}}}}}
    ''',


    'maketitle': r'''
        \pagenumbering{Roman} %%% to avoid page 1 conflict with actual page 1

        \begin{titlepage}
            \centering

            \vspace*{40mm} %%% * is used to give space from top
            \textbf{\Huge {Recipes}}

            \vspace{0mm}

            \vspace{0mm}
            \Large \textbf{{Carlo Giacometti}}


            %% \vfill adds at the bottom
            \vfill
        \end{titlepage}

        \clearpage
        \pagenumbering{roman}
        \tableofcontents
        \clearpage
        \pagenumbering{arabic}

        ''',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
    'sphinxsetup': 'hmargin={0.7in,0.7in}, vmargin={1in,1in}, \
        verbatimwithframe=true, \
        TitleColor={rgb}{0,0,0}, \
        HeaderFamily=\\rmfamily\\bfseries, \
        InnerLinkColor={rgb}{0,0,1}, \
        OuterLinkColor={rgb}{0,0,1}',
    'tableofcontents':' '
}
