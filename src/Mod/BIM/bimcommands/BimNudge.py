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

"""BIM nudge commands"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate


class BIM_Nudge:
    # base class for the different nudge commands

    def getNudgeValue(self, mode):
        "mode can be dist, up, down, left, right. dist returns a float in mm, other modes return a 3D vector"

        from PySide import QtGui
        import WorkingPlane

        mw = CivilCvCADGui.getMainWindow()
        if mw:
            st = mw.statusBar()
            statuswidget = st.findChild(QtGui.QToolBar, "BIMStatusWidget")
            if statuswidget:
                nudgeValue = statuswidget.nudge.text().replace("&", "")
                dist = 0
                if "auto" in nudgeValue.lower():
                    unit = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt(
                        "UserSchema", 0
                    )
                    if unit in [2, 3, 5, 7]:
                        scale = [1.5875, 3.175, 6.35, 25.4, 152.4, 304.8]
                    else:
                        scale = [1, 5, 10, 50, 100, 500]
                    viewsize = (
                        CivilCvCADGui.ActiveDocument.ActiveView.getCameraNode()
                        .getViewVolume()
                        .getWidth()
                    )
                    if viewsize < 250:
                        dist = scale[0]
                    elif viewsize < 750:
                        dist = scale[1]
                    elif viewsize < 4500:
                        dist = scale[2]
                    elif viewsize < 8000:
                        dist = scale[3]
                    elif viewsize < 25000:
                        dist = scale[4]
                    else:
                        dist = scale[5]
                    # u = CivilCvCAD.Units.Quantity(dist,CivilCvCAD.Units.Length).UserString
                    statuswidget.nudge.setText(translate("BIM", "Auto"))
                else:
                    try:
                        dist = CivilCvCAD.Units.Quantity(nudgeValue)
                    except ValueError:
                        try:
                            dist = float(nudgeValue)
                        except ValueError:
                            return None
                    else:
                        dist = dist.Value
                if not dist:
                    return None
                if mode == "dist":
                    return dist
                wp = WorkingPlane.get_working_plane()
                if mode == "up":
                    return CivilCvCAD.Vector(wp.v).multiply(dist)
                if mode == "down":
                    return CivilCvCAD.Vector(wp.v).negative().multiply(dist)
                if mode == "right":
                    return CivilCvCAD.Vector(wp.u).multiply(dist)
                if mode == "left":
                    return CivilCvCAD.Vector(wp.u).negative().multiply(dist)
        return None

    def toStr(self, objs):
        "builds a string which is a list of objects"

        return "[" + ",".join(["CivilCvCAD.ActiveDocument." + obj.Name for obj in objs]) + "]"

    def getCenter(self, objs):
        "returns the center point of a group of objects"

        bb = None
        for obj in objs:
            if hasattr(obj, "Shape") and hasattr(obj.Shape, "BoundBox"):
                if not bb:
                    bb = obj.Shape.BoundBox
                else:
                    bb.add(obj.Shape.BoundBox)
        if bb:
            return bb.Center
        else:
            return None


class BIM_Nudge_Switch(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Switch", "Nudge Switch"),
            "Accel": "Alt+/",
        }

    def Activated(self):
        from PySide import QtGui

        mw = CivilCvCADGui.getMainWindow()
        if mw:
            st = mw.statusBar()
            statuswidget = st.findChild(QtGui.QToolBar, "BIMStatusWidget")
            if statuswidget:
                nudgeValue = statuswidget.nudge.text()
                nudge = self.getNudgeValue("dist")
                if nudge:
                    u = CivilCvCAD.Units.Quantity(nudge, CivilCvCAD.Units.Length).UserString
                    if "auto" in nudgeValue.lower():
                        statuswidget.nudge.setText(u)
                    else:
                        statuswidget.nudge.setText(translate("BIM", "Auto"))


class BIM_Nudge_Up(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Up", "Nudge Up"),
            "Accel": "Alt+'",
        }

    def Activated(self):
        sel = CivilCvCADGui.Selection.getSelection()
        if sel:
            nudge = self.getNudgeValue("up")
            if nudge:
                CivilCvCADGui.addModule("Draft")
                CivilCvCADGui.doCommand(
                    "Draft.move(" + self.toStr(sel) + ",CivilCvCAD." + str(nudge) + ")"
                )
                CivilCvCADGui.doCommand("CivilCvCAD.ActiveDocument.recompute()")


class BIM_Nudge_Down(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Down", "Nudge Down"),
            "Accel": "Alt+;",
        }

    def Activated(self):
        sel = CivilCvCADGui.Selection.getSelection()
        if sel:
            nudge = self.getNudgeValue("down")
            if nudge:
                CivilCvCADGui.addModule("Draft")
                CivilCvCADGui.doCommand(
                    "Draft.move(" + self.toStr(sel) + ",CivilCvCAD." + str(nudge) + ")"
                )
                CivilCvCADGui.doCommand("CivilCvCAD.ActiveDocument.recompute()")


class BIM_Nudge_Left(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Left", "Nudge Left"),
            "Accel": "Alt+[",
        }

    def Activated(self):
        sel = CivilCvCADGui.Selection.getSelection()
        if sel:
            nudge = self.getNudgeValue("left")
            if nudge:
                CivilCvCADGui.addModule("Draft")
                CivilCvCADGui.doCommand(
                    "Draft.move(" + self.toStr(sel) + ",CivilCvCAD." + str(nudge) + ")"
                )
                CivilCvCADGui.doCommand("CivilCvCAD.ActiveDocument.recompute()")


class BIM_Nudge_Right(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Right", "Nudge Right"),
            "Accel": "Alt+]",
        }

    def Activated(self):
        sel = CivilCvCADGui.Selection.getSelection()
        if sel:
            nudge = self.getNudgeValue("right")
            if nudge:
                CivilCvCADGui.addModule("Draft")
                CivilCvCADGui.doCommand(
                    "Draft.move(" + self.toStr(sel) + ",CivilCvCAD." + str(nudge) + ")"
                )
                CivilCvCADGui.doCommand("CivilCvCAD.ActiveDocument.recompute()")


class BIM_Nudge_Extend(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Extend", "Nudge Extend"),
            "Accel": "Alt+PgUp",
        }

    def Activated(self):
        sel = CivilCvCADGui.Selection.getSelection()
        if sel:
            nudge = self.getNudgeValue("dist")
            if nudge:
                for obj in sel:
                    if hasattr(obj, "Height"):
                        CivilCvCADGui.doCommand(
                            "CivilCvCAD.ActiveDocument."
                            + obj.Name
                            + ".Height="
                            + str(obj.Height.Value + nudge)
                        )
                        CivilCvCADGui.doCommand("CivilCvCAD.ActiveDocument.recompute()")


class BIM_Nudge_Shrink(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_Shrink", "Nudge Shrink"),
            "Accel": "Alt+PgDown",
        }

    def Activated(self):
        sel = CivilCvCADGui.Selection.getSelection()
        if sel:
            nudge = self.getNudgeValue("dist")
            if nudge:
                for obj in sel:
                    if hasattr(obj, "Height"):
                        CivilCvCADGui.doCommand(
                            "CivilCvCAD.ActiveDocument."
                            + obj.Name
                            + ".Height="
                            + str(obj.Height.Value - nudge)
                        )
                        CivilCvCADGui.doCommand("CivilCvCAD.ActiveDocument.recompute()")


class BIM_Nudge_RotateLeft(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_RotateLeft", "Nudge Rotate Left"),
            "Accel": "Alt+,",
        }

    def Activated(self):

        import WorkingPlane

        sel = CivilCvCADGui.Selection.getSelection()
        if sel:
            center = self.getCenter(sel)
            if center:
                CivilCvCADGui.addModule("Draft")
                CivilCvCADGui.doCommand(
                    "Draft.rotate("
                    + self.toStr(sel)
                    + ",45,CivilCvCAD."
                    + str(center)
                    + ",CivilCvCAD."
                    + str(WorkingPlane.get_working_plane().axis)
                    + ")"
                )
                CivilCvCADGui.doCommand("CivilCvCAD.ActiveDocument.recompute()")


class BIM_Nudge_RotateRight(BIM_Nudge):

    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("BIM_Nudge_RotateRight", "Nudge Rotate Right"),
            "Accel": "Alt+.",
        }

    def Activated(self):

        import WorkingPlane

        sel = CivilCvCADGui.Selection.getSelection()
        if sel:
            center = self.getCenter(sel)
            if center:
                CivilCvCADGui.addModule("Draft")
                CivilCvCADGui.doCommand(
                    "Draft.rotate("
                    + self.toStr(sel)
                    + ",-45,CivilCvCAD."
                    + str(center)
                    + ",CivilCvCAD."
                    + str(WorkingPlane.get_working_plane().axis)
                    + ")"
                )
                CivilCvCADGui.doCommand("CivilCvCAD.ActiveDocument.recompute()")


CivilCvCADGui.addCommand("BIM_Nudge_Switch", BIM_Nudge_Switch())
CivilCvCADGui.addCommand("BIM_Nudge_Up", BIM_Nudge_Up())
CivilCvCADGui.addCommand("BIM_Nudge_Down", BIM_Nudge_Down())
CivilCvCADGui.addCommand("BIM_Nudge_Left", BIM_Nudge_Left())
CivilCvCADGui.addCommand("BIM_Nudge_Right", BIM_Nudge_Right())
CivilCvCADGui.addCommand("BIM_Nudge_Extend", BIM_Nudge_Extend())
CivilCvCADGui.addCommand("BIM_Nudge_Shrink", BIM_Nudge_Shrink())
CivilCvCADGui.addCommand("BIM_Nudge_RotateLeft", BIM_Nudge_RotateLeft())
CivilCvCADGui.addCommand("BIM_Nudge_RotateRight", BIM_Nudge_RotateRight())
