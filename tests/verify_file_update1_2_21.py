from pathlib import Path
import shutil,subprocess,sys,json,hashlib
base=Path(__file__).parent.resolve();test=base/'page-messages-update-test';test.mkdir(exist_ok=True)
program=test/'NestSimple Money';program.mkdir(exist_ok=True)
for p in (base/'installed-source').glob('*.py'):shutil.copy2(p,program/p.name)
shutil.copy2(base/'installed-source/launch.pyw',program/'launch.pyw')
names=('budget_hierarchy.py', 'visuals.py', 'budget_page.py', 'program_updates.py', 'update_runtime.py', 'testing_history.py', 'STYLE_GUIDE.md', 'app.py', 'settings.py', 'upgrade.py', 'storage_page.py', 'modal_windows.py', 'friendly_messages.py', 'budget_review.py', 'budget_planner.py', 'page_messages.py', 'message_art.py', 'chart_hierarchy.py', 'report_order.py', 'category_reports.py', 'reports.py', 'bills_print.py', 'page_print.py', 'budget_print.py', 'planning_print.py', 'calendar_print.py', 'card_print.py', 'transactions_print.py', 'testing_ui.py', 'release_notes.py', 'layout.py', 'currency_menu.py', 'table_ui.py', 'currency_ui.py', 'modern_ui.py', 'expense_page.py', 'manual_bill.py')
before={name:(program/name).read_bytes() if (program/name).exists() else None for name in names}
sentinels={'household/finances.sqlite3':b'household unchanged','settings.json':b'profile unchanged','testing/edits.txt':b'testing edits unchanged','../temp/program-updates/sessions/broken.json':b'invalid stale session must not matter'}
for relative,data in sentinels.items():
 p=program/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
other=subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)'])
try:
 repair=subprocess.run('"'+str(base/'NestSimple-Money-Update-v1.2.21.exe')+'" /S /D='+str(program),timeout=30)
 assert repair.returncode==0,repair.returncode
 assert other.poll() is None,'Repair stopped an unrelated running process'
 for name in names:assert (program/name).read_bytes()==(base/'current-source'/name).read_bytes(),name
 for relative,data in sentinels.items():assert (program/relative).read_bytes()==data,relative
 backup=max((program/'program-update-backups').glob('update-v1.2.21-*'),key=lambda p:p.stat().st_mtime)
 for name,data in before.items():
  if data is not None:assert (backup/name).read_bytes()==data,'Backup mismatch: '+name
 script=(base/'update1_2_21.nsi').read_text(encoding='utf-8')
 assert 'ExecWait' not in script and 'Exec ' not in script
 print('PASS actual native file-only repair: 30 exact files, verified previous-file backups, stale sessions ignored, no process shutdown/start, household/profile/testing sentinels unchanged')
 print('Repair bytes:',(base/'NestSimple-Money-Update-v1.2.21.exe').stat().st_size)
finally:other.terminate();other.wait()

