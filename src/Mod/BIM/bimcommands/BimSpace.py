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

"""BIM Schedule command"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate

PARAMS = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Space:
    "the Arch Space command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Space",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Space", "Space"),
            "Accel": "S, A",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Space", "Creates a space object from selected boundary objects"
            ),
        }

    def IsActive(self):

        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        import ArchComponent

        CivilCvCAD.ActiveDocument.openTransaction(translate("Arch", "Create Space"))
        CivilCvCADGui.addModule("Arch")
        sel = CivilCvCADGui.Selection.getSelection()
        if sel:
            CivilCvCADGui.Control.closeDialog()
            CivilCvCADGui.doCommand("obj = Arch.makeSpace(CivilCvCADGui.Selection.getSelectionEx())")
            CivilCvCADGui.addModule("Draft")
            CivilCvCADGui.doCommand("Draft.autogroup(obj)")
            CivilCvCAD.ActiveDocument.commitTransaction()
            CivilCvCAD.ActiveDocument.recompute()
        else:
            CivilCvCAD.Console.PrintMessage(translate("Arch", "Select a base object") + "\n")
            CivilCvCADGui.Control.showDialog(ArchComponent.SelectionTaskPanel())
            CivilCvCAD.ArchObserver = ArchComponent.ArchSelectionObserver(nextCommand="Arch_Space")
            CivilCvCADGui.Selection.addObserver(CivilCvCAD.ArchObserver)


CivilCvCADGui.addCommand("Arch_Space", Arch_Space())
