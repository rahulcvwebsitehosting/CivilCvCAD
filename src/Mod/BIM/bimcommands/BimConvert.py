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

"""The BIM Convert command"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP


class BIM_Convert:

    def GetResources(self):
        return {
            "Pixmap": "Arch_Component",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Convert", "Convert to BIM"),
            "ToolTip": QT_TRANSLATE_NOOP("BIM_Convert", "Converts any object to a BIM component"),
        }

    def IsActive(self):
        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):
        sel = CivilCvCADGui.Selection.getSelection()
        if sel:
            CivilCvCADGui.Control.showDialog(BIM_Convert_TaskPanel(sel))


class BIM_Convert_TaskPanel:

    def __init__(self, objs):
        from PySide import QtGui

        self.types = [
            "Wall",
            "Structure",
            "Rebar",
            "Window",
            "Stairs",
            "Roof",
            "Panel",
            "Frame",
            "Space",
            "Equipment",
            "Component",
        ]
        self.objs = objs
        self.form = QtGui.QListWidget()
        for t in self.types:
            ti = t + "_Tree"
            tx = t
            if t == "Component":
                ti = t
                tx = "Generic component"
            i = QtGui.QListWidgetItem(QtGui.QIcon(":/icons/Arch_" + ti + ".svg"), tx)
            i.setToolTip(t)
            self.form.addItem(i)
        self.form.itemDoubleClicked.connect(self.accept)

    def accept(self, idx=None):
        i = self.form.currentItem()
        if i:
            import Arch

            CivilCvCAD.ActiveDocument.openTransaction("Convert to BIM")
            for o in self.objs:
                getattr(Arch, "make" + i.toolTip())(o)
            CivilCvCAD.ActiveDocument.commitTransaction()
            CivilCvCAD.ActiveDocument.recompute()
        if idx:
            from draftutils import todo

            todo.ToDo.delay(CivilCvCADGui.Control.closeDialog, None)
        return True


CivilCvCADGui.addCommand("BIM_Convert", BIM_Convert())
