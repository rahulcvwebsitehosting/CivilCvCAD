/*
CivilCvCAD Installer Language File
Language: Turkish
*/

!insertmacro LANGFILE_EXT "Turkish"

${LangFileString} TEXT_INSTALL_CURRENTUSER "(Installed for Current User)"

${LangFileString} TEXT_WELCOME "Bu sihirbaz size CivilCvCAD programını kuracak.$\r$\n\
				$\r$\n\
				$_CLICK"

#${LangFileString} TEXT_CONFIGURE_PYTHON "Compiling Python scripts..."

${LangFileString} TEXT_FINISH_DESKTOP "Create desktop shortcut"

#${LangFileString} FileTypeTitle "CivilCvCAD-Document"

#${LangFileString} SecAllUsersTitle "Tüm kullanıcılar için kur?"
${LangFileString} SecFileAssocTitle "Dosya eşleşmeleri"
${LangFileString} SecDesktopTitle "Masaüstü ikonu"

${LangFileString} SecCoreDescription "CivilCvCAD dosyaları."
#${LangFileString} SecAllUsersDescription "CivilCvCAD tüm kullanıcılar için mi yoksa yalnızca bu kullanıcıya mı kurulacak."
${LangFileString} SecFileAssocDescription "Uzantısı .FCStd olan dosyalar otomatik olarak CivilCvCAD ile açılsın."
${LangFileString} SecDesktopDescription "Masaüstüne bir CivilCvCAD ikonu koy."
#${LangFileString} SecDictionaries "Sözlükleri"
#${LangFileString} SecDictionariesDescription "Spell-checker dictionaries that can be downloaded and installed."

#${LangFileString} PathName 'Path to the file $\"xxx.exe$\"'
#${LangFileString} InvalidFolder '$\"xxx.exe$\" dosyası belirttiğiniz dizinde bulunamadı.'

#${LangFileString} DictionariesFailed 'Download of dictionary for language $\"$R3$\" failed.'

#${LangFileString} ConfigInfo "Sıradaki CivilCvCAD yapılandırması biraz zaman alacak."

#${LangFileString} RunConfigureFailed "Yapılandırma programı çalıştırılamadı"
${LangFileString} InstallRunning "Kurulum programı zaten çalışıyor!"
${LangFileString} AlreadyInstalled "CivilCvCAD ${APP_SERIES_KEY2} kurulu zaten!$\r$\n\
				Dou you nevertheles want to install CivilCvCAD over the existing version?"
${LangFileString} NewerInstalled "You are trying to install an older version of CivilCvCAD than what you have installed.$\r$\n\
				  If you really want this, you must uninstall the existing CivilCvCAD $OldVersionNumber before."

#${LangFileString} FinishPageMessage "Tebrikler! CivilCvCAD başarıyla kuruldu.$\r$\n\
#					$\r$\n\
#					(CivilCvCAD in ilk açılışı birkaç saniye alabilir.)"
${LangFileString} FinishPageRun "CivilCvCAD Başlat"

${LangFileString} UnNotInRegistryLabel "Sistem kütüğünde CivilCvCAD bulunamadı.$\r$\n\
					Başlat menüsü ve masaüstünüzdeki kısayollar silinemeyecek."
${LangFileString} UnInstallRunning "Önce CivilCvCAD i kapatmalısınız!"
${LangFileString} UnNotAdminLabel "CivilCvCAD kaldırabilmek için yönetici yetkileri gerekiyor!"
${LangFileString} UnReallyRemoveLabel "CivilCvCAD ve tüm bileşenlerini kaldırmak istediğinize emin misiniz?"
${LangFileString} UnCivilCvCADPreferencesTitle 'CivilCvCAD$\'s user preferences'

#${LangFileString} SecUnProgDescription "Uninstalls xxx."
${LangFileString} SecUnPreferencesDescription 'Deletes CivilCvCAD$\'s configuration folder$\r$\n\
						$\"$AppPre\username\$\r$\n\
						$AppSuff\$\r$\n\
						${APP_DIR_USERDATA}$\")$\r$\n\
						for all users.'
${LangFileString} DialogUnPreferences 'You chose to delete the CivilCvCADs user configuration.$\r$\n\
						This will also delete all installed CivilCvCAD addons.$\r$\n\
						Do you agree with this?'
${LangFileString} SecUnProgramFilesDescription "Uninstall CivilCvCAD and all of its components."

${LangFileString} DirNotEmptyWarning "The selected folder '$INSTDIR' is not empty.$\r$\n\
                        The installer will remove all its content before installing. Continue?"
${LangFileString} RMInstDirFailed "Failed to remove '$INSTDIR'.$\r$\n\
                        Make sure you have sufficient permissions and that no files are in use."
