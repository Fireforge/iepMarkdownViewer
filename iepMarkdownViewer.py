# -*- coding: utf-8 -*-
# Copyright (C) 2014, David Salter
#
# This is distributed under the terms of The MIT License.
# The full license can be found in 'LICENSE'.

import os
import webbrowser
from pyzolib.qt import QtCore, QtGui
imported_qtwebkit = True
try:
    from pyzolib.qt import QtWebKit
except ImportError:
    imported_qtwebkit = False

import markdown
from mdx_linkify.mdx_linkify import LinkifyExtension

import iep
from iep.tools.iepWebBrowser import WebView

tool_name = "Markdown Viewer"
tool_summary = "A live preview of your Markdown in IEP."

accepted_fileext = ['.md',
                    '.markdown',
                    '.txt']
css_link = '<link rel="stylesheet" type="text/css" href="{0}">'


def dont_linkify_python(attrs, new=False):
    if not new:  # This is an existing <a> tag, leave it be.
        return attrs

    # If the TLD is '.py', make sure it starts with http: or https:
    text = attrs['_text']
    if text.endswith('.py') and \
       not text.startswith(('www.', 'http:', 'https:')):
        # This looks like a Python file, not a URL. Don't make a link.
        return None

    # Everything checks out, keep going to the next callback.
    return attrs
linkify_configs = {
    'linkifycallbacks': [[dont_linkify_python], '']
}
linkify = LinkifyExtension(configs=linkify_configs)
markdown_extensions = ['extra',
                       'codehilite',
                       'sane_lists',
                       linkify]


class IepMarkdownViewer(QtGui.QFrame):
    """ The main window, containing browser widget.
    """

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        # Init config
        toolId = self.__class__.__name__.lower()
        self._config = iep.config.tools[toolId]

        # Create web view
        if imported_qtwebkit:
            self._view = QtWebKit.QWebView()
            page = self._view.page()
            page.setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
            page.linkClicked.connect(self.onLinkClicked)

            filedir = os.path.abspath(os.path.dirname(__file__))
            cssurl = filedir + os.sep + "github.css"
            self._cssurl = QtCore.QUrl.fromLocalFile(cssurl)
        else:
            self._view = WebView(self)
            self._view.setOpenExternalLinks(True)
            self._cssurl = None
#         self._view.settings().setUserStyleSheetUrl(self._cssurl)
#         print(self._view.settings().userStyleSheetUrl())

        # Bind to events
        iep.editors.currentChanged.connect(self.onEditorsCurrentChanged)
        iep.editors.parserDone.connect(self.getEditorContent)

        # Create Markdown parser
        self._md = markdown.Markdown(extensions=markdown_extensions)

        # Layout
        self._sizer1 = QtGui.QVBoxLayout(self)
        self._sizer2 = QtGui.QHBoxLayout()
        #
        self._sizer1.addLayout(self._sizer2, 0)
        self._sizer1.addWidget(self._view, 1)
        #
        self._sizer1.setSpacing(2)
        self.setLayout(self._sizer1)

        # Start
        self.getEditorContent()
        self._view.show()

    def onEditorsCurrentChanged(self):
        self.getEditorContent()

    def getEditorContent(self):
        # Get editor
        if not iep:
            return

        editor = iep.editors.getCurrentEditor()
        if not editor:
            return

        if os.path.splitext(editor.filename)[1] in accepted_fileext:
            text = editor.toPlainText()
            html = self._md.convert(text)
            if self._cssurl:
                html = css_link.format(self._cssurl.toString()) + html
            self._view.setHtml(html)
        else:
            self._view.setHtml('')

    def onLinkClicked(self, url):
        webbrowser.open(url.toString())
