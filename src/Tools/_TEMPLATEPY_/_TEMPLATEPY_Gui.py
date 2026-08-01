# SPDX-License-Identifier: LGPL-2.1-or-later

# CivilCvCAD tools of the _TEMPLATEPY_ workbench
# (c) 2001 Juergen Riegel
# License LGPL

import CivilCvCAD, CivilCvCADGui


class CmdHelloWorld:
    def Activated(self):
        CivilCvCAD.Console.PrintMessage("Hello, World!\n")

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            "Pixmap": "civilcvcad",
            "MenuText": "Hello World",
            "ToolTip": "Print Hello World",
        }


CivilCvCADGui.addCommand("_TEMPLATEPY__HelloWorld", CmdHelloWorld())
