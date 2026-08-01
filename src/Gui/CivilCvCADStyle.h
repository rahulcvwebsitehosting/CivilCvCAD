// SPDX-License-Identifier: LGPL-2.1-or-later
/****************************************************************************
 *                                                                          *
 *   Copyright (c) 2025 Kacper Donat <kacper@kadet.net>                     *
 *                                                                          *
 *   This file is part of CivilCvCAD.                                          *
 *                                                                          *
 *   CivilCvCAD is free software: you can redistribute it and/or modify it     *
 *   under the terms of the GNU Lesser General Public License as            *
 *   published by the Free Software Foundation, either version 2.1 of the   *
 *   License, or (at your option) any later version.                        *
 *                                                                          *
 *   CivilCvCAD is distributed in the hope that it will be useful, but         *
 *   WITHOUT ANY WARRANTY; without even the implied warranty of             *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU       *
 *   Lesser General Public License for more details.                        *
 *                                                                          *
 *   You should have received a copy of the GNU Lesser General Public       *
 *   License along with CivilCvCAD. If not, see                                *
 *   <https://www.gnu.org/licenses/>.                                       *
 *                                                                          *
 ***************************************************************************/

#pragma once

#include <FCGlobal.h>
#include <QProxyStyle>
#include <QEvent>
#include <QPushButton>

namespace Gui
{

class GuiExport CivilCvCADStyle: public QProxyStyle
{
    Q_OBJECT

public:
    CivilCvCADStyle()
        : QProxyStyle(QStringLiteral("Fusion"))
    {}

protected:
    bool eventFilter(QObject* obj, QEvent* event) override;
};

}  // namespace Gui
