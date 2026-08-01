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

"""Misc Arch util commands"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate

PARAMS = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_CurtainWall:
    "the Arch Curtain Wall command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_CurtainWall",
            "MenuText": QT_TRANSLATE_NOOP("Arch_CurtainWall", "Curtain Wall"),
            "Accel": "C, W",
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_CurtainWall",
                "Creates a curtain wall object from selected line or from scratch",
            ),
        }

    def IsActive(self):

        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        self.doc = CivilCvCAD.ActiveDocument
        sel = CivilCvCADGui.Selection.getSelection()
        if len(sel) > 1:
            CivilCvCAD.Console.PrintError(
                translate("Arch", "Select only one base object or none") + "\n"
            )
        elif len(sel) == 1:
            # build on selection
            CivilCvCADGui.Control.closeDialog()
            self.doc.openTransaction(translate("Arch", "Create Curtain Wall"))
            CivilCvCADGui.addModule("Draft")
            CivilCvCADGui.addModule("Arch")
            CivilCvCADGui.doCommand(
                "obj = Arch.makeCurtainWall(CivilCvCAD.ActiveDocument."
                + CivilCvCADGui.Selection.getSelection()[0].Name
                + ")"
            )
            CivilCvCADGui.doCommand("Draft.autogroup(obj)")
            self.doc.commitTransaction()
            self.doc.recompute()
        else:
            # interactive line drawing
            import WorkingPlane

            CivilCvCAD.activeDraftCommand = self  # register as a Draft command for auto grid on/off
            self.wp = WorkingPlane.get_working_plane()
            self.wp._save()
            self.points = []
            CivilCvCADGui.Snapper.getPoint(callback=self.getPoint, hints=self.get_hints())

    def get_hints(self):
        "returns status bar input hints for the current tool state"
        from draftguitools import gui_tool_utils

        if not self.points:
            label = translate("Arch", "%1 pick first point")
        else:
            label = translate("Arch", "%1 pick next point")
        return (
            [CivilCvCADGui.InputHint(label, CivilCvCADGui.UserInput.MouseLeft)]
            + gui_tool_utils._get_hint_xyz_constrain()
            + gui_tool_utils._get_hint_mod_constrain()
            + gui_tool_utils._get_hint_mod_snap()
        )

    def getPoint(self, point=None, obj=None):
        """Callback for clicks during interactive mode"""

        if point is None:
            # cancelled
            self.wp._restore()
            CivilCvCAD.activeDraftCommand = None
            CivilCvCADGui.Snapper.off()
            return
        self.points.append(point)
        if len(self.points) == 1:
            CivilCvCADGui.Snapper.getPoint(
                last=self.points[0], callback=self.getPoint, hints=self.get_hints()
            )
        elif len(self.points) == 2:
            self.wp._restore()
            CivilCvCAD.activeDraftCommand = None
            CivilCvCADGui.Snapper.off()
            CivilCvCADGui.Control.closeDialog()
            self.doc.openTransaction(translate("Arch", "Create Curtain Wall"))
            CivilCvCADGui.addModule("Draft")
            CivilCvCADGui.addModule("Arch")
            CivilCvCADGui.doCommand(
                "base = Draft.makeLine(CivilCvCAD."
                + str(self.points[0])
                + ",CivilCvCAD."
                + str(self.points[1])
                + ")"
            )
            CivilCvCADGui.doCommand("obj = Arch.makeCurtainWall(base)")
            CivilCvCADGui.doCommand("Draft.autogroup(obj)")
            self.doc.commitTransaction()
            self.doc.recompute()


CivilCvCADGui.addCommand("Arch_CurtainWall", Arch_CurtainWall())
