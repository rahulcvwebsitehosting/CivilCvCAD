import CivilCvCAD
import unittest
from .TechDrawTestUtilities import createPageWithSVGTemplate


class DrawProjectionGroupTest(unittest.TestCase):
    def setUp(self):
        """Creates a box and sphere to make a fusions from them.
        Then creates a page and projection group"""
        CivilCvCAD.newDocument("TDGroup")
        CivilCvCAD.setActiveDocument("TDGroup")
        CivilCvCAD.ActiveDocument = CivilCvCAD.getDocument("TDGroup")
        self.document = CivilCvCAD.ActiveDocument
        print("document created")

        # make Fusion feature
        box = CivilCvCAD.ActiveDocument.addObject("Part::Box", "Box")
        box.recompute()
        print("box created")
        sphere = CivilCvCAD.ActiveDocument.addObject("Part::Sphere", "Sphere")
        sphere.recompute()
        print("sphere created")
        self.fusion = CivilCvCAD.ActiveDocument.addObject("Part::MultiFuse", "Fusion")
        CivilCvCAD.ActiveDocument.Fusion.Shapes = [box, sphere]
        self.fusion.recompute()
        print("Fusion created")

        # make a page
        print("making a page")
        self.page = createPageWithSVGTemplate()
        print("Page created")

    def tearDown(self):
        CivilCvCAD.closeDocument("TDGroup")

    def testMakeProjectionGroup(self):
        """Tests if a projection group can be added to view1"""
        # make projection group
        print("making a projection group")
        self.document.openTransaction("Create Proj Group")
        groupName = "ProjGroup"
        group = CivilCvCAD.ActiveDocument.addObject("TechDraw::DrawProjGroup", groupName)
        self.page.addView(group)
        print("Group created")
        group.Source = [self.fusion]

        print("adding views")
        group.addProjection("Front")  # need an Anchor
        print("added Front")

        # update group
        anchorDir = CivilCvCAD.Vector(0.0, 0.0, 1.0)
        anchorRot = CivilCvCAD.Vector(1.0, 0.0, 0.0)
        group.Anchor.Direction = anchorDir
        group.Anchor.RotationVector = anchorRot
        print("Anchor values set")
        group.Anchor.recompute()
        self.document.commitTransaction()
        print("Front/Anchor recomputed")
        group.addProjection("Left")
        print("added Left")
        group.addProjection("Top")
        print("added Top")
        group.addProjection("Right")
        print("added Right")
        group.addProjection("Rear")
        print("added Rear")
        group.addProjection("Bottom")
        print("added Bottom")

        # remove a view from projection group
        group.removeProjection("Left")
        print("removed Left")

        # test getItemByLabel method
        print("testing getItemByLabel")
        label = "Top"
        item = group.getItemByLabel(label)
        print("Item Label: " + label + " Item Name: " + item.Name)

        print("recomputing document")
        CivilCvCAD.ActiveDocument.recompute()

        for v in group.Views:
            print("View: " + v.Label + " " + v.TypeId)
            v.autoPosition()

        group.recompute()

        self.assertTrue("Up-to-date" in group.State)


if __name__ == "__main__":
    unittest.main()
