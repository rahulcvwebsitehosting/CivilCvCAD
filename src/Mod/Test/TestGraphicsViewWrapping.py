# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2026 FreeCAD contributors
# SPDX-FileNotice: Part of the CivilCvCAD project.

"""GUI regression tests for wrapping 3D views as PySide widgets.

To run tests:
    CivilCvCAD -t TestGraphicsViewWrapping.TestGraphicsViewWrapping
"""

import unittest

import CivilCvCAD
import CivilCvCADGui
from PySide6 import QtWidgets


class TestGraphicsViewWrapping(unittest.TestCase):
    def setUp(self):
        self.doc = CivilCvCAD.newDocument("TestGraphicsViewWrapping")
        CivilCvCADGui.ActiveDocument = CivilCvCADGui.getDocument(self.doc.Name)

    def tearDown(self):
        CivilCvCAD.closeDocument(self.doc.Name)

    def test_active_view_wraps_as_qgraphics_view(self):
        view = CivilCvCADGui.ActiveDocument.ActiveView

        # graphicsView() wraps a C++ QGraphicsView through Shiboken. Some
        # Shiboken builds do not resolve Qt widget RTTI names, so this used to
        # raise "RuntimeError: Failed to wrap widget" instead of falling back to
        # PySide's public type names.
        graphics_view = view.graphicsView()

        self.assertIsInstance(graphics_view, QtWidgets.QGraphicsView)
        self.assertIsNotNone(graphics_view.viewport())
