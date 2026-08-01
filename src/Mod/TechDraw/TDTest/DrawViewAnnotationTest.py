

import CivilCvCAD
import unittest
from .TechDrawTestUtilities import createPageWithSVGTemplate


class DrawViewAnnotationTest(unittest.TestCase):
    def setUp(self):
        """Creates a page"""
        CivilCvCAD.newDocument("TDAnno")
        CivilCvCAD.setActiveDocument("TDAnno")
        CivilCvCAD.ActiveDocument = CivilCvCAD.getDocument("TDAnno")
        self.page = createPageWithSVGTemplate()

    def tearDown(self):
        CivilCvCAD.closeDocument("TDAnno")

    def testMakeAnnotation(self):
        """Tests if an annotation can be added to page"""
        anno = CivilCvCAD.ActiveDocument.addObject(
            "TechDraw::DrawViewAnnotation", "TestAnno"
        )
        s = "Different Text"
        sl = list()
        sl.append(s)
        anno.Text = sl
        anno.TextStyle = "Bold"
        self.page.addView(anno)
        anno.X = 30.0
        anno.Y = 150.0
        CivilCvCAD.ActiveDocument.recompute()

        self.assertTrue("Up-to-date" in anno.State)


if __name__ == "__main__":
    unittest.main()
