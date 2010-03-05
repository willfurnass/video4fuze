; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "video4fuze"
!define PRODUCT_VERSION "0.5"
!define PRODUCT_PUBLISHER "ssorgatem productions"
!define PRODUCT_WEB_SITE "http://code.google.com/p/video4fuze/"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\video4fuze.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define PRODUCT_STARTMENU_REGVAL "NSIS:StartMenuDir"

SetCompressor lzma

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Language Selection Dialog Settings
!define MUI_LANGDLL_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_LANGDLL_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
; Components page
!insertmacro MUI_PAGE_COMPONENTS
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Start menu page
var ICONS_GROUP
!define MUI_STARTMENUPAGE_NODISABLE
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "video4fuze"
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "${PRODUCT_STARTMENU_REGVAL}"
!insertmacro MUI_PAGE_STARTMENU Application $ICONS_GROUP
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\video4fuze.exe"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\README.txt"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Spanish"
!insertmacro MUI_LANGUAGE "Catalan"

; Reserve files
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "${PRODUCT_NAME}-${PRODUCT_VERSION}_installer.exe"
InstallDir "$PROGRAMFILES\${PRODUCT_NAME}-${PRODUCT_VERSION}"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY

  ${Unless} ${FileExists} $TEMP\VS2008_SP1_vcredist_x86.exe
    DetailPrint "Installing VC++ 2008 runtime"
    SetoutPath "$TEMP"
    File ..\vcredist_x86.exe
    ExecWait "$TEMP\vcredist_x86.exe /q"
    DetailPrint "Cleaning up"
    Delete $TEMP\vcredist_x86.exe
  ${EndUnless}
FunctionEnd

Section "Principal" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite on
  File "dist\win32\video4fuze.exe"
  File "dist\win32\_imaging.pyd"
  File "dist\win32\bz2.pyd"
  File "dist\win32\PyQt4.QtCore.pyd"
  File "dist\win32\PyQt4.QtGui.pyd"
  File "dist\win32\python26.dll"
  File "dist\win32\QtCore4.dll"
  File "dist\win32\QtGui4.dll"
  File "dist\win32\select.pyd"
  File "dist\win32\sip.pyd"
  File "dist\win32\unicodedata.pyd"
  SetOverwrite ifnewer
  File "README.txt"
  File "LICENSE.txt"
  File "CHANGELOG.txt"
  SetOutPath "$INSTDIR\translations"
  SetOverwrite try
  File "translations\v4f_es.qm"
  File "translations\v4f_en.qm"
  File "translations\v4f_ca.qm"
  SetOutPath "$INSTDIR"


; Shortcuts
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
  CreateDirectory "$SMPROGRAMS\$ICONS_GROUP"
  CreateShortCut "$SMPROGRAMS\$ICONS_GROUP\video4fuze.lnk" "$INSTDIR\video4fuze.exe"
  CreateShortCut "$DESKTOP\video4fuze.lnk" "$INSTDIR\video4fuze.exe"
  !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section "mencoder" SEC02
  SetOutPath "$INSTDIR"
  File "mencoder.exe"

; Shortcuts
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
  !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section "ffmpeg" SEC03
  SetOutPath "$INSTDIR"
  File "ffmpeg.exe"

; Shortcuts
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
  !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section "fuzemux" SEC04
  SetOutPath "$INSTDIR"
  File "fuzemux.exe"

; Shortcuts
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
  !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section -AdditionalIcons
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\$ICONS_GROUP\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\$ICONS_GROUP\Uninstall.lnk" "$INSTDIR\uninst.exe"
  !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\video4fuze.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\video4fuze.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

; Section descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC01} "Video4fuze"
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC02} "Unselect this only if you know what are you doing. If selected, it will install mencoder, which video4fuze needs"
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC03} "Needed for thumbnail generation. If you choose not to install it, you will have to manually place a copy of ffmpeg.exe into vide4fuze-s installation directory"
    !insertmacro MUI_DESCRIPTION_TEXT ${SEC04} "Needed in order to output avi files playable in the fuze"
!insertmacro MUI_FUNCTION_DESCRIPTION_END


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "La desinstalaci贸n de $(^Name) finaliz贸 satisfactoriamente."
FunctionEnd

Function un.onInit
!insertmacro MUI_UNGETLANGUAGE
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "偶Est谩 completamente seguro que desea desinstalar $(^Name) junto con todos sus componentes?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  !insertmacro MUI_STARTMENU_GETFOLDER "Application" $ICONS_GROUP
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\ffmpeg.exe"
  Delete "$INSTDIR\fuzemux.exe"
  Delete "$INSTDIR\mencoder.exe"
  Delete "$INSTDIR\w9xpopen.exe"
  Delete "$INSTDIR\LICENSE.txt"
  Delete "$INSTDIR\README.txt"
  Delete "$INSTDIR\unicodedata.pyd"
  Delete "$INSTDIR\sip.pyd"
  Delete "$INSTDIR\select.pyd"
  Delete "$INSTDIR\QtGui4.dll"
  Delete "$INSTDIR\QtCore4.dll"
  Delete "$INSTDIR\python26.dll"
  Delete "$INSTDIR\PyQt4.QtGui.pyd"
  Delete "$INSTDIR\PyQt4.QtCore.pyd"
  Delete "$INSTDIR\bz2.pyd"
  Delete "$INSTDIR\_imaging.pyd"
  Delete "$INSTDIR\video4fuze.exe"
  Delete "$INSTDIR\language_codes.txt"
  Delete "$INSTDIR\translations\v4f_ca.qm"
  Delete "$INSTDIR\translations\v4f_en.qm"
  Delete "$INSTDIR\translations\v4f_es.qm"

  Delete "$SMPROGRAMS\$ICONS_GROUP\Uninstall.lnk"
  Delete "$SMPROGRAMS\$ICONS_GROUP\Website.lnk"
  Delete "$DESKTOP\video4fuze.lnk"
  Delete "$SMPROGRAMS\$ICONS_GROUP\video4fuze.lnk"

  RMDir "$SMPROGRAMS\$ICONS_GROUP"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd
