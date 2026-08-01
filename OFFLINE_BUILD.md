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
