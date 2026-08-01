// SPDX-License-Identifier: LGPL-2.1-or-later

#pragma once

#include <QDesktopServices>
#include <QDir>
#include <QUrl>

namespace Gui::OfflinePolicy
{

inline bool openLocalUrl(const QUrl& url)
{
    if (url.isLocalFile()) {
        return QDesktopServices::openUrl(url);
    }
    if (url.scheme().isEmpty()) {
        return QDesktopServices::openUrl(QUrl::fromLocalFile(QDir::current().absoluteFilePath(url.toString())));
    }
    return false;
}

}  // namespace Gui::OfflinePolicy
