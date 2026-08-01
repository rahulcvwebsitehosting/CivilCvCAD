# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2022 Yorik van Havre <yorik@uncreated.net>              *
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

# add import/export types
CivilCvCAD.addExportType("Industry Foundation Classes (*.ifc)", "importers.exportIFC")
# CivilCvCAD.addImportType("Industry Foundation Classes (*.ifc)","importIFC")
CivilCvCAD.addImportType("Industry Foundation Classes (*.ifc)", "nativeifc.ifc_import")
CivilCvCAD.addExportType("Industry Foundation Classes - IFCJSON (*.ifcJSON)", "importers.exportIFC")
CivilCvCAD.addImportType("Wavefront OBJ - BIM (*.obj *.OBJ)", "importers.importOBJ")
CivilCvCAD.addExportType("Wavefront OBJ - BIM (*.obj)", "importers.importOBJ")
CivilCvCAD.addExportType("WebGL (*.html)", "importers.importWebGL")
CivilCvCAD.addExportType("JSON (*.json)", "importers.importJSON")
CivilCvCAD.addImportType("Collada (*.dae *.DAE)", "importers.importDAE")
CivilCvCAD.addExportType("Collada (*.dae)", "importers.importDAE")
CivilCvCAD.addImportType("3D Studio mesh (*.3ds *3DS)", "importers.import3DS")
CivilCvCAD.addImportType("SweetHome3D (*.sh3d)", "importers.importSH3D")
CivilCvCAD.addImportType("Shapefile (*.shp *.SHP)", "importers.importSHP")

CivilCvCAD.__unit_test__ += ["TestArch"]
