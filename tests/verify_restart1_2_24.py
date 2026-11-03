"""Actual two-window close, package install, first reopen receipt and same fictional household."""
from pathlib import Path
import os,sys,subprocess,ctypes,uuid,shutil,zipfile,json,time,sqlite3
base=Path(__file__).parent.resolve();test=base/'restart-qa24';test.mkdir(exist_ok=True)
if '--child' not in sys.argv:
 user=ctypes.WinDLL('user32',use_last_error=True);user.CreateDesktopW.argtypes=[ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_void_p,ctypes.c_uint,ctypes.c_uint,ctypes.c_void_p];user.CreateDesktopW.restype=ctypes.c_void_p;user.CloseDesktop.argtypes=[ctypes.c_void_p]
 name='RestartQA24-'+uuid.uuid4().hex;desktop=user.CreateDesktopW(name,None,None,0,0x1ff,None);assert desktop
 si=subprocess.STARTUPINFO();si.lpDesktop='winsta0\\'+name
 try:
  r=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--child'],startupinfo=si,timeout=55,capture_output=True,text=True);print(r.stdout);print(r.stderr);assert r.returncode==0
 finally:user.CloseDesktop(desktop)
else:
 root=test/'program';shutil.copytree(base/'installed-source',root,dirs_exist_ok=True)
 with zipfile.ZipFile(base/'NestSimple-Money-v1.2.23.nsmupdate') as z:
  for name in z.namelist():
   if name.startswith('payload/'):(root/name[8:]).write_bytes(z.read(name))
 data=test/'Fictional Household';shutil.copytree(base/'income-reference24/Fictional Household',data,dirs_exist_ok=True)
 profile=json.loads((data/'demo-profile.json').read_text());profile.update(data_dir=str(data),backup_dir=str(data/'backups'));(data/'demo-profile.json').write_text(json.dumps(profile))
 env=dict(os.environ,NESTSIMPLE_DEMO_WINDOW='1',NESTSIMPLE_PROFILE_FILE=str(data/'demo-profile.json'),NESTSIMPLE_DEMO_FOLDER=str(data),LOCALAPPDATA=str(test/'localappdata'))
 log=(test/'process.log').open('wb');children=[];sys.path.insert(0,str(base/'current-source'));import program_updates as u
 sessions=u.stage_root(root)/'sessions'
 def spawn():
  p=subprocess.Popen([sys.executable,str(root/'launch.pyw'),'--demo-window'],env=env,cwd=root,stdout=log,stderr=log);children.append(p)
  deadline=time.monotonic()+12
  while time.monotonic()<deadline:
   if (sessions/(str(p.pid)+'.json')).exists():return p
   assert p.poll() is None,'App exited: '+(test/'process.log').read_text(errors='replace');time.sleep(.1)
  raise AssertionError('App did not register session')
 try:
  first=spawn();second=spawn();time.sleep(1)
  db=sqlite3.connect(data/'finances.sqlite3');before=db.execute('SELECT * FROM transactions ORDER BY id').fetchall();db.close()
  folder,manifest=u.prepare(base/'NestSimple-Money-v1.2.24.nsmupdate',root)
  from hashlib import sha256
  household=sha256(str(data.resolve()).casefold().encode()).hexdigest()
  (folder/'request.json').write_text(json.dumps(dict(sessions=u.active_sessions(root),household_id=household,environment={k:v for k,v in env.items() if k.startswith('NESTSIMPLE_')})))
  runner=u.stage_runner(folder)
  worker=subprocess.Popen([sys.executable,str(runner),'--apply',str(root),str(folder)],env=env,cwd=root,stdout=log,stderr=log);children.append(worker)
  assert worker.wait(timeout=30)==0,'Worker failed'
  assert first.wait(timeout=3)==0 and second.wait(timeout=3)==0,'Original windows did not close'
  result=(folder/'result.txt').read_text();assert result.count('Launching:')==1 and 'REOPENED:' in result and 'FAILED:' not in result,result
  ready=json.loads((folder/'restart-ready.json').read_text());assert ready['version']=='1.2.24' and ready['household_id']==household,ready
  db=sqlite3.connect(data/'finances.sqlite3');after=db.execute('SELECT * FROM transactions ORDER BY id').fetchall();db.close();assert after==before,'Fictional household entries changed'
  rows=[json.loads(p.read_text()) for p in sessions.glob('*.json') if p.stem.isdecimal()]
  (sessions/'close-request.json').write_text(json.dumps(dict(sessions=[r['token'] for r in rows])))
  print('PASS actual Windows two-window shutdown, v1.2.23->v1.2.24 install, ONE reopen, ready version/same-household receipt and unchanged fictional records',flush=True)
 finally:
  for p in children:
   if p.poll() is None:p.terminate()
  log.close()

