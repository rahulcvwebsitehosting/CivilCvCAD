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

"""The Bim Sketch command"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP


class BIM_Sketch:
    def GetResources(self):
        return {
            "Pixmap": "Sketch",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Sketch", "New Sketch"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_Sketch", "Creates a new sketch in the current working plane"
            ),
            "Accel": "S,K",
        }

    def IsActive(self):
        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        import WorkingPlane
        from draftutils import params
        from draftutils import utils
        from CivilCvCAD import Units

        wp = WorkingPlane.get_working_plane()  # also updates the grid
        sk = CivilCvCAD.ActiveDocument.addObject("Sketcher::SketchObject", "Sketch")
        sk.Placement = wp.get_placement()
        sk.MapMode = "Deactivated"

        if not params.get_param("BIMSketchPlacementOnly", path="Mod/BIM"):
            sk.ViewObject.LineWidth = params.get_param_view("DefaultShapeLineWidth")
            sk.ViewObject.PointSize = params.get_param_view("DefaultShapePointSize")
            sk.ViewObject.AutoColor = False
            sk.ViewObject.LineColor = params.get_param_view("DefaultShapeLineColor")
            sk.ViewObject.PointColor = params.get_param_view("DefaultShapeVertexColor")
            sk.ViewObject.ShapeAppearance = [utils.get_view_material()]
            if getattr(CivilCvCADGui, "Snapper", None) and CivilCvCADGui.Snapper.grid.Visible:
                sk.ViewObject.GridSize = Units.Quantity(params.get_param("gridSpacing"))
                sk.ViewObject.ShowGrid = True

        CivilCvCADGui.ActiveDocument.setEdit(sk.Name)
        CivilCvCADGui.activateWorkbench("SketcherWorkbench")


CivilCvCADGui.addCommand("BIM_Sketch", BIM_Sketch())
