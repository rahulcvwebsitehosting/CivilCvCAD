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

"""BIM Panel-related Arch_"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate

PARAMS = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Pipe:
    "the Arch Pipe command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Pipe",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Pipe", "Pipe"),
            "Accel": "P, I",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Pipe", "Creates a pipe object from a given wire or line"
            ),
        }

    def IsActive(self):

        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        s = CivilCvCADGui.Selection.getSelection()
        if s:
            for obj in s:
                if hasattr(obj, "Shape"):
                    if len(obj.Shape.Wires) == 1:
                        CivilCvCAD.ActiveDocument.openTransaction(translate("Arch", "Create Pipe"))
                        CivilCvCADGui.addModule("Arch")
                        CivilCvCADGui.addModule("Draft")
                        CivilCvCADGui.doCommand(
                            "obj = Arch.makePipe(CivilCvCAD.ActiveDocument." + obj.Name + ")"
                        )
                        CivilCvCADGui.doCommand("Draft.autogroup(obj)")
                        CivilCvCAD.ActiveDocument.commitTransaction()
        else:
            CivilCvCAD.ActiveDocument.openTransaction(translate("Arch", "Create Pipe"))
            CivilCvCADGui.addModule("Arch")
            CivilCvCADGui.addModule("Draft")
            CivilCvCADGui.doCommand("obj = Arch.makePipe()")
            CivilCvCADGui.doCommand("Draft.autogroup(obj)")
            CivilCvCAD.ActiveDocument.commitTransaction()
        CivilCvCAD.ActiveDocument.recompute()


class Arch_PipeConnector:
    "the Arch Pipe command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_PipeConnector",
            "MenuText": QT_TRANSLATE_NOOP("Arch_PipeConnector", "Connector"),
            "Accel": "P, C",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_PipeConnector", "Creates a connector between 2 or 3 selected pipes"
            ),
        }

    def IsActive(self):

        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        import Draft

        s = CivilCvCADGui.Selection.getSelection()
        if not (len(s) in [2, 3]):
            CivilCvCAD.Console.PrintError(
                translate("Arch", "Select exactly 2 or 3 pipe objects") + "\n"
            )
            return
        o = "["
        for obj in s:
            if Draft.getType(obj) != "Pipe":
                CivilCvCAD.Console.PrintError(translate("Arch", "Select only pipe objects") + "\n")
                return
            o += "CivilCvCAD.ActiveDocument." + obj.Name + ","
        o += "]"
        CivilCvCAD.ActiveDocument.openTransaction(translate("Arch", "Create Connector"))
        CivilCvCADGui.addModule("Arch")
        CivilCvCADGui.addModule("Draft")
        CivilCvCADGui.doCommand("obj = Arch.makePipeConnector(" + o + ")")
        CivilCvCADGui.doCommand("Draft.autogroup(obj)")
        CivilCvCAD.ActiveDocument.commitTransaction()
        CivilCvCAD.ActiveDocument.recompute()


class Arch_PipeGroupCommand:

    def GetCommands(self):
        return tuple(["Arch_Pipe", "Arch_PipeConnector"])

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("Arch_PipeTools", "Pipe Tools"),
            "ToolTip": QT_TRANSLATE_NOOP("Arch_PipeTools", "Pipe tools"),
        }

    def IsActive(self):
        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v


CivilCvCADGui.addCommand("Arch_Pipe", Arch_Pipe())
CivilCvCADGui.addCommand("Arch_PipeConnector", Arch_PipeConnector())
CivilCvCADGui.addCommand("Arch_PipeTools", Arch_PipeGroupCommand())
