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
#include <QPainter>
#include <QPixmap>
#include <QPushButton>
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
    setMinimumSize(460, 520);
    setAutoFillBackground(true);

    // Blueprint-style grid background
    QPixmap grid(48, 48);
    grid.fill(QColor(QStringLiteral("#0E1F38")));
    QPainter painter(&grid);
    painter.setPen(QPen(QColor(QStringLiteral("#1E3A5F")), 1));
    painter.drawLine(0, 0, 48, 0);
    painter.drawLine(0, 0, 0, 48);
    painter.end();
    QPalette palette = this->palette();
    palette.setBrush(QPalette::Window, QBrush(grid));
    setPalette(palette);

    // Blueprint theme stylesheet
    setStyleSheet(QStringLiteral(
        "#CreditsDialog { border: 2px solid #F5A623; }"
        "#HeaderFrame { border: 2px solid #F5A623; border-radius: 4px; background-color: rgba(14, 31, 56, 200); }"
        "#TitleLabel { color: #F5A623; font-size: 22px; font-weight: 800; letter-spacing: 3px; }"
        "#SubtitleLabel { color: #8FA8C8; font-size: 11px; font-weight: 600; letter-spacing: 2px; }"
        "#BodyLabel { color: #D8E4F2; font-size: 13px; }"
        "#BodyLabel a { color: #F5A623; text-decoration: none; font-weight: 700; }"
        "#SocialFrame { border: 1px solid #2C4A73; border-radius: 4px; background-color: rgba(14, 31, 56, 220); }"
        "#SocialTitle { color: #F5A623; font-size: 13px; font-weight: 700; letter-spacing: 2px; }"
        "#SocialLink { color: #D8E4F2; font-size: 13px; font-weight: 700; }"
        "#SocialLink a { color: #F5A623; text-decoration: none; }"
        "#SocialLink:hover { color: #FFFFFF; }"
        "#DontShowAgain { color: #8FA8C8; font-size: 12px; }"
        "QPushButton { background-color: #F5A623; color: #0E1F38; border: none; border-radius: 4px;"
        "  padding: 8px 22px; font-weight: 800; letter-spacing: 1px; }"
        "QPushButton:hover { background-color: #FFC14D; }"
        "QPushButton:pressed { background-color: #D98F1C; }"
    ));

    auto* mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(20, 20, 20, 20);
    mainLayout->setSpacing(14);

    // Header: engineering title block
    auto* headerFrame = new QFrame(this);
    headerFrame->setObjectName(QStringLiteral("HeaderFrame"));
    auto* headerLayout = new QVBoxLayout(headerFrame);
    headerLayout->setContentsMargins(16, 12, 16, 12);
    headerLayout->setSpacing(2);

    auto* titleLabel = new QLabel(QStringLiteral("CIVILCVCAD"), headerFrame);
    titleLabel->setObjectName(QStringLiteral("TitleLabel"));
    titleLabel->setAlignment(Qt::AlignCenter);
    headerLayout->addWidget(titleLabel);

    auto* subtitleLabel = new QLabel(tr("CREDITS & CONNECTIONS"), headerFrame);
    subtitleLabel->setObjectName(QStringLiteral("SubtitleLabel"));
    subtitleLabel->setAlignment(Qt::AlignCenter);
    headerLayout->addWidget(subtitleLabel);

    mainLayout->addWidget(headerFrame);

    // Credits body
    auto* bodyLabel = new QLabel(
        tr("<p>CivilCvCAD is designed, engineered and built by:</p>"
           "<p style=\"color:#FFFFFF; font-size:16px; font-weight:700;\">Rahul Shyam</p>"
           "<p>Civil engineer who codes. Built AI apps, browser games, client sites, "
           "and construction tools - 40+ projects live on Vercel.<br/>"
           "B.E. Civil Engineering, ESEC Chennai.</p>"),
        this);
    bodyLabel->setObjectName(QStringLiteral("BodyLabel"));
    bodyLabel->setWordWrap(true);
    bodyLabel->setTextFormat(Qt::RichText);
    bodyLabel->setOpenExternalLinks(false);
    mainLayout->addWidget(bodyLabel);

    // Socials
    auto* socialFrame = new QFrame(this);
    socialFrame->setObjectName(QStringLiteral("SocialFrame"));
    auto* socialLayout = new QVBoxLayout(socialFrame);
    socialLayout->setContentsMargins(16, 12, 16, 12);
    socialLayout->setSpacing(8);

    auto* socialTitle = new QLabel(tr("CONNECT WITH THE CREATOR"), socialFrame);
    socialTitle->setObjectName(QStringLiteral("SocialTitle"));
    socialTitle->setAlignment(Qt::AlignCenter);
    socialLayout->addWidget(socialTitle);

    auto* socialGrid = new QGridLayout();
    socialGrid->setHorizontalSpacing(24);
    socialGrid->setVerticalSpacing(4);

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
        linkLabel->setObjectName(QStringLiteral("SocialLink"));
        linkLabel->setCursor(Qt::PointingHandCursor);
        linkLabel->setTextFormat(Qt::RichText);
        linkLabel->setOpenExternalLinks(false);
        QString name = QString::fromUtf8(social.name);
        linkLabel->setText(
            QStringLiteral("<a href=\"%1\">&#9656; %2</a>").arg(QLatin1String(social.url), name)
        );
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
    _dontShowAgainCheckBox->setObjectName(QStringLiteral("DontShowAgain"));
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
