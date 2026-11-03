Unicode true
RequestExecutionLevel user
SetCompressor /SOLID lzma
Name "NestSimple Money Update v1.2.26"
OutFile "NestSimple-Money-Update-v1.2.26.exe"
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
!include "installer_layout1_2_26.nsh"
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
 StrCpy $Backup "$INSTDIR\program-update-backups\update-v1.2.26-$0"
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
 !insertmacro BackupFile "chart_hierarchy.py"
 !insertmacro BackupFile "report_order.py"
 !insertmacro BackupFile "category_reports.py"
 !insertmacro BackupFile "reports.py"
 !insertmacro BackupFile "bills_print.py"
 !insertmacro BackupFile "page_print.py"
 !insertmacro BackupFile "budget_print.py"
 !insertmacro BackupFile "planning_print.py"
 !insertmacro BackupFile "calendar_print.py"
 !insertmacro BackupFile "card_print.py"
 !insertmacro BackupFile "transactions_print.py"
 !insertmacro BackupFile "testing_ui.py"
 !insertmacro BackupFile "release_notes.py"
 !insertmacro BackupFile "layout.py"
 !insertmacro BackupFile "currency_menu.py"
 !insertmacro BackupFile "table_ui.py"
 !insertmacro BackupFile "currency_ui.py"
 !insertmacro BackupFile "modern_ui.py"
 !insertmacro BackupFile "expense_page.py"
 !insertmacro BackupFile "manual_bill.py"
 !insertmacro BackupFile "income_dashboard.py"
 !insertmacro BackupFile "list_filters.py"
 !insertmacro BackupFile "control_size.py"
 !insertmacro BackupFile "income_skin.py"
 !insertmacro BackupFile "record_pages.py"
 !insertmacro BackupFile "income_filters.py"
 !insertmacro BackupFile "income_reference_art.py"
 !insertmacro BackupFile "income_workspace.py"
 !insertmacro BackupFile "income_calendar.py"
 !insertmacro BackupFile "icon_ui.py"
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
 File "current-source\chart_hierarchy.py"
 File "current-source\report_order.py"
 File "current-source\category_reports.py"
 File "current-source\reports.py"
 File "current-source\bills_print.py"
 File "current-source\page_print.py"
 File "current-source\budget_print.py"
 File "current-source\planning_print.py"
 File "current-source\calendar_print.py"
 File "current-source\card_print.py"
 File "current-source\transactions_print.py"
 File "current-source\testing_ui.py"
 File "current-source\release_notes.py"
 File "current-source\layout.py"
 File "current-source\currency_menu.py"
 File "current-source\table_ui.py"
 File "current-source\currency_ui.py"
 File "current-source\modern_ui.py"
 File "current-source\expense_page.py"
 File "current-source\manual_bill.py"
 File "current-source\income_dashboard.py"
 File "current-source\list_filters.py"
 File "current-source\control_size.py"
 File "current-source\income_skin.py"
 File "current-source\record_pages.py"
 File "current-source\income_filters.py"
 File "current-source\income_reference_art.py"
 File "current-source\income_workspace.py"
 File "current-source\income_calendar.py"
 File "current-source\icon_ui.py"
 FileOpen $0 "$INSTDIR\Installed Files v1.2.26.txt" w
 FileWrite $0 "NestSimple Money v1.2.26 installed files:$\r$\n$INSTDIR\budget_hierarchy.py$\r$\n$INSTDIR\visuals.py$\r$\n$INSTDIR\budget_page.py$\r$\n$INSTDIR\program_updates.py$\r$\n$INSTDIR\update_runtime.py$\r$\n$INSTDIR\testing_history.py$\r$\n$INSTDIR\STYLE_GUIDE.md$\r$\n$INSTDIR\app.py$\r$\n$INSTDIR\settings.py$\r$\n$INSTDIR\upgrade.py$\r$\n$INSTDIR\storage_page.py$\r$\n$INSTDIR\modal_windows.py$\r$\n$INSTDIR\friendly_messages.py$\r$\n$INSTDIR\budget_review.py$\r$\n$INSTDIR\budget_planner.py$\r$\n$INSTDIR\page_messages.py$\r$\n$INSTDIR\message_art.py$\r$\n$INSTDIR\chart_hierarchy.py$\r$\n$INSTDIR\report_order.py$\r$\n$INSTDIR\category_reports.py$\r$\n$INSTDIR\reports.py$\r$\n$INSTDIR\bills_print.py$\r$\n$INSTDIR\page_print.py$\r$\n$INSTDIR\budget_print.py$\r$\n$INSTDIR\planning_print.py$\r$\n$INSTDIR\calendar_print.py$\r$\n$INSTDIR\card_print.py$\r$\n$INSTDIR\transactions_print.py$\r$\n$INSTDIR\testing_ui.py$\r$\n$INSTDIR\release_notes.py$\r$\n$INSTDIR\layout.py$\r$\n$INSTDIR\currency_menu.py$\r$\n$INSTDIR\table_ui.py$\r$\n$INSTDIR\currency_ui.py$\r$\n$INSTDIR\modern_ui.py$\r$\n$INSTDIR\expense_page.py$\r$\n$INSTDIR\manual_bill.py$\r$\n$INSTDIR\income_dashboard.py$\r$\n$INSTDIR\list_filters.py$\r$\n$INSTDIR\control_size.py$\r$\n$INSTDIR\income_skin.py$\r$\n$INSTDIR\record_pages.py$\r$\n$INSTDIR\income_filters.py$\r$\n$INSTDIR\income_reference_art.py$\r$\n$INSTDIR\income_workspace.py$\r$\n$INSTDIR\income_calendar.py$\r$\n$INSTDIR\icon_ui.py$\r$\n$\r$\nProgram backup: $Backup$\r$\n"
 FileClose $0
 DetailPrint "40 program files installed. No app processes were closed or started."
SectionEnd

