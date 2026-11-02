Unicode true
RequestExecutionLevel user
SetCompressor /SOLID lzma
Name "NestSimple Money Repair v1.2.01"
OutFile "NestSimple-Money-Repair-v1.2.01.exe"
InstallDir "E:\Documents\NestSimple-Money-Windows\NestSimpleMoney"
BrandingText "NestSimple Money — Home Accounting Made Simple"
!include "MUI2.nsh"
!include "LogicLib.nsh"
!define MUI_ICON "installed-source\assets\nestsimple-money.ico"
!define MUI_DIRECTORYPAGE_TEXT_TOP "Select the existing NestSimpleMoney program folder. This repair replaces six program files and saves their previous versions. It does not close or open the app. Household data and settings are not replaced."
!define MUI_PAGE_CUSTOMFUNCTION_LEAVE CheckProgramFolder
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_TITLE "Program Files Repaired"
!define MUI_FINISHPAGE_TEXT "The six program files were installed. Previous files were saved in program-update-backups. Household data and settings were preserved. Open NestSimple Money normally when you are ready."
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"
Var Backup
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
Section "Repair Program Files"
 Call CheckProgramFolder
 System::Call 'kernel32::GetTickCount()i.r0'
 StrCpy $Backup "$INSTDIR\program-update-backups\repair-v1.2.01-$0"
 CreateDirectory "$Backup"
 !insertmacro BackupFile "visuals.py"
 !insertmacro BackupFile "budget_page.py"
 !insertmacro BackupFile "program_updates.py"
 !insertmacro BackupFile "update_runtime.py"
 !insertmacro BackupFile "testing_history.py"
 !insertmacro BackupFile "STYLE_GUIDE.md"
 SetOutPath "$INSTDIR"
 SetOverwrite on
 File "current-source\visuals.py"
 File "current-source\budget_page.py"
 File "current-source\program_updates.py"
 File "current-source\update_runtime.py"
 File "current-source\testing_history.py"
 File "current-source\STYLE_GUIDE.md"
 DetailPrint "Six program files installed. No app processes were closed or started."
SectionEnd
