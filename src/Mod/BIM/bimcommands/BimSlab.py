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

"""The BIM Slab command"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate


class BIM_Slab:

    def __init__(self):
        self.callback = None
        self.view = None

    def GetResources(self):
        return {
            "Pixmap": "BIM_Slab",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Slab", "Slab"),
            "ToolTip": QT_TRANSLATE_NOOP("BIM_Slab", "Creates a slab from a planar shape"),
            "Accel": "S,B",
        }

    def IsActive(self):
        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        import DraftTools

        self.removeCallback()
        sel = CivilCvCADGui.Selection.getSelection()
        if sel:
            self.proceed()
        else:
            if hasattr(CivilCvCADGui, "draftToolBar"):
                CivilCvCADGui.draftToolBar.selectUi()
            CivilCvCAD.Console.PrintMessage(translate("BIM", "Select a planar object") + "\n")
            self.view = CivilCvCADGui.ActiveDocument.ActiveView
            self.callback = self.view.addEventCallback("SoEvent", DraftTools.selectObject)

    def proceed(self):
        self.removeCallback()
        sel = CivilCvCADGui.Selection.getSelection()
        if len(sel) == 1:
            CivilCvCADGui.addModule("Arch")
            CivilCvCAD.ActiveDocument.openTransaction("Create Slab")
            CivilCvCADGui.doCommand(
                "s = Arch.makeStructure(CivilCvCAD.ActiveDocument." + sel[0].Name + ",height=200)"
            )
            CivilCvCADGui.doCommand("s.Label = " + repr(translate("BIM", "Slab")))
            CivilCvCADGui.doCommand('s.IfcType = "Slab"')
            CivilCvCADGui.doCommand("s.Normal = CivilCvCAD.Vector(0,0,-1)")
            CivilCvCAD.ActiveDocument.commitTransaction()
            CivilCvCAD.ActiveDocument.recompute()
        self.finish()

    def removeCallback(self):
        if self.callback:
            try:
                self.view.removeEventCallback("SoEvent", self.callback)
            except RuntimeError:
                pass
            self.callback = None

    def finish(self):
        self.removeCallback()
        if hasattr(CivilCvCADGui, "draftToolBar"):
            CivilCvCADGui.draftToolBar.offUi()


CivilCvCADGui.addCommand("BIM_Slab", BIM_Slab())
