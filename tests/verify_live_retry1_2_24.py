from pathlib import Path
import sys,shutil,json,tkinter as tk,time,types,subprocess
from tkinter import ttk
from unittest.mock import patch
base=Path(__file__).parent.resolve();sys.path.insert(0,str(base/'current-source'));import program_updates as u;import update_runtime as runtime
root=base/'live-retry-qa24/program';shutil.copytree(base/'installed-source',root,dirs_exist_ok=True)
shutil.copy2(base/'v198/payload/STYLE_GUIDE.md',root/'STYLE_GUIDE.md')
(root/'launch.pyw').write_text("import time;time.sleep(1.5)\nimport tkinter as tk\nfrom program_updates import install_session\nr=tk.Tk();install_session(r);r.after(5000,r.destroy);r.mainloop()\n")
folder,manifest=u.prepare(base/'NestSimple-Money-v1.2.24.nsmupdate',root);(folder/'request.json').write_text(json.dumps(dict(sessions=[],environment={})))
real_tk=tk.Tk;real_clock=time.monotonic;real_spawn=subprocess.Popen;advanced=[False];retried=[];launched=[]
def spawn(*args,**kwargs):
 p=real_spawn(*args,**kwargs);launched.append(p);return p
def create(*args,**kwargs):
 win=real_tk(*args,**kwargs)
 def observe():
  result=(folder/'result.txt').read_text() if (folder/'result.txt').exists() else ''
  if 'Started reopened app PID' in result and not retried:advanced[0]=True
  if 'FAILED:' in result and not retried:
   assert 'REOPENED:' not in result
   def walk(w):
    for c in w.winfo_children():yield c;yield from walk(c)
   button=next(w for w in walk(win) if isinstance(w,ttk.Button) and w.cget('text')=='Continue Waiting')
   assert len(launched)==1 and launched[0].poll() is None
   retried.append(True);advanced[0]=False;button.invoke();assert len(launched)==1,'Live retry started a duplicate'
  if win.winfo_exists():win.after(30,observe)
 win.after(30,observe);win.after(14000,win.destroy);return win
with patch.object(tk,'Tk',side_effect=create),patch.object(runtime,'time',types.SimpleNamespace(monotonic=lambda:real_clock()+(200 if advanced[0] else 0))),patch.object(runtime,'subprocess',types.SimpleNamespace(Popen=spawn,CREATE_NO_WINDOW=getattr(subprocess,'CREATE_NO_WINDOW',0))):runtime.run_worker(root,folder,u)
assert retried and len(launched)==1 and 'REOPENED:' in (folder/'result.txt').read_text()
for p in launched:
 if p.poll() is None:p.terminate();p.wait()
print('PASS delayed live startup: no false completion, Continue Waiting reuses the SAME process, one launch and real ready receipt')


