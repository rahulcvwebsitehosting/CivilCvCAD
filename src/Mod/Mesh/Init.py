# SPDX-License-Identifier: LGPL-2.1-or-later

# CivilCvCAD init script of the Mesh module
# (c) 2004 Werner Mayer LGPL

import CivilCvCAD

translate = CivilCvCAD.Qt.translate

# Append the open handler
CivilCvCAD.addImportType("STL Mesh (*.stl *.STL *.ast *.AST)", "Mesh")
CivilCvCAD.addImportType("Binary Mesh (*.bms *.BMS)", "Mesh")
CivilCvCAD.addImportType("Alias Mesh (*.obj *.OBJ)", "Mesh")
CivilCvCAD.addImportType("Object File Format Mesh (*.off *.OFF)", "Mesh")
CivilCvCAD.addImportType("Stanford Triangle Mesh (*.ply *.PLY)", "Mesh")
CivilCvCAD.addImportType("Simple Model Format (*.smf *.SMF)", "Mesh")
CivilCvCAD.addImportType("3D Manufacturing Format (*.3mf *.3MF)", "Mesh")

CivilCvCAD.addTranslatableExportType(translate("FileFormat", "STL Mesh"), ["stl", "ast"], "Mesh")
CivilCvCAD.addTranslatableExportType(translate("FileFormat", "Binary Mesh"), ["bms"], "Mesh")

#: Translation note: "Alias" in this case is a product/format name and should not be translated
CivilCvCAD.addTranslatableExportType(translate("FileFormat", "Alias Mesh"), ["obj"], "Mesh")

#: Translation note: "Object File Format" is the official name and should not be translated
CivilCvCAD.addTranslatableExportType(
    translate("FileFormat", "Object File Format Mesh"), ["off"], "Mesh"
)

CivilCvCAD.addExportType("Stanford Triangle Mesh (*.ply)", "Mesh")
CivilCvCAD.addExportType("Additive Manufacturing Format (*.amf)", "Mesh")
CivilCvCAD.addExportType("Simple Model Format (*.smf)", "Mesh")
CivilCvCAD.addExportType("3D Manufacturing Format (*.3mf)", "Mesh")

CivilCvCAD.__unit_test__ += ["MeshTestsApp"]
