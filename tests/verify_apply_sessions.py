"""Exercise the real Apply callback with a leftover update-close command."""
import sys,json,tempfile,importlib.util,shutil
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
sys.path.insert(0,str(Path('HomeMoney').resolve()))
import program_updates as u
from verify_update_handoff import Widget,find
import tkinter.ttk as ttk
import tkinter.messagebox as messages

def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=load('release192/payload/program_updates.py','old_updater')
with tempfile.TemporaryDirectory() as d:
 root=Path(d)/'NestSimpleMoney';root.mkdir();folder=Path(d)/'package';folder.mkdir()
 sessions=u.stage_root(root)/'sessions';sessions.mkdir(parents=True)
 command=sessions/'close-request.json';command.write_text(json.dumps({'sessions':['earlier-window']}))
 live={'pid':123,'token':'live-window'};(sessions/'123.json').write_text(json.dumps(live))
 (sessions/'456.json').write_text(json.dumps({'pid':456,'token':'closed-window'}))
 def click(module):
  Widget.widgets=[];app=Widget();parent=Widget(app)
  with ExitStack() as stack:
   for n in ('Frame','Label','Button'):stack.enter_context(patch.object(ttk,n,Widget))
   stack.enter_context(patch.object(module,'__file__',str(root/'program_updates.py')))
   stack.enter_context(patch.object(module,'validate',return_value={'to':'1.0.193','files':{'app.py':{'new':'x'}}}))
   stack.enter_context(patch.object(module,'alive',side_effect=lambda pid:pid==123))
   stage=stack.enter_context(patch.object(module,'stage_runner',return_value=folder/'installed-updater.py'))
   launch=stack.enter_context(patch.object(module.subprocess,'Popen'))
   error=stack.enter_context(patch.object(messages,'showerror'))
   module.update_page(parent,app,folder)
   find('Apply Update and Restart').kw['command']()
   return stage,launch,error
 stage,launch,error=click(old)
 assert error.call_args.args[:2]==('Update Not Started',"'pid'")
 assert not launch.called
 print("PASS v192 reproduces screenshot: Update Not Started / 'pid'")
 stage,launch,error=click(u)
 assert not error.called,error.call_args
 assert stage.call_count==1 and launch.call_count==1
 assert json.loads((folder/'request.json').read_text())['sessions']==[live]
 assert command.exists() and not (sessions/'456.json').exists()
 print('PASS fixed Apply callback launches installed runner; ignores close command; retains live sessions; removes stale PID')
 (sessions/'789.json').write_text('{}')
 with patch.object(u,'alive',return_value=True):
  try:u.active_sessions(root);raise AssertionError('Malformed PID must block install')
  except ValueError as e:assert '789.json' in str(e)
 (sessions/'789.json').unlink()
 print('PASS malformed PID blocks installation with clear error')
 # Repair calls the same session reader and must not skip a running household.
 repair=load('repair193/update.py','repair193_test')
 # Install verification occurs against the actual packaged files after build.
 with patch.object(u,'alive',return_value=False):assert u.active_sessions(root)==[]
 assert command.exists()
 print('PASS closed-session retry retains command without pid error')
