# SPDX-License-Identifier: LGPL-2.1-or-later

"""Shared offline-only policy helpers for CivilCvCAD Python modules."""

from __future__ import annotations

import os


class OfflineOnlyError(PermissionError):
    """Raised when a removed network feature is invoked."""


def reject_network(feature: str = "Network access"):
    """Reject a network-backed operation with a consistent error."""

    raise OfflineOnlyError(f"{feature} is disabled in this offline-only CivilCvCAD build")


def open_local_url(value) -> bool:
    """Open a local file or directory and reject every other URL scheme."""

    from PySide import QtCore, QtGui

    url = value if isinstance(value, QtCore.QUrl) else QtCore.QUrl(str(value))
    if url.isLocalFile():
        return bool(QtGui.QDesktopServices.openUrl(url))
    if not url.scheme():
        return bool(
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(os.path.abspath(url.toString())))
        )
    return False
