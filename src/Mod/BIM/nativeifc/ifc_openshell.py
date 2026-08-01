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

"""Local IfcOpenShell status helpers for the offline-only distribution."""

from packaging.version import Version

import CivilCvCAD

translate = CivilCvCAD.Qt.translate
QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP


class IFC_UpdateIOS:
    """Shows a dialog to update IfcOpenShell"""

    def GetResources(self):
        tt = QT_TRANSLATE_NOOP("IFC_UpdateIOS", "Shows a dialog to update IfcOpenShell")
        return {
            "Pixmap": "IFC",
            "MenuText": QT_TRANSLATE_NOOP("IFC_UpdateIOS", "IfcOpenShell Update"),
            "ToolTip": tt,
        }

    def Activated(self):
        """Explain the local-only dependency policy."""

        from PySide import QtGui

        QtGui.QMessageBox.information(
            None,
            translate("BIM", "Offline dependency management"),
            translate(
                "BIM",
                "Automatic dependency checks and installation are disabled. "
                "Install IfcOpenShell from trusted local media and restart CivilCvCAD.",
            ),
        )

    def show_dialog(self, mode, version=None):
        """Show the offline dependency policy."""

        from PySide import QtGui

        del mode, version
        QtGui.QMessageBox.information(
            None,
            translate("BIM", "Offline dependency management"),
            translate(
                "BIM",
                "Automatic dependency checks and installation are disabled. "
                "Install IfcOpenShell from trusted local media and restart CivilCvCAD.",
            ),
        )

    def install(self):
        """Automatic installation is unavailable in an offline-only build."""

        return None

    def run_pip(self, args):
        """Reject package-index and installation subprocesses."""

        del args
        return None

    def get_current_version(self):
        """Retrieves the current ifcopenshell version"""

        import addonmanager_utilities as utils
        from packaging.version import InvalidVersion

        try:
            import ifcopenshell

            version = ifcopenshell.version
            try:
                Version(version)
            except InvalidVersion:
                CivilCvCAD.Console.PrintWarning(f"Invalid IfcOpenShell version: {version}\n")
                version = ""
        except:
            version = ""

        return version

    def get_avail_version(self):
        """Network version discovery is disabled."""

        return None
