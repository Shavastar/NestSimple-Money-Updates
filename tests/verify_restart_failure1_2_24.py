"""Real child exit must not be called success; Retry Reopen must handshake."""
from pathlib import Path
import sys,shutil,json,tkinter as tk,time
from tkinter import ttk
from unittest.mock import patch
base=Path(__file__).parent.resolve();sys.path.insert(0,str(base/'current-source'))
import program_updates as u
from update_runtime import run_worker
test=base/'restart-failure-qa24';test.mkdir(exist_ok=True);root=test/'program';root.mkdir(exist_ok=True)
for p in (base/'installed-source').glob('*.py'):shutil.copy2(p,root/p.name)
shutil.copy2(base/'v198/payload/STYLE_GUIDE.md',root/'STYLE_GUIDE.md')
(root/'launch.pyw').write_text("import sys\nprint('deliberate startup failure',flush=True)\nsys.exit(23)\n",encoding='utf-8')
(root/'household.sqlite3').write_bytes(b'unchanged household sentinel')
folder,manifest=u.prepare(base/'NestSimple-Money-v1.2.24.nsmupdate',root)
(folder/'request.json').write_text(json.dumps({'sessions':[],'environment':{}}),encoding='utf-8')
real_tk=tk.Tk;retried=[]
def create_window(*args,**kwargs):
 win=real_tk(*args,**kwargs)
 def observe():
  result=(folder/'result.txt').read_text(encoding='utf-8') if (folder/'result.txt').exists() else ''
  if 'FAILED:' in result and not retried:
   assert 'REOPENED:' not in result,'A failed launch was reported as success'
   assert 'Restart exit status: 23' in result,result
   assert b'deliberate startup failure' in (folder/'restart.log').read_bytes()
   def descendants(w):
    for c in w.winfo_children():yield c;yield from descendants(c)
   retry=next(w for w in descendants(win) if isinstance(w,ttk.Button) and w.cget('text')=='Retry Reopen')
   win.update_idletasks()
   assert retry.winfo_ismapped(),'Retry action is not visible'
   # Replace only the disposable deliberately broken entry point.
   (root/'launch.pyw').write_text("import tkinter as tk\nfrom program_updates import install_session\nr=tk.Tk();install_session(r);r.after(4000,r.destroy);r.mainloop()\n",encoding='utf-8')
   retried.append(True);retry.invoke()
  if win.winfo_exists():win.after(50,observe)
 win.after(50,observe)
 # A broken implementation must fail the test instead of waiting for input.
 win.after(20000,win.destroy)
 return win
with patch.object(tk,'Tk',side_effect=create_window):run_worker(root,folder,u)
assert retried and 'REOPENED:' in (folder/'result.txt').read_text(encoding='utf-8')
assert (root/'household.sqlite3').read_bytes()==b'unchanged household sentinel'
print('PASS real startup exit 23: no false completion, saved stderr, visible retry, successful real retry receipt, household unchanged')



