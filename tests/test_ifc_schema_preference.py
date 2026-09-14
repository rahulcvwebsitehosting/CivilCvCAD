"""Headless regression coverage for BIM schema preference recovery."""
import runpy
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class SchemaPreferenceTests(unittest.TestCase):
    def test_schema_selection_and_invalid_preferences(self):
        for value, expected in [(0, "IFC4"), (1, "IFC2X3"), (None, "IFC4"),
                                (-1, "IFC4"), (2, "IFC4"), (999, "IFC4"),
                                ("1", "IFC4"), (True, "IFC4")]:
            with self.subTest(value=value):
                app = types.ModuleType("CivilCvCAD")
                app.getResourceDir = lambda: str(ROOT / "src")
                draft = types.ModuleType("draftutils")
                draft.params = types.SimpleNamespace(get_param_arch=lambda key: value)
                with patch.dict(sys.modules, CivilCvCAD=app, draftutils=draft):
                    result = runpy.run_path(str(ROOT / "src/Mod/BIM/ArchIFCSchema.py"))
                self.assertEqual(result["IfcVersion"], expected)
                for key in ("IfcContexts", "IfcProducts", "IfcTypes"):
                    self.assertTrue(result[key])


if __name__ == "__main__":
    unittest.main()
