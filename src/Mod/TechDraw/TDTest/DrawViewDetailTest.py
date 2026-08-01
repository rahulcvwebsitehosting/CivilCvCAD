# test script for DrawViewDetail
# creates a page, a view and a detail view


import CivilCvCAD
import unittest
from .TechDrawTestUtilities import createPageWithSVGTemplate
from PySide import QtCore

class DrawViewDetailTest(unittest.TestCase):
    def setUp(self):
        """Creates a page"""
        CivilCvCAD.newDocument("TDPart")
        CivilCvCAD.setActiveDocument("TDPart")
        CivilCvCAD.ActiveDocument = CivilCvCAD.getDocument("TDPart")

        CivilCvCAD.ActiveDocument.addObject("Part::Box", "Box")

        self.page = createPageWithSVGTemplate()
        self.page.Scale = 5.0
        # page.ViewObject.show()    # unit tests run in console mode
        print("DrawViewDetail test: page created")

        self.view = CivilCvCAD.ActiveDocument.addObject("TechDraw::DrawViewPart", "View")
        self.page.addView(self.view)
        CivilCvCAD.ActiveDocument.View.Source = [CivilCvCAD.ActiveDocument.Box]
        CivilCvCAD.ActiveDocument.recompute()

        #wait for threads to complete before checking result
        loop = QtCore.QEventLoop()

        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)

        timer.start(2000)   #2 second delay
        loop.exec_()
        print("DrawViewDetail test: view created")

    def tearDown(self):
        print("DrawViewDetail test finished")
        CivilCvCAD.closeDocument("TDPart")

    def testMakeDrawViewPart(self):
        """Tests if a view can be added to page"""
        print("testing DrawViewDetail")

        detail = CivilCvCAD.ActiveDocument.addObject(
            "TechDraw::DrawViewDetail", "Detail"
        )
        detail.BaseView = self.view
        detail.Direction = self.view.Direction
        detail.XDirection = self.view.XDirection
        self.page.addView(detail)
        CivilCvCAD.ActiveDocument.recompute()
        print("DrawViewDetail test: Detail created")

        #wait for threads to complete before checking result
        loop = QtCore.QEventLoop()

        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)

        timer.start(2000)   #2 second delay
        loop.exec_()

        edges = detail.getVisibleEdges()

        self.assertEqual(len(edges), 4, "DrawViewDetail has wrong number of edges")
        self.assertTrue("Up-to-date" in detail.State, "DrawViewDetail is not Up-to-date")

if __name__ == "__main__":
    unittest.main()
