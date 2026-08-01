# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2021 Yorik van Havre <yorik@uncreated.net>              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

"""
Provide tools to access local CivilCvCAD documentation.

The main usage is the ``show`` function. It accepts a local Markdown or
HTML file, or resolves a page below the configured offline documentation
directory.

It doesn't matter what you give, the system will recognize if the contents are
HTML or Markdown and render it appropriately.

Basic usage:

    import Help
    Help.show("Draft Line")
    Help.show("Draft_Line") # works with spaces or underscores
    Help.show("/home/myUser/CivilCvCAD/Documentation/Draft_Line.md")

Preferences keys (in "User parameter:BaseApp/Preferences/Mod/Help"):

    optionBrowser/optionTab/optionDialog (bool): Where to open the help dialog
    Location (string): offline location
    StyleSheet (string): optional CSS stylesheet to style the output
"""

import os
import re
import CivilCvCAD

translate = CivilCvCAD.Qt.translate
QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP

# texts and icons
ERRORTXT = translate(
    "Help",
    "Contents for this page could not be retrieved. Please check settings under menu Edit → Preferences → General → Help",
)
LOCTXT = translate(
    "Help",
    "Help files location could not be determined. Please check settings under menu Edit → Preferences → General → Help",
)
LOGTXT = translate(
    "Help",
    "PySide QtWebEngineWidgets module is not available. Help rendering is done with the system browser",
)
CONVERTTXT = translate(
    "Help",
    "There is no Markdown renderer installed on your system, so this help page is rendered as is. Please install the Markdown or Pandoc Python modules to improve the rendering of this page.",
)
PREFS = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Help")
PREFS.SetBool("optionWiki", False)
PREFS.SetBool("optionMarkdown", False)
PREFS.SetBool("optionGithub", False)
PREFS.SetBool("optionCustom", True)
if not PREFS.GetString("Location", ""):
    PREFS.SetString(
        "Location",
        os.path.join(
            CivilCvCAD.getUserAppDataDir(),
            "Mod",
            "offline-documentation",
            "CivilCvCAD-documentation-main",
            "wiki",
        ),
    )
ICON = ":/icons/help-browser.svg"


def show(page, view=None, conv=None):
    """
    show(page,view=None, conv=None):
    Opens a help viewer and shows the given help page.
    The given help page can be a page or command name, or a local file path pointing to a Markdown
    or HTML file. If view is given (an instance of openBrowserHTML.HelpPage or
    any other object with a 'setHtml()' method), the page will be
    rendered there, otherwise a new tab/widget will be created according to
    preferences settings. If conv is given (markdown, pandoc, github, builtin or
    none), the corresponding markdown conversion method is used. Otherwise, the
    module will use the best available.
    In non-GUI mode, this function simply outputs the markdown or HTML text.
    """

    page = underscore_page(page)
    location, _pagename = get_location(page)
    CivilCvCAD.Console.PrintLog("Help: opening " + location + "\n")
    if not location:
        CivilCvCAD.Console.PrintError(LOCTXT + "\n")
        return
    md = get_contents(location)
    html = convert(md, conv)
    baseurl = get_uri(location)
    if _pagename != "":
        pagename = _pagename
    else:
        pagename = os.path.basename(page.replace("_", " ").replace(".md", ""))
    title = translate("Help", "Help") + ": " + pagename
    if CivilCvCAD.GuiUp:
        if PREFS.GetBool("optionTab", False) and get_qtwebwidgets():
            # MDI tab
            show_tab(html, baseurl, title, view)
        elif PREFS.GetBool("optionDialog", False) and get_qtwebwidgets():
            # floating dock window
            show_dialog(html, baseurl, title, view)
        else:
            # desktop web browser - default
            show_browser(location)
    else:
        # console mode, we just print the output
        print(md)


def underscore_page(page):
    """change spaces by underscores in the given page name"""

    if "/" in page:
        page = page.split("/")
        page[-1] = page[-1].replace(" ", "_")
        page = "/".join(page)
    else:
        page.replace(" ", "_")
    return page


def get_uri(location):
    """Return a file URI for a local disk location."""

    baseurl = os.path.dirname(location) + "/"
    if baseurl.startswith("/"):  # unix path
        baseurl = "file://" + baseurl
    if baseurl[0].isupper() and (baseurl[1] == ":"):  # windows path
        baseurl = baseurl.replace("\\", "/")
        baseurl = "file:///" + baseurl
    return baseurl


def location_url(url_localized: str, url_english: str) -> tuple:
    """Reject network locations in the offline-only distribution."""
    del url_localized, url_english
    return ("", "")


