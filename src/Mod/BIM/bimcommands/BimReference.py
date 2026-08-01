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

"""BIM Rebar command"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate

PARAMS = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class Arch_Reference:
    "the Arch Reference command definition"

    def GetResources(self):

        return {
            "Pixmap": "Arch_Reference",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Reference", "External Reference"),
            "Accel": "E, X",
            "ToolTip": QT_TRANSLATE_NOOP("Arch_Reference", "Creates an external reference object"),
        }

    def IsActive(self):

        v = hasattr(CivilCvCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        CivilCvCADGui.Control.closeDialog()
        CivilCvCAD.ActiveDocument.openTransaction(translate("Arch", "Create external reference"))
        CivilCvCADGui.addModule("Arch")
        CivilCvCADGui.addModule("Draft")
        CivilCvCADGui.doCommand("obj = Arch.makeReference()")
        CivilCvCADGui.doCommand("Draft.autogroup(obj)")
        CivilCvCAD.ActiveDocument.commitTransaction()
        CivilCvCADGui.doCommand("obj.ViewObject.Document.setEdit(obj.ViewObject, 0)")


CivilCvCADGui.addCommand("Arch_Reference", Arch_Reference())
