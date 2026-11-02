from pathlib import Path
import sys,tempfile,json,os,ast
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0,str(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'current-source'))
import settings,storage_page,modal_windows as modal

with patch.object(settings.shutil,'which',return_value='winget'),patch.object(settings.subprocess,'Popen') as launch,patch.object(settings.sys,'platform','win32'),patch.object(settings.sys,'version_info',SimpleNamespace(major=3,minor=14)):
 settings.manage_python('install');assert 'Python.Python.3.14' in launch.call_args.args[0]
 settings.manage_python('upgrade');assert 'Python.Python.3.14' in launch.call_args.args[0]
with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as d:
 root=Path(d);program=root/'app';data=root/'household';program.mkdir();data.mkdir()
 (program/'app.py').write_bytes(b'x'*123)
 (data/'finances.sqlite3').write_bytes(b'x'*456);(data/'finances.sqlite3-wal').write_bytes(b'x'*34);(data/'bill.pdf').write_bytes(b'x'*78)
 snapshot=storage_page.storage_snapshot(program,data,root/'backup')
 assert snapshot['application_bytes']==123
 assert snapshot['database_bytes']==490
 assert snapshot['household_bytes']==568
 assert len(snapshot['drives'])==1
 drive=snapshot['drives'][0];assert drive['total']==drive['used']+drive['free']
 assert drive['purposes']==['Application','Household','Backups']
class Window:
 def __init__(self,parent=None,state='normal'):
  self.master=parent;self.mode=state;self.events={};self.tasks=[];self.calls=[];self.previous=None
 def winfo_toplevel(self):return self
 def grab_current(self):return self.previous
 def state(self):return self.mode
 def transient(self,owner):self.calls.append(('owner',owner))
 def bind(self,event,callback,add=None):self.events[event]=callback;return event+'-id'
 def unbind(self,event,identifier):self.calls.append(('unbind',event,identifier))
 def winfo_exists(self):return True
 def lift(self):self.calls.append(('lift',))
 def focus_set(self):self.calls.append(('focus',))
 def after_idle(self,fn):self.tasks.append(fn)
with patch.object(modal.tk,'Toplevel',Window):
 owner=Window();window=Window(owner);modal.keep_in_front(window)
 assert ('owner',owner) in window.calls
 window.tasks[0]();assert ('lift',) in window.calls and ('focus',) in window.calls
 window.calls.clear();owner.events['<FocusIn>'](SimpleNamespace(widget=owner));assert ('lift',) in window.calls
 hidden=Window(state='withdrawn');startup=Window(hidden);modal.keep_in_front(startup);assert ('owner','') in startup.calls
 nested=Window(owner);nested.previous=window;modal.keep_in_front(nested);assert ('owner',window) in nested.calls
 window.events['<Destroy>'](SimpleNamespace(widget=window));assert any(c[0]=='unbind' for c in owner.calls)
from tkinter import commondialog
root=Window();child=Window(root);root.previous=child
with patch.object(modal.tk,'_default_root',root),patch.object(commondialog.Dialog,'show',return_value='chosen') as native:
 modal.install()
 dialog=commondialog.Dialog.__new__(commondialog.Dialog);dialog.options={};dialog.master=None
 assert dialog.show()=='chosen';assert native.call_args.kwargs['parent'] is child
for name in ('modal_windows.py','app.py','settings.py','upgrade.py','storage_page.py'):
 ast.parse((Path(__file__).parent/'current-source'/name).read_text(encoding='utf-8'),feature_version=(3,10))
print('PASS headless: Python 3.14 install/update targets; application/household/database byte counts; drive capacity and de-duplication; modal owner, nested owner, startup hidden-root handling, raise-on-owner-focus, binding cleanup; Python 3.10 syntax')
