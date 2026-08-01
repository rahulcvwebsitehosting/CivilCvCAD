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

"""The BIM DrawingView command"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate

PARAMS = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")
view_params = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/View")
arch_params = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Arch")


class BIM_DrawingView:
    """The command definition for the Drawing View command"""

    def GetResources(self):

        return {
            "Pixmap": "BIM_ArchView",
            "MenuText": QT_TRANSLATE_NOOP("BIM_DrawingView", "2D Drawing"),
            "Accel": "V, D",
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_DrawingView", "Creates a drawing container to contain elements of a 2D view"
            ),
        }

    def IsActive(self):

        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        import Draft

        default_line_width = view_params.GetInt("DefaultShapeLineWidth", 2)
        thickness_ratio = arch_params.GetFloat("CutLineThickness", 2.0)
        cut_lines_width = default_line_width * thickness_ratio

        CivilCvCAD.ActiveDocument.openTransaction(translate("Arch", "Create 2D View"))
        CivilCvCADGui.addModule("Arch")
        CivilCvCADGui.addModule("Draft")
        CivilCvCADGui.addModule("WorkingPlane")
        CivilCvCADGui.doCommand("obj = Arch.make2DDrawing()")
        CivilCvCADGui.doCommand("Draft.autogroup(obj)")
        s = CivilCvCADGui.Selection.getSelection()
        if len(s) == 1:
            s = s[0]
            if Draft.getType(s) == "SectionPlane":
                CivilCvCADGui.doCommand(
                    "vobj = Draft.make_shape2dview(CivilCvCAD.ActiveDocument." + s.Name + ")"
                )
                CivilCvCADGui.doCommand("vobj.Label = " + repr(translate("BIM", "Viewed lines")))
                CivilCvCADGui.doCommand("vobj.InPlace = False")
                CivilCvCADGui.doCommand("obj.addObject(vobj)")
                CivilCvCADGui.doCommand(
                    "cobj = Draft.make_shape2dview(CivilCvCAD.ActiveDocument." + s.Name + ")"
                )
                CivilCvCADGui.doCommand("cobj.Label = " + repr(translate("BIM", "Cut lines")))
                CivilCvCADGui.doCommand("cobj.InPlace = False")
                CivilCvCADGui.doCommand('cobj.ProjectionMode = "Cutfaces"')
                CivilCvCADGui.doCommand("cobj.ViewObject.LineWidth = " + str(cut_lines_width))
                CivilCvCADGui.doCommand("obj.addObject(cobj)")
        CivilCvCAD.ActiveDocument.commitTransaction()
        CivilCvCAD.ActiveDocument.recompute()


CivilCvCADGui.addCommand("BIM_DrawingView", BIM_DrawingView())
