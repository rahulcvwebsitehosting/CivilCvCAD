# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2024 Werner Mayer <wmayer[at]users.sourceforge.net>     *
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

import unittest

import CivilCvCAD
import CivilCvCADGui

""" Test active object list """


class TestActiveObject(unittest.TestCase):
    def setUp(self):
        self.doc = CivilCvCAD.newDocument("PartDesignTestSketch")

    def testPartBody(self):
        self.doc.openTransaction("Create part")
        part = self.doc.addObject("App::Part", "Part")
        CivilCvCADGui.activateView("Gui::View3DInventor", True)
        CivilCvCADGui.activeView().setActiveObject("part", part)
        self.doc.commitTransaction()

        self.doc.openTransaction("Create body")
        body = self.doc.addObject("PartDesign::Body", "Body")
        part.addObject(body)
        CivilCvCADGui.activateView("Gui::View3DInventor", True)
        CivilCvCADGui.activeView().setActiveObject("pdbody", body)
        self.doc.commitTransaction()

        self.doc.undo()  # undo body creation
        self.doc.undo()  # undo part creation

        CivilCvCADGui.updateGui()

        self.doc.openTransaction("Create body")
        body = self.doc.addObject("PartDesign::Body", "Body")
        CivilCvCADGui.activateView("Gui::View3DInventor", True)
        CivilCvCADGui.activeView().setActiveObject("pdbody", body)
        self.doc.commitTransaction()

        CivilCvCADGui.updateGui()

    def _createBooleanWithTwoTools(self):
        CivilCvCADGui.activateView("Gui::View3DInventor", True)

        tools = []
        for index in range(2):
            body = self.doc.addObject("PartDesign::Body", f"ToolBody{index}")
            box = self.doc.addObject("PartDesign::AdditiveBox", f"ToolBox{index}")
            body.addObject(box)
            tools.append(body)

        resultBody = self.doc.addObject("PartDesign::Body", "ResultBody")
        boolean = self.doc.addObject("PartDesign::Boolean", "Boolean")
        resultBody.addObject(boolean)
        boolean.Group = tools
        boolean.ViewObject.Display = "Result"
        self.doc.recompute()

        for tool in tools:
            tool.ViewObject.hide()
        boolean.ViewObject.show()
        CivilCvCADGui.updateGui()

        return boolean, tools

    def testBooleanActiveBodyVisibilitySwitch(self):
        boolean, tools = self._createBooleanWithTwoTools()
        view = CivilCvCADGui.activeView()

        view.setActiveObject("pdbody", tools[0])
        self.assertTrue(tools[0].ViewObject.isVisible())
        self.assertFalse(tools[1].ViewObject.isVisible())

        view.setActiveObject("pdbody", tools[1])
        self.assertFalse(tools[0].ViewObject.isVisible())
        self.assertTrue(tools[1].ViewObject.isVisible())

        view.setActiveObject("pdbody", None)
        self.assertFalse(tools[0].ViewObject.isVisible())
        self.assertFalse(tools[1].ViewObject.isVisible())
        self.assertTrue(boolean.ViewObject.isVisible())

        view.setActiveObject("pdbody", tools[0])
        boolean.Group = [tools[1]]
        CivilCvCADGui.updateGui()
        self.assertFalse(tools[0].ViewObject.isVisible())
        self.assertTrue(boolean.ViewObject.isVisible())

    def testBooleanActiveBodyVisibilityRestoresState(self):
        boolean, tools = self._createBooleanWithTwoTools()
        view = CivilCvCADGui.activeView()
        booleanMode = boolean.ViewObject.SwitchNode.whichChild.getValue()

        tools[0].ViewObject.show()
        toolMode = tools[0].ViewObject.SwitchNode.whichChild.getValue()
        view.setActiveObject("pdbody", tools[0])
        view.setActiveObject("pdbody", None)
        self.assertTrue(tools[0].ViewObject.isVisible())
        self.assertEqual(boolean.ViewObject.SwitchNode.whichChild.getValue(), booleanMode)
        self.assertEqual(tools[0].ViewObject.SwitchNode.whichChild.getValue(), toolMode)

        tools[0].ViewObject.hide()
        view.setActiveObject("pdbody", tools[0])
        boolean.Visibility = False
        CivilCvCADGui.updateGui()
        self.assertTrue(tools[0].ViewObject.isVisible())
        self.assertFalse(boolean.ViewObject.Visibility)

        view.setActiveObject("pdbody", None)
        self.assertFalse(tools[0].ViewObject.isVisible())
        self.assertFalse(boolean.ViewObject.isVisible())

    def testBooleanActiveNestedBodyVisibility(self):
        innerBoolean, tools = self._createBooleanWithTwoTools()
        innerBody = innerBoolean.getParentGeoFeatureGroup()
        innerLaterFeature = self.doc.addObject("PartDesign::AdditiveBox", "InnerLaterFeature")
        innerBody.addObject(innerLaterFeature)

        outerBody = self.doc.addObject("PartDesign::Body", "OuterResultBody")
        outerBoolean = self.doc.addObject("PartDesign::Boolean", "OuterBoolean")
        outerBody.addObject(outerBoolean)
        outerBoolean.Group = [innerBody]
        outerLaterFeature = self.doc.addObject("PartDesign::AdditiveBox", "OuterLaterFeature")
        outerBody.addObject(outerLaterFeature)
        self.doc.recompute()

        innerBody.ViewObject.hide()
        outerBoolean.ViewObject.show()
        outerLaterFeature.ViewObject.show()
        view = CivilCvCADGui.activeView()

        view.setActiveObject("pdbody", tools[0])
        self.assertTrue(tools[0].ViewObject.isVisible())
        self.assertTrue(innerBody.ViewObject.isVisible())
        self.assertTrue(innerLaterFeature.ViewObject.isVisible())
        self.assertTrue(outerLaterFeature.ViewObject.isVisible())

        view.setActiveObject("pdbody", None)
        self.assertFalse(tools[0].ViewObject.isVisible())
        self.assertFalse(innerBody.ViewObject.isVisible())
        self.assertTrue(innerLaterFeature.ViewObject.isVisible())
        self.assertTrue(outerLaterFeature.ViewObject.isVisible())

    def testBooleanActiveBodyVisibilityWhenBooleanIsNotTip(self):
        boolean, tools = self._createBooleanWithTwoTools()
        resultBody = boolean.getParentGeoFeatureGroup()
        laterFeature = self.doc.addObject("PartDesign::AdditiveBox", "LaterFeature")
        resultBody.addObject(laterFeature)
        self.doc.recompute()
        CivilCvCADGui.updateGui()

        self.assertFalse(boolean.ViewObject.Visibility)
        self.assertTrue(laterFeature.ViewObject.isVisible())

        CivilCvCADGui.activeView().setActiveObject("pdbody", tools[0])
        self.assertTrue(tools[0].ViewObject.isVisible())
        self.assertFalse(boolean.ViewObject.Visibility)
        self.assertTrue(laterFeature.ViewObject.isVisible())

        CivilCvCADGui.activeView().setActiveObject("pdbody", None)
        self.assertFalse(tools[0].ViewObject.isVisible())
        self.assertFalse(boolean.ViewObject.isVisible())
        self.assertTrue(laterFeature.ViewObject.isVisible())

    def testBooleanActiveBodyVisibilityWhenBooleanBecomesNonTip(self):
        boolean, tools = self._createBooleanWithTwoTools()
        view = CivilCvCADGui.activeView()
        view.setActiveObject("pdbody", tools[0])

        resultBody = boolean.getParentGeoFeatureGroup()
        laterFeature = self.doc.addObject("PartDesign::AdditiveBox", "LaterFeature")
        resultBody.addObject(laterFeature)
        self.doc.recompute()
        CivilCvCADGui.updateGui()

        self.assertTrue(tools[0].ViewObject.isVisible())
        self.assertFalse(boolean.ViewObject.Visibility)
        self.assertTrue(laterFeature.ViewObject.isVisible())

        view.setActiveObject("pdbody", None)
        self.assertFalse(tools[0].ViewObject.isVisible())
        self.assertFalse(boolean.ViewObject.isVisible())
        self.assertTrue(laterFeature.ViewObject.isVisible())

    def testBooleanActiveBodyVisibilityRestoresModeWithOverride(self):
        boolean, tools = self._createBooleanWithTwoTools()
        view = CivilCvCADGui.activeView()
        viewer = view.getViewer()
        booleanMode = boolean.ViewObject.SwitchNode.whichChild.getValue()

        tools[0].ViewObject.show()
        toolMode = tools[0].ViewObject.SwitchNode.whichChild.getValue()
        tools[0].ViewObject.hide()

        try:
            viewer.setOverrideMode("Wireframe")
            view.setActiveObject("pdbody", tools[0])
            view.setActiveObject("pdbody", None)
        finally:
            viewer.setOverrideMode("As Is")

        self.assertEqual(boolean.ViewObject.SwitchNode.whichChild.getValue(), booleanMode)
        tools[0].ViewObject.show()
        self.assertEqual(tools[0].ViewObject.SwitchNode.whichChild.getValue(), toolMode)

    def tearDown(self):
        CivilCvCAD.closeDocument("PartDesignTestSketch")
