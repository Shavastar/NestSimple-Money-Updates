Unicode true
RequestExecutionLevel user
SetCompressor /SOLID lzma
Name "NestSimple Money Repair v1.2.00"
OutFile "NestSimple-Money-Repair-v1.2.00.exe"
InstallDir "E:\Documents\NestSimple-Money-Windows\NestSimpleMoney"
BrandingText "NestSimple Money — Home Accounting Made Simple"
!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "FileFunc.nsh"
!define MUI_ICON "installed-source\assets\nestsimple-money.ico"
!define MUI_ABORTWARNING
!define MUI_DIRECTORYPAGE_TEXT_TOP "Select the existing NestSimpleMoney program folder. This repair backs up program files, preserves household data, and verifies that the app reopens."
!define MUI_PAGE_CUSTOMFUNCTION_LEAVE CheckProgramFolder
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_TITLE "Repair Complete"
!define MUI_FINISHPAGE_TEXT "NestSimple Money reopened and confirmed version 1.2.00. Your household data and testing edits were preserved."
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"
Var Python
Var Result
Function CheckProgramFolder
 IfFileExists "$INSTDIR\app.py" 0 Missing
 IfFileExists "$INSTDIR\launch.pyw" Valid Missing
 Missing:
 MessageBox MB_ICONSTOP "Choose the existing program folder containing app.py and launch.pyw."
 Abort
 Valid:
FunctionEnd
Function .onInit
 StrCpy $Python "$LOCALAPPDATA\Python\pythoncore-3.14-64\pythonw.exe"
 IfFileExists "$Python" Found
 StrCpy $Python "$LOCALAPPDATA\Programs\Python\Python314\pythonw.exe"
 IfFileExists "$Python" Found
 StrCpy $Python "$LOCALAPPDATA\Programs\Python\Python313\pythonw.exe"
 IfFileExists "$Python" Found
 StrCpy $Python "$LOCALAPPDATA\Programs\Python\Python312\pythonw.exe"
 IfFileExists "$Python" Found
 StrCpy $Python "$LOCALAPPDATA\Programs\Python\Python310\pythonw.exe"
 IfFileExists "$Python" Found
 SetRegView 64
 ReadRegStr $Python HKCU "Software\Python\PythonCore\3.14\InstallPath" "ExecutablePath"
 IfFileExists "$Python" Found
 ReadRegStr $Python HKLM "Software\Python\PythonCore\3.12\InstallPath" "ExecutablePath"
 IfFileExists "$Python" Found
 MessageBox MB_ICONSTOP "The existing Python runtime could not be located. No files were changed."
 Abort
 Found:
FunctionEnd
Section "Repair And Reopen" Main
 SetOutPath "$INSTDIR\..\temp\repair-v1.2.00"
 File /oname=repair.py "repair200.py"
 File "current-source\program_updates.py"
 File "current-source\file_io.py"
 File "current-source\update_runtime.py"
 File "NestSimple-Money-v1.2.00.nsmupdate"
 DetailPrint "Verifying, backing up and repairing program files."
 DetailPrint "Household databases, personal profiles and testing edits are not replaced."
 ExecWait '"$Python" "$OUTDIR\repair.py" "$INSTDIR"' $Result
 ${If} $Result != 0
  DetailPrint "Repair did not confirm completion. See the repair status and saved diagnostics."
  MessageBox MB_ICONSTOP "The repair did not confirm that the app reopened. Review the repair window or diagnostics under the program folder's temp directory."
  SetErrorLevel 1
  Quit
 ${EndIf}
 DetailPrint "Verified: NestSimple Money reopened and confirmed v1.2.00."
SectionEnd
