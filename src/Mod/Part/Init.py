# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2001, 2002 Juergen Riegel <juergen.riegel@web.de>       *
# *                                                                         *
# *   This file is part of the CivilCvCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   CivilCvCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Lesser General Public License for more details.                   *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with CivilCvCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************/

# CivilCvCAD init script of the part module

import CivilCvCAD

translate = CivilCvCAD.Qt.translate

# CivilCvCAD.addImportType("CAD formats (*.igs *.iges *.step *.stp *.brep *.brp)","Part")
# CivilCvCAD.addExportType("CAD formats (*.igs *.iges *.step *.stp *.brep *.brp)","Part")
CivilCvCAD.addImportType("BREP (*.brep *.BREP *.brp *.BRP)", "Part")
CivilCvCAD.addExportType("BREP (*.brep *.brp)", "Part")
CivilCvCAD.addImportType("IGES (*.iges *.IGES *.igs *.IGS)", "Part")
CivilCvCAD.addExportType("IGES (*.iges *.igs)", "Part")
CivilCvCAD.addImportType("STEP with colors (*.step *.STEP *.stp *.STP)", "Import")

#: Translation note: "STEP" is a file type end should not be translated
CivilCvCAD.addTranslatableExportType(
    translate("FileFormat", "STEP with colors"), ["step", "stp"], "Import"
)

CivilCvCAD.__unit_test__ += ["TestPartApp"]
