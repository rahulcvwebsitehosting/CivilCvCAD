/*
CivilCvCAD Installer Language File
Language: Danish
*/

!insertmacro LANGFILE_EXT "Danish"

${LangFileString} TEXT_INSTALL_CURRENTUSER "(Installed for Current User)"

${LangFileString} TEXT_WELCOME "Denne guide vil installere CivilCvCAD på din computer.$\r$\n\
				$\r$\n\
				$_CLICK"

#${LangFileString} TEXT_CONFIGURE_PYTHON "Compiling Python scripts..."

${LangFileString} TEXT_FINISH_DESKTOP "Create desktop shortcut"

#${LangFileString} FileTypeTitle "CivilCvCAD-Dokument"

#${LangFileString} SecAllUsersTitle "Installer til alle brugere?"
${LangFileString} SecFileAssocTitle "Fil-associationer"
${LangFileString} SecDesktopTitle "Skrivebordsikon"

${LangFileString} SecCoreDescription "Filerne til CivilCvCAD."
#${LangFileString} SecAllUsersDescription "Installer CivilCvCAD til alle brugere, eller kun den aktuelle bruger."
${LangFileString} SecFileAssocDescription "Opret association mellem CivilCvCAD og .FCStd filer."
${LangFileString} SecDesktopDescription "Et CivilCvCAD ikon på skrivebordet"
#${LangFileString} SecDictionaries "Ordbøger"
#${LangFileString} SecDictionariesDescription "Spell-checker dictionaries that can be downloaded and installed."

#${LangFileString} PathName 'Sti til filen $\"xxx.exe$\"'
#${LangFileString} InvalidFolder 'Kunne ikke finde $\"xxx.exe$\".'

#${LangFileString} DictionariesFailed 'Download of dictionary for language $\"$R3$\" failed.'

#${LangFileString} ConfigInfo "Den følgende konfiguration af CivilCvCAD vil tage et stykke tid."

#${LangFileString} RunConfigureFailed "Mislykket forsog på at afvikle konfigurations-scriptet"
${LangFileString} InstallRunning "Installationsprogrammet kører allerede!"
${LangFileString} AlreadyInstalled "CivilCvCAD ${APP_SERIES_KEY2} er allerede installeret!$\r$\n\
				Dou you nevertheles want to install CivilCvCAD over the existing version?"
${LangFileString} NewerInstalled "You are trying to install an older version of CivilCvCAD than what you have installed.$\r$\n\
				  If you really want this, you must uninstall the existing CivilCvCAD $OldVersionNumber before."

#${LangFileString} FinishPageMessage "Tillykke!! CivilCvCAD er installeret.$\r$\n\
#					$\r$\n\
#					(Når CivilCvCAD startes første gang, kan det tage noget tid.)"
${LangFileString} FinishPageRun "Start CivilCvCAD"

${LangFileString} UnNotInRegistryLabel "Kunne ikke finde CivilCvCAD i registreringsdatabsen.$\r$\n\
					Genvejene på skrivebordet og i Start-menuen bliver ikke fjernet"
${LangFileString} UnInstallRunning "Du ma afslutte CivilCvCAD forst!"
${LangFileString} UnNotAdminLabel "Du skal have administrator-rettigheder for at afinstallere CivilCvCAD!"
${LangFileString} UnReallyRemoveLabel "Er du sikker på, at du vil slette CivilCvCAD og alle tilhørende komponenter?"
${LangFileString} UnCivilCvCADPreferencesTitle 'CivilCvCAD$\'s user preferences'

#${LangFileString} SecUnProgDescription 'Afinstallerer programmet $\"xxx$\".'
${LangFileString} SecUnPreferencesDescription 'Sletter CivilCvCAD$\'s konfigurations mappe$\r$\n\
						$\"$AppPre\username\$\r$\n\
						$AppSuff\$\r$\n\
						${APP_DIR_USERDATA}$\")$\r$\n\
						for alle brugere.'
${LangFileString} DialogUnPreferences 'You chose to delete the CivilCvCADs user configuration.$\r$\n\
						This will also delete all installed CivilCvCAD addons.$\r$\n\
						Do you agree with this?'
${LangFileString} SecUnProgramFilesDescription "Afinstallerer CivilCvCAD og alle dets komponenter."

${LangFileString} DirNotEmptyWarning "The selected folder '$INSTDIR' is not empty.$\r$\n\
                        The installer will remove all its content before installing. Continue?"
${LangFileString} RMInstDirFailed "Failed to remove '$INSTDIR'.$\r$\n\
                        Make sure you have sufficient permissions and that no files are in use."
