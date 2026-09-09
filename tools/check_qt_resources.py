"""Check packaged Qt bundles using the application's Python/Qt runtime.

Usage: <install>/bin/python.exe tools/check_qt_resources.py <install>
This check is read-only and does not start the CAD application.
"""

import argparse
from pathlib import Path

from PySide6.QtCore import QResource


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("install", type=Path)
    args = parser.parse_args()
    bundles = sorted((args.install / "Mod").glob("**/*_rc.rcc"))
    if not bundles:
        parser.error("No binary Qt resource bundles found under <install>/Mod")

    failures = 0
    for bundle in bundles:
        with bundle.open("rb") as stream:
            is_binary = stream.read(4) == b"qres"
        # Isolate bundles so duplicate resource paths cannot hide a bad bundle.
        path = str(bundle.resolve())
        prefix = "/civilcvcad_resource_check"
        registered = is_binary and QResource.registerResource(path, prefix)
        if registered:
            QResource.unregisterResource(path, prefix)
            print(f"PASS {bundle.relative_to(args.install)}")
        else:
            failures += 1
            print(f"FAIL {bundle.relative_to(args.install)}: invalid Qt binary resource")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
