"""Real Tk page construction against the original installed layout helper."""
import sys,zipfile,types,tkinter as tk
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,'HomeMoney')
import program_updates as u
import layout
z=zipfile.ZipFile('NestSimple-Money-Windows-v1.0.29.zip')
s=z.read(next(n for n in z.namelist() if n.endswith('/layout.py'))).decode()
old=types.ModuleType('old_layout');exec(compile(s,'original-installed-layout.py','exec'),old.__dict__)
r=tk.Tk();r.geometry('800x500');errors=[];r.report_callback_exception=lambda *e:errors.append(e)
# Reproduce the previously shipped constructor failure with genuine Tk widgets.
try:old.ScrollArea(r,min_width=0,min_height=0,vertical_only=True)
except tk.TclError as e:assert 'vertical_only' in str(e);print('Reproduced old failure:',e)
else:raise AssertionError('Old failure not reproduced')
for helper in (old.ScrollArea,layout.ScrollArea):
 parent=tk.ttk.Frame(r);parent.pack(fill='both',expand=True)
 with patch.object(layout,'ScrollArea',helper),patch.object(u.threading,'Thread'):
  u.online_page(parent,r)
 r.update()
 def descendants(w):
  for c in w.winfo_children():yield c;yield from descendants(c)
 buttons={w.cget('text'):w for w in descendants(parent) if isinstance(w,tk.ttk.Button)}
 assert all(buttons[n].winfo_ismapped() for n in ('Check Again','Download Update','Choose Update File'))
 assert not errors,errors
 parent.destroy();r.update()
r.destroy();print('PASS real Tk page construction and visible controls with original/current layout; no callback errors')
