

import CivilCvCAD
import os
import unittest
from .TechDrawTestUtilities import createPageWithSVGTemplate


class DrawViewImageTest(unittest.TestCase):
    def setUp(self):
        """Creates a page"""
        CivilCvCAD.newDocument("TDAnno")
        CivilCvCAD.setActiveDocument("TDAnno")
        CivilCvCAD.ActiveDocument = CivilCvCAD.getDocument("TDAnno")
        self.page = createPageWithSVGTemplate()

    def tearDown(self):
        CivilCvCAD.closeDocument("TDAnno")

    def testMakeImage(self):
        """Tests if an image can be added to page"""
        path = os.path.dirname(os.path.abspath(__file__))
        imageFileSpec = path + "/TestImage.png"
        img = CivilCvCAD.ActiveDocument.addObject("TechDraw::DrawViewImage", "TestImage")
        img.ImageFile = imageFileSpec
        self.page.addView(img)

        CivilCvCAD.ActiveDocument.recompute()

        self.assertTrue("Up-to-date" in img.State)


if __name__ == "__main__":
    unittest.main()
