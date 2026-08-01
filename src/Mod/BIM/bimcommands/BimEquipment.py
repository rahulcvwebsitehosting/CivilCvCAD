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

"""BIM equipment commands"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate

PARAMS = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Equipment:
    "the Arch Equipment command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Equipment",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Equipment", "Equipment"),
            "Accel": "E, Q",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Equipment", "Creates an equipment from a selected object (Part or Mesh)"
            ),
        }

    def IsActive(self):

        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        s = CivilCvCADGui.Selection.getSelection()
        if not s:
            CivilCvCAD.Console.PrintError(
                translate("Arch", "Select a base shape object and optionally a mesh object")
            )
        else:
            base = ""
            mesh = ""
            if len(s) == 2:
                if hasattr(s[0], "Shape"):
                    base = s[0].Name
                elif s[0].isDerivedFrom("Mesh::Feature"):
                    mesh = s[0].Name
                if hasattr(s[1], "Shape"):
                    if mesh:
                        base = s[1].Name
                elif s[1].isDerivedFrom("Mesh::Feature"):
                    if base:
                        mesh = s[1].Name
            else:
                if hasattr(s[0], "Shape"):
                    base = s[0].Name
                elif s[0].isDerivedFrom("Mesh::Feature"):
                    mesh = s[0].Name
            CivilCvCAD.ActiveDocument.openTransaction(str(translate("Arch", "Create Equipment")))
            CivilCvCADGui.addModule("Arch")
            if base:
                base = "CivilCvCAD.ActiveDocument." + base
            CivilCvCADGui.doCommand("obj = Arch.makeEquipment(" + base + ")")
            if mesh:
                CivilCvCADGui.doCommand("obj.HiRes = CivilCvCAD.ActiveDocument." + mesh)
            CivilCvCADGui.addModule("Draft")
            CivilCvCADGui.doCommand("Draft.autogroup(obj)")
            CivilCvCAD.ActiveDocument.commitTransaction()
            CivilCvCAD.ActiveDocument.recompute()
            # get diffuse color info from base object
            if base and hasattr(s[0].ViewObject, "DiffuseColor"):
                CivilCvCADGui.doCommand(
                    "CivilCvCAD.ActiveDocument.Objects[-1].ViewObject.DiffuseColor = "
                    + base
                    + ".ViewObject.DiffuseColor"
                )
        return


CivilCvCADGui.addCommand("Arch_Equipment", Arch_Equipment())
