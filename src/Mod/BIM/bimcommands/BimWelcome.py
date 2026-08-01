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

"""This module contains CivilCvCAD commands for the BIM workbench"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP

PARAMS = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class BIM_Welcome:
    def GetResources(self):
        return {
            "Pixmap": "BIM_Welcome.svg",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Welcome", "BIM Welcome Screen"),
            "ToolTip": QT_TRANSLATE_NOOP("BIM_Welcome", "Shows the BIM workbench welcome screen"),
        }

    def Activated(self):
        self.form = CivilCvCADGui.PySideUic.loadUi(":ui/dialogWelcome.ui")

        # handle the tutorial links
        self.form.label_4.linkActivated.connect(self.handleLink)
        self.form.label_7.linkActivated.connect(self.handleLink)

        self.form.adjustSize()

        # center the dialog over CivilCvCAD window
        mw = CivilCvCADGui.getMainWindow()
        self.form.move(
            mw.frameGeometry().topLeft() + mw.rect().center() - self.form.rect().center()
        )

        # show dialog and run setup dialog afterwards if OK was pressed
        result = self.form.exec_()
        if result:
            CivilCvCADGui.runCommand("BIM_Setup")

        # remove first time flag
        PARAMS.SetBool("FirstTime", False)

    def handleLink(self, link):
        from PySide import QtCore, QtGui

        if hasattr(self, "form"):
            self.form.hide()
            if "BIM_Start_Tutorial" in link:
                CivilCvCADGui.runCommand("BIM_Tutorial")
            else:
                # print("Opening link:",link)
                from civilcvcad.offline import open_local_url

                url = QtCore.QUrl(link)
                open_local_url(url)


CivilCvCADGui.addCommand("BIM_Welcome", BIM_Welcome())
