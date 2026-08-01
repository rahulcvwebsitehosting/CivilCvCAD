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

"""BIM Frame command"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate

PARAMS = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Frame:
    "the Arch Frame command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Frame",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Frame", "Frame"),
            "Accel": "F, R",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Frame",
                "Creates a frame object from a planar 2D object (the extrusion path(s)) and a profile. Make sure objects are selected in that order.",
            ),
        }

    def IsActive(self):

        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        s = CivilCvCADGui.Selection.getSelection()
        if len(s) == 2:
            CivilCvCAD.ActiveDocument.openTransaction(translate("Arch", "Create Frame"))
            CivilCvCADGui.addModule("Arch")
            CivilCvCADGui.addModule("Draft")
            CivilCvCADGui.doCommand(
                "obj = Arch.makeFrame(CivilCvCAD.ActiveDocument."
                + s[0].Name
                + ",CivilCvCAD.ActiveDocument."
                + s[1].Name
                + ")"
            )
            CivilCvCADGui.doCommand("Draft.autogroup(obj)")
            CivilCvCAD.ActiveDocument.commitTransaction()
            CivilCvCAD.ActiveDocument.recompute()


CivilCvCADGui.addCommand("Arch_Frame", Arch_Frame())
