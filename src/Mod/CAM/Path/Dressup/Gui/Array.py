# SPDX-License-Identifier: LGPL-2.1-or-later

import CivilCvCAD
import CivilCvCADGui
import Path
import Path.Dressup.Array as DressupArray
import Path.Dressup.Utils as PathDressup

from PySide.QtCore import QT_TRANSLATE_NOOP

translate = CivilCvCAD.Qt.translate


class DressupArrayViewProvider(object):
    def __init__(self, vobj):
        self.attach(vobj)

    def dumps(self):
        return None

    def loads(self, state):
        return None

    def attach(self, vobj):
        self.vobj = vobj
        self.obj = vobj.Object
        self.panel = None

    def claimChildren(self):
        return [self.obj.Base]

    def onDelete(self, vobj, args=None):
        if vobj.Object and vobj.Object.Proxy:
            vobj.Object.Proxy.onDelete(vobj.Object, args)
        return True

    def setEdit(self, vobj, mode=0):
        return True

    def unsetEdit(self, vobj, mode=0):
        pass

    def setupTaskPanel(self, panel):
        pass

    def clearTaskPanel(self):
        pass

    def getIcon(self):
        if getattr(PathDressup.baseOp(self.obj), "Active", True):
            return ":/icons/CAM_Dressup.svg"
        else:
            return ":/icons/CAM_OpActive.svg"


class CommandPathDressupArray:
    def GetResources(self):
        return {
            "Pixmap": "CAM_Dressup",
            "MenuText": QT_TRANSLATE_NOOP("CAM_DressupArray", "Array"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "CAM_DressupArray",
                "Creates an array from a selected toolpath",
            ),
        }

    def IsActive(self):
        return bool(PathDressup.selection())

    def Activated(self):
        # check that the selection contains exactly what we want
        op = PathDressup.selection(verbose=True)
        if not op:
            return

        # everything ok!
        CivilCvCAD.ActiveDocument.openTransaction("Create Path Array Dress-up")
        CivilCvCADGui.addModule("Path.Dressup.Gui.Array")
        CivilCvCADGui.doCommand(f"base = CivilCvCAD.ActiveDocument.getObject('{op.Name}')")
        CivilCvCADGui.doCommand("Path.Dressup.Gui.Array.Create(base)")
        # CivilCvCAD.ActiveDocument.commitTransaction()  # Final `commitTransaction()` called via TaskPanel.accept()
        CivilCvCAD.ActiveDocument.recompute()


def Create(base, name="DressupPathArray"):
    CivilCvCAD.ActiveDocument.openTransaction("Create an Array dressup")
    obj = DressupArray.Create(base, name)
    obj.ViewObject.Proxy = DressupArrayViewProvider(obj.ViewObject)
    obj.Base.ViewObject.Visibility = False
    CivilCvCAD.ActiveDocument.commitTransaction()
    return obj


if CivilCvCAD.GuiUp:
    # register the CivilCvCAD command
    CivilCvCADGui.addCommand("CAM_DressupArray", CommandPathDressupArray())
