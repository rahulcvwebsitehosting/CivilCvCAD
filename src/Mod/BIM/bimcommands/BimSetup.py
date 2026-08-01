# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2017 Yorik van Havre <yorik@uncreated.net>              *
# *                                                                         *
# *   This file is part of CivilCvCAD.                                         *
# *                                                                         *
# *   CivilCvCAD is free software: you can redistribute it and/or modify it    *
# *   under the terms of the GNU Lesser General Public License as           *
# *   published by the Free Software Foundation, either version 2.1 of the  *
# *   License, or (at your option) any later version.                       *
# *                                                                         *
# *   CivilCvCAD is distributed in the hope that it will be useful, but        *
# *   WITHOUT ANY WARRANTY; without even the implied warranty of            *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      *
# *   Lesser General Public License for more details.                       *
# *                                                                         *
# *   You should have received a copy of the GNU Lesser General Public      *
# *   License along with CivilCvCAD. If not, see                               *
# *   <https://www.gnu.org/licenses/>.                                      *
# *                                                                         *
# ***************************************************************************

"""The BIM Setup command"""

import os
import sys

import CivilCvCAD
import CivilCvCADGui

translate = CivilCvCAD.Qt.translate
QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP


class BIM_Setup:

    def GetResources(self):
        return {
            "Pixmap": ":icons/preferences-system.svg",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Setup", "BIM Setup"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_Setup", "Sets common CivilCvCAD preferences for a BIM workflow"
            ),
        }

    def Activated(self):

        # only raise the dialog if it is already open
        if getattr(self, "form", None):
            self.form.raise_()
            return

        TARGETVERSION = 0.19
        TECHDRAWDIMFACTOR = 0.16  # How many times TechDraw dim arrows are smaller than Draft

        from PySide import QtGui
        import WorkingPlane

        # load dialog
        self.form = CivilCvCADGui.PySideUic.loadUi(":/ui/dialogSetup.ui")

        # center the dialog over CivilCvCAD window
        mw = CivilCvCADGui.getMainWindow()
        self.form.move(
            mw.frameGeometry().topLeft() + mw.rect().center() - self.form.rect().center()
        )

        # connect signals / slots
        self.form.comboPresets.currentIndexChanged[int].connect(self.setPreset)
        self.form.labelIfcOpenShell.linkActivated.connect(self.handleLink)

        # fill default values
        self.setPreset(None)

        # check missing addons
        self.form.labelMissingWorkbenches.hide()
        self.form.labelIfcOpenShell.hide()
        self.form.labelSnapTip.hide()
        self.form.labelVersion.hide()
        m = []
        try:
            import RebarTools
        except ImportError:
            m.append("Reinforcement")
        # disabled as WebTools can currentyl not be installed because of WebGui dependency
        # try:
        #    import BIMServer
        # except ImportError:
        #    m.append("WebTools")
        if sys.version_info.major < 3:
            try:
                import CommandsFrame
            except ImportError:
                m.append("Flamingo")
        else:
            try:
                import CFrame
            except ImportError:
                m.append("Dodo")
        try:
            import FastenerBase
        except ImportError:
            m.append("Fasteners")
        try:
            import report
        except ImportError:
            m.append("Reporting")
        try:
            import ifcopenshell
        except ImportError:
            ifcok = False
        else:
            ifcok = True
        libok = False
        librarypath = CivilCvCAD.ParamGet("User parameter:Plugins/parts_library").GetString(
            "destination", ""
        )
        if librarypath and os.path.exists(librarypath):
            libok = True
        else:
            # check if the library is at the standard addon location
            librarypath = os.path.join(CivilCvCAD.getUserAppDataDir(), "Mod", "parts_library")
            if os.path.exists(librarypath):
                CivilCvCAD.ParamGet("User parameter:Plugins/parts_library").SetString(
                    "destination", librarypath
                )
                libok = True
        if not libok:
            m.append("parts_library")
        if m:
            t = (
                translate(
                    "BIM",
                    "Some additional workbenches are not installed, that extend BIM functionality:",
                )
                + " <b>"
                + ",".join(m)
                + "</b>. "
                + translate("BIM", "Install them from menu Tools -> Addon Manager.")
            )
            self.form.labelMissingWorkbenches.setText(t)
            self.form.labelMissingWorkbenches.show()
        if not ifcok:
            self.form.labelIfcOpenShell.show()
        if (
            CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetString(
                "snapModes", "111111111101111"
            )
            == "111111111101111"
        ):
            self.form.labelSnapTip.show()
        version = float(str(CivilCvCAD.Version()[0]) + "." + str(CivilCvCAD.Version()[1]))
        if version < TARGETVERSION:
            t = self.form.labelVersion.text
            self.form.labelVersion.text = t.replace("%1", str(version)).replace(
                "%2", str(TARGETVERSION)
            )
            self.form.labelVersion.show()

        # show dialog and exit if cancelled
        CivilCvCADGui.BIMSetupDialog = True  # this is there to be easily detected by the BIM tutorial
        result = self.form.exec_()
        del CivilCvCADGui.BIMSetupDialog
        if not result:
            self.form.hide()
            del self.form
            return

        # set preference values
        unit = self.form.settingUnits.currentIndex()
        unit = [0, 4, 1, 3, 7, 5][unit]  # less choices in our simplified dialog
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Units").SetInt("UserSchema", unit)
        if CivilCvCAD.ActiveDocument is not None:
            docs_dict = CivilCvCAD.listDocuments()
            for doc in docs_dict.values():
                doc.UnitSystem = unit
            if len(docs_dict) == 1:
                CivilCvCAD.Console.PrintWarning(
                    translate("BIM", "Unit system updated for active document") + "\n"
                )
            else:
                CivilCvCAD.Console.PrintWarning(
                    translate("BIM", "Unit system updated for all opened documents") + "\n"
                )
        if hasattr(CivilCvCAD.Units, "setSchema"):
            CivilCvCAD.Units.setSchema(unit)
        decimals = self.form.settingDecimals.value()
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Units").SetInt("Decimals", decimals)
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/TechDraw/Dimensions").SetBool(
            "UseGlobalDecimals", True
        )
        grid = self.form.settingGrid.text()
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Sketcher/General").SetString(
            "GridSize", grid
        )  # Also set sketcher grid
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetString(
            "gridSpacing", grid
        )
        squares = self.form.settingSquares.value()
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetInt(
            "gridEvery", squares
        )
        wp = self.form.settingWP.currentIndex()
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetInt("defaultWP", wp)
        tsize = self.form.settingText.text()
        tsize = CivilCvCAD.Units.Quantity(tsize).Value
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetFloat(
            "textheight", tsize
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/TechDraw/Dimensions").SetFloat(
            "FontSize", tsize
        )  # TODO - check if this needs a mult factor?
        font = self.form.settingFont.currentFont().family()
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetString("textfont", font)
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/TechDraw/Labels").SetString(
            "LabelFont", font
        )
        linewidth = self.form.settingLinewidth.value()
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").SetInt(
            "DefaultShapeLineWidth", linewidth
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetInt(
            "linewidth", linewidth
        )
        # TODO - TechDraw default line styles
        dimstyle = self.form.settingDimstyle.currentIndex()
        ddimstyle = [0, 2, 3, 4][dimstyle]  # less choices in our simplified dialog
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetInt(
            "dimsymbol", ddimstyle
        )
        tdimstyle = [3, 0, 2, 2][dimstyle]  # TechDraw has different order than Draft
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/TechDraw/Dimensions").SetInt(
            "dimsymbol", tdimstyle
        )
        asize = self.form.settingArrowsize.text()
        asize = CivilCvCAD.Units.Quantity(asize).Value
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetFloat(
            "arrowsize", asize
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/TechDraw/Dimensions").SetFloat(
            "ArrowSize", asize * TECHDRAWDIMFACTOR
        )
        author = self.form.settingAuthor.text()
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Document").SetString(
            "prefAuthor", author
        )
        lic = self.form.settingLicense.currentIndex()
        lic = [0, 1, 2, 4, 5][lic]  # less choices in our simplified dialog
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Document").SetInt(
            "prefLicenseType", lic
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Document").SetString(
            "prefLicenseUrl", ""
        )  # TODO - set correct license URL
        newdoc = self.form.settingNewdocument.isChecked()
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Document").SetBool(
            "CreateNewDoc", newdoc
        )
        bkp = self.form.settingBackupfiles.value()
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Document").SetInt(
            "CountBackupFiles", bkp
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").SetUnsigned(
            "BackgroundColor2", self.form.colorButtonTop.property("color").rgb() << 8
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").SetUnsigned(
            "BackgroundColor3", self.form.colorButtonBottom.property("color").rgb() << 8
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").SetUnsigned(
            "DefaultShapeColor", self.form.colorButtonFaces.property("color").rgb() << 8
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetUnsigned(
            "color", self.form.colorButtonFaces.property("color").rgb() << 8
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").SetUnsigned(
            "DefaultShapeLineColor",
            self.form.colorButtonLines.property("color").rgb() << 8,
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Arch").SetUnsigned(
            "ColorHelpers", self.form.colorButtonHelpers.property("color").rgb() << 8
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetUnsigned(
            "constructioncolor",
            self.form.colorButtonConstruction.property("color").rgb() << 8,
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").SetUnsigned(
            "ConstructionColor",
            self.form.colorButtonConstruction.property("color").rgb() << 8,
        )
        height = self.form.settingCameraHeight.value()
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetInt(
            "defaultCameraHeight", height
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetUnsigned(
            "DefaultTextColor", self.form.colorButtonText.property("color").rgb() << 8
        )
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").SetUnsigned(
            "BackgroundColor", self.form.colorButtonSimple.property("color").rgb() << 8
        )

        # set the working plane
        wplane = WorkingPlane.get_working_plane()
        if wp == 1:
            wplane.set_to_top()
        elif wp == 2:
            wplane.set_to_front()
        elif wp == 3:
            wplane.set_to_side()
        else:
            wplane.set_to_auto()

        # set Draft toolbar
        if hasattr(CivilCvCADGui, "draftToolBar"):
            if hasattr(CivilCvCADGui.draftToolBar, "setStyleButton"):
                CivilCvCADGui.draftToolBar.setStyleButton()
            else:
                # pre-v0.19
                CivilCvCADGui.draftToolBar.widthButton.setValue(linewidth)
                CivilCvCADGui.draftToolBar.fontsizeButton.setValue(tsize)

        # set the grid
        if hasattr(CivilCvCADGui, "Snapper"):
            CivilCvCADGui.Snapper.setGrid()

        # set the status bar widgets
        mw = CivilCvCADGui.getMainWindow()
        if mw:
            st = mw.statusBar()
            statuswidget = st.findChild(QtGui.QToolBar, "BIMStatusWidget")
            if statuswidget:
                if hasattr(statuswidget, "unitLabel"):
                    statuswidget.unitLabel.setText(
                        statuswidget.unitsList[self.form.settingUnits.currentIndex()]
                    )
                # change the unit of the nudge button
                nudgeactions = statuswidget.nudge.menu().actions()
                if unit in [2, 3, 5, 7]:
                    nudgelabels = statuswidget.nudgeLabelsI
                else:
                    nudgelabels = statuswidget.nudgeLabelsM
                for i in range(len(nudgelabels)):
                    nudgeactions[i].setText(nudgelabels[i])
                try:
                    t = CivilCvCAD.Units.Quantity(
                        statuswidget.nudge.text().replace("&", "")
                    ).UserString
                except:
                    pass  # auto mode
                else:
                    statuswidget.nudge.setText(t)

        # Set different default values
        if CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM").GetBool(
            "FirstTime", True
        ):
            CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetString(
                "svgDashedLine", "3,1"
            )
            CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetString(
                "svgDashdotLine", "3,1,0.2,1"
            )
            CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetString(
                "svgDottedLine", "0.5,1"
            )
            CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").SetFloat(
                "HatchPatternSize", 0.025
            )

        # finish
        CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM").SetBool("FirstTime", False)
        self.form.hide()
        del self.form

    def setPreset(self, preset=None):
        from PySide import QtGui

        unit = None
        decimals = None
        grid = None
        squares = None
        wp = None
        tsize = None
        font = None
        linewidth = None
        dimstyle = None
        asize = None
        author = None
        lic = None
        bimdefault = None
        newdoc = None
        bkp = None
        colTop = None
        colBottom = None
        colFace = None
        colLine = None
        colHelp = None
        colConst = None
        height = None
        colSimple = None
        colText = None

        if preset == 0:
            # the "Choose..." item from the presets box. Do nothing
            return

        elif preset == 1:
            # centimeters
            unit = 1
            decimals = 2
            grid = "10cm"
            squares = 10
            tsize = "20cm"
            linewidth = 1
            dimstyle = 0
            asize = "4cm"
            bkp = 2
            bimdefault = 2
            newdoc = False
            height = 4500

        elif preset == 2:
            # meters
            unit = 2
            decimals = 2
            grid = "0.1m"
            squares = 10
            tsize = "0.2m"
            linewidth = 1
            dimstyle = 0
            asize = "0.04m"
            bkp = 2
            bimdefault = 2
            newdoc = False
            height = 4500

        elif preset == 3:
            # US
            unit = 5
            decimals = 2
            grid = "1in"
            squares = 12
            tsize = "8in"
            linewidth = 1
            dimstyle = 3
            asize = "2in"
            bkp = 2
            bimdefault = 2
            newdoc = False
            height = 4500

        elif preset is None:
            # get values from settings
            unit = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt(
                "UserSchema", 0
            )
            unit = [0, 2, 3, 3, 1, 5, 0, 4, 0, 2][unit]  # less choices in our simplified dialog
            decimals = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt(
                "Decimals", 2
            )
            grid = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetString(
                "gridSpacing", "1 cm"
            )
            grid = CivilCvCAD.Units.Quantity(grid).UserString
            squares = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetInt(
                "gridEvery", 10
            )
            wp = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetInt(
                "defaultWP", 1
            )
            tsize = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetFloat(
                "textheight", 10
            )
            tsize = CivilCvCAD.Units.Quantity(tsize, CivilCvCAD.Units.Length).UserString
            font = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetString(
                "textfont", "Sans"
            )
            linewidth = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").GetInt(
                "DefaultShapeLineWidth", 2
            )
            dimstyle = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetInt(
                "dimsymbol", 0
            )
            dimstyle = [0, 0, 1, 2, 3][dimstyle]  # less choices in our simplified dialog
            asize = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetFloat(
                "arrowsize", 5
            )
            asize = CivilCvCAD.Units.Quantity(asize, CivilCvCAD.Units.Length).UserString
            author = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Document").GetString(
                "prefAuthor", ""
            )
            lic = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Document").GetInt(
                "prefLicenseType", 0
            )
            lic = [0, 1, 2, 1, 3, 4, 1, 1, 2, 1, 3, 4, 1, 0, 0, 0, 0, 0, 0][
                lic
            ]  # less choices in our simplified dialog
            newdoc = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Document").GetBool(
                "CreateNewDoc", False
            )
            bkp = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Document").GetInt(
                "CountBackupFiles", 2
            )
            colTop = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned(
                "BackgroundColor2", 775244287
            )
            colBottom = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned(
                "BackgroundColor3", 1905041919
            )
            colFace = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned(
                "DefaultShapeColor", 4294967295
            )
            colLine = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned(
                "DefaultShapeLineColor", 255
            )
            colHelp = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Arch").GetUnsigned(
                "ColorHelpers", 674321151
            )
            colConst = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetUnsigned(
                "constructioncolor", 746455039
            )
            height = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetInt(
                "defaultCameraHeight", 5
            )
            colSimple = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned(
                "BackgroundColor", 4294967295
            )
            colText = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetUnsigned(
                "DefaultTextColor", 255
            )

        if unit != None:
            self.form.settingUnits.setCurrentIndex(unit)
        if decimals != None:
            self.form.settingDecimals.setValue(decimals)
        if grid != None:
            self.form.settingGrid.setText(grid)
        if squares != None:
            self.form.settingSquares.setValue(squares)
        if wp != None:
            self.form.settingWP.setCurrentIndex(wp)
        if tsize != None:
            self.form.settingText.setText(tsize)
        if font != None:
            self.form.settingFont.setCurrentFont(QtGui.QFont(font))
        if linewidth != None:
            self.form.settingLinewidth.setValue(linewidth)
        if dimstyle != None:
            self.form.settingDimstyle.setCurrentIndex(dimstyle)
        if asize != None:
            self.form.settingArrowsize.setText(asize)
        if author != None:
            self.form.settingAuthor.setText(author)
        if lic != None:
            self.form.settingLicense.setCurrentIndex(lic)
        if newdoc != None:
            self.form.settingNewdocument.setChecked(newdoc)
        if bkp != None:
            self.form.settingBackupfiles.setValue(bkp)
        if colTop != None:
            self.form.colorButtonTop.setProperty("color", self.getPrefColor(colTop))
        if colBottom != None:
            self.form.colorButtonBottom.setProperty("color", self.getPrefColor(colBottom))
        if colFace != None:
            self.form.colorButtonFaces.setProperty("color", self.getPrefColor(colFace))
        if colLine != None:
            self.form.colorButtonLines.setProperty("color", self.getPrefColor(colLine))
        if colHelp != None:
            self.form.colorButtonHelpers.setProperty("color", self.getPrefColor(colHelp))
        if colConst != None:
            self.form.colorButtonConstruction.setProperty("color", self.getPrefColor(colConst))
        if colSimple != None:
            self.form.colorButtonSimple.setProperty("color", self.getPrefColor(colSimple))
        if colText != None:
            self.form.colorButtonText.setProperty("color", self.getPrefColor(colText))
        if height:
            self.form.settingCameraHeight.setValue(height)
        # TODO - antialiasing?

    def handleLink(self, link):
        if hasattr(self, "form"):
            if "#install" in link:
                self.getIfcOpenShell()
            else:
                # print("Opening link:",link)
                from PySide import QtCore
                from civilcvcad.offline import open_local_url

                url = QtCore.QUrl(link)
                open_local_url(url)

    def getPrefColor(self, color):
        r = ((color >> 24) & 0xFF) / 255.0
        g = ((color >> 16) & 0xFF) / 255.0
        b = ((color >> 8) & 0xFF) / 255.0
        from PySide import QtGui

        return QtGui.QColor.fromRgbF(r, g, b)

    def getIfcOpenShell(self, force=False):
        """Reject automatic dependency installation."""

        del force
        CivilCvCAD.Console.PrintError(
            "Automatic dependency downloads are disabled. "
            "Install IfcOpenShell from local media and restart CivilCvCAD.\n"
        )


CivilCvCADGui.addCommand("BIM_Setup", BIM_Setup())
