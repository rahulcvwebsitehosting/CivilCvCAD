# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2002 Jürgen Riegel <juergen.riegel@web.de>              *
# *   Copyright (c) 2025 Frank Martínez <mnesarco at gmail dot com>         *
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

# CivilCvCAD init module - Tests
#
# Gathering all the information to start CivilCvCAD.
# This is the third of four init scripts:
# +------+------------------+-----------------------------+
# | This | Script           | Runs                        |
# +------+------------------+-----------------------------+
# |      | CMakeVariables   | always                      |
# |      | CivilCvCADInit      | always                      |
# | >>>> | CivilCvCADTest      | only if test and not Gui    |
# |      | CivilCvCADGuiInit   | only if Gui is up           |
# +------+------------------+-----------------------------+

# Testing the function of the base system and run
# (if existing) the test function of the modules

import CivilCvCAD
import typing

if typing.TYPE_CHECKING:
    from __main__ import Log

Log("CivilCvCAD test running...\n\n")
Log("Init: starting App::CivilCvCADTest.py\n")
Log("░░░▀█▀░█▀█░▀█▀░▀█▀░░░▀█▀░█▀▀░█▀▀░▀█▀░█▀▀░░░\n")
Log("░░░░█░░█░█░░█░░░█░░░░░█░░█▀░░▀▀█░░█░░▀▀█░░░\n")
Log("░░░▀▀▀░▀░▀░▀▀▀░░▀░░░░░▀░░▀▀▀░▀▀▀░░▀░░▀▀▀░░░\n")

import sys
import TestApp

testResult = TestApp.RunConfiguredTextTest()

Log("CivilCvCAD test done\n")

sys.exit(0 if testResult.wasSuccessful() else 1)