def get_location(page) -> tuple:
    """Resolve a documentation page strictly from local storage."""

    location = ""
    if page.startswith(("http:", "https:", "ftp:")):
        return ("", "")
    if page.startswith("file://"):
        return (page[7:], "")
    # offline location
    if os.path.exists(page):
        return (page, "")
    page = page.replace(".md", "")
    page = page.replace(" ", "_")
    page = page.replace("wiki/", "")
    page = page.split("#")[0]
    pagename = ""
    location = PREFS.GetString("Location", "")
    if not location:
        return ("", "")
    for ext in (".md", ".html", ".htm"):
        candidate = os.path.join(location, page + ext)
        if os.path.isfile(candidate):
            return (candidate, pagename)
    location = ""
    return (location, pagename)


def show_browser(url):
    """Open a local help file in the desktop browser."""

    from PySide import QtCore, QtGui

    path = os.path.abspath(url)
    if os.path.isfile(path):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path))


def show_dialog(html, baseurl, title, view=None):
    """opens a dock dialog with the given html"""

    from PySide import QtCore

    if view:  # reusing existing view
        view.setHtml(html, baseUrl=QtCore.QUrl(baseurl))
        view.parent().parent().setWindowTitle(title)
    else:
        openBrowserHTML(html, baseurl, title, ICON, dialog=True)


def show_tab(html, baseurl, title, view=None):
    """opens a MDI tab with the given html"""

    from PySide import QtCore

    if view:  # reusing existing view
        view.setHtml(html, baseUrl=QtCore.QUrl(baseurl))
        view.parent().parent().setWindowTitle(title)
    else:
        openBrowserHTML(html, baseurl, title, ICON)


def get_qtwebwidgets():
    """verifies if qtwebengine is available"""

    try:
        from PySide import QtWebEngineWidgets
    except:
        CivilCvCAD.Console.PrintLog(LOGTXT + "\n")
        return False
    else:
        return True


def get_contents(location):
    """retrieves text contents of a given page"""

    if location.startswith(("http:", "https:", "ftp:")):
        return ERRORTXT
    if os.path.isfile(location):
        with open(location, mode="r", encoding="utf8") as f:
            contents = f.read()
        return contents
    return ERRORTXT


def convert(content, force=None):
    """converts the given markdown code to html. Force can be None (automatic)
    or markdown, pandoc, github or raw/builtin"""

    import urllib

    def convert_markdown(m):
        try:
            import markdown
            from markdown.extensions import codehilite

            return markdown.markdown(m, extensions=["codehilite"])
        except:
            return None

    def convert_pandoc(m):
        try:
            import pypandoc

            return pypandoc.convert_text(m, "html", format="md")
        except:
            return None

    def convert_github(m):
        del m
        return None

    def convert_raw(m):
        # simple and dirty regex-based markdown to html

        import re

        f = re.DOTALL | re.MULTILINE
        m = re.sub(r"^##### (.*?)\n", r"<h5>\1</h5>\n", m, flags=f)  # ##### titles
        m = re.sub(r"^#### (.*?)\n", r"<h4>\1</h4>\n", m, flags=f)  # #### titles
        m = re.sub(r"^### (.*?)\n", r"<h3>\1</h3>\n", m, flags=f)  # ### titles
        m = re.sub(r"^## (.*?)\n", r"<h2>\1</h2>\n", m, flags=f)  # ## titles
        m = re.sub(r"^# (.*?)\n", r"<h1>\1</h1>\n", m, flags=f)  # # titles
        m = re.sub(r"!\[(.*?)\]\((.*?)\)", r'<img alt="\1" src="\2">', m, flags=f)  # images
        m = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', m, flags=f)  # links
        m = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", m)  # bold
        m = re.sub(r"\*(.*?)\*", r"<i>\1</i>", m)  # italic
        m = re.sub(r"\n\n", r"<br/>", m, flags=f)  # double new lines
        m += "\n<br/><hr/><small>" + CONVERTTXT + "</small>"
        return m

    if "<html" in content:
        # this is html already
        return content

    if force == "markdown":
        html = convert_markdown(content)
    elif force == "pandoc":
        html = convert_pandoc(content)
    elif force == "github":
        html = convert_github(content)
    elif force in ["raw", "builtin"]:
        html = convert_raw(content)
    elif force == "none":
        return content
    else:
        # auto mode
        html = convert_pandoc(content)
        if not html:
            html = convert_markdown(content)
            if not html:
                html = convert_raw(content)
    if not "<html" in html:
        html = (
            '<html>\n<head>\n<meta charset="utf-8"/>\n</head>\n<body>\n\n'
            + html
            + "</body>\n</html>"
        )
    # insert css
    css = None
    cssfile = PREFS.GetString("StyleSheet", "")
    if not cssfile:
        cssfile = os.path.join(os.path.dirname(__file__), "default.css")
    if False:  # linked CSS file
        # below code doesn't work in CivilCvCAD apparently because it prohibits cross-URL stuff
        cssfile = urllib.parse.urljoin("file:", urllib.request.pathname2url(cssfile))
        css = '<link rel="stylesheet" type="text/css" href="' + cssfile + '"/>'
    else:
        if os.path.exists(cssfile):
            with open(cssfile) as cf:
                css = cf.read()
            if css:
                css = "<style>\n" + css + "\n</style>"
        else:
            print("Debug: Help: Unable to open css file:", cssfile)
    if css:
        html = html.replace("</head>", css + "\n</head>")
    return html


