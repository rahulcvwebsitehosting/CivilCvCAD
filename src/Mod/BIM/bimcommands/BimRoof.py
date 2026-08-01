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

"""BIM Roof command"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate

PARAMS = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Roof:
    """the Arch Roof command definition"""

    def GetResources(self):
        return {
            "Pixmap": "Arch_Roof",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Roof", "Roof"),
            "Accel": "R, F",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Roof", "Creates a roof object from the selected wire."
            ),
        }

    def IsActive(self):
        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        import ArchComponent

        sel = CivilCvCADGui.Selection.getSelectionEx()
        if sel:
            sel = sel[0]
            obj = sel.Object
            CivilCvCADGui.Control.closeDialog()
            if sel.HasSubObjects:
                if "Face" in sel.SubElementNames[0]:
                    i = int(sel.SubElementNames[0][4:])
                    CivilCvCAD.ActiveDocument.openTransaction(translate("Arch", "Create Roof"))
                    CivilCvCADGui.addModule("Arch")
                    CivilCvCADGui.doCommand(
                        "obj = Arch.makeRoof(CivilCvCAD.ActiveDocument."
                        + obj.Name
                        + ","
                        + str(i)
                        + ")"
                    )
                    CivilCvCADGui.addModule("Draft")
                    CivilCvCADGui.doCommand("Draft.autogroup(obj)")
                    CivilCvCAD.ActiveDocument.commitTransaction()
                    CivilCvCAD.ActiveDocument.recompute()
                    return
            if hasattr(obj, "Shape"):
                if obj.Shape.Wires:
                    CivilCvCAD.ActiveDocument.openTransaction(translate("Arch", "Create Roof"))
                    CivilCvCADGui.addModule("Arch")
                    CivilCvCADGui.doCommand(
                        "obj = Arch.makeRoof(CivilCvCAD.ActiveDocument." + obj.Name + ")"
                    )
                    CivilCvCADGui.addModule("Draft")
                    CivilCvCADGui.doCommand("Draft.autogroup(obj)")
                    CivilCvCAD.ActiveDocument.commitTransaction()
                    CivilCvCAD.ActiveDocument.recompute()
                    return
            else:
                CivilCvCAD.Console.PrintMessage(translate("Arch", "Unable to create a roof"))
        else:
            CivilCvCAD.Console.PrintMessage(translate("Arch", "Select a base object") + "\n")
            CivilCvCADGui.Control.showDialog(ArchComponent.SelectionTaskPanel())
            CivilCvCAD.ArchObserver = ArchComponent.ArchSelectionObserver(nextCommand="Arch_Roof")
            CivilCvCADGui.Selection.addObserver(CivilCvCAD.ArchObserver)


CivilCvCADGui.addCommand("Arch_Roof", Arch_Roof())
