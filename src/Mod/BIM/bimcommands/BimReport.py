# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Copyright (c) 2025 The FreeCAD Project

import CivilCvCAD
import CivilCvCADGui


class BIM_Report:
    """The command to create a new BIM Report object."""

    def GetResources(self):
        return {
            "Pixmap": "BIM_Report",
            "MenuText": "BIM Report",
            "ToolTip": "Create a new BIM Report to query model data with SQL",
        }

    def Activated(self):
        CivilCvCADGui.addModule("Arch")
        CivilCvCADGui.doCommand("Arch.makeReport()")

    def IsActive(self):
        return CivilCvCAD.ActiveDocument is not None


CivilCvCADGui.addCommand("BIM_Report", BIM_Report())
