/*
CivilCvCAD Installer Language File
Language: Basque
*/

!insertmacro LANGFILE_EXT "Basque"

${LangFileString} TEXT_INSTALL_CURRENTUSER "(Instalatu uneko erabiltzailearentzat)"

${LangFileString} TEXT_WELCOME "Morroi honek $(^NameDA) aplikazioaren instalazio urratsetan zehar lagunduko dizu, $\r$\n\
				$\r$\n\
				$_CLICK"

#${LangFileString} TEXT_CONFIGURE_PYTHON "Python script-ak konpilatzen..."

${LangFileString} TEXT_FINISH_DESKTOP "Sortu mahaigaineko lasterbidea"

#${LangFileString} FileTypeTitle "CivilCvCAD-dokumentua"

#${LangFileString} SecAllUsersTitle "Instalatu erabiltzaile guztientzako?"
${LangFileString} SecFileAssocTitle "Fitxategiaren esleipenak"
${LangFileString} SecDesktopTitle "Mahaigaineko ikonoa"

${LangFileString} SecCoreDescription "CivilCvCAD fitxategiak."
#${LangFileString} SecAllUsersDescription "Instalatu CivilCvCAD erabiltzaile guztientzako, edo soilik uneko erabiltzailearentzako."
${LangFileString} SecFileAssocDescription ".FCStd luzapeneko fitxategiak CivilCvCAD-ekin irekiko dira automatikoki."
${LangFileString} SecDesktopDescription "CivilCvCAD ikonoa mahaigainean."
#${LangFileString} SecDictionaries "Hiztegia"
#${LangFileString} SecDictionariesDescription "Zuzentzaile ortografikoen hiztegiak deskarga eta instala daitezke."

#${LangFileString} PathName '$\"xxx.exe$\" fitxategiaren bide-izena'
#${LangFileString} InvalidFolder '$\"xxx.exe$\" fitxategia ez dago zehaztutako bide-izenean.'

#${LangFileString} DictionariesFailed 'Huts egin du  $\"$R3$\" hizkuntzaren hiztegia deskargatzean.'

#${LangFileString} ConfigInfo "CivilCvCAD-en hurrengo konfigurazioak denbora piskat beharko du."

#${LangFileString} RunConfigureFailed "Ezin izan da konfigurazioaren script-a exekutatu"
${LangFileString} InstallRunning "Instalatzailea jadanik exekutatzen ari da."
${LangFileString} AlreadyInstalled "CivilCvCAD ${APP_SERIES_KEY2} jadanik instalatuta dago!$\r$\n\
				Dou you nevertheles want to install CivilCvCAD over the existing version?"
${LangFileString} NewerInstalled "Instalatuta dagoen CivilCvCAD baino bertsio zaharragoa instalatzen saiatzen ari zara.$\r$\n\
				  Hori egitea nahi baduzu, lehenbizi existitzen den CivilCvCAD $OldVersionNumber desinstalatu beharko duzu."

#${LangFileString} FinishPageMessage "Zorionak! CivilCvCAD ongi instalatu da.$\r$\n\
#					$\r$\n\
#					(CivilCvCAD aurreneko aldiz abiatzean denbora piskat beharko du.)"
${LangFileString} FinishPageRun "Abiarazi CivilCvCAD"

${LangFileString} UnNotInRegistryLabel "Ezin da CivilCvCAD aurkitu erregistroan.$\r$\n\
					Mahaigaineko eta Hasiera menuko lasterbideak ez dira kenduko."
${LangFileString} UnInstallRunning "Aurrenik CivilCvCAD itxi behar duzu."
${LangFileString} UnNotAdminLabel "Administratzailearen baimenak behar dituzu CivilCvCAD desinstalatzeko."
${LangFileString} UnReallyRemoveLabel "Ziur zaude CivilCvCAD eta bere osagai guztiak kentzea nahi dituzula??"
${LangFileString} UnCivilCvCADPreferencesTitle 'CivilCvCAD-eko erabiltzailearen hobespenak'

#${LangFileString} SecUnProgDescription "xxx kudeatzailea desinstalatzen du."
${LangFileString} SecUnPreferencesDescription 'CivilCvCAD-en konfigurazioa ezabatzen du$\r$\n\
						($\"$AppPre\erabiltzailea\$\r$\n\
						$AppSuff\$\r$\n\
						\${APP_DIR_USERDATA}$\"$\r$\n\
						zuretzako edo erabiltzaile guztientzako (administratzailea bazara).'
${LangFileString} DialogUnPreferences 'You chose to delete the CivilCvCADs user configuration.$\r$\n\
						This will also delete all installed CivilCvCAD addons.$\r$\n\
						Do you agree with this?'
${LangFileString} SecUnProgramFilesDescription "Desinstalatu CivilCvCAD eta bere osagai guztiak."

${LangFileString} DirNotEmptyWarning "The selected folder '$INSTDIR' is not empty.$\r$\n\
                        The installer will remove all its content before installing. Continue?"
${LangFileString} RMInstDirFailed "Failed to remove '$INSTDIR'.$\r$\n\
                        Make sure you have sufficient permissions and that no files are in use."
