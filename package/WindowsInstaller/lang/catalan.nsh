/*
CivilCvCAD Installer Language File
Language: Catalan
*/

!insertmacro LANGFILE_EXT "Catalan"

${LangFileString} TEXT_INSTALL_CURRENTUSER "(Installed for Current User)"

${LangFileString} TEXT_WELCOME "Aquest assistent us guiarà en la instal·lació del CivilCvCAD.$\r$\n\
				$\r$\n\
				$_CLICK"

#${LangFileString} TEXT_CONFIGURE_PYTHON "Compiling Python scripts..."

${LangFileString} TEXT_FINISH_DESKTOP "Create desktop shortcut"

#${LangFileString} FileTypeTitle "Document CivilCvCAD"

#${LangFileString} SecAllUsersTitle "Voleu instal·lar-ho per a tots els usuaris?"
${LangFileString} SecFileAssocTitle "Associació de fitxers"
${LangFileString} SecDesktopTitle "Icona a l'escriptori"

${LangFileString} SecCoreDescription "Els fitxers del CivilCvCAD."
#${LangFileString} SecAllUsersDescription "Instal·la el CivilCvCAD per a tots els usuaris o només per a l'usuari actual."
${LangFileString} SecFileAssocDescription "Els fitxers amb extensió .FCStd s'obriran automàticament amb el CivilCvCAD."
${LangFileString} SecDesktopDescription "Una icona del CivilCvCAD a l'escriptori."
#${LangFileString} SecDictionaries "Diccionaris"
#${LangFileString} SecDictionariesDescription "Spell-checker dictionaries that can be downloaded and installed."

#${LangFileString} PathName 'Camí al fitxer $\"xxx.exe$\"'
#${LangFileString} InvalidFolder 'El fitxer $\"xxx.exe$\" no es troba al camí indicat.'

#${LangFileString} DictionariesFailed 'Download of dictionary for language $\"$R3$\" failed.'

#${LangFileString} ConfigInfo "La configuració següent del CivilCvCAD pot trigar una mica."

#${LangFileString} RunConfigureFailed "No es pot executar el programa de configuració"
${LangFileString} InstallRunning "L'instal·lador ja s'està executant!"
${LangFileString} AlreadyInstalled "El CivilCvCAD ${APP_SERIES_KEY2} ja es troba instal·lat!$\r$\n\
				Dou you nevertheles want to install CivilCvCAD over the existing version?"
${LangFileString} NewerInstalled "You are trying to install an older version of CivilCvCAD than what you have installed.$\r$\n\
				  If you really want this, you must uninstall the existing CivilCvCAD $OldVersionNumber before."

#${LangFileString} FinishPageMessage "Felicitats! Heu instal·lat correctament el CivilCvCAD.$\r$\n\
#					$\r$\n\
#					(La primera execució del CivilCvCAD pot trigar alguns segons.)"
${LangFileString} FinishPageRun "Executa el CivilCvCAD"

${LangFileString} UnNotInRegistryLabel "No es possible trobar el CivilCvCAD al registre.$\r$\n\
					No se suprimiran les dreceres de l'escriptori i del menú inici."
${LangFileString} UnInstallRunning "Primer heu de tancar el CivilCvCAD!"
${LangFileString} UnNotAdminLabel "Necessiteu drets d'administrador per desinstal·lar el CivilCvCAD!"
${LangFileString} UnReallyRemoveLabel "Esteu segur de voler suprimir completament el CivilCvCAD i tots els seus components?"
${LangFileString} UnCivilCvCADPreferencesTitle 'Preferències d$\'usuari del CivilCvCAD'

#${LangFileString} SecUnProgDescription "Desinstal·xxx."
${LangFileString} SecUnPreferencesDescription 'Suprimeix les carptes de configuració del CivilCvCAD$\r$\n\
						$\"$AppPre\username\$\r$\n\
						$AppSuff\$\r$\n\
						${APP_DIR_USERDATA}$\")$\r$\n\
						de tots els usuaris.'
${LangFileString} DialogUnPreferences 'You chose to delete the CivilCvCADs user configuration.$\r$\n\
						This will also delete all installed CivilCvCAD addons.$\r$\n\
						Do you agree with this?'
${LangFileString} SecUnProgramFilesDescription "Desinstal·la el CivilCvCAD i tots els seus components."

${LangFileString} DirNotEmptyWarning "The selected folder '$INSTDIR' is not empty.$\r$\n\
                        The installer will remove all its content before installing. Continue?"
${LangFileString} RMInstDirFailed "Failed to remove '$INSTDIR'.$\r$\n\
                        Make sure you have sufficient permissions and that no files are in use."
