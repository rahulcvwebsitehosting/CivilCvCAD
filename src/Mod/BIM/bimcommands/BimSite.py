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


class Arch_Site:
    "the Arch Site command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Site",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Site", "Site"),
            "Accel": "S, I",
            "ToolTip": QT_TRANSLATE_NOOP("Arch_Site", "Creates a site including selected objects"),
        }

    def IsActive(self):

        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        CivilCvCAD.ActiveDocument.openTransaction(translate("Arch", "Create Site"))
        CivilCvCADGui.addModule("Arch")
        CivilCvCADGui.addModule("Draft")
        CivilCvCADGui.doCommand("obj = Arch.makeSite()")
        CivilCvCADGui.doCommand("Draft.autogroup(obj)")
        CivilCvCAD.ActiveDocument.commitTransaction()
        CivilCvCAD.ActiveDocument.recompute()


CivilCvCADGui.addCommand("Arch_Site", Arch_Site())
