import CivilCvCAD
import unittest
from .TechDrawTestUtilities import createPageWithSVGTemplate
from PySide import QtCore

class DrawViewSectionTest(unittest.TestCase):
    def setUp(self):
        """Creates a page and a view"""
        CivilCvCAD.newDocument("TDSection")
        CivilCvCAD.setActiveDocument("TDSection")
        CivilCvCAD.ActiveDocument = CivilCvCAD.getDocument("TDSection")

        self.box = CivilCvCAD.ActiveDocument.addObject("Part::Box", "Box")

        self.page = createPageWithSVGTemplate()
        self.page.Scale = 5.0
        # page.ViewObject.show()    # unit tests run in console mode
        print("DrawViewSection test: page created")

        self.view = CivilCvCAD.ActiveDocument.addObject("TechDraw::DrawViewPart", "View")
        self.page.addView(self.view)
        self.view.Source = [self.box]
        self.view.Direction = (0.0, 0.0, 1.0)
        self.view.Rotation = 0.0
        self.view.X = 30.0
        self.view.Y = 150.0
        CivilCvCAD.ActiveDocument.recompute()

        #wait for threads to complete before checking result
        loop = QtCore.QEventLoop()

        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)

        timer.start(2000)   #2 second delay
        loop.exec_()

        print("DrawViewSection test: view created")

    def tearDown(self):
        print("DrawViewSection test: finished")
        CivilCvCAD.closeDocument("TDSection")

    def testMakeDrawViewSection(self):
        """Tests if a DrawViewSection can be added to page"""
        section = CivilCvCAD.ActiveDocument.addObject(
            "TechDraw::DrawViewSection", "Section"
        )
        self.page.addView(section)
        section.Source = [self.box]
        section.BaseView = self.view
        section.Direction = (0.0, 1.0, 0.0)
        section.SectionNormal = (0.0, 1.0, 0.0)
        section.SectionOrigin = (5.0, 5.0, 5.0)
        print("DrawViewSection test: section created")
        CivilCvCAD.ActiveDocument.recompute()

        #wait for threads to complete before checking result
        loop = QtCore.QEventLoop()

        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)

        timer.start(2000)   #2 second delay
        loop.exec_()

        edges = section.getVisibleEdges()
        self.assertEqual(len(edges), 4, "DrawViewSection has wrong number of edges")
        self.assertTrue("Up-to-date" in section.State)


if __name__ == "__main__":
    unittest.main()
