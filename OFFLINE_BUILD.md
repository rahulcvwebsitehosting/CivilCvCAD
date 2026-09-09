# Building CivilCvCAD

CivilCvCAD is permanently configured as an offline-only application.

The build system forces `BUILD_ADDONMGR=OFF` and `BUILD_WEB=OFF`. All C and C++
targets receive `CIVILCVCAD_OFFLINE_ONLY=1`; this setting is not exposed as a
supported opt-out.

Dependencies must be installed from local package caches, local SDKs, or other
approved offline media before configuring the build. A normal CMake build is:

```text
cmake -S . -B build
cmake --build build
```

Package-manager lock files may contain origin metadata used to identify
dependencies. They are build provenance, not application runtime endpoints.

## Check the packaged Windows application

Before distributing a binary-resource build, run with its bundled Python:

```text
<install>/bin/python.exe tools/check_qt_resources.py <install>
```

The check rejects C++ output accidentally saved as `.rcc`, and verifies that
the shipped Qt runtime can register each bundle. Such a broken BIM bundle
causes the Architecture start action to fail while loading `IfcVersion`.
Regenerate affected bundles from their `src/Mod/<module>/Resources/*.qrc`
files with a compatible Qt `rcc --binary`, then repackage. Renaming C++ output
to `.rcc` does not create a binary resource.

Also smoke-test the installed application: open BIM/Architecture, create a
wall, save the document, close it, and reopen it. A successful compile alone
does not verify the installed resource files.
