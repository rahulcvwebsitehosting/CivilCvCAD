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

#include "CreditsDialog.h"

#include <QCheckBox>
#include <QDesktopServices>
#include <QDialogButtonBox>
#include <QFrame>
#include <QGridLayout>
#include <QLabel>
#include <QUrl>
#include <QVBoxLayout>

#include <App/Application.h>

using namespace StartGui;

CreditsDialog::CreditsDialog(QWidget* parent)
    : QDialog(parent)
{
    setObjectName(QStringLiteral("CreditsDialog"));
    setWindowTitle(tr("Credits"));
    setModal(true);
    setMinimumSize(480, 500);

    // Use native dialog styling - no custom theming
    // to blend with the application's standard Qt style

    auto* mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(24, 24, 24, 24);
    mainLayout->setSpacing(16);

    // Header: simple title
    auto* titleLabel = new QLabel(QStringLiteral("CivilCvCAD"), this);
    titleLabel->setAlignment(Qt::AlignCenter);
    QFont titleFont = titleLabel->font();
    titleFont.setPointSize(20);
    titleFont.setWeight(QFont::Bold);
    titleLabel->setFont(titleFont);
    mainLayout->addWidget(titleLabel);

    auto* subtitleLabel = new QLabel(tr("Credits & Connections"), this);
    subtitleLabel->setAlignment(Qt::AlignCenter);
    QFont subtitleFont = subtitleLabel->font();
    subtitleFont.setPointSize(10);
    subtitleFont.setWeight(QFont::Medium);
    subtitleLabel->setFont(subtitleFont);
    subtitleLabel->setStyleSheet("color: palette(mid);");
    mainLayout->addWidget(subtitleLabel);

    // Separator line
    auto* separator = new QFrame(this);
    separator->setFrameShape(QFrame::HLine);
    separator->setFrameShadow(QFrame::Sunken);
    mainLayout->addWidget(separator);

    // Credits body
    auto* bodyLabel = new QLabel(
        tr("<p>CivilCvCAD is designed, engineered and built by:</p>"
           "<p style=\"font-size:15px; font-weight:600;\">Rahul Shyam</p>"
           "<p>Civil engineer who codes. Built AI apps, browser games, client sites, "
           "and construction tools - 40+ projects live on Vercel.<br/>"
           "B.E. Civil Engineering, ESEC Chennai.</p>"),
        this);
    bodyLabel->setWordWrap(true);
    bodyLabel->setTextFormat(Qt::RichText);
    bodyLabel->setOpenExternalLinks(false);
    mainLayout->addWidget(bodyLabel);

    // Socials section
    auto* socialTitle = new QLabel(tr("Connect with the Creator"), this);
    socialTitle->setAlignment(Qt::AlignCenter);
    QFont socialTitleFont = socialTitle->font();
    socialTitleFont.setPointSize(11);
    socialTitleFont.setWeight(QFont::Bold);
    socialTitle->setFont(socialTitleFont);
    mainLayout->addWidget(socialTitle);

    auto* socialFrame = new QFrame(this);
    socialFrame->setFrameShape(QFrame::StyledPanel);
    auto* socialLayout = new QVBoxLayout(socialFrame);
    socialLayout->setContentsMargins(16, 12, 16, 12);
    socialLayout->setSpacing(8);

    auto* socialGrid = new QGridLayout();
    socialGrid->setHorizontalSpacing(24);
    socialGrid->setVerticalSpacing(6);

    struct Social
    {
        const char* name;
        const char* url;
    };
    static const Social socials[] = {
        {"GitHub", "https://github.com/rahulcvwebsitehosting"},
        {"LinkedIn", "https://www.linkedin.com/in/rahulshyamcivil"},
        {"X (Twitter)", "https://x.com/RahulShyamCV"},
        {"Threads", "https://www.threads.net/@RahulCvJPS"},
        {"Instagram", "https://www.instagram.com/rahulcvjps"},
        {"WhatsApp", "https://wa.me/+919487276632"},
        {"Portfolio", "https://rahulshyam-portfolio.vercel.app"},
        {"Email", "mailto:rahulcvfiitjee@gmail.com"},
    };

    int row = 0;
    int col = 0;
    for (const auto& social : socials) {
        auto* linkLabel = new QLabel(socialFrame);
        linkLabel->setCursor(Qt::PointingHandCursor);
        linkLabel->setTextFormat(Qt::RichText);
        linkLabel->setOpenExternalLinks(false);
        QString name = QString::fromUtf8(social.name);
        linkLabel->setText(
            QStringLiteral("<a href=\"%1\" style=\"color: palette(link); text-decoration: none;\">%2</a>").arg(QLatin1String(social.url), name)
        );
        linkLabel->setStyleSheet("font-size: 13px; padding: 2px 0;");
        connect(linkLabel, &QLabel::linkActivated, this, [this](const QString& url) {
            openUrl(url);
        });
        socialGrid->addWidget(linkLabel, row, col, Qt::AlignLeft);
        ++row;
        if (row == 4) {
            row = 0;
            ++col;
        }
    }
    socialLayout->addLayout(socialGrid);
    mainLayout->addWidget(socialFrame);

    // Don't show again
    _dontShowAgainCheckBox = new QCheckBox(
        tr("Don't show this credits popup again on startup"), this);
    auto hGrp = App::GetApplication().GetParameterGroupByPath(
        "User parameter:BaseApp/Preferences/Mod/Start");
    _dontShowAgainCheckBox->setChecked(hGrp->GetBool("CreditsDontShowAgain", false));
    connect(_dontShowAgainCheckBox, &QCheckBox::toggled, this, [hGrp](bool checked) {
        hGrp->SetBool("CreditsDontShowAgain", checked);
    });
    mainLayout->addWidget(_dontShowAgainCheckBox);

    // Close button
    auto* buttonBox = new QDialogButtonBox(QDialogButtonBox::Close, this);
    buttonBox->button(QDialogButtonBox::Close)->setText(tr("Done"));
    connect(buttonBox, &QDialogButtonBox::rejected, this, &QDialog::reject);
    mainLayout->addWidget(buttonBox);
}

bool CreditsDialog::dontShowAgain() const
{
    return _dontShowAgainCheckBox ? _dontShowAgainCheckBox->isChecked() : false;
}

void CreditsDialog::showIfEnabled(QWidget* parent)
{
    auto hGrp = App::GetApplication().GetParameterGroupByPath(
        "User parameter:BaseApp/Preferences/Mod/Start");
    if (hGrp->GetBool("CreditsDontShowAgain", false)) {
        return;
    }
    CreditsDialog dialog(parent);
    dialog.exec();
}

void CreditsDialog::openUrl(const QString& url)
{
    QDesktopServices::openUrl(QUrl(url));
}
