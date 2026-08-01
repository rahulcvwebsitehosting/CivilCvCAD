# CivilCvCAD

CivilCvCAD is a desktop parametric CAD application configured for offline-only
operation. It supports local modeling, drafting, BIM, CAM, technical drawings,
file import/export, macros, and other installed workbenches without providing
web-backed application features.

## Offline-only behavior

- Addon Manager and the Web workbench are excluded from every build.
- Website, forum, donation, issue-reporting, and online-documentation commands
  are not registered in the application.
- Qt download paths are blocked and Qt networking is routed only to an unused
  loopback endpoint as defense in depth.
- Internet sockets and network name resolution are denied in the embedded
  Python runtime.
- Help resolves only local Markdown or HTML files.
- URL widgets open only local files and directories.
- Remote debugging and automatic dependency downloads are not packaged.

The application is designed to operate with locally installed dependencies and
locally stored documentation. See `OFFLINE_BUILD.md` and `OFFLINE_MODE.md`.

## Licensing

CivilCvCAD is a modified distribution of LGPL-covered and third-party software.
The complete license is in `LICENSE`; original author and contributor notices
remain in source headers and `src/Doc/CONTRIBUTORS`. See `NOTICE` for the
modification and attribution statement.
