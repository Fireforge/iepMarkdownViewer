# -*- coding: utf-8 -*-
# Copyright (C) 2013, the IEP development team
#
# IEP is distributed under the terms of the (new) BSD License.
# The full license can be found in 'license.txt'.

import os
import time
import webbrowser
import urllib.request, urllib.parse
from pyzolib.qt import QtCore, QtGui

import iep
import markdown

tool_name = "Markdown Viewer"
tool_summary = "A live preview of your Markdown in IEP."

markdown_extensions = [ 'extra',
                        'nl2br', 
                        'codehilite', 
                        'sane_lists',
                        'linkify']
accepted_fileext =  [ '.md',
                      '.markdown',
                      '.txt']

class MarkdownView(QtGui.QTextBrowser):
    """ Inherit the webview class to implement zooming using
    the mouse wheel. 
    """
    
    loadStarted = QtCore.Signal()
    loadFinished = QtCore.Signal(bool)
    
    def __init__(self, parent):
        QtGui.QTextBrowser.__init__(self, parent)
        
        # Get markdown parser
        self._md = markdown.Markdown(markdown_extensions)
        
        self.setOpenExternalLinks(True)
        
    def setHtmlWithMarkdown(self, text):
        html = self._md.convert(text)
        self.setHtml(html)


class IepMarkdownViewer(QtGui.QFrame):
    """ The main window, containing browser widget.
    """
    
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        
        # Init config
        toolId =  self.__class__.__name__.lower()
        self._config = iep.config.tools[toolId]
        
        # Get style object (for icons)
        style = QtGui.QApplication.style()
        
        # Create web view
        self._view = MarkdownView(self)
        
        # Layout
        self._sizer1 = QtGui.QVBoxLayout(self)
        self._sizer2 = QtGui.QHBoxLayout()
        #
        self._sizer1.addLayout(self._sizer2, 0)
        self._sizer1.addWidget(self._view, 1)
        #
        self._sizer1.setSpacing(2)
        self.setLayout(self._sizer1)
        
        # Bind to events
        iep.editors.currentChanged.connect(self.onEditorsCurrentChanged)
        iep.editors.parserDone.connect(self.getEditorContent)
        
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
            self._view.setHtmlWithMarkdown(editor.toPlainText())
        else:
            self._view.setText('')
            
