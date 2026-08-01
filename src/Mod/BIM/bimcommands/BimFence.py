# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2024 Yorik van Havre <yorik@uncreated.net>              *
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

"""BIM fence command"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate

PARAMS = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Fence:
    "the Arch Fence command definition"

    def GetResources(self):
        return {
            "Pixmap": "Arch_Fence",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Fence", "Fence"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Fence", "Creates a fence object from a selected section, post and path"
            ),
        }

    def IsActive(self):
        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        if len(CivilCvCADGui.Selection.getSelection()) != 3:
            CivilCvCAD.Console.PrintError(
                translate(
                    "Arch Fence selection",
                    "Select a section, post and path in exactly this order to build a fence.",
                )
                + "\n"
            )
            return
        doc = CivilCvCAD.ActiveDocument
        doc.openTransaction(translate("Arch", "Create Fence"))
        CivilCvCADGui.addModule("Arch")
        CivilCvCADGui.doCommand("section = CivilCvCADGui.Selection.getSelection()[0]")
        CivilCvCADGui.doCommand("post = CivilCvCADGui.Selection.getSelection()[1]")
        CivilCvCADGui.doCommand("path = CivilCvCADGui.Selection.getSelection()[2]")
        CivilCvCADGui.doCommand("Arch.makeFence(section, post, path)")
        doc.commitTransaction()
        doc.recompute()


CivilCvCADGui.addCommand("Arch_Fence", Arch_Fence())
