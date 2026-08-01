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

"""The BIM Help command"""

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP


class BIM_Help:

    def GetResources(self):
        return {
            "Pixmap": "BIM_Help",
            "MenuText": QT_TRANSLATE_NOOP("BIM_Help", "BIM Help"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_Help",
                "Opens the BIM help page on the CivilCvCAD documentation website",
            ),
        }

    def Activated(self):
        CivilCvCAD.Console.PrintWarning(
            "Online BIM help is unavailable in this offline-only CivilCvCAD build.\n"
        )


CivilCvCADGui.addCommand("BIM_Help", BIM_Help())
