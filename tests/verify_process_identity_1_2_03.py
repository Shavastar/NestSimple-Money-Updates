from pathlib import Path
import sys,subprocess,tempfile,json,os,time
base=Path(__file__).parent.resolve();sys.path.insert(0,str(base/'current-source'))
import program_updates as u
child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'])
try:
 started=u.process_started(child.pid);assert started is not None
 with tempfile.TemporaryDirectory(dir=base) as d:
  root=Path(d)/'app';root.mkdir();sessions=u.stage_root(root)/'sessions';sessions.mkdir(parents=True)
  entry=sessions/(str(child.pid)+'.json');entry.write_text(json.dumps({'pid':child.pid,'token':'old-app-record'}));os.utime(entry,(started-600,started-600))
  assert u.active_sessions(root)==[],'Reused PID was treated as a live app'
  assert not entry.exists() and child.poll() is None
  entry.write_text(json.dumps({'pid':child.pid,'token':'current-record','started':started}))
  current=u.active_sessions(root);assert len(current)==1 and u.session_alive(current[0])
  assert not u.session_alive(dict(current[0],started=started-600))
  lock=u.stage_root(root)/'apply.lock';lock.write_text(str(child.pid));os.utime(lock,(started-600,started-600))
  acquired=u.acquire_lock(root);assert json.loads(acquired.read_text())['pid']==os.getpid();acquired.unlink()
 assert child.poll() is None
 print('PASS real Windows PID reuse: legacy stale session and lock ignored, unrelated live process untouched, current session retained, birth-time mismatch rejected')
finally:child.terminate();child.wait()
