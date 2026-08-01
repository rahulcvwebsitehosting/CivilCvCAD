# SPDX-License-Identifier: LGPL-2.1-or-later
# ****************************************************************************
# *                                                                          *
# *   Copyright (c) 2025 Pieter Hijma <info@pieterhijma.net>                 *
# *                                                                          *
# *   This file is part of CivilCvCAD.                                          *
# *                                                                          *
# *   CivilCvCAD is free software: you can redistribute it and/or modify it     *
# *   under the terms of the GNU Lesser General Public License as            *
# *   published by the Free Software Foundation, either version 2.1 of the   *
# *   License, or (at your option) any later version.                        *
# *                                                                          *
# *   CivilCvCAD is distributed in the hope that it will be useful, but         *
# *   WITHOUT ANY WARRANTY; without even the implied warranty of             *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU       *
# *   Lesser General Public License for more details.                        *
# *                                                                          *
# *   You should have received a copy of the GNU Lesser General Public       *
# *   License along with CivilCvCAD. If not, see                                *
# *   <https://www.gnu.org/licenses/>.                                       *
# *                                                                          *
# ***************************************************************************/

import unittest

import CivilCvCAD
import CivilCvCADGui as Gui


from Recompute import createPartDesignSketch


class FineGrainedRecomputeCasesGui(unittest.TestCase):
    def setUp(self):
        self.Doc = CivilCvCAD.newDocument(f"RecomputeTestsGui_{self._testMethodName}")
        self.ParamGroup = CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/General")
        self.fineGrainedPref = self.ParamGroup.GetBool("FineGrainedRecompute", False)
        self.ParamGroup.SetBool("FineGrainedRecompute", True)

    def tearDown(self):
        CivilCvCAD.closeDocument(self.Doc.Name)
        self.ParamGroup.SetBool("FineGrainedRecompute", self.fineGrainedPref)

    def testSketchWithInputPropertyAndPad(self):
        # References to input properties of dependent objects only works in
        # fine-grained mode.
        if not CivilCvCAD.GuiUp:
            self.skipTest("This test requires the GUI")

        if not CivilCvCAD.ParamGet("User parameter:BaseApp/Preferences/General").GetBool(
            "FineGrainedRecompute"
        ):
            self.skipTest("This test requires fine-grained recompute")

        createPartDesignSketch(self)

        body = self.Doc.Body
        body.addProperty("App::PropertyLength", "Length", "Params")
        body.Length = "20 mm"
        body.setPropertyStatus("Length", ["Input"])

        sketch = self.Doc.Sketch
        sketch.setExpression("Constraints[10]", "Body.Length")
        self.Doc.recompute()

        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.Doc.Name, body.Name, sketch.Name + ".")
        Gui.runCommand("PartDesign_Pad")

        taskDialog = Gui.Control.activeTaskDialog()
        if taskDialog:
            taskDialog.accept()

        self.Doc.recompute()

        self.assertEqual(body.Shape.BoundBox.XLength, 20.0)
        self.assertEqual(body.Shape.BoundBox.ZLength, 10.0)
