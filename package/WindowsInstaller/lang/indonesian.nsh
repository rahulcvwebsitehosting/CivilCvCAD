/*
CivilCvCAD Installer Language File
Language: Indonesian
*/

!insertmacro LANGFILE_EXT "Indonesian"

${LangFileString} TEXT_INSTALL_CURRENTUSER "(Pasang untuk Pengguna Yang Ini)"

${LangFileString} TEXT_WELCOME "Program ini akan memandu anda dalam melakukan instalasi CivilCvCAD.$\r$\n\
				$\r$\n\
				$_CLICK"

#${LangFileString} TEXT_CONFIGURE_PYTHON "Proses kompilasi skrip Python ..."

${LangFileString} TEXT_FINISH_DESKTOP "Membuat pintasan ikon di destop"

#${LangFileString} FileTypeTitle "Dokumen-CivilCvCAD"

#${LangFileString} SecAllUsersTitle "Pasang untuk semua pengguna?"
${LangFileString} SecFileAssocTitle "Berkas yang terkait"
${LangFileString} SecDesktopTitle "Ikon Desktop"

${LangFileString} SecCoreDescription "Berkas-berkas CivilCvCAD."
#${LangFileString} SecAllUsersDescription "Pasang CivilCvCAD untuk semua pengguna atau hanya untuk pengguna ini saja."
${LangFileString} SecFileAssocDescription "Berkas dengan ekstensi .FCStd akan otomatis dibuka menggunakan CivilCvCAD."
${LangFileString} SecDesktopDescription "Ikon CivilCvCAD muncul di desktop."
#${LangFileString} SecDictionaries "Kamus"
#${LangFileString} SecDictionariesDescription "Kamus pemeriksa ejaan yang dapat diunduh dan dipasang."

#${LangFileString} PathName 'Lokasi tempat berkas $\"xxx.exe$\" berada'
#${LangFileString} InvalidFolder 'Berkas $\"xxx.exe$\" tidak berada di lokasi tempat yang dinyatakan.'

#${LangFileString} DictionariesFailed 'Download of dictionary for language $\"$R3$\" failed.'

#${LangFileString} ConfigInfo "Proses konfigurasi CivilCvCAD selanjutnya akan memerlukan waktu beberapa saat."

#${LangFileString} RunConfigureFailed "Tidak bisa menjalankan skrip konfigurasi"
${LangFileString} InstallRunning "Program instalasi sedang berjalan!"
${LangFileString} AlreadyInstalled "CivilCvCAD ${APP_SERIES_KEY2} sudah pernah diinstal!$\r$\n\
				Dou you nevertheles want to install CivilCvCAD over the existing version?"
${LangFileString} NewerInstalled "Anda akan memasang versi CivilCvCAD yang lama dari yang sudah terpasang.$\r$\n\
				  Jika memang dikehendaki, anda harus menghapus dulu CivilCvCAD yang ada, CivilCvCAD $OldVersionNumber."

#${LangFileString} FinishPageMessage "Selamat! CivilCvCAD berhasil diinstal dengan sukses.$\r$\n\
#					$\r$\n\
#					(Menjalankan CivilCvCAD untuk pertama kali memerlukan waktu beberapa detik.)"
${LangFileString} FinishPageRun "Menjalankan CivilCvCAD"

${LangFileString} UnNotInRegistryLabel "Tidak bisa menemukan CivilCvCAD di catatan registry.$\r$\n\
					Shortcuts pada desktop dan yang ada di Menu Start tidak dihapus."
${LangFileString} UnInstallRunning "Anda harus menutup CivilCvCAD terlebih dahulu!"
${LangFileString} UnNotAdminLabel "Anda harus berlaku dan mempunyai hak sebagai administrator untuk menghapus CivilCvCAD!"
${LangFileString} UnReallyRemoveLabel "Apakah anda yakin akan menghapus CivilCvCAD secara menyeluruh termasuk semua komponen yang ada?"
${LangFileString} UnCivilCvCADPreferencesTitle 'Preferensi pengguna CivilCvCAD'

#${LangFileString} SecUnProgDescription "Penghapusan program xxx."
${LangFileString} SecUnPreferencesDescription 'Menghapus berkas konfigurasi CivilCvCAD pada folder$\r$\n\
						$\"$AppPre\username\$\r$\n\
						$AppSuff\$\r$\n\
						${APP_DIR_USERDATA}$\")$\r$\n\
						untuk semua pengguna.'
${LangFileString} DialogUnPreferences 'You chose to delete the CivilCvCADs user configuration.$\r$\n\
						This will also delete all installed CivilCvCAD addons.$\r$\n\
						Do you agree with this?'
${LangFileString} SecUnProgramFilesDescription "Penghapusan CivilCvCAD serta semua komponen yang ada."

${LangFileString} DirNotEmptyWarning "The selected folder '$INSTDIR' is not empty.$\r$\n\
                        The installer will remove all its content before installing. Continue?"
${LangFileString} RMInstDirFailed "Failed to remove '$INSTDIR'.$\r$\n\
                        Make sure you have sufficient permissions and that no files are in use."
