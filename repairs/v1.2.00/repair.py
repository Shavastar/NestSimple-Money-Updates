"""Offline repair: existing program directory only, no household replacement."""
from pathlib import Path
import json,os,sys,traceback
here=Path(__file__).resolve().parent;sys.path.insert(0,str(here))
import program_updates as u
def main():
 root=Path(sys.argv[1]).resolve()
 if not (root/'app.py').is_file() or not (root/'launch.pyw').is_file():raise ValueError('Select the existing NestSimpleMoney program folder containing app.py and launch.pyw.')
 # Prefer the environment saved by the most recent update attempt. This keeps
 # the previously selected personal or testing household without reading it.
 environment={}
 requests=sorted(u.stage_root(root).glob('*/request.json'),key=lambda p:p.stat().st_mtime,reverse=True)
 if requests:
  saved=json.loads(requests[0].read_text(encoding='utf-8')).get('environment',{})
  environment={k:v for k,v in saved.items() if k in ('NESTSIMPLE_PROFILE_FILE','NESTSIMPLE_DEMO_WINDOW','NESTSIMPLE_DEMO_FOLDER') and isinstance(v,str)}
 folder,manifest=u.prepare(here/'NestSimple-Money-v1.2.00.nsmupdate',root)
 (folder/'request.json').write_text(json.dumps({'sessions':u.active_sessions(root),'environment':environment}),encoding='utf-8')
 u.worker(root,folder)
 result=(folder/'result.txt').read_text(encoding='utf-8') if (folder/'result.txt').exists() else ''
 return 0 if 'REOPENED:' in result else 1
if __name__=='__main__':
 try:raise SystemExit(main())
 except Exception:
  details=traceback.format_exc();(here/'repair-error.log').write_text(details,encoding='utf-8')
  import tkinter as tk
  from tkinter import messagebox
  win=tk.Tk();win.withdraw();messagebox.showerror('Repair Could Not Start',details[-1400:],parent=win);win.destroy();raise SystemExit(1)
