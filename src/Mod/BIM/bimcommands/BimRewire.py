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

"""The BIM Rewire command"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP


class BIM_Rewire:

    def GetResources(self):
        return {
            "Pixmap": "BIM_Rewire",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Rewire", "Rewire"),
            "ToolTip": QT_TRANSLATE_NOOP("BIM_Rewire", "Recreates wires from selected objects"),
            "Accel": "R,W",
        }

    def IsActive(self):
        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        import Part
        import Draft
        import DraftGeomUtils

        objs = CivilCvCADGui.Selection.getSelection()
        names = []
        edges = []
        for obj in objs:
            if hasattr(obj, "Shape") and hasattr(obj.Shape, "Edges") and obj.Shape.Edges:
                edges.extend(obj.Shape.Edges)
                names.append(obj.Name)
        wires = DraftGeomUtils.findWires(edges)
        CivilCvCAD.ActiveDocument.openTransaction("Rewire")
        selectlist = []
        for wire in wires:
            if DraftGeomUtils.hasCurves(wire):
                nobj = CivilCvCAD.ActiveDocument.addObject("Part::Feature", "Wire")
                nobj.shape = wire
                selectlist.append(nobj)
            else:
                selectlist.append(Draft.makeWire([v.Point for v in wire.OrderedVertexes]))
        for name in names:
            CivilCvCAD.ActiveDocument.removeObject(name)
        CivilCvCAD.ActiveDocument.commitTransaction()
        CivilCvCADGui.Selection.clearSelection()
        for obj in selectlist:
            CivilCvCADGui.Selection.addSelection(obj)
        CivilCvCAD.ActiveDocument.recompute()


CivilCvCADGui.addCommand("BIM_Rewire", BIM_Rewire())
