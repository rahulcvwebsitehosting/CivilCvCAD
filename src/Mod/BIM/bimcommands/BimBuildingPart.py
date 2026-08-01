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

"""The BIM Building part-related commands"""

# TODO: Refactor the Site code so it becomes a BuildingPart too


import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate

PARAMS = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Level:
    """The command definition for the Arch workbench's gui tool, Arch Floor"""

    def GetResources(self):

        return {
            "Pixmap": "Arch_Floor",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Level", "Level"),
            "Accel": "L, V",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Level", "Creates a building part object that represents a level"
            ),
        }

    def IsActive(self):

        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        CivilCvCAD.ActiveDocument.openTransaction(translate("Arch", "Create Level"))
        CivilCvCADGui.addModule("Arch")
        CivilCvCADGui.addModule("Draft")
        CivilCvCADGui.addModule("WorkingPlane")
        CivilCvCADGui.doCommand("obj = Arch.makeFloor(CivilCvCADGui.Selection.getSelection())")
        CivilCvCADGui.doCommand("obj.Placement = WorkingPlane.get_working_plane().get_placement()")
        CivilCvCADGui.doCommand("Draft.autogroup(obj)")
        CivilCvCAD.ActiveDocument.commitTransaction()
        CivilCvCAD.ActiveDocument.recompute()


class Arch_Building:
    "the Arch Building command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Building",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Building", "Building"),
            "Accel": "B, U",
            "ToolTip": QT_TRANSLATE_NOOP("Arch_Building", "Creates a building object"),
        }

    def IsActive(self):

        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        CivilCvCAD.ActiveDocument.openTransaction(translate("Arch", "Create Building"))
        CivilCvCADGui.addModule("Arch")
        CivilCvCADGui.addModule("Draft")
        CivilCvCADGui.doCommand("obj = Arch.makeBuilding()")
        CivilCvCADGui.doCommand("Draft.autogroup(obj)")
        CivilCvCAD.ActiveDocument.commitTransaction()
        CivilCvCAD.ActiveDocument.recompute()


CivilCvCADGui.addCommand("Arch_Building", Arch_Building())
CivilCvCADGui.addCommand("Arch_Level", Arch_Level())
