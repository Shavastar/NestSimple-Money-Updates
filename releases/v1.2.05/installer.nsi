Unicode true
RequestExecutionLevel user
SetCompressor /SOLID lzma
Name "NestSimple Money Update v1.2.05"
OutFile "NestSimple-Money-Update-v1.2.05.exe"
InstallDir "E:\Documents\NestSimple-Money-Windows\NestSimpleMoney"
BrandingText "NestSimple Money — Program Update"
!include "MUI2.nsh"
!include "LogicLib.nsh"
!define MUI_ICON "installed-source\assets\nestsimple-money.ico"
!define MUI_CUSTOMFUNCTION_GUIINIT BrandingInit
Var Backup
Page custom ChooseCreate ChooseLeave
!define MUI_PAGE_CUSTOMFUNCTION_SHOW InstallShow
!insertmacro MUI_PAGE_INSTFILES
Page custom FinishedCreate
!insertmacro MUI_LANGUAGE "English"
!include "installer_layout1_2_05.nsh"
Function CheckProgramFolder
 IfFileExists "$INSTDIR\app.py" 0 Missing
 IfFileExists "$INSTDIR\launch.pyw" Valid Missing
 Missing:
 MessageBox MB_ICONSTOP "Choose the existing program folder containing app.py and launch.pyw."
 Abort
 Valid:
FunctionEnd
!macro BackupFile FileName
 IfFileExists "$INSTDIR\${FileName}" 0 +5
  ClearErrors
  CopyFiles /SILENT "$INSTDIR\${FileName}" "$Backup"
  IfErrors 0 +2
   Abort "Could not save the program backup. No program files were replaced."
!macroend
Section "Update Program Files"
 Call CheckProgramFolder
 System::Call 'kernel32::GetTickCount()i.r0'
 StrCpy $Backup "$INSTDIR\program-update-backups\update-v1.2.05-$0"
 CreateDirectory "$Backup"
 !insertmacro BackupFile "budget_hierarchy.py"
 !insertmacro BackupFile "visuals.py"
 !insertmacro BackupFile "budget_page.py"
 !insertmacro BackupFile "program_updates.py"
 !insertmacro BackupFile "update_runtime.py"
 !insertmacro BackupFile "testing_history.py"
 !insertmacro BackupFile "STYLE_GUIDE.md"
 !insertmacro BackupFile "app.py"
 !insertmacro BackupFile "settings.py"
 !insertmacro BackupFile "upgrade.py"
 !insertmacro BackupFile "storage_page.py"
 !insertmacro BackupFile "modal_windows.py"
 !insertmacro BackupFile "friendly_messages.py"
 !insertmacro BackupFile "budget_review.py"
 !insertmacro BackupFile "budget_planner.py"
 !insertmacro BackupFile "page_messages.py"
 !insertmacro BackupFile "message_art.py"
 SetOutPath "$INSTDIR"
 SetOverwrite on
 File "current-source\budget_hierarchy.py"
 File "current-source\visuals.py"
 File "current-source\budget_page.py"
 File "current-source\program_updates.py"
 File "current-source\update_runtime.py"
 File "current-source\testing_history.py"
 File "current-source\STYLE_GUIDE.md"
 File "current-source\app.py"
 File "current-source\settings.py"
 File "current-source\upgrade.py"
 File "current-source\storage_page.py"
 File "current-source\modal_windows.py"
 File "current-source\friendly_messages.py"
 File "current-source\budget_review.py"
 File "current-source\budget_planner.py"
 File "current-source\page_messages.py"
 File "current-source\message_art.py"
 FileOpen $0 "$INSTDIR\Installed Files v1.2.05.txt" w
 FileWrite $0 "NestSimple Money v1.2.05 installed files:$\r$\n$INSTDIR\budget_hierarchy.py$\r$\n$INSTDIR\visuals.py$\r$\n$INSTDIR\budget_page.py$\r$\n$INSTDIR\program_updates.py$\r$\n$INSTDIR\update_runtime.py$\r$\n$INSTDIR\testing_history.py$\r$\n$INSTDIR\STYLE_GUIDE.md$\r$\n$INSTDIR\app.py$\r$\n$INSTDIR\settings.py$\r$\n$INSTDIR\upgrade.py$\r$\n$INSTDIR\storage_page.py$\r$\n$INSTDIR\modal_windows.py$\r$\n$INSTDIR\friendly_messages.py$\r$\n$INSTDIR\budget_review.py$\r$\n$INSTDIR\budget_planner.py$\r$\n$INSTDIR\page_messages.py$\r$\n$INSTDIR\message_art.py$\r$\n$\r$\nProgram backup: $Backup$\r$\n"
 FileClose $0
 DetailPrint "Seventeen program files installed. No app processes were closed or started."
SectionEnd
