# CivilCvCAD focused review — 2026-09-14

## Fixed

- BIM schema import indexed a list directly with the IFC preference. Missing
  preferences raised TypeError, out-of-range values raised IndexError, and
  negative values silently selected the wrong schema. Invalid values now use
  IFC4; valid IFC4/IFC2X3 selections are preserved.
- The desktop shortcut referenced an icon in a separate downloaded source
  folder. It now uses the icon stored in the installed application's icons folder.
- Embedded the existing CivilCvCAD logo icon in the Windows executable and
  self-extracting package, and included the logo PNG and ICO in the package.
- The package includes the previously repaired BIM, Help, OpenSCAD and Tux
  binary Qt bundles. The installed resource checker passes all five bundles.

## Validation

- Regression test loads the real IFC JSON files for eight preference cases:
  0, 1, None, -1, 2, 999, a string and a boolean.
- Bundled Python successfully creates a solid, checks validity and volume,
  recomputes, saves FCStd, closes, reopens and verifies the persisted volume.
- Staged release passes Qt resource registration with its own Python runtime.

## Distribution and limits

This is a repaired/repackaged 26.3.0 binary distribution, not a full C++ rebuild.
The dated EXE is a self-extracting portable archive: extract it, then run
CivilCvCAD/bin/CivilCvCAD.exe. It does not automatically launch or clean up.
The existing GitHub release asset is retained as a legacy package.
No further desktop control was used after the user requested code-only review.
This focused review does not certify all workbenches or interactive workflows.
Original installed EXE, BIM Python module and shortcut are backed up under
.codex_tmp/backup-20260914 in the working source folder.
