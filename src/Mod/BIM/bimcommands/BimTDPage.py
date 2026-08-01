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

"""The BIM TDPage command"""

import os

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate


class BIM_TDPage:
    def GetResources(self):
        return {
            "Pixmap": "BIM_PageDefault",
            "MenuText": QT_TRANSLATE_NOOP("BIM_TDPage", "New Page"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_TDPage", "Creates a new TechDraw page from a template"
            ),
            "Accel": "T, P",
        }

    def IsActive(self):
        return CivilCvCADGui.ActiveDocument is not None

    def Activated(self):
        from PySide import QtGui
        import TechDraw

        templatedir = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM").GetString(
            "TDTemplateDir", ""
        )
        if not templatedir:
            templatedir = None
        filename, _ = QtGui.QFileDialog.getOpenFileName(
            QtGui.QApplication.activeWindow(),
            translate("BIM", "Select Page Template"),
            templatedir,
            "SVG file (*.svg)",
        )
        if filename:
            name = os.path.splitext(os.path.basename(filename))[0]
            CivilCvCAD.ActiveDocument.openTransaction("Create page")
            page = CivilCvCAD.ActiveDocument.addObject("TechDraw::DrawPage", "Page")
            page.Label = name
            template = CivilCvCAD.ActiveDocument.addObject("TechDraw::DrawSVGTemplate", "Template")
            template.Template = filename
            template.Label = translate("BIM", "Template")
            page.Template = template
            CivilCvCAD.ActiveDocument.commitTransaction()
            CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM").SetString(
                "TDTemplateDir", filename.replace("\\", "/")
            )
            for txt in ["scale", "Scale", "SCALE", "scaling", "Scaling", "SCALING"]:
                if txt in page.Template.EditableTexts:
                    val = page.Template.EditableTexts[txt]
                    if val:
                        val = val.replace(":", "/")
                        if "/" in val:
                            try:
                                num, den = val.split("/", 1)
                                page.Scale = float(num) / float(den)
                            except (ValueError, ZeroDivisionError):
                                pass
                            else:
                                break
                        else:
                            try:
                                page.Scale = float(val)
                            except ValueError:
                                pass
                            else:
                                break
            else:
                page.Scale = CivilCvCAD.ParamGet(
                    "User parameter:BaseApp/Preferences/Mod/BIM"
                ).GetFloat("DefaultPageScale", 0.01)
            page.ViewObject.show()
            CivilCvCAD.ActiveDocument.recompute()


CivilCvCADGui.addCommand("BIM_TDPage", BIM_TDPage())
