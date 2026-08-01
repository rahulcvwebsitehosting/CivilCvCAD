# ***************************************************************************
# *   Copyright (c) 2001,2002 Juergen Riegel <juergen.riegel@web.de>        *
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
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with CivilCvCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************/

# CivilCvCAD Part module
#
# Part design module

# import CivilCvCAD modules
import CivilCvCAD, CivilCvCADGui

# import the App Test module
import TestApp  # Test as Module name not possible
import sys


# ---------------------------------------------------------------------------
# define the Commands of the Test Application module
# ---------------------------------------------------------------------------
class TestCmd:
    """Opens a Qt dialog with all inserted unit tests"""

    def Activated(self):
        import QtUnitGui

        tests = CivilCvCAD.__unit_test__

        QtUnitGui.addTest("TestApp.All")
        QtUnitGui.setTest("TestApp.All")
        for test in tests:
            QtUnitGui.addTest(test)

    def GetResources(self):
        return {
            "MenuText": "Self-test...",
            "ToolTip": "Runs a self-test to check if the application works properly",
        }


class TestAllCmd:
    "Test all commando object"

    def Activated(self):
        import QtUnitGui

        QtUnitGui.addTest("TestApp.All")
        QtUnitGui.setTest("TestApp.All")

    def GetResources(self):
        return {
            "Pixmap": "Std_Tool1",
            "MenuText": "Test all",
            "ToolTip": "Runs all tests at once (can take very long!)",
        }


class TestDocCmd:
    "Document test commando object"

    def Activated(self):
        import QtUnitGui

        QtUnitGui.addTest("Document")
        QtUnitGui.setTest("Document")

    def GetResources(self):
        return {
            "Pixmap": "Std_Tool1",
            "MenuText": "Test Document",
            "ToolTip": "Test the document (creation, save, load and destruction)",
        }


class TestBaseCmd:
    "Base test commando object"

    def Activated(self):
        import QtUnitGui

        QtUnitGui.addTest("BaseTests")
        QtUnitGui.setTest("BaseTests")

    def GetResources(self):
        return {
            "Pixmap": "Std_Tool1",
            "MenuText": "Test base",
            "ToolTip": "Test the basic functions of CivilCvCAD",
        }


class TestAllTextCmd:
    "Test all commando object"

    def Activated(self):
        import unittest, TestApp

        unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromName("TestApp.All")
        )

    def GetResources(self):
        return {
            "Pixmap": "Std_Tool1",
            "MenuText": "Test all",
            "ToolTip": "Runs all tests at once (can take very long!)",
        }


class TestDocTextCmd:
    "Document test commando object"

    def Activated(self):
        TestApp.TestText("Document")

    def GetResources(self):
        return {
            "Pixmap": "Std_Tool1",
            "MenuText": "Test Document",
            "ToolTip": "Test the document (creation, save, load and destruction)",
        }


class TestBaseTextCmd:
    "Base test commando object"

    def Activated(self):
        TestApp.TestText("BaseTests")

    def GetResources(self):
        return {
            "Pixmap": "Std_Tool1",
            "MenuText": "Test base",
            "ToolTip": "Test the basic functions of CivilCvCAD",
        }


class TestWorkbenchCmd:
    "Workbench test"

    def Activated(self):
        i = 0
        while i < 20:
            CivilCvCADGui.activateWorkbench("MeshWorkbench")
            CivilCvCADGui.updateGui()
            CivilCvCADGui.activateWorkbench("NoneWorkbench")
            CivilCvCADGui.updateGui()
            CivilCvCADGui.activateWorkbench("PartWorkbench")
            CivilCvCADGui.updateGui()
            print(i)
            i = i + 1
        CivilCvCADGui.activateWorkbench("TestWorkbench")

    def GetResources(self):
        return {
            "Pixmap": "Std_Tool1",
            "MenuText": "Test workbench",
            "ToolTip": "Test the switching of workbenches in CivilCvCAD",
        }


class TestCreateMenuCmd:
    "Base test commando object"

    def Activated(self):
        TestApp.TestText("Menu.MenuCreateCases")

    def GetResources(self):
        return {
            "Pixmap": "Std_Tool1",
            "MenuText": "Add menu",
            "ToolTip": "Test the menu stuff of CivilCvCAD",
        }


class TestDeleteMenuCmd:
    "Base test commando object"

    def Activated(self):
        TestApp.TestText("Menu.MenuDeleteCases")

    def GetResources(self):
        return {
            "Pixmap": "Std_Tool1",
            "MenuText": "Remove menu",
            "ToolTip": "Test the menu stuff of CivilCvCAD",
        }


class TestInsertFeatureCmd:
    "Base test commando object"

    def Activated(self):
        if CivilCvCAD.activeDocument() is not None:
            CivilCvCAD.activeDocument().addObject("App::FeatureTest")
        else:
            CivilCvCAD.PrintMessage("No active document.\n")

    def GetResources(self):
        return {
            "Pixmap": "Std_Tool1",
            "MenuText": "Insert a TestFeature",
            "ToolTip": "Insert a TestFeature in the active Document",
        }


# ---------------------------------------------------------------------------
# Adds the commands to the CivilCvCAD command manager
# ---------------------------------------------------------------------------
CivilCvCADGui.addCommand("Test_Test", TestCmd())
CivilCvCADGui.addCommand("Test_TestAllText", TestAllTextCmd())
CivilCvCADGui.addCommand("Test_TestDocText", TestDocTextCmd())
CivilCvCADGui.addCommand("Test_TestBaseText", TestBaseTextCmd())
CivilCvCADGui.addCommand("Test_TestAll", TestAllCmd())
CivilCvCADGui.addCommand("Test_TestDoc", TestDocCmd())
CivilCvCADGui.addCommand("Test_TestBase", TestBaseCmd())
CivilCvCADGui.addCommand("Test_TestWork", TestWorkbenchCmd())
CivilCvCADGui.addCommand("Test_TestCreateMenu", TestCreateMenuCmd())
CivilCvCADGui.addCommand("Test_TestDeleteMenu", TestDeleteMenuCmd())
CivilCvCADGui.addCommand("Test_InsertFeature", TestInsertFeatureCmd())
