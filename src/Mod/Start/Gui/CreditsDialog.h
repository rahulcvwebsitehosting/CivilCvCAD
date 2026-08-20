// SPDX-License-Identifier: LGPL-2.1-or-later
/****************************************************************************
 *                                                                          *
 *   Copyright (c) 2026 Rahul Shyam                                          *
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

#include <QDialog>

class QCheckBox;
class QWidget;

namespace StartGui
{

/**
 * Civil-engineering themed credits dialog showing the application creator
 * and clickable social media links. Supports a "don't show again" checkbox
 * persisted in the application parameter tree.
 */
class CreditsDialog: public QDialog
{
    Q_OBJECT

public:
    explicit CreditsDialog(QWidget* parent = nullptr);

    /** Whether the user asked not to see this dialog again on startup. */
    bool dontShowAgain() const;

    /** Static helper: show the dialog unless the user has disabled it. */
    static void showIfEnabled(QWidget* parent);

private:
    void addSocialRow(const QString& label, const QString& url);
    void openUrl(const QString& url);

    QCheckBox* _dontShowAgainCheckBox = nullptr;
};

}  // namespace StartGui
