# SPDX-License-Identifier: LGPL-2.1-or-later

import CivilCvCAD
import CivilCvCADGui

QT_TRANSLATE_NOOP = CivilCvCAD.Qt.QT_TRANSLATE_NOOP
translate = CivilCvCAD.Qt.translate


class BIM_LinkMake:
    def GetResources(self):
        return {
            "Pixmap": "Link",
            "MenuText": QT_TRANSLATE_NOOP("BIM_LinkMake", "Make Link"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "BIM_LinkMake",
                "Creates a Link to the selected object and immediately enables moving it",
            ),
            "Accel": "L, K",
        }

    def IsActive(self):
        return not CivilCvCAD.ActiveDocument is None

    def Activated(self):
        from draftutils.todo import ToDo

        sel = CivilCvCADGui.Selection.getSelection()
        if not sel:
            CivilCvCAD.Console.PrintError(translate("BIM", "Select an object to link") + "\n")
            return

        doc = CivilCvCAD.ActiveDocument
        doc.openTransaction("Create BIM Link")

        new_links = []

        try:
            for obj in sel:
                # Create the native Link
                lnk = doc.addObject("App::Link", obj.Label + "_Link")
                lnk.LinkedObject = obj

                # We do not manipulate LinkCopyOnChange here.
                # The 'appLinkExecute' hook in the object's proxy will handle the injection of
                # shadow properties (like Hosts) to ensure the link remains lightweight.

                new_links.append(lnk)

            doc.commitTransaction()
            doc.recompute()

            # Enter Move mode
            if new_links:
                CivilCvCADGui.Selection.clearSelection()
                for lnk in new_links:
                    CivilCvCADGui.Selection.addSelection(lnk)

                # Defer the Move command to ensure the document is stable
                ToDo.delay(CivilCvCADGui.runCommand, "Draft_Move")

        except Exception as e:
            CivilCvCAD.Console.PrintError(f"BIM Link creation failed: {e}\n")
            doc.abortTransaction()


CivilCvCADGui.addCommand("BIM_LinkMake", BIM_LinkMake())
