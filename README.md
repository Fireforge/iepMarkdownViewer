iepMarkdownViewer
=================

An [IEP][iepurl] Tool that gives a live preview of [Markdown][markdownurl] text using Github's Markdown styling.

### How To Install
- Install [Pyzo][pyzourl]
- Install the following packages to the Pyzo distro (*this can be done inside the editor's shell*)
  * Markdown: `pip install markdown` 
  * Linkify Markdown Extension: `pip install mdx_linkify`
- Download the repository and copy the `iepMarkdownViewer` folder into your IEP userdata directory
  * *Can't find the IEP userdata directory? It's listed under Help > About IEP in the editor*

### How To Use
- In IEP (that's the IDE that comes with Pyzo), select Tools > Markdown Viewer
- A widget named Markdown Viewer will appear in the IDE.
- Any .md, .markdown, or .txt file selected in the editor will be rendered in real-time (as you type!) in the Markdown Viewer tool
- Clicking external links opens them in your default browser

### Why do I need Pyzo? Isn't IEP a separate thing?
It's true that this tool is really for [IEP][iepurl] itself. However it needs the whole Pyzo environment to work for the following reasons:
-  There's no good way (yet) to import this tools dependencies in stand-alone IEP. Hopefully there will be a way to install tools into IEP in the near future that handles this issue.
-  This tool uses QWebKit for all the pretty Github CSS styling, which is not bundled into stand-alone IEP because of its enormous size. If QWebKit is not present, this tool will load in the same non-QWebKit based view that the built-in web browser uses. So this doesn't stop iepMarkdownViewer from working, it just means it's less pretty.

[markdownurl]: https://help.github.com/articles/markdown-basics
[iepurl]: http://www.iep-project.org/
[pyzourl]: http://www.pyzo.org
