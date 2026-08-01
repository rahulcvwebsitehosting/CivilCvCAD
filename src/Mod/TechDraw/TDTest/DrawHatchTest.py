import CivilCvCAD
import os
import unittest


class DrawHatchTest(unittest.TestCase):
    def setUp(self):
        """Creates a page and view"""
        self.path = os.path.dirname(os.path.abspath(__file__))
        print("TDHatch path: " + self.path)
        templateFileSpec = self.path + "/TestTemplate.svg"

        CivilCvCAD.newDocument("TDHatch")
        CivilCvCAD.setActiveDocument("TDHatch")
        CivilCvCAD.ActiveDocument = CivilCvCAD.getDocument("TDHatch")

        # make source feature
        box = CivilCvCAD.ActiveDocument.addObject("Part::Box", "Box")

        # make a page
        self.page = CivilCvCAD.ActiveDocument.addObject("TechDraw::DrawPage", "Page")
        CivilCvCAD.ActiveDocument.addObject("TechDraw::DrawSVGTemplate", "Template")
        CivilCvCAD.ActiveDocument.Template.Template = templateFileSpec
        CivilCvCAD.ActiveDocument.Page.Template = CivilCvCAD.ActiveDocument.Template
        self.page.Scale = 5.0
        # page.ViewObject.show()  #unit tests run in console mode

        # make Views
        self.view = CivilCvCAD.ActiveDocument.addObject("TechDraw::DrawViewPart", "View")
        CivilCvCAD.ActiveDocument.View.Source = [box]
        self.page.addView(self.view)
        CivilCvCAD.ActiveDocument.recompute()

    def tearDown(self):
        CivilCvCAD.closeDocument("TDHatch")

    def testMakeHatchCase(self):
        """Tests if hatch area can be added to view"""
        # make hatch
        print("making hatch")
        hatch = CivilCvCAD.ActiveDocument.addObject("TechDraw::DrawHatch", "Hatch")
        hatch.Source = (self.view, ["Face0"])
        hatchFileSpec = self.path + "/TestHatch.svg"
        # comment out to use default from preferences
        hatch.HatchPattern = (
            hatchFileSpec
        )
        print("finished hatch")
        CivilCvCAD.ActiveDocument.recompute()

        self.assertTrue("Up-to-date" in hatch.State)


if __name__ == "__main__":
    unittest.main()
