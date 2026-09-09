# Desktop demo repair — 2026-09-09

Tested the installed CivilCvCAD 26.3.0dev on Windows using desktop control
before changing files. This is a focused smoke test, not a full CAD audit.

## Confirmed demo blocker

The Start page's BIM/Architecture action failed with:
`list indices must be integers or slices, not NoneType`.
The report traceback ended at `ArchIFCSchema.py`, where the missing
`IfcVersion` preference was used as a list index. The BIM start icon was
also missing.

The installed `Mod/BIM/Arch_rc.rcc` contained generated C++ text, not an RCC
binary. Qt rejected it, leaving the BIM preference forms unavailable.
Help, OpenSCAD and Tux had the same invalid bundle format. Draft's bundle
was valid and was preserved.

## Repair applied

- Regenerated the four invalid bundles from this source tree using the
  locally installed FreeCAD 1.1 Qt 6.8.3 resource compiler with `--binary`.
- Validated registration with CivilCvCAD's own PySide6 runtime before copying
  them to `C:/Users/saini/AppData/Local/Programs/CivilCvCAD/Mod`.
- Preserved each original beside the repaired file with suffix
  `.pre-repair-20260909`.
- Added a CMake generation check for the binary `qres` signature. The source
  already requested `--binary` and checked registration in generated loaders;
  the new check catches this failure during the build.
- Added `tools/check_qt_resources.py` for read-only checks of packaged bundles
  and documented its use in `OFFLINE_BUILD.md`.

The standalone installer was not rebuilt. Redistributing an older installer
will not include this local repair; regenerate/repackage its resources first.

## Verification

- Installed BIM/Architecture opened with its icon and toolbars restored.
- Created a wall through the 3D/BIM menu and viewport, without a traceback.
- Saved, closed, and reopened `.codex_tmp/resource-repair/BIM-smoke.FCStd`.
  The wall remained visible and the Report View was empty.
- All five installed binary resource bundles passed the package checker.
- The original broken BIM bundle failed both the package checker and the
  extracted CMake generation script; the regenerated bundle passed both.

Help/OpenSCAD/Tux resource registration was checked, but their full workflows
were not tested. No full C++ rebuild was performed. Existing document recovery
data was not cleaned up. Cosmetic changes and new features were excluded.
