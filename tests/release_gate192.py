"""Run updater/hover gates against actual packaged source and its prior release."""
from pathlib import Path
import tempfile,zipfile,shutil,subprocess,sys,json,hashlib
package=Path(sys.argv[1]).resolve();baseline=Path(sys.argv[2]).resolve()
feed_path=package.parent.parent/'latest.json'
if feed_path.is_file():
 info=json.loads(feed_path.read_text());data=package.read_bytes()
 assert len(data)==info['size'],'Published package size differs from feed'
 assert hashlib.sha256(data).hexdigest()==info['sha256'],'Published package checksum differs from feed'
with zipfile.ZipFile(package) as archive:
 assert archive.testzip() is None,'Published ZIP contains damaged files'
with tempfile.TemporaryDirectory() as d:
 root=Path(d);home=root/'HomeMoney';home.mkdir()
 with zipfile.ZipFile(package) as z:
  for name in z.namelist():
   if name.startswith('payload/'):
    target=home/name[8:];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(name))
 with zipfile.ZipFile(baseline) as z:
  target=root/'release191/payload/program_updates.py';target.parent.mkdir(parents=True);target.write_bytes(z.read('payload/program_updates.py'))
 for name in ('verify_update_handoff.py','verify_trend192.py'):
  script=Path(__file__).parent/name;shutil.copy2(script,root/name)
  subprocess.run([sys.executable,str(root/name),str(package)],cwd=root,check=True)
