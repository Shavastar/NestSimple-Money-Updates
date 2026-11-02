!include "nsDialogs.nsh"
!include "WinMessages.nsh"
Var Panel
Var BitmapHandle
Var BrandControl
Var MainWidth
Var MainHeight
Var BodyTop
Var BodyHeight
Var BrandWidth
Var Margin
Var FooterHeight
Var RightX
Var RightWidth
Var PathControl
Var Dialog

Function BrandingInit
 InitPluginsDir
 SetOutPath "$PLUGINSDIR"
 File /oname=brand-panel.bmp "brand-panel.bmp"
 System::Call 'user32::GetDpiForWindow(p $HWNDPARENT)i.r0'
 ${If} $0 == 0
  StrCpy $0 96
 ${EndIf}
 IntOp $BodyTop $0 * 60
 IntOp $BodyTop $BodyTop / 96
 IntOp $Margin $0 * 10
 IntOp $Margin $Margin / 96
 IntOp $FooterHeight $0 * 50
 IntOp $FooterHeight $FooterHeight / 96
 System::Call '*(i0,i0,i0,i0)p.r1'
 System::Call 'user32::GetClientRect(p $HWNDPARENT,p r1)'
 System::Call '*$1(i.r2,i.r3,i.r4,i.r5)'
 System::Free $1
 StrCpy $MainWidth $4
 StrCpy $MainHeight $5
 IntOp $BrandWidth $MainWidth * 40
 IntOp $BrandWidth $BrandWidth / 100
 IntOp $BodyHeight $MainHeight - $BodyTop
 IntOp $BodyHeight $BodyHeight - $FooterHeight
 IntOp $RightX $BrandWidth + $Margin
 IntOp $RightWidth $MainWidth - $RightX
 IntOp $RightWidth $RightWidth - $Margin
 System::Call 'user32::CreateWindowExW(i0,w"STATIC",w"",i0x5000000E,i0,i$BodyTop,i$BrandWidth,i$BodyHeight,p$HWNDPARENT,p0,p0,p0)p.r0'
 StrCpy $BrandControl $0
 ${NSD_SetStretchedImage} $BrandControl "$PLUGINSDIR\brand-panel.bmp" $BitmapHandle
FunctionEnd

Function PositionRightPage
 IntOp $0 $BodyTop + $Margin
 IntOp $1 $BodyHeight - $Margin
 IntOp $1 $1 - $Margin
 System::Call 'user32::MoveWindow(p$Dialog,i$RightX,i r0,i$RightWidth,i r1,i1)'
 SetCtlColors $Dialog 000000 FFFFFF
FunctionEnd

Function ChooseCreate
 !insertmacro MUI_HEADER_TEXT "Program Update" "NestSimple Money v1.2.05"
 nsDialogs::Create 1018
 Pop $Dialog
 Call PositionRightPage
 ${NSD_CreateLabel} 0 0 100% 38u "Choose the existing program folder. Only program files are replaced; household data and settings are preserved."
 Pop $0
 ${NSD_CreateLabel} 0 46u 100% 12u "Program folder:"
 Pop $0
 ${NSD_CreateDirRequest} 0 61u 100% 14u "$INSTDIR"
 Pop $PathControl
 ${NSD_CreateBrowseButton} 0 83u 72u 16u "Browse..."
 Pop $0
 ${NSD_OnClick} $0 BrowseFolder
 ${NSD_CreateLabel} 0 112u 100% 35u "Previous program files will be saved in program-update-backups."
 Pop $0
 nsDialogs::Show
FunctionEnd

Function BrowseFolder
 Pop $0
 ${NSD_GetText} $PathControl $INSTDIR
 nsDialogs::SelectFolderDialog "Select the existing NestSimpleMoney program folder" "$INSTDIR"
 Pop $0
 ${If} $0 != error
  ${NSD_SetText} $PathControl $0
 ${EndIf}
FunctionEnd

Function ChooseLeave
 ${NSD_GetText} $PathControl $INSTDIR
 Call CheckProgramFolder
