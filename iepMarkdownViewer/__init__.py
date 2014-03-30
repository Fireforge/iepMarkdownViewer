# -*- coding: utf-8 -*-
# Copyright (C) 2014, David Salter
#
# This is distributed under the terms of The MIT License.
# The full license can be found in 'LICENSE'.

import os
import sys
import webbrowser

from pyzolib.qt import QtCore, QtGui
imported_qtwebkit = True
try:
    from pyzolib.qt import QtWebKit
except ImportError:
    imported_qtwebkit = False
import iep
from iep.tools.iepWebBrowser import WebView

# Add the directory of this file so we can access the rest of the package
filedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(filedir)
import markdownparser

tool_name = "Markdown Viewer"
tool_summary = "A live preview of your Markdown in IEP."

accepted_fileext = ['.md',
                    '.markdown',
                    '.txt']
css_link = '<link rel="stylesheet" type="text/css" href="{0}">'


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

            cssurl = filedir + os.sep + "github.css"
            self._cssurl = QtCore.QUrl.fromLocalFile(cssurl)
        else:
            self._view = WebView(self)
            self._view.setOpenExternalLinks(True)
            self._cssurl = None
#         self._view.settings().setUserStyleSheetUrl(self._cssurl)
#         print(self._view.settings().userStyleSheetUrl())

        # Bind to events
        self._view.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        iep.editors.currentChanged.connect(self.onEditorsCurrentChanged)
        iep.editors.parserDone.connect(self.getEditorContent)

        # Get the Markdown parser
        self._md = markdownparser.getparser()

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