def add_preferences_page():
    """adds the Help preferences page to the UI"""

    import CivilCvCADGui

    page = os.path.join(os.path.dirname(__file__), "dlgPreferencesHelp.ui")
    CivilCvCADGui.addPreferencePage(page, QT_TRANSLATE_NOOP("QObject", "General"))


def add_language_path():
    """registers the Help translations to CivilCvCAD"""

    import CivilCvCADGui
    import Help_rc

    CivilCvCADGui.addLanguagePath(":/translations")


def openBrowserHTML(html, baseurl, title, icon, dialog=False):
    """creates a browser view and adds it as a CivilCvCAD MDI tab or dockable dialog"""

    import CivilCvCADGui
    from PySide import QtCore, QtGui, QtWidgets, QtWebEngineWidgets

    # turn an int into a qt dock area
    def getDockArea(area):
        if area == 1:
            return QtCore.Qt.LeftDockWidgetArea
        elif area == 4:
            return QtCore.Qt.TopDockWidgetArea
        elif area == 8:
            return QtCore.Qt.BottomDockWidgetArea
        else:
            return QtCore.Qt.RightDockWidgetArea

    # save dock widget size and location
    def onDockLocationChanged(area):
        PREFS.SetInt("dockWidgetArea", int(area.value))
        mw = CivilCvCADGui.getMainWindow()
        dock = mw.findChild(QtWidgets.QDockWidget, "HelpWidget")
        if dock:
            PREFS.SetBool("dockWidgetFloat", dock.isFloating())
            PREFS.SetInt("dockWidgetWidth", dock.width())
            PREFS.SetInt("dockWidgetHeight", dock.height())

    # a custom page that handles .md links
    class HelpPage(QtWebEngineWidgets.QWebEnginePage):
        def acceptNavigationRequest(self, url, _type, isMainFrame):
            if _type == QtWebEngineWidgets.QWebEnginePage.NavigationTypeLinkClicked:
                if url.isLocalFile():
                    show(url.toLocalFile(), view=self)
                return False
            return super().acceptNavigationRequest(url, _type, isMainFrame)

    mw = CivilCvCADGui.getMainWindow()
    view = QtWebEngineWidgets.QWebEngineView()
    page = HelpPage(None, view)
    page.setHtml(html, baseUrl=QtCore.QUrl(baseurl))
    view.setPage(page)

    if dialog:
        area = PREFS.GetInt("dockWidgetArea", 2)
        floating = PREFS.GetBool("dockWidgetFloat", True)
        height = PREFS.GetBool("dockWidgetWidth", 200)
        width = PREFS.GetBool("dockWidgetHeight", 300)
        dock = mw.findChild(QtWidgets.QDockWidget, "HelpWidget")
        if not dock:
            dock = QtWidgets.QDockWidget()
            dock.setObjectName("HelpWidget")
            mw.addDockWidget(getDockArea(area), dock)
            dock.setFloating(floating)
            dock.setGeometry(dock.x(), dock.y(), width, height)
            dock.dockLocationChanged.connect(onDockLocationChanged)
        dock.setWidget(view)
        dock.setWindowTitle(title)
        dock.setWindowIcon(QtGui.QIcon(icon))
        dock.show()
    else:
        mdi = mw.findChild(QtWidgets.QMdiArea)
        sw = mdi.addSubWindow(view)
        sw.setWindowTitle(title)
        sw.setWindowIcon(QtGui.QIcon(icon))
        sw.show()
        mdi.setActiveSubWindow(sw)