FunctionEnd

Function InstallShow
 StrCpy $Dialog $mui.InstFilesPage
 Call PositionRightPage
 IntOp $0 $Margin * 3
 System::Call 'user32::MoveWindow(p$mui.InstFilesPage.Text,i0,i0,i$RightWidth,i r0,i1)'
 IntOp $1 $0 + $Margin
 IntOp $2 $Margin + 3
 System::Call 'user32::MoveWindow(p$mui.InstFilesPage.ProgressBar,i0,i r1,i$RightWidth,i r2,i1)'
 ShowWindow $mui.InstFilesPage.ShowLogButton ${SW_HIDE}
 IntOp $1 $1 + $2
 IntOp $1 $1 + $Margin
 IntOp $2 $BodyHeight - $1
 IntOp $2 $2 - $Margin
 IntOp $2 $2 - $Margin
 System::Call 'user32::MoveWindow(p$mui.InstFilesPage.Log,i0,i r1,i$RightWidth,i r2,i1)'
 ShowWindow $mui.InstFilesPage.Log ${SW_SHOW}
FunctionEnd

Function FinishedCreate
 !insertmacro MUI_HEADER_TEXT "Update Complete" "NestSimple Money Program Update"
 nsDialogs::Create 1018
 Pop $Dialog
 IntOp $0 $MainHeight - $BodyTop
 System::Call 'user32::MoveWindow(p$Dialog,i0,i$BodyTop,i$MainWidth,i r0,i1)'
 SetCtlColors $Dialog 000000 FFFFFF
 ${NSD_CreateBitmap} 0 0 $BrandWidth $BodyHeight ""
 Pop $0
 ${NSD_SetStretchedImage} $0 "$PLUGINSDIR\brand-panel.bmp" $Panel
 ${NSD_CreateLabel} $RightX $Margin $RightWidth 40 "NestSimple Money v1.2.05 is installed."
 Pop $0
 IntOp $1 $Margin * 6
 ${NSD_CreateLabel} $RightX $1 $RightWidth 140 "Your program files were updated.$\r$\n$\r$\nPrevious files were saved in program-update-backups.$\r$\n$\r$\nYour household data and settings were preserved.$\r$\n$\r$\nOpen NestSimple Money normally."
 Pop $0
 ${NSD_CreateLabel} 0 $BodyHeight 100% $FooterHeight ""
 Pop $0
 SetCtlColors $0 808080 F0F0F0
 IntOp $1 $BodyHeight + 5
 ${NSD_CreateLabel} 8 $1 220 12 "NestSimple Money — Program Update"
 Pop $0
 SetCtlColors $0 808080 F0F0F0
 GetDlgItem $0 $HWNDPARENT 3
 System::Call '*(i0,i0,i0,i0)p.r1'
 System::Call 'user32::GetWindowRect(p r0,p r1)'
 System::Call 'user32::MapWindowPoints(p0,p$HWNDPARENT,p r1,i2)'
 System::Call '*$1(i.r2,i.r3,i.r4,i.r5)'
 System::Free $1
 IntOp $4 $4 - $2
 IntOp $5 $5 - $3
 IntOp $3 $3 - $BodyTop
 ShowWindow $0 ${SW_HIDE}
 ${NSD_CreateButton} $2 $3 $4 $5 "Show Files"
 Pop $0
 ${NSD_OnClick} $0 ShowFiles
 GetDlgItem $0 $HWNDPARENT 1
 SendMessage $0 ${WM_SETTEXT} 0 "STR:Close"
 System::Call 'user32::SetWindowPos(p r0,p0,i0,i0,i0,i0,i0x43)'
 GetDlgItem $0 $HWNDPARENT 2
 EnableWindow $0 0
 System::Call 'user32::SetWindowPos(p r0,p0,i0,i0,i0,i0,i0x43)'
 nsDialogs::Show
FunctionEnd

Function ShowFiles
 Pop $0
 ExecShell "open" "$INSTDIR\Installed Files v1.2.05.txt"
FunctionEnd
